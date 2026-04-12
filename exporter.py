"""Экспорт результатов анализа в JSON и Markdown."""

from __future__ import annotations

import json
import os
from dataclasses import asdict

from image_processor import ImageMetadata
from style_parser import StyleAnalysis


def export_json(meta: ImageMetadata, analysis: StyleAnalysis, path: str) -> str:
    """Записать результат анализа в JSON файл.

    Args:
        meta: метаданные изображения
        analysis: результат анализа стиля
        path: базовый путь (без расширения) или полный путь с .json

    Returns:
        Путь к созданному файлу

    Raises:
        IOError: если файл невозможно записать
    """
    out = path if path.endswith(".json") else f"{path}.json"
    data = {
        "image": asdict(meta),
        "analysis": asdict(analysis),
    }
    try:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        raise IOError(f"Не удалось записать файл {out}: {e}") from e
    return out


def export_markdown(meta: ImageMetadata, analysis: StyleAnalysis, path: str) -> str:
    """Записать результат анализа в Markdown файл.

    Args:
        meta: метаданные изображения
        analysis: результат анализа стиля
        path: базовый путь (без расширения) или полный путь с .md

    Returns:
        Путь к созданному файлу

    Raises:
        IOError: если файл невозможно записать
    """
    out = path if path.endswith(".md") else f"{path}.md"

    palette_swatches = " ".join(
        f"`{color}`" for color in analysis.palette
    )

    lines = [
        f"# VisionStyle Report",
        f"",
        f"**Файл:** `{os.path.basename(meta.path)}`  ",
        f"**Формат:** {meta.format} | **Размер:** {meta.width}×{meta.height}px | **Вес:** {meta.size_kb} КБ",
        f"",
        f"---",
        f"",
        f"## Стиль",
        f"",
        f"> {analysis.style}",
        f"",
        f"## Вердикт",
        f"",
        f"> {analysis.verdict}",
        f"",
        f"---",
        f"",
        f"## Характеристики",
        f"",
        f"| Параметр | Значение |",
        f"|----------|----------|",
        f"| Стиль | {analysis.style} |",
        f"| Материалы | {', '.join(analysis.materials)} |",
        f"| Настроение | {', '.join(analysis.mood)} |",
        f"| Ключевые слова | {', '.join(analysis.keywords)} |",
        f"",
        f"## Цветовая палитра",
        f"",
        palette_swatches,
        f"",
    ]

    # Таблица цветов
    lines.append("| # | HEX |")
    lines.append("|---|-----|")
    for i, color in enumerate(analysis.palette, 1):
        lines.append(f"| {i} | {color} |")

    lines.append("")

    try:
        with open(out, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    except OSError as e:
        raise IOError(f"Не удалось записать файл {out}: {e}") from e
    return out
