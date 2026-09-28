#!/bin/zsh
# Horizon 日报 · 生成任务（03:00 本地跑）
# 隔离进程 + caffeinate 防睡 + 剥代理直连 + 完整链路 + 落盘 GH Pages
HORIZON=/Users/constantine/.openclaw/workspace/projects/horizon
cd "$HORIZON"
set -a; . ./.env; set +a
export PATH="/usr/local/bin:$PATH"
LOG="data/daily/run-$(date +%Y-%m-%d).log"
# 互斥锁：03:00 主任务与 03:30 兜底可能重叠，同一时刻只允许一条管线在跑
LOCK=/tmp/horizon-gen.lock
if mkdir "$LOCK" 2>/dev/null; then
  echo $$ > "$LOCK/pid"
  trap 'rmdir "$LOCK" 2>/dev/null' EXIT
else
  oldpid=$(cat "$LOCK/pid" 2>/dev/null)
  if [ -n "$oldpid" ] && kill -0 "$oldpid" 2>/dev/null; then
    echo "==== $(date '+%F %T') SKIP: generate_daily.sh already running (pid $oldpid) ====" >> "$LOG"
    exit 0
  fi
  echo "==== $(date '+%F %T') stale lock (pid ${oldpid:-?}), taking over ====" >> "$LOG"
  rm -rf "$LOCK"; mkdir "$LOCK"; echo $$ > "$LOCK/pid"
  trap 'rmdir "$LOCK" 2>/dev/null' EXIT
fi
echo "==== run start $(date '+%F %T') pid $$ ====" >> "$LOG"
(
  # 保留 HTTP(S)_PROXY：X 抓取需经网关 egress 代理自动注入 TWITTERAPI_IO_KEY 明文
  # 其余源（Reddit/HN/PH/中文）在 fetch.py 内用 trust_env=False 直连，不受代理影响
  # 日志用 >> 追加：并发/重跑时保留前一次尝试的痕迹，不再互相覆盖
  env -u CURL_CA_BUNDLE -u SSL_CERT_FILE -u REQUESTS_CA_BUNDLE \
      caffeinate -i -s .venv/bin/python -m daily_pipeline.run --hours 48 \
  >> "$LOG" 2>&1
)
echo "EXIT=$?" >> "$LOG"
