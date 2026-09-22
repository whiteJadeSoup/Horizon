"""Horizon 聚合台 · LLM 层
1) 批量打分 + 板块归类（一次调用，JSON 数组）
2) 条目结构化分析（概述/分析/思考 + 板块专属字段）
3) TLDR（核心看点 + 趋势分析）
容错: 增量落盘 / finish_reason 校验 / 剥 markdown 围栏 / 小批次防截断。
"""
from __future__ import annotations

import datetime as dt
import json
import logging
import os
import re
import time
from typing import Any, Optional

from .fetch import CAT_NAMES, ContentItem

log = logging.getLogger("horizon_daily.llm")

MODEL = os.environ.get("HORIZON_LLM_MODEL", "glm-5-3-flash")
BASE_URL = os.environ.get("HORIZON_LLM_BASE", "https://ark.cn-beijing.volces.com/api/plan/v3/chat/completions")
MAX_ANALYSIS_TOKENS = 8000
BATCH_SCORE = 35  # 打分 prompt v8 (2026-09-22): 时效审查淘汰旧文 + 行内附发布日期
BATCH_ANALYSIS = 6   # 五要素板块更小批次防截断
RETRIES = 4


class LLMError(RuntimeError):
    pass


def _headers() -> dict:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise LLMError("OPENAI_API_KEY not set")
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def _chat(messages: list[dict], max_tokens: int = 4000, temperature: float = 0.3) -> str:
    """同步调用（管线是串行步骤，够用）。返回模型文本，校验 finish_reason==stop。"""
    import urllib.request

    body = json.dumps({"model": MODEL, "messages": messages,
                       "temperature": temperature, "max_tokens": max_tokens}).encode()
    req = urllib.request.Request(BASE_URL, data=body, headers=_headers())
    # 方舟调用显式直连（ProxyHandler({}) 绕开环境代理）：
    # run.py 不再全局剥代理，X 抓取需保留代理注入 secret，此处必须独立直连。
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    last: Optional[Exception] = None
    for a in range(RETRIES):
        try:
            with opener.open(req, timeout=240) as r:
                resp = json.load(r)
            ch = resp["choices"][0]
            if ch.get("finish_reason") != "stop":
                raise LLMError(f"finish_reason={ch.get('finish_reason')} (truncated)")
            return ch["message"]["content"]
        except Exception as e:
            last = e
            wait = 8 * (a + 1)
            log.warning("LLM call fail (try %d): %s; wait %ds", a + 1, str(e)[:90], wait)
            time.sleep(wait)
    raise LLMError(f"LLM call failed after {RETRIES} tries: {last}")


def _strip_fence(txt: str) -> str:
    return re.sub(r"^```(?:json)?\s*|\s*```$", "", txt.strip(), flags=re.M).strip()


def _extract_json_array(txt: str) -> Optional[list]:
    txt = _strip_fence(txt)
    m = re.search(r"\[.*\]", txt, re.S)
    if not m:
        return None
    raw = m.group(0)
    # LLM 常在 JSON 字符串值里输出裸换行/裸制表符，先转义再解析
    raw = re.sub(r"(?<!\\)\n", "\\n", raw)
    raw = re.sub(r"(?<!\\)\t", "\\t", raw)
    try:
        return json.loads(raw)
    except Exception:
        return None


def _pubtag(p) -> str:
    """published 可能是 datetime（fetch 期）或 ISO 字符串（skip-fetch 恢复期），统一转日期标签。"""
    if isinstance(p, str):
        try:
            p = dt.datetime.fromisoformat(p)
        except ValueError:
            return "日期未知"
    if isinstance(p, dt.datetime):
        return p.strftime("%Y-%m-%d")
    return "日期未知"


def _extract_json_obj(txt: str) -> Optional[dict]:
    txt = _strip_fence(txt)
    try:
        return json.loads(txt[txt.index("{"): txt.rindex("}") + 1])
    except Exception:
        return None


def _extract_json_objects(txt: str) -> list[dict]:
    """从残破的 LLM 输出（截断/夹带文字/裸换行）中抢救所有可解析的 JSON 对象，按出现顺序。"""
    txt = _strip_fence(txt)
    out: list[dict] = []
    depth, start, in_str, esc = 0, -1, False, False
    for i, ch in enumerate(txt):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and start >= 0:
                    raw = txt[start:i + 1]
                    e = None
                    for frag in (raw,
                                 re.sub(r"(?<!\\)\t", "\\t", re.sub(r"(?<!\\)\n", "\\n", raw))):
                        try:
                            e = json.loads(frag)
                            break
                        except Exception:
                            continue
                    if isinstance(e, dict):
                        out.append(e)
                    start = -1
    return out


