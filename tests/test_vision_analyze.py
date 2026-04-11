"""Тесты analyze_style в vision_agent.py (Sprint 2)."""

from __future__ import annotations

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

from vision_agent import analyze_style, get_provider
from style_parser import parse_response


def make_test_image(tmp_path, size=(200, 200)):
    """Создать тестовое PNG изображение."""
    p = str(tmp_path / "test.png")
    img = Image.new("RGB", size, color=(180, 120, 80))
    img.save(p, format="PNG")
    return p


# --- Unit тесты с моком ---

def test_analyze_style_returns_string():
    mock_provider = MagicMock()
    mock_provider.analyze.return_value = '{"style": "test", "palette": ["#fff","#000","#aaa","#bbb","#ccc"], "materials": [], "mood": [], "keywords": [], "verdict": "test"}'
    result = analyze_style("base64data", "image/png", provider=mock_provider)
    assert isinstance(result, str)
    assert len(result) > 0


def test_analyze_style_uses_style_prompt():
    from style_parser import STYLE_ANALYSIS_PROMPT
    mock_provider = MagicMock()
    mock_provider.analyze.return_value = '{"style":"x","palette":["#1","#2","#3","#4","#5"],"materials":[],"mood":[],"keywords":[],"verdict":"x"}'
    analyze_style("b64", "image/jpeg", provider=mock_provider)
    call_args = mock_provider.analyze.call_args
    assert call_args[0][2] == STYLE_ANALYSIS_PROMPT


def test_analyze_style_empty_response_raises():
    mock_provider = MagicMock()
    mock_provider.analyze.return_value = ""
    with pytest.raises(ValueError, match="пустой ответ"):
        analyze_style("b64", "image/png", provider=mock_provider)


def test_analyze_style_whitespace_response_raises():
    mock_provider = MagicMock()
    mock_provider.analyze.return_value = "   \n  "
    with pytest.raises(ValueError, match="пустой ответ"):
        analyze_style("b64", "image/png", provider=mock_provider)


def test_analyze_style_result_parseable():
    """Результат analyze_style должен успешно парситься через parse_response."""
    mock_provider = MagicMock()
    mock_provider.analyze.return_value = """{
        "style": "Modern minimalism",
        "palette": ["#F0F0F0", "#E0E0E0", "#C0C0C0", "#808080", "#404040"],
        "materials": ["glass", "steel"],
        "mood": ["clean", "modern"],
        "keywords": ["minimal", "sleek", "modern", "clean", "simple"],
        "verdict": "Monochromatic palette and geometric forms define this minimalist aesthetic."
    }"""
    raw = analyze_style("b64", "image/png", provider=mock_provider)
    analysis = parse_response(raw)
    assert analysis.style == "Modern minimalism"
    assert len(analysis.palette) >= 5


# --- Интеграционный тест с реальным API ---

@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="Требует ANTHROPIC_API_KEY"
)
def test_analyze_style_real_api(tmp_path):
    """Реальный вызов API с тестовым изображением."""
    from image_processor import prepare_image

    img_path = make_test_image(tmp_path)
    b64, meta = prepare_image(img_path)

    raw = analyze_style(b64, meta.media_type)
    assert raw and raw.strip()

    analysis = parse_response(raw)
    assert analysis.style
    assert len(analysis.palette) >= 5
    assert analysis.verdict
