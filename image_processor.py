"""Загрузка, ресайз и конвертация изображения в base64 для Vision API."""

from __future__ import annotations

import base64
import io
import os
from dataclasses import dataclass

from PIL import Image


SUPPORTED_FORMATS = {"JPEG", "PNG", "WEBP"}
MAX_SIDE = 1200

MEDIA_TYPES = {
    "JPEG": "image/jpeg",
    "PNG": "image/png",
    "WEBP": "image/webp",
}


@dataclass
class ImageMetadata:
    path: str
    format: str          # "JPEG" | "PNG" | "WEBP"
    media_type: str      # "image/jpeg" | ...
    width: int
    height: int
    size_kb: float


def load_image(path: str) -> tuple[Image.Image, ImageMetadata]:
    """Загрузить изображение и вернуть объект PIL + метаданные.

    Raises:
        FileNotFoundError: если файл не существует.
        ValueError: если формат не поддерживается.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл не найден: {path}")

    img = Image.open(path)
    fmt = img.format or ""

    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Формат '{fmt}' не поддерживается. Допустимые: JPG, PNG, WebP."
        )

    size_kb = os.path.getsize(path) / 1024
    meta = ImageMetadata(
        path=path,
        format=fmt,
        media_type=MEDIA_TYPES[fmt],
        width=img.width,
        height=img.height,
        size_kb=round(size_kb, 1),
    )
    return img, meta


def resize_image(img: Image.Image, max_side: int = MAX_SIDE) -> Image.Image:
    """Уменьшить изображение так, чтобы длинная сторона не превышала max_side.

    Если изображение уже меньше — возвращает без изменений.
    """
    w, h = img.size
    longest = max(w, h)
    if longest <= max_side:
        return img

    scale = max_side / longest
    new_size = (int(w * scale), int(h * scale))
    return img.resize(new_size, Image.LANCZOS)


def to_base64(img: Image.Image, fmt: str) -> str:
    """Конвертировать PIL Image в base64-строку."""
    buffer = io.BytesIO()
    save_fmt = "JPEG" if fmt == "JPEG" else fmt
    img.save(buffer, format=save_fmt)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def prepare_image(path: str) -> tuple[str, ImageMetadata]:
    """Полный pipeline: загрузка → ресайз → base64.

    Returns:
        (base64_string, metadata)
    """
    img, meta = load_image(path)
    img = resize_image(img)

    # Обновляем размеры после ресайза
    meta.width, meta.height = img.size

    b64 = to_base64(img, meta.format)
    return b64, meta
