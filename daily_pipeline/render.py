"""Horizon 聚合台 · 渲染层
1) 全文版 HTML/Markdown（GitHub Pages）
2) 飞书推送版（每板块 Top5 + TLDR + 站点链接）
"""
from __future__ import annotations

import datetime as dt
import html
import json
import logging
import os
import re
from typing import Any, Optional

from .fetch import CAT_NAMES, ContentItem

log = logging.getLogger("horizon_daily.render")

SITE_URL = os.environ.get("HORIZON_SITE_URL", "https://whitejadesoup.github.io/Horizon/")
SECTIONS_FULL = {
    1: "一、技术前沿发展",
    2: "二、创业产品",
    3: "三、创业动态",
    4: "四、大家在靠什么赚钱",
    5: "五、AI工作流、方法、效率",
}

# 各章节信源优先级（越靠前越优先收录）。匹配 src 子串，忽略大小写。
# 技术前沿: HN > 量子位 > X > 其他
# 创业产品: Product Hunt > Reddit > HN > X > 其他
# 创业动态: X > Reddit > HN > 其他
# 赚钱模式: X > Reddit > HN > 其他
# AI工作流: X > HN > 其他
_SRC_PRIORITY: dict[int, list[tuple[str, ...]]] = {
    1: [("hacker", "show hn"), ("量子位",), ("x/",)],
    2: [("product hunt",), ("r/",), ("hacker", "show hn"), ("x/",)],
    3: [("x/",), ("r/",), ("hacker", "show hn")],
    4: [("x/",), ("r/",), ("hacker", "show hn")],
    5: [("x/",), ("hacker", "show hn")],
}


def _src_rank(cat: int, src: str) -> int:
    """章节内信源优先级：返回 rank，越小越优先；未列出的来源排最后。"""
    s = (src or "").lower()
    for rank, keys in enumerate(_SRC_PRIORITY.get(cat, [])):
        if any(k in s for k in keys):
            return rank
    return len(_SRC_PRIORITY.get(cat, []))


def _color(score: float) -> str:
    if score >= 8:
        return "#e11d48"
    if score >= 7:
        return "#ea580c"
    if score >= 6:
        return "#ca8a04"
    return "#8b949e"


def _score_badge(score: float) -> str:
    return (f'<span class="score" style="background:{_color(score)}">'
            f'{score}</span>')


def _selected_by_section(selected: list[ContentItem], max_per: int = 10) -> dict[int, list[ContentItem]]:
    out: dict[int, list[ContentItem]] = {}
    # 章节内先按信源优先级（_SRC_PRIORITY），同优先级按分数降序
    for it in sorted(selected, key=lambda x: (_src_rank(x.category or x.cat, x.src), -(x.score or 0))):
        c = it.category or it.cat
        if c not in out:
            out[c] = []
        if len(out[c]) < max_per:
            out[c].append(it)
    return out


