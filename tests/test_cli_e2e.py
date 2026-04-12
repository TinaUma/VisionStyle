"""E2E тесты vision_cli.py (Sprint 3)."""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest
from PIL import Image


def make_test_image(tmp_path, size=(400, 300)):
    p = str(tmp_path / "sample.jpg")
    img = Image.new("RGB", size, color=(180, 120, 80))
    img.save(p, format="JPEG")
    return p


def run_cli(*args, env_override=None):
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    if env_override:
        env.update(env_override)
    return subprocess.run(
        [sys.executable, "vision_cli.py", *args],
        capture_output=True, text=True, encoding="utf-8", env=env,
    )


# --- Unit тесты CLI (без API) ---

def test_help():
    result = run_cli("--help")
    assert result.returncode == 0
    assert "--image" in result.stdout


def test_missing_image_arg():
    result = run_cli()
    assert result.returncode != 0


def test_nonexistent_image(tmp_path):
    result = run_cli("--image", "/nonexistent/photo.jpg", "--output", str(tmp_path / "out"))
    assert result.returncode != 0
    assert "Ошибка" in result.stderr


# --- E2E тест с реальным API ---

@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="Требует ANTHROPIC_API_KEY"
)
def test_full_pipeline_creates_reports(tmp_path):
    """Полный e2e: картинка → report.json + report.md."""
    img_path = make_test_image(tmp_path)
    out_base = str(tmp_path / "report")

    result = run_cli("--image", img_path, "--output", out_base)

    assert result.returncode == 0, f"CLI завершился с ошибкой:\n{result.stderr}"

    # Проверяем JSON
    json_path = f"{out_base}.json"
    assert os.path.exists(json_path), "report.json не создан"
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    assert "image" in data
    assert "analysis" in data
    assert len(data["analysis"]["palette"]) >= 5

    # Проверяем Markdown
    md_path = f"{out_base}.md"
    assert os.path.exists(md_path), "report.md не создан"
    content = open(md_path, encoding="utf-8").read()
    assert "| Параметр | Значение |" in content
    assert "#" in content  # hex цвета
