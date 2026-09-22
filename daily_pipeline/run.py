"""Horizon 聚合台 · 主入口
完整链路: 抓取 → 打分归类 → 结构化分析 → TLDR → 渲染(全文+飞书) → 部署GH Pages → 飞书推送
用法:  uv run python -m daily_pipeline.run [--date YYYY-MM-DD] [--hours 48] [--skip-fetch] [--skip-deploy]
失败会尝试飞书通知。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import os
import sys
from typing import Optional

# 注意：此处不再全局剥代理。
# X 抓取（twitterapi.io）依赖网关代理自动注入 TWITTERAPI_IO_KEY 密文句柄 → 真 key；
# 方舟 LLM 调用在 llm.py 内用 ProxyHandler({}) 显式直连，其余抓取源用 trust_env=False 直连，互不干扰。

from . import deliver, fetch, llm, render  # noqa: E402

log = logging.getLogger("horizon_daily")


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def _load_state(data_dir: str, name: str, default):
    p = os.path.join(data_dir, name)
    if os.path.exists(p):
        try:
            with open(p) as f:
                return json.load(f)
        except Exception as e:
            log.warning("load %s fail: %s", name, e)
    return default


def _save_state(data_dir: str, name: str, obj) -> None:
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, name), "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def run(args) -> int:
    setup_logging()
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_dir, "data", "daily")
    today = args.date or dt.date.today().isoformat()
    errors: list[str] = []

    try:
        # 1. 抓取
        if args.skip_fetch:
            items = [fetch.ContentItem(**it) for it in _load_state(data_dir, "items.json", [])]
            log.info("loaded %d cached items", len(items))
        else:
            cfg = fetch.SourceConfig()
            items = fetch.run_sync_fetch(cfg, args.hours) if hasattr(fetch, "run_sync_fetch") else fetch.fetch_all_sync(cfg, args.hours)
            _save_state(data_dir, "items.json", [dict(
                title=it.title, url=it.url, src=it.src, cat=it.cat,
                published=it.published.isoformat() if it.published else None,
                extra=it.extra,
            ) for it in items])
            log.info("fetched %d items", len(items))
    except Exception as e:
        log.exception("fetch failed")
        errors.append(f"抓取失败: {e}")

    # 2. 打分归类
    scores: dict[int, tuple[float, int]] = {}
    try:
        if items:
            scored = llm.score_and_classify(items)
            scores.update(scored)
            _save_state(data_dir, "scores.json",
                        {str(k): list(v) for k, v in scores.items()})
            log.info("scored %d/%d", len(scores), len(items))
    except Exception as e:
        log.exception("scoring failed")
        errors.append(f"打分失败: {e}")

    # 3. 分析（同日重跑/补漏时合并已有 analysis.json；跨天全新运行则从零开始，
    #    避免把昨天的分析键带进今天的文件）
    analyses: dict[str, dict] = {}
    try:
        existing = _load_state(data_dir, "analysis.json", {}) if args.skip_fetch else {}
        analyses = llm.analyze(items, scores, existing=existing)
        _save_state(data_dir, "analysis.json", analyses)
        log.info("analyzed %d items", len(analyses))
    except Exception as e:
        log.exception("analysis failed")
        errors.append(f"分析失败: {e}")

    # 4. TLDR
    selected = [it for it in items if it.score is not None and (it.score or 0) >= 6.0]
    tldr = None
    try:
        tldr = llm.tldr(selected, analyses)
        _save_state(data_dir, "tldr.json", tldr or {})
    except Exception as e:
        log.exception("tldr failed")
        errors.append(f"TLDR失败: {e}")

    # 缺分析条目显性上报（渲染会降级成无解释行，不能静默出门）
    _missing = [it for it in selected if it.title not in analyses]
    if _missing:
        err = f"{len(_missing)}条缺分析(将无解释行): " + " | ".join(it.title[:30] for it in _missing[:5])
        log.error("analysis missing: %s", err)
        errors.append(err)

    if not selected or not analyses:
        err = "没有生成足够内容（可能抓取/打分全失败）"
        errors.append(err)
        deliver.push_feishu(f"❌ Horizon 日报生成失败\n\n{err}\n\n日志: {', '.join(errors)}")
        return 1

    # 5. 渲染
    full_html = render.render_full_html(selected, analyses, tldr, today, len(items), len(selected))
    full_md = render.render_full_markdown(selected, analyses, tldr, today)
    feishu_txt = render.render_feishu(selected, analyses, tldr, today, len(items), len(selected))

    # 6. 落盘全文
    html_path = os.path.join(data_dir, f"daily-{today}.html")
    md_path = deliver.build_post_path(project_dir, today)
    with open(html_path, "w") as f:
        f.write(full_html)
    with open(md_path, "w") as f:
        f.write(full_md)
    log.info("wrote full html=%s md=%s", html_path, md_path)

    # 7. 部署
    deployed = False
    if not args.skip_deploy:
        try:
            deployed = deliver.deploy_ghpages(project_dir)
        except Exception as e:
            log.exception("deploy failed")
            errors.append(f"部署失败: {e}")

    # 8. 飞书推送
    pushed = False
    try:
        pushed = deliver.push_feishu(feishu_txt, "; ".join(errors) if errors else "")
    except Exception as e:
        log.exception("feishu push failed")
        errors.append(f"飞书推送失败: {e}")

    log.info("deployed=%s pushed=%s", deployed, pushed)
    if errors:
        # 已尽量通知，返回非零
        return 2
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", type=str, default=None)
    ap.add_argument("--hours", type=int, default=48)
    ap.add_argument("--skip-fetch", action="store_true")
    ap.add_argument("--skip-deploy", action="store_true")
    args = ap.parse_args()
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
