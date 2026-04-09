"""Тесты check_api.py (Sprint 0)."""

import os
import subprocess
import sys


def run_check_api(env_override=None):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    if env_override:
        env.update(env_override)
    return subprocess.run(
        [sys.executable, "check_api.py"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def test_missing_api_key():
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    # убираем .env из пути, запускаем из другой директории
    result = subprocess.run(
        [sys.executable, "check_api.py"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**env, "ANTHROPIC_API_KEY": "", "PYTHONIOENCODING": "utf-8"},
    )
    assert result.returncode != 0
    assert "ANTHROPIC_API_KEY" in result.stdout or "ANTHROPIC_API_KEY" in result.stderr
