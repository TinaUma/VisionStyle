"""Извлечение структуры StyleAnalysis из ответа LLM.

Модель иногда оборачивает JSON в ```json ... ``` — парсер это обрабатывает.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass


STYLE_ANALYSIS_PROMPT = """Analyze the visual style of this image and respond with a JSON object.

IMPORTANT: Return ONLY the JSON object, no markdown, no explanation, no ```json wrapper.

Required JSON structure:
{
  "style": "one phrase describing the overall visual style",
  "palette": ["#hex1", "#hex2", "#hex3", "#hex4", "#hex5"],
  "materials": ["material1", "material2"],
  "mood": ["mood1", "mood2", "mood3"],
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
  "verdict": "one sentence explaining why this looks the way it does"
}

Rules:
- palette: exactly 5 or more dominant colors as HEX codes (e.g. #F5E6D3)
- style: single descriptive phrase (e.g. "Scandinavian minimalism", "Dark industrial")
- verdict: one sentence maximum
- All text in English"""


@dataclass
class StyleAnalysis:
    style: str
    palette: list[str]
    materials: list[str]
    mood: list[str]
    keywords: list[str]
    verdict: str


class ParseError(Exception):
    """Ошибка парсинга ответа LLM."""


def _extract_json_string(raw: str) -> str:
    """Извлечь JSON-строку из сырого текста модели.

    Обрабатывает:
    - чистый JSON
    - JSON обёрнутый в ```json ... ```
    - JSON обёрнутый в ``` ... ```
    """
    text = raw.strip()

    # Попытка 1: ищем ```json ... ``` или ``` ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        return match.group(1).strip()

    # Попытка 2: ищем первый { ... } блок
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return match.group(0)

    return text


def _validate(data: dict) -> StyleAnalysis:
    """Валидировать и создать StyleAnalysis из словаря."""
    required = ["style", "palette", "materials", "mood", "keywords", "verdict"]
    missing = [f for f in required if f not in data]
    if missing:
        raise ParseError(f"Отсутствуют обязательные поля: {', '.join(missing)}")

    palette = data["palette"]
    if not isinstance(palette, list) or len(palette) < 5:
        raise ParseError(
            f"palette должен содержать минимум 5 цветов, получено: {len(palette) if isinstance(palette, list) else 0}"
        )

    return StyleAnalysis(
        style=str(data["style"]),
        palette=[str(c) for c in palette],
        materials=[str(m) for m in data.get("materials", [])],
        mood=[str(m) for m in data.get("mood", [])],
        keywords=[str(k) for k in data.get("keywords", [])],
        verdict=str(data["verdict"]),
    )


def parse_response(raw_text: str) -> StyleAnalysis:
    """Распарсить сырой ответ LLM в StyleAnalysis.

    Args:
        raw_text: текстовый ответ от модели

    Returns:
        StyleAnalysis с заполненными полями

    Raises:
        ParseError: если JSON невалидный или отсутствуют обязательные поля
    """
    if not raw_text or not raw_text.strip():
        raise ParseError("Получен пустой ответ от модели")

    json_str = _extract_json_string(raw_text)

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ParseError(
            f"Не удалось распарсить JSON из ответа модели: {e}\n"
            f"Полученный текст (первые 200 символов): {raw_text[:200]}"
        ) from e

    return _validate(data)
