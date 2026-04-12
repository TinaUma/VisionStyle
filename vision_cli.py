"""VisionStyle — Анализатор визуального стиля.

Подаёшь картинку → получаешь паспорт стиля в JSON и Markdown-отчёт.

Использование:
    python vision_cli.py --image photo.jpg
    python vision_cli.py --image photo.jpg --output my_report
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

    try:
        # Загрузка .env
        _load_env()

        # Шаг 1: Image pipeline
        print(f"Загрузка изображения: {args.image}")
        from image_processor import prepare_image
        image_b64, meta = prepare_image(args.image)
        print(f"  ✓ {meta.format} {meta.width}×{meta.height}px ({meta.size_kb} КБ)")

        # Шаг 2: Анализ через Vision API
        print("Анализ стиля через Vision API...")
        from vision_agent import analyze_style
        raw_response = analyze_style(image_b64, meta.media_type)
        print("  ✓ Ответ получен")

        # Шаг 3: Парсинг JSON из ответа
        print("Извлечение структуры стиля...")
        from style_parser import parse_response
        analysis = parse_response(raw_response)
        print(f"  ✓ Стиль: {analysis.style}")

        # Шаг 4: Экспорт
        print(f"Сохранение отчёта в {args.output}.*")
        from exporter import export_json, export_markdown
        json_path = export_json(meta, analysis, args.output)
        md_path = export_markdown(meta, analysis, args.output)
        print(f"  ✓ {json_path}")
        print(f"  ✓ {md_path}")

        print("\nГотово!")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка API: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Ошибка записи: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


def _load_env(path: str = ".env") -> None:
    import os
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


if __name__ == "__main__":
    main()
