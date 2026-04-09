"""Тесты точки входа CLI (Sprint 0)."""

import os
import subprocess
import sys


def run_cli(*args):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    return subprocess.run(
        [sys.executable, "vision_cli.py", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )


def test_help():
    result = run_cli("--help")
    assert result.returncode == 0
    assert "--image" in result.stdout
    assert "--output" in result.stdout


def test_missing_image_arg():
    result = run_cli()
    assert result.returncode != 0
    assert "--image" in result.stderr
