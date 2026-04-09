"""Проверка связи с Claude API.

Запуск: python check_api.py
Требует: ANTHROPIC_API_KEY в .env или переменных окружения.
"""

import os
import sys


def load_env(path: str = ".env") -> None:
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


def main() -> None:
    load_env()

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("Ошибка: ANTHROPIC_API_KEY не задан. Создай .env файл по образцу .env.example")
        sys.exit(1)

    try:
        import anthropic
    except ImportError:
        print("Ошибка: пакет anthropic не установлен. Запусти: pip install anthropic")
        sys.exit(1)

    print("Подключение к Claude API...")
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=64,
        messages=[{"role": "user", "content": "Ответь одним словом: API работает?"}],
    )

    print("Ответ Claude:")
    print(message.content[0].text)
    print("\nСвязь с API установлена успешно.")


if __name__ == "__main__":
    main()
