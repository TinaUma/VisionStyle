"""Тесты style_parser.py (Sprint 2)."""

from __future__ import annotations

import pytest

from style_parser import ParseError, StyleAnalysis, parse_response


VALID_JSON = """{
  "style": "Scandinavian minimalism",
  "palette": ["#F5F5F0", "#E8E0D5", "#C4B9A8", "#8B7355", "#3D2B1F"],
  "materials": ["wood", "linen", "concrete"],
  "mood": ["calm", "airy", "neutral"],
  "keywords": ["minimal", "nordic", "clean", "natural", "muted"],
  "verdict": "The design achieves serenity through restrained palette and natural textures."
}"""

VALID_JSON_IN_MARKDOWN = """Here is the analysis:

```json
{
  "style": "Dark industrial",
  "palette": ["#1A1A1A", "#2D2D2D", "#4A4A4A", "#8C8C8C", "#C0C0C0"],
  "materials": ["metal", "concrete", "glass"],
  "mood": ["bold", "edgy", "urban"],
  "keywords": ["dark", "industrial", "raw", "urban", "texture"],
  "verdict": "Raw materials and monochromatic palette create a powerful industrial atmosphere."
}
```"""

VALID_JSON_IN_PLAIN_BACKTICKS = """```
{
  "style": "Bohemian eclectic",
  "palette": ["#D4956A", "#8B4513", "#556B2F", "#9370DB", "#DAA520"],
  "materials": ["rattan", "cotton", "ceramic"],
  "mood": ["warm", "playful", "eclectic"],
  "keywords": ["boho", "colorful", "layered", "artsy", "free"],
  "verdict": "Layered textures and warm earth tones evoke a free-spirited bohemian aesthetic."
}
```"""


# --- Успешные сценарии ---

def test_parse_clean_json():
    result = parse_response(VALID_JSON)
    assert isinstance(result, StyleAnalysis)
    assert result.style == "Scandinavian minimalism"
    assert len(result.palette) >= 5
    assert all(c.startswith("#") for c in result.palette)
    assert len(result.keywords) > 0
    assert result.verdict


def test_parse_json_in_markdown_block():
    result = parse_response(VALID_JSON_IN_MARKDOWN)
    assert result.style == "Dark industrial"
    assert len(result.palette) >= 5


def test_parse_json_in_plain_backticks():
    result = parse_response(VALID_JSON_IN_PLAIN_BACKTICKS)
    assert result.style == "Bohemian eclectic"


def test_palette_minimum_5_colors():
    result = parse_response(VALID_JSON)
    assert len(result.palette) >= 5


def test_all_fields_present():
    result = parse_response(VALID_JSON)
    assert result.style
    assert result.palette
    assert result.materials
    assert result.mood
    assert result.keywords
    assert result.verdict


# --- Негативные сценарии ---

def test_empty_response_raises_parse_error():
    with pytest.raises(ParseError, match="пустой ответ"):
        parse_response("")


def test_whitespace_response_raises_parse_error():
    with pytest.raises(ParseError, match="пустой ответ"):
        parse_response("   \n  ")


def test_invalid_json_raises_parse_error():
    with pytest.raises(ParseError, match="Не удалось распарсить"):
        parse_response("This is not JSON at all, just plain text.")


def test_missing_fields_raises_parse_error():
    incomplete = '{"style": "minimal", "palette": ["#fff", "#000", "#aaa", "#bbb", "#ccc"]}'
    with pytest.raises(ParseError, match="Отсутствуют обязательные поля"):
        parse_response(incomplete)


def test_palette_too_short_raises_parse_error():
    short_palette = """{
      "style": "minimal",
      "palette": ["#fff", "#000"],
      "materials": ["wood"],
      "mood": ["calm"],
      "keywords": ["simple"],
      "verdict": "Too simple."
    }"""
    with pytest.raises(ParseError, match="минимум 5 цветов"):
        parse_response(short_palette)
