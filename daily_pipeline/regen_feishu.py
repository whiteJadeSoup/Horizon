#!/usr/bin/env python3
"""从 data/daily/*.json 重建 render_feishu 输入并输出推送文本到 stdout。"""
import datetime as dt
import json
import os
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

from daily_pipeline import render  # noqa: E402
from daily_pipeline.fetch import ContentItem  # noqa: E402

DATA_DIR = os.path.join(PROJECT_DIR, "data", "daily")
today = dt.date.today().isoformat()


def load(name, default):
    p = os.path.join(DATA_DIR, name)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return default


items = [ContentItem(**it) for it in load("items.json", [])]
scores = load("scores.json", {})
analyses = load("analysis.json", {})
tldr = load("tldr.json", None)

# 应用打分（llm.apply_scores 同款逻辑：score/category/sublabel）
for i, it in enumerate(items):
    sc = scores.get(str(i))
    if not sc:
        continue
    it.score, it.category = float(sc[0]), int(sc[1])
    if len(sc) >= 3:
        it.extra["sublabel"] = str(sc[2])

selected = [it for it in items if it.score is not None and (it.score or 0) >= 6.0]
if not selected or not analyses:
    print("NO_CONTENT", file=sys.stderr)
    sys.exit(2)

txt = render.render_feishu(selected, analyses, tldr, today, len(items), len(selected))
out = os.path.join(DATA_DIR, f"feishu-{today}.txt")
with open(out, "w") as f:
    f.write(txt)
print(f"WROTE {out} ({len(txt)} chars), selected={len(selected)}/{len(items)}, tldr={'yes' if tldr else 'no'}", file=sys.stderr)
