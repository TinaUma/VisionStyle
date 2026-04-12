"""Vision provider adapter — абстракция над разными LLM-провайдерами.

Переключение провайдера через .env:
    VISION_PROVIDER=anthropic   # или openai / groq / together
    VISION_MODEL=claude-sonnet-4-5  # опционально, есть дефолты
    OPENAI_COMPATIBLE_BASE_URL=https://api.groq.com/openai/v1  # для groq/together
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod

DEFAULT_MODELS = {
    "anthropic": "claude-haiku-4-5-20251001",
    "openai": "gpt-4o-mini",
    "groq": "llama-3.2-11b-vision-preview",
    "together": "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
}

AVAILABLE_PROVIDERS = list(DEFAULT_MODELS.keys())


class VisionProvider(ABC):
    """Абстрактный интерфейс для vision-провайдеров."""

    @abstractmethod
    def analyze(self, image_b64: str, media_type: str, prompt: str) -> str:
        """Отправить изображение в модель и получить текстовый ответ.

        Args:
            image_b64: изображение в base64
            media_type: MIME-тип ("image/jpeg", "image/png", "image/webp")
            prompt: текстовый запрос к модели

        Returns:
            Текстовый ответ модели
        """


class AnthropicAdapter(VisionProvider):
    """Адаптер для Claude (Anthropic API)."""

    def __init__(self, model: str | None = None, api_key: str | None = None):
        import anthropic as _anthropic
        key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        if not key:
            raise ValueError("ANTHROPIC_API_KEY не задан")
        self.model = model or DEFAULT_MODELS["anthropic"]
        self.client = _anthropic.Anthropic(api_key=key)

    def analyze(self, image_b64: str, media_type: str, prompt: str) -> str:
        message = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_b64,
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        return message.content[0].text


class OpenAICompatibleAdapter(VisionProvider):
    """Адаптер для OpenAI-совместимых провайдеров (OpenAI, Groq, Together AI)."""

    def __init__(
        self,
        provider: str = "openai",
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
    ):
        import openai as _openai

        key_env = {
            "openai": "OPENAI_API_KEY",
            "groq": "GROQ_API_KEY",
            "together": "TOGETHER_API_KEY",
        }.get(provider, "OPENAI_API_KEY")

        key = api_key or os.environ.get(key_env, "")
        if not key:
            raise ValueError(f"{key_env} не задан")

        default_urls = {
            "groq": "https://api.groq.com/openai/v1",
            "together": "https://api.together.xyz/v1",
        }
        url = base_url or os.environ.get("OPENAI_COMPATIBLE_BASE_URL") or default_urls.get(provider)

        self.model = model or DEFAULT_MODELS.get(provider, "gpt-4o-mini")
        self.client = _openai.OpenAI(api_key=key, base_url=url)

    def analyze(self, image_b64: str, media_type: str, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{media_type};base64,{image_b64}"},
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )
        return response.choices[0].message.content


def analyze_style(image_b64: str, media_type: str, provider: VisionProvider | None = None, api_key: str | None = None) -> str:
    """Отправить изображение на анализ стиля и вернуть сырой ответ модели.

    Args:
        image_b64: изображение в base64
        media_type: MIME-тип ("image/jpeg", "image/png", "image/webp")
        provider: провайдер (если None — создаётся через get_provider())

    Returns:
        Сырой текст ответа модели (JSON или JSON в ```json блоке)

    Raises:
        ValueError: если ответ модели пустой
    """
    from style_parser import STYLE_ANALYSIS_PROMPT

    p = provider or get_provider(api_key=api_key)
    result = p.analyze(image_b64, media_type, STYLE_ANALYSIS_PROMPT)

    if not result or not result.strip():
        raise ValueError("Получен пустой ответ от модели. Проверь API-ключ и лимиты.")

    return result


def get_provider(
    provider: str | None = None,
    model: str | None = None,
    api_key: str | None = None,
) -> VisionProvider:
    """Фабрика: создать адаптер по имени провайдера.

    Читает VISION_PROVIDER и VISION_MODEL из окружения если не переданы явно.

    Raises:
        ValueError: если провайдер неизвестен.
    """
    name = (provider or os.environ.get("VISION_PROVIDER", "anthropic")).lower()
    mdl = model or os.environ.get("VISION_MODEL")

    if name == "anthropic":
        return AnthropicAdapter(model=mdl, api_key=api_key)
    elif name in ("openai", "groq", "together"):
        return OpenAICompatibleAdapter(provider=name, model=mdl, api_key=api_key)
    else:
        raise ValueError(
            f"Неизвестный провайдер: '{name}'. "
            f"Доступные: {', '.join(AVAILABLE_PROVIDERS)}"
        )