def render_full_html(
    selected: list[ContentItem],
    analyses: dict[str, dict],
    tldr: Optional[dict],
    today: str,
    total_fetched: int,
    total_scored: int,
    max_per_section: int = 10,
) -> str:
    """全文版：TLDR + 五章节（每章节 max_per_section 条，概述/分析/思考 + 板块专属）。"""
    by_cat = _selected_by_section(selected, max_per_section)
    P: list[str] = []
    P.append(f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Horizon 创业日报 · {today}</title><style>
body{{font-family:-apple-system,'PingFang SC','Segoe UI',sans-serif;max-width:820px;margin:0 auto;padding:24px 18px;color:#1f2328;line-height:1.75;background:#fafafa}}
h1{{font-size:1.5em;border-bottom:2px solid #e11d48;padding-bottom:8px}}.meta{{color:#656d76;font-size:.92em}}
.tldr{{background:#fff8e6;border-left:4px solid #f59e0b;padding:14px 18px;border-radius:6px;margin:18px 0}}
.tldr h3{{margin:0 0 8px;color:#92400e;font-size:1.05em}}.tldr li{{margin:6px 0}}
h2{{font-size:1.25em;margin-top:40px;border-bottom:1px solid #d0d7de;padding-bottom:6px}}
.item{{background:#fff;border:1px solid #e1e4e8;border-radius:10px;padding:16px 20px;margin:12px 0;box-shadow:0 1px 2px rgba(0,0,0,.04)}}
.item h3{{margin:0 0 8px;font-size:1.03em}}.item h3 a{{color:#0969da;text-decoration:none}}
.score{{display:inline-block;color:#fff;font-weight:700;font-size:.8em;padding:2px 9px;border-radius:999px;margin-right:8px;vertical-align:2px}}
.src{{color:#8b949e;font-size:.85em;margin-left:8px}}
.row{{margin-top:8px;font-size:.95em}}.row b{{color:#0550ae}}
.struct{{background:#f6f8fa;border:1px solid #d0d7de;border-radius:8px;padding:10px 14px;margin-top:10px;font-size:.92em}}
.srow{{margin:4px 0}}.srow b{{color:#0550ae}}
footer{{margin-top:40px;color:#8b949e;font-size:.85em;text-align:center}}
</style></head><body>
<h1>📰 Horizon 创业日报 <span class="meta">· {today}</span></h1>
<div class="meta">从 {total_fetched} 条资讯中筛选出 {total_scored} 条（每章节 ≤ {max_per_section}）· Horizon Pipeline</div>""")
    if tldr:
        P.append('<div class="tldr"><h3>TLDR · 核心看点</h3><ul>'
                 + "".join(f"<li>{html.escape(x)}</li>" for x in tldr.get("highlights", []))
                 + '</ul><h3>趋势分析</h3><ul>'
                 + "".join(f"<li>{html.escape(x)}</li>" for x in tldr.get("trends", []))
                 + "</ul></div>")
    else:
        P.append('<div class="tldr">TLDR 生成失败（可稍后重试）</div>')
    for c in range(1, 6):
        items = by_cat.get(c, [])
        if not items:
            continue
        P.append(f"<h2>{SECTIONS_FULL[c]} <span class='meta'>({len(items)} 条)</span></h2>")
        for it in items:
            a = analyses.get(it.title, {})
            if not a:
                continue
            P.append(f"""<div class="item"><h3>{_score_badge(it.score or 0)}<a href="{html.escape(it.url)}">{html.escape(it.title)}</a><span class="src">— {it.src}</span></h3>""")
            for k, lb in (("overview", "概述"), ("analysis", "分析"), ("think", "思考")):
                if a.get(k):
                    P.append(f"<div class='row'><b>{lb}</b>：{html.escape(a[k])}</div>")
            if c == 4 and a.get("who"):
                P.append('<div class="struct">' + "".join(
                    f"<div class='srow'><b>{lb}</b>：{html.escape(a.get(k, ''))}</div>"
                    for k, lb in (("who", "客户是谁"), ("where", "客户从哪儿来"),
                                  ("why_pay", "为什么会付钱"), ("biz", "商业模式"),
                                  ("moat", "核心护城河"))
                ) + "</div>")
            if c == 5 and a.get("flow"):
                P.append('<div class="struct">'
                         + f"<div class='srow'><b>核心流程</b>：{html.escape(a['flow'])}</div>"
                         + f"<div class='srow'><b>关键点</b>：{html.escape(a.get('key', ''))}</div>"
                         + "</div>")
            P.append("</div>")
    P.append(f"<footer>Horizon 创业日报 · {today} · <a href=\"{SITE_URL}\">站点首页</a></footer></body></html>")
    return "\n".join(P)


def render_full_markdown(
    selected: list[ContentItem], analyses: dict[str, dict], tldr: Optional[dict], today: str
) -> str:
    """站点 Jekyll 用 Markdown 版（docs/_posts）。"""
    by_cat = _selected_by_section(selected, 10)
    L: list[str] = [f"---\nlayout: post\ntitle: \"Horizon 创业日报 · {today}\"\ndate: {today}\ncategories: daily\n---\n"]
    if tldr:
        L.append("## TLDR\n")
        L.append("### 核心看点\n")
        L.extend(f"- {x}" for x in tldr.get("highlights", []))
        L.append("\n### 趋势分析\n")
        L.extend(f"- {x}" for x in tldr.get("trends", []))
        L.append("")
    for c in range(1, 6):
        items = by_cat.get(c, [])
        if not items:
            continue
        L.append(f"\n## {SECTIONS_FULL[c]}\n")
        for it in items:
            a = analyses.get(it.title, {})
            L.append(f"### [{it.title}]({it.url}) ⭐️ {it.score}/10 · {it.src}\n")
            for k, lb in (("overview", "概述"), ("analysis", "分析"), ("think", "思考")):
                if a.get(k):
                    L.append(f"- **{lb}**：{a[k]}")
            if c == 4 and a.get("who"):
                L.append("")
                L.append(f"  - **客户是谁**：{a['who']}")
                L.append(f"  - **客户从哪儿来**：{a['where']}")
                L.append(f"  - **为什么会付钱**：{a['why_pay']}")
                L.append(f"  - **商业模式**：{a['biz']}")
                L.append(f"  - **核心护城河**：{a['moat']}")
            if c == 5 and a.get("flow"):
                L.append("")
                L.append(f"  - **核心流程**：{a['flow']}")
                L.append(f"  - **关键点**：{a.get('key', '')}")
            L.append("")
    return "\n".join(L)


def render_feishu(
    selected: list[ContentItem],
    analyses: dict[str, dict],
    tldr: Optional[dict],
    today: str,
    total_fetched: int,
    total_scored: int,
    top_per_section: int = 5,
) -> str:
    """飞书推送版：TLDR（编号）+ 每板块 Top3 + 站点链接（结构化、可扫读）。"""
    by_cat = _selected_by_section(selected, top_per_section)
    CAT_ICON = {1: "🔬", 2: "🚀", 3: "📈", 4: "💰", 5: "⚙️"}
    lines = [
        f"📰 **Horizon 创业日报** · {today}",
        f"—— 从 {total_fetched} 条资讯中筛选出 {total_scored} 条 ————————",
        "",
    ]
    if tldr:
        lines.append("✨ **核心看点**")
        for i, h in enumerate(tldr.get("highlights", []), 1):
            lines.append(f"{i}. {h}")
        lines.append("")
        lines.append("📈 **趋势分析**")
        for i, t in enumerate(tldr.get("trends", []), 1):
            lines.append(f"{i}. {t}")
        lines.append("")
    # 每板块 Top N → 按章节顺序(1→5)展示，章节内保持信源优先级+分数，板块间用分隔线
    prev_cat = None
    for c in range(1, 6):
        for it in by_cat.get(c, []):
            if prev_cat is not None and c != prev_cat:
                lines.append("━━━━━━━━━━━━━━")
            prev_cat = c
            a = analyses.get(it.title, {})
            brief = a.get("brief", "")
            icon = CAT_ICON.get(c, "·")
            cat_name = CAT_NAMES.get(c, "")
            lines.append(f"{icon} **{it.score}** 【{cat_name}】{it.title}")
            if brief:
                lines.append(brief)
            lines.append(it.url)
            lines.append("")
    lines.append("━━━━━━━━━━━━━━")
    lines.append(f"📄 **全文版（每章节最多 10 条，含逐条深入分析）**：{SITE_URL}")
    return "\n".join(lines).strip()
