"""Тесты exporter.py (Sprint 3)."""

from __future__ import annotations

import json
import os

import pytest

from exporter import export_json, export_markdown
from image_processor import ImageMetadata
from style_parser import StyleAnalysis


def make_meta():
    return ImageMetadata(
        path="/tmp/test.jpg",
        format="JPEG",
        media_type="image/jpeg",
        width=800,
        height=600,
        size_kb=120.5,
    )


def make_analysis():
    return StyleAnalysis(
        style="Scandinavian minimalism",
        palette=["#F5F5F0", "#E8E0D5", "#C4B9A8", "#8B7355", "#3D2B1F"],
        materials=["wood", "linen", "concrete"],
        mood=["calm", "airy", "neutral"],
        keywords=["minimal", "nordic", "clean", "natural", "muted"],
        verdict="The design achieves serenity through restrained palette and natural textures.",
    )


# --- export_json ---

def test_export_json_creates_file(tmp_path):
    out = export_json(make_meta(), make_analysis(), str(tmp_path / "report"))
    assert os.path.exists(out)
    assert out.endswith(".json")


def test_export_json_contains_all_fields(tmp_path):
    out = export_json(make_meta(), make_analysis(), str(tmp_path / "report"))
    with open(out, encoding="utf-8") as f:
        data = json.load(f)
    assert "image" in data
    assert "analysis" in data
    assert data["image"]["format"] == "JPEG"
    assert data["analysis"]["style"] == "Scandinavian minimalism"
    assert len(data["analysis"]["palette"]) >= 5


def test_export_json_with_full_path(tmp_path):
    out = export_json(make_meta(), make_analysis(), str(tmp_path / "result.json"))
    assert out.endswith(".json")
    assert os.path.exists(out)


def test_export_json_invalid_path():
    with pytest.raises(IOError, match="Не удалось записать"):
        export_json(make_meta(), make_analysis(), "/nonexistent/dir/report")


# --- export_markdown ---

def test_export_markdown_creates_file(tmp_path):
    out = export_markdown(make_meta(), make_analysis(), str(tmp_path / "report"))
    assert os.path.exists(out)
    assert out.endswith(".md")


def test_export_markdown_contains_table(tmp_path):
    out = export_markdown(make_meta(), make_analysis(), str(tmp_path / "report"))
    content = open(out, encoding="utf-8").read()
    assert "| Параметр | Значение |" in content
    assert "Scandinavian minimalism" in content


def test_export_markdown_contains_palette(tmp_path):
    out = export_markdown(make_meta(), make_analysis(), str(tmp_path / "report"))
    content = open(out, encoding="utf-8").read()
    assert "#F5F5F0" in content
    assert "#3D2B1F" in content


def test_export_markdown_contains_verdict(tmp_path):
    out = export_markdown(make_meta(), make_analysis(), str(tmp_path / "report"))
    content = open(out, encoding="utf-8").read()
    assert "serenity" in content


def test_export_markdown_invalid_path():
    with pytest.raises(IOError, match="Не удалось записать"):
        export_markdown(make_meta(), make_analysis(), "/nonexistent/dir/report")
