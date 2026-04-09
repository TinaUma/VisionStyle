"""VisionStyle — Анализатор визуального стиля.

Подаёшь картинку → получаешь паспорт стиля в JSON и Markdown-отчёт.
"""

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vision_cli",
        description="VisionStyle — анализатор визуального стиля изображений. "
                    "Подай картинку, получи паспорт стиля в JSON и Markdown.",
    )
    parser.add_argument(
        "--image",
        required=True,
        metavar="PATH",
        help="Путь к изображению (JPG, PNG, WebP)",
    )
    parser.add_argument(
        "--output",
        default="report",
        metavar="PATH",
        help="Базовый путь для вывода (без расширения). "
             "Создаст <PATH>.json и <PATH>.md. По умолчанию: report",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # Точка входа — будет реализована в следующих спринтах
    print(f"Анализ изображения: {args.image}")
    print(f"Вывод в: {args.output}.json и {args.output}.md")
    print("(Логика анализа будет добавлена в Sprint 1–3)")


if __name__ == "__main__":
    main()
