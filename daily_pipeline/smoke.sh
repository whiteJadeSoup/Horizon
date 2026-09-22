#!/bin/zsh
cd /Users/constantine/.openclaw/workspace/projects/horizon
set -a; . .env; set +a
export PATH="/usr/local/bin:$PATH"
# 真实冒烟：抓取→打分→分析→TLDR→渲染（跳过部署和飞书推送，先看产物）
.venv/bin/python -m daily_pipeline.run --hours 48 --skip-deploy 2>&1 | tee data/daily/smoke.log
echo "SMOKE_EXIT=$?"