def _absorb(arr: list, chunk: list, results: dict) -> int:
    """把 LLM 输出的分析对象吸收进 results。
    所有对象的 i 字段有效且唯一时按 i 对齐（数量不齐也可信，如截断/跳条）；
    否则退回顺序对齐（模型输出顺序=输入顺序）。返回吸收条数。"""
    if not arr:
        return 0
    idxs = [e.get("i") if isinstance(e, dict) else None for e in arr]
    use_i = (all(isinstance(x, int) and 0 <= x < len(chunk) for x in idxs)
             and len(set(idxs)) == len(arr))
    n = 0
    for pos, e in enumerate(arr):
        if not isinstance(e, dict) or not e.get("brief"):
            continue
        j = e["i"] if use_i else pos
        if (use_i or pos < len(chunk)) and isinstance(j, int) and 0 <= j < len(chunk):
            results[chunk[j][1].title] = e
            n += 1
    return n


def score_and_classify(items: list[ContentItem]) -> dict[int, tuple[float, int]]:
    """分批打分+归类。返回 {item_index: (score, category)}。"""
    out: dict[int, tuple[float, int]] = {}
    for start in range(0, len(items), BATCH_SCORE):
        batch = items[start:start + BATCH_SCORE]
        def _datetag(it: ContentItem) -> str:
            return f" 发布:{_pubtag(it.published)}"

        lines = "\n".join(f"{j}| {it.title[:110]} [{it.src}]{_datetag(it)}"
                          for j, it in enumerate(batch))
        prompt = f"""你是为一位中国创业者筛选日报的编辑。对下列资讯逐条打分(0-10)：对"了解创业产品/商业模式/赚钱方式/技术前沿/AI效率"的价值。0-3=噪音,4-5=一般,6-7=值得看,8+=必看。
先做时效审查：明显是多年前的旧文/旧闻（过时的产品发布、早已失效的经验）直接 0 分淘汰；发布日期未知但内容明显陈旧（如提及多年前的年份/事件）从严；旧但观点至今成立、对当下创业仍有启发的可正常打分。
同时归入唯一章节: 1=技术前沿(机器人/大模型/AI研究) 2=创业产品(新AI应用/SaaS/硬件) 3=创业动态(行业事件/大佬言论/讨论) 4=赚钱模式(收入/商业化/案例) 5=AI工作流(提示词/工具/效率方法)。
子标签k(仅描述性归类，绝不影响打分高低): cat3用big(大厂/宏观/大佬言论)或startup(早期创业实战)；cat4用wild(野路子/卖水人/早期蓝海)或biz(常规商业模式/收入)；cat1/cat5用tech；cat2用other。
只输出JSON数组: [{{"i":编号,"s":分数,"c":章节号,"k":子标签}}]，无其他文字，无markdown围栏。
{lines}"""
        try:
            txt = _chat([{"role": "user", "content": prompt}], max_tokens=6000, temperature=0.2)
        except LLMError as e:
            log.warning("score batch %d fail: %s", start // BATCH_SCORE, e)
            continue
        arr = _extract_json_array(txt)
        if not arr:
            log.warning("score batch %d unparseable", start // BATCH_SCORE)
            continue
        for e in arr:
            try:
                i = int(e.get("i"))
                s = float(e.get("s"))
                c = int(e.get("c"))
            except (TypeError, ValueError):
                continue
            k = str(e.get("k") or "")
            if 0 <= i < len(batch):
                out[start + i] = (s, c, k)
        log.info("score batch %d: +%d (total %d)", start // BATCH_SCORE, len(arr), len(out))
    return out


def _analysis_field_spec(cat: int) -> str:
    if cat == 4:
        return ('"brief":"飞书一句话概述(60字内)", "overview":"概述:发生了什么(2-3句)", '
                '"analysis":"分析:为什么值得注意(3-4句)", "think":"思考:对创业者的启示(2-3句)", '
                '"who":"客户是谁", "where":"客户从哪儿来", "why_pay":"为什么会付钱", '
                '"biz":"商业模式", "moat":"核心护城河", '
                '"risk":"风险与合规:平台ToS风险/灰色程度/明显违法则只报现象不展开细节"')
    if cat == 5:
        return ('"brief":"飞书一句话概述(60字内)", "overview":"概述:发生了什么(2-3句)", '
                '"analysis":"分析:为什么值得注意(3-4句)", "think":"思考:对创业者的启示(2-3句)", '
                '"flow":"核心流程:步骤化拆解", "key":"关键点:最值得抄的一个点"')
    return ('"brief":"飞书一句话概述(60字内)", "overview":"概述:发生了什么(2-3句)", '
            '"analysis":"分析:为什么值得注意(3-4句)", "think":"思考:对创业者的启示(2-3句)"')


def analyze(items: list[ContentItem], scores: dict,
            existing: Optional[dict[str, dict]] = None) -> dict[str, dict]:
    """对入选条目生成结构化分析。返回 {title: analysis_dict}。
    existing: 已有分析（标题命中则跳过，用于增量/补漏）。
    scores 值为 (score, category) 或 (score, category, sublabel)。
    容错：解析失败→逐对象抢救；缺漏→3条小批重试；仍失败→ERROR 日志，绝不整批静默丢失。"""
    results: dict[str, dict] = dict(existing or {})
    # 按板块分组
    by_cat: dict[int, list[tuple[int, ContentItem]]] = {}
    for i, it in enumerate(items):
        if i not in scores:
            continue
        sc = scores[i]
        s, c = sc[0], sc[1]
        if s < 6.0:
            continue
        it.score, it.category = s, c
        if len(sc) >= 3 and sc[2]:
            it.extra["sublabel"] = str(sc[2])
        by_cat.setdefault(c, []).append((i, it))

    def _analyze_chunk(chunk: list[tuple[int, ContentItem]], tag: str) -> None:
        c = chunk[0][1].category or 1
        lines = "\n".join(
            f"{j}| {it.score}分| [{_pubtag(it.published)}] "
            f"{it.title} | 来源:{it.src}"
            for j, (_, it) in enumerate(chunk))
        spec = _analysis_field_spec(c)
        prompt = (f"你是创业日报编辑，读者是中国创业者。以下{len(chunk)}条资讯（标题保持原语言）。"
                  f"基于标题与你的知识，为每条生成中文分析。\n"
                  f"每条输出JSON对象: {{{spec}}}\n"
                  f"全部字段用中文（标题除外）。只输出JSON数组，无其他文字，无markdown围栏。\n\n{lines}")
        for attempt in (1, 2):
            try:
                txt = _chat([{"role": "user", "content": prompt}], max_tokens=MAX_ANALYSIS_TOKENS)
            except LLMError as e:
                log.warning("analyze %s chunk fail(try%d): %s", tag, attempt, str(e)[:90])
                continue
            before = len(results)
            arr = _extract_json_array(txt)
            if arr:
                _absorb(arr, chunk, results)
            if len(results) - before < len(chunk):
                # 整体数组解析失败/部分缺失：从残破输出逐对象抢救
                _absorb(_extract_json_objects(txt), chunk, results)
            got = len(results) - before
            if got >= len(chunk):
                log.info("analyze %s: +%d (total %d)", tag, got, len(results))
                return
            log.warning("analyze %s chunk parsed %d/%d (try%d); salvaged",
                        tag, got, len(chunk), attempt)
        missing = [it.title for _, it in chunk if it.title not in results]
        if missing:
            log.error("analyze %s 放弃 %d 条: %s", tag, len(missing),
                      " | ".join(t[:50] for t in missing))

    for c, group in by_cat.items():
        group.sort(key=lambda x: -x[1].score)
        todo = [(i, it) for i, it in group if it.title not in results]
        batch_size = BATCH_ANALYSIS if c in (4, 5) else 8
        for start in range(0, len(todo), batch_size):
            _analyze_chunk(todo[start:start + batch_size], CAT_NAMES[c])
    # 残余兜底：仍缺分析的条目按 3 条小批重试一轮
    leftover = [(i, it) for g in by_cat.values() for i, it in g if it.title not in results]
    if leftover:
        log.warning("analyze: %d 条缺分析，进入小批重试", len(leftover))
        by_cat2: dict[int, list[tuple[int, ContentItem]]] = {}
        for i, it in leftover:
            by_cat2.setdefault(it.category or 1, []).append((i, it))
        for c2, group2 in by_cat2.items():
            for start in range(0, len(group2), 3):
                _analyze_chunk(group2[start:start + 3], CAT_NAMES[c2] + "·补")
    return results


def tldr(selected: list[ContentItem], analyses: dict[str, dict]) -> Optional[dict]:
    """基于分析过的 brief 生成核心看点+趋势分析。"""
    rows = []
    for it in selected:
        a = analyses.get(it.title)
        if a and a.get("brief"):
            rows.append((it.score, CAT_NAMES[it.category], it.title[:70], a["brief"]))
    rows.sort(key=lambda x: -x[0])
    if not rows:
        return None
    feed = "\n".join(f"{s}分[{c}] {t} — {b[:60]}" for s, c, t, b in rows[:30])
    prompt = f"""你是创业日报主编。今日{min(30, len(rows))}条高价值资讯如下（分数[章节]标题—要点）。写日报TLDR：
1. 核心看点：3-4条，每条一两句，提炼当日最重要信息（综合判断，不复述标题）
2. 趋势分析：2-3条，跨事件暗线/趋势+对创业者的含义
只输出JSON: {{"highlights":["..."],"trends":["..."]}}，全部中文，无markdown围栏。

{feed}"""
    try:
        txt = _chat([{"role": "user", "content": prompt}], max_tokens=3000)
    except LLMError as e:
        log.warning("tldr fail: %s", e)
        return None
    obj = _extract_json_obj(txt)
    if not obj or not obj.get("highlights"):
        log.warning("tldr unparseable")
        return None
    return {"highlights": obj.get("highlights", []), "trends": obj.get("trends", [])}
