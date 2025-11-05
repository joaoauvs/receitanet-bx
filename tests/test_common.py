import logging

import pytest

from src.modules.common import attempts, time_execution


def test_attempts_retries_until_success(monkeypatch):
    calls = {"value": 0}

    def fake_sleep(_seconds):
        return None

    monkeypatch.setattr("src.modules.common.time.sleep", fake_sleep)

    @attempts(max_attempts=3, waiting_time=0)
    def flaky():
        calls["value"] += 1
        if calls["value"] < 3:
            raise ValueError("temporary error")
        return "ok"

    assert flaky() == "ok"
    assert calls["value"] == 3


def test_attempts_raises_after_max_retries(monkeypatch):
    monkeypatch.setattr("src.modules.common.time.sleep", lambda _seconds: None)

    @attempts(max_attempts=2, waiting_time=0)
    def always_fail():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        always_fail()


def test_time_execution_logs_duration(caplog):
    @time_execution
    def simple():
        return 42

    with caplog.at_level(logging.INFO):
        result = simple()

    assert result == 42
    joined = " ".join(caplog.messages)
    assert "Execucao iniciada" in joined
    assert "Execucao finalizada" in joined
