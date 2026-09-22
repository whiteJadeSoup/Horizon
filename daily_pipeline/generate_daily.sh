#!/bin/zsh
# Horizon 日报 · 生成任务（03:00 本地跑）
# 隔离进程 + caffeinate 防睡 + 剥代理直连 + 完整链路 + 落盘 GH Pages
HORIZON=/Users/constantine/.openclaw/workspace/projects/horizon
cd "$HORIZON"
set -a; . ./.env; set +a
export PATH="/usr/local/bin:$PATH"
LOG="data/daily/run-$(date +%Y-%m-%d).log"
(
  # 保留 HTTP(S)_PROXY：X 抓取需经网关 egress 代理自动注入 TWITTERAPI_IO_KEY 明文
  # 其余源（Reddit/HN/PH/中文）在 fetch.py 内用 trust_env=False 直连，不受代理影响
  env -u CURL_CA_BUNDLE -u SSL_CERT_FILE -u REQUESTS_CA_BUNDLE \
      caffeinate -i -s .venv/bin/python -m daily_pipeline.run --hours 48 \
  > "$LOG" 2>&1
)
echo "EXIT=$?" >> "$LOG"
