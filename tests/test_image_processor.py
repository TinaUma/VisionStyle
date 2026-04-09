"""Тесты image_processor.py (Sprint 1)."""

from __future__ import annotations

import os
import tempfile

import pytest
from PIL import Image

from image_processor import (
    ImageMetadata,
    MAX_SIDE,
    load_image,
    prepare_image,
    resize_image,
    to_base64,
)


def make_image(path: str, size: tuple[int, int], fmt: str = "PNG") -> str:
    """Создать тестовое изображение и сохранить в path."""
    img = Image.new("RGB", size, color=(100, 150, 200))
    img.save(path, format=fmt)
    return path


# --- load_image ---

def test_load_jpeg(tmp_path):
    p = str(tmp_path / "test.jpg")
    make_image(p, (800, 600), "JPEG")
    img, meta = load_image(p)
    assert meta.format == "JPEG"
    assert meta.media_type == "image/jpeg"
    assert meta.width == 800
    assert meta.height == 600
    assert meta.size_kb > 0


def test_load_png(tmp_path):
    p = str(tmp_path / "test.png")
    make_image(p, (400, 300), "PNG")
    _, meta = load_image(p)
    assert meta.format == "PNG"
    assert meta.media_type == "image/png"


def test_load_webp(tmp_path):
    p = str(tmp_path / "test.webp")
    make_image(p, (400, 300), "WEBP")
    _, meta = load_image(p)
    assert meta.format == "WEBP"
    assert meta.media_type == "image/webp"


def test_load_nonexistent_file():
    with pytest.raises(FileNotFoundError, match="Файл не найден"):
        load_image("/nonexistent/path/image.png")


# --- resize_image ---

def test_resize_large_landscape(tmp_path):
    p = str(tmp_path / "big.png")
    make_image(p, (2400, 1200), "PNG")
    img, _ = load_image(p)
    resized = resize_image(img)
    assert max(resized.size) <= MAX_SIDE


def test_resize_large_portrait(tmp_path):
    p = str(tmp_path / "tall.png")
    make_image(p, (800, 2400), "PNG")
    img, _ = load_image(p)
    resized = resize_image(img)
    assert max(resized.size) <= MAX_SIDE


def test_resize_preserves_aspect_ratio(tmp_path):
    p = str(tmp_path / "wide.png")
    make_image(p, (2400, 1200), "PNG")
    img, _ = load_image(p)
    resized = resize_image(img)
    orig_ratio = 2400 / 1200
    new_ratio = resized.width / resized.height
    assert abs(orig_ratio - new_ratio) < 0.01


def test_resize_small_image_unchanged(tmp_path):
    p = str(tmp_path / "small.png")
    make_image(p, (400, 300), "PNG")
    img, _ = load_image(p)
    resized = resize_image(img)
    assert resized.size == (400, 300)


# --- to_base64 ---

def test_to_base64_returns_string(tmp_path):
    p = str(tmp_path / "test.png")
    make_image(p, (100, 100), "PNG")
    img, meta = load_image(p)
    b64 = to_base64(img, meta.format)
    assert isinstance(b64, str)
    assert len(b64) > 0


# --- prepare_image (full pipeline) ---

def test_prepare_image_pipeline(tmp_path):
    p = str(tmp_path / "big.jpg")
    make_image(p, (2000, 1500), "JPEG")
    b64, meta = prepare_image(p)
    assert isinstance(b64, str) and len(b64) > 0
    assert max(meta.width, meta.height) <= MAX_SIDE
    assert isinstance(meta, ImageMetadata)
