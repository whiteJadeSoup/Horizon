import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.ai import codex_subscription as subscription


def good_reply():
    return {"status": "ok", "result": {"meta": {
        "agentMeta": {"provider": "openai", "model": "gpt-6.1-sol",
                      "agentHarnessId": "codex", "credentialSource": {"kind": "profile"},
                      "terminalReceipt": {"effective": {"provider": "openai", "model": "gpt-6.1-sol"},
                                          "rerouted": False, "successfulToolNames": []}},
        "executionTrace": {"fallbackUsed": False,
                           "attempts": [{"provider": "openai", "model": "gpt-6.1-sol", "result": "success"}]},
        "completion": {"finishReason": "stop"}, "finalAssistantVisibleText": '{"ok":true}',
    }}}


def setup_runner(monkeypatch, reply, returncode=0):
    monkeypatch.setattr(subscription.shutil, "which", lambda _: "/usr/local/bin/openclaw")
    calls = []

    def run(argv, **kwargs):
        if argv[1:5] == ["models", "auth", "list", "--agent"]:
            return SimpleNamespace(returncode=0, stdout=json.dumps({"profiles": [
                {"id": "openai:chatgpt", "provider": "openai", "type": "oauth"}
            ]}))
        prompt_path = Path(argv[argv.index("--message-file") + 1])
        calls.append((argv, kwargs, prompt_path, prompt_path.read_text()))
        return SimpleNamespace(returncode=returncode, stdout=json.dumps(reply))

    monkeypatch.setattr(subscription.subprocess, "run", run)
    return calls


def test_subscription_only_no_api_key_fallback_or_delivery(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "unusable-test-placeholder")
    monkeypatch.setenv("CODEX_API_KEY", "unusable-test-placeholder")
    calls = setup_runner(monkeypatch, good_reply())
    assert subscription.complete_subscription([{"role": "user", "content": "news"}]) == '{"ok":true}'
    argv, kwargs, prompt_path, prompt = calls[0]
    assert "exec" not in argv and "--deliver" not in argv and "--fallback" not in argv
    assert argv[argv.index("--agent") + 1] == "horizon-text"
    assert argv[argv.index("--model") + 1] == "openai/gpt-6.1-sol@openai:chatgpt"
    assert "OPENAI_API_KEY" not in kwargs["env"] and "CODEX_API_KEY" not in kwargs["env"]
    assert "news" in prompt and not prompt_path.exists()


@pytest.mark.parametrize("path,value", [
    (("agentMeta", "provider"), "agent-plan"),
    (("agentMeta", "model"), "glm-5-3-flash"),
    (("agentMeta", "agentHarnessId"), "openclaw"),
    (("agentMeta", "credentialSource", "kind"), "env"),
    (("agentMeta", "terminalReceipt", "successfulToolNames"), ["message"]),
    (("agentMeta", "terminalReceipt", "rerouted"), True),
    (("executionTrace", "fallbackUsed"), True),
    (("executionTrace", "attempts"), [{"provider": "agent-plan", "model": "glm-5-3-flash"}]),
    (("completion", "finishReason"), "length"),
    (("finalAssistantVisibleText",), ""),
    (("aborted",), True),
])
def test_rejects_unsafe_or_incomplete_receipts(monkeypatch, path, value):
    reply = copy.deepcopy(good_reply())
    node = reply["result"]["meta"]
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value
    calls = setup_runner(monkeypatch, reply)
    with pytest.raises(subscription.SubscriptionError):
        subscription.complete_subscription([{"role": "user", "content": "news"}])
    assert len(calls) == 1


def test_rejects_auth_failure_without_retry(monkeypatch):
    calls = setup_runner(monkeypatch, {"ok": False, "error": {"type": "auth"}}, 1)
    with pytest.raises(subscription.SubscriptionError):
        subscription.complete_subscription([])
    assert len(calls) == 1


def test_calls_use_fresh_sessions(monkeypatch):
    calls = setup_runner(monkeypatch, good_reply())
    subscription.complete_subscription([])
    subscription.complete_subscription([])
    keys = [c[0][c[0].index("--session-key") + 1] for c in calls]
    assert keys[0] != keys[1]


def test_rejects_legacy_model_before_call():
    with pytest.raises(subscription.SubscriptionError, match="OpenAI"):
        subscription.complete_subscription([], model="glm-5-3-flash")


def test_rejects_api_profile_before_inference(monkeypatch):
    monkeypatch.setattr(subscription.shutil, "which", lambda _: "/usr/local/bin/openclaw")
    calls = []

    def run(argv, **kwargs):
        calls.append(argv)
        return SimpleNamespace(returncode=0, stdout=json.dumps({"profiles": [
            {"id": "openai:chatgpt", "provider": "openai", "type": "api_key"}
        ]}))

    monkeypatch.setattr(subscription.subprocess, "run", run)
    with pytest.raises(subscription.SubscriptionError, match="OAuth"):
        subscription.complete_subscription([])
    assert len(calls) == 1 and calls[0][1] == "models"


def test_native_client_rejects_api_or_fallback_configuration():
    from src.ai.client import CodexSubscriptionClient
    from src.models import AIConfig

    with pytest.raises(ValueError, match="API keys"):
        CodexSubscriptionClient(AIConfig(
            provider="codex_subscription", model="gpt-6.1-sol", api_key_env="OPENAI_API_KEY",
        ))
