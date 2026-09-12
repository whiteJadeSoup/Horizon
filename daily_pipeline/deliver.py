"""Horizon 聚合台 · 推送/部署层
1) 飞书推送（简要版日报）
2) GitHub Pages 部署（全文入库 docs/_posts + push，触发 Actions）
3) 失败/成功通知
"""
from __future__ import annotations

import logging
import os
import subprocess
import urllib.parse

log = logging.getLogger("horizon_daily.deliver")

SITE_URL = os.environ.get("HORIZON_SITE_URL", "https://whitejadesoup.github.io/Horizon/")


def _feishu_send(text: str) -> bool:
    """通过 OpenClaw message 工具投递——管线作为 OpenClaw agent 任务运行时可用。
    若直接 python 运行则回退到环境变量 FEISHU_WEBHOOK 的飞书机器人 webhook。"""
    webhook = os.environ.get("FEISHU_WEBHOOK")
    if not webhook:
        log.warning("no FEISHU_WEBHOOK and not running under agent; cannot push feishu")
        return False
    import json
    import urllib.request

    body = json.dumps({"msg_type": "text", "content": {"text": text}}).encode()
    req = urllib.request.Request(webhook, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            resp = json.load(r)
        ok = resp.get("code") == 0 or resp.get("Status") == 0
        if not ok:
            log.warning("feishu webhook rejected: %s", resp)
        return ok
    except Exception as e:
        log.warning("feishu webhook fail: %s", e)
        return False


def push_feishu(report_text: str, notify_error: str = "") -> bool:
    """推送日报；可选附加错误说明。"""
    if notify_error:
        report_text = f"{report_text}\n\n> ⚠️ 本次生成有异常：{notify_error}"
    return _feishu_send(report_text)


def _no_proxy_env() -> dict:
    env = dict(os.environ)
    for k in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy",
              "CURL_CA_BUNDLE", "SSL_CERT_FILE", "REQUESTS_CA_BUNDLE"):
        env.pop(k, None)
    return env


def deploy_ghpages(project_dir: str, docs_rel: str = "docs") -> bool:
    """把 docs/_posts 提交并 push main，触发 deploy-docs workflow。直连避免代理 403。"""
    repo = os.path.join(project_dir, ".git")
    if not os.path.isdir(repo):
        log.warning("not a git repo: %s", project_dir)
        return False
    env = _no_proxy_env()
    try:
        subprocess.run(["git", "-C", project_dir, "add", "-A", docs_rel],
                       check=True, capture_output=True, env=env)
        changed = subprocess.run(
            ["git", "-C", project_dir, "status", "--porcelain", docs_rel],
            check=True, capture_output=True, text=True, env=env,
        ).stdout.strip()
        if not changed:
            log.info("no docs changes; skip commit/push")
            return True
        subprocess.run(
            ["git", "-C", project_dir, "commit", "-m",
             f"docs: daily report {__import__('datetime').date.today()}"],
            check=True, capture_output=True, env=env,
        )
        subprocess.run(["git", "-C", project_dir, "push", "origin", "main"],
                       check=True, capture_output=True, env=env)
        log.info("pushed docs to origin/main; Actions deploys to gh-pages")
        _trigger_deploy(project_dir)
        return True
    except subprocess.CalledProcessError as e:
        log.warning("deploy fail: %s stderr=%s", e, (e.stderr or b"")[:300])
        return False


def _trigger_deploy(project_dir: str) -> None:
    """显式触发 Deploy Docs workflow（push 触发历史上偶发失效，加显式 dispatch 兑底）。"""
    try:
        subprocess.run(
            ["gh", "-R", "whiteJadeSoup/Horizon", "workflow", "run", "deploy-docs.yml"],
            check=True, capture_output=True, timeout=30, env=_no_proxy_env(),
        )
        log.info("explicitly dispatched deploy-docs workflow")
    except Exception as e:
        log.warning("explicit dispatch failed (push trigger may still cover): %s", e)


def build_post_path(project_dir: str, today: str) -> str:
    return os.path.join(project_dir, "docs", "_posts", f"{today}-summary-zh.md")
