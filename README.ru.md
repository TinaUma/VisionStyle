# VisionStyle — Анализатор визуального стиля

[English](README.md) | **Русский**

> Подай картинку → получи структурированный паспорт стиля в JSON и Markdown-отчёт.

Консольный Python-инструмент на базе Claude Vision API. Никаких веб-сервисов — только CLI.

## Что делает

VisionStyle анализирует любое изображение JPG, PNG или WebP и извлекает:

| Поле | Описание |
|------|----------|
| **style** | Стиль одной фразой (например, «Скандинавский минимализм») |
| **palette** | 5+ доминирующих цветов в HEX |
| **materials** | Определённые материалы (дерево, металл, лён…) |
| **mood** | Эмоциональный тон (спокойный, смелый, игривый…) |
| **keywords** | Ключевые слова стиля |
| **verdict** | Одно предложение: почему это выглядит именно так |

## Быстрый старт

```bash
# 1. Клонировать
git clone https://github.com/TinaUma/VisionStyle.git
cd VisionStyle
git submodule update --init

# 2. Установить зависимости
pip install -r requirements.txt

# 3. Настроить API-ключ
cp .env.example .env
# Открой .env и вставь ANTHROPIC_API_KEY

# 4. Запустить
python vision_cli.py --image photo.jpg --output report
```

Результат: `report.json` + `report.md`

## Поддержка нескольких провайдеров

VisionStyle работает с разными vision-провайдерами через единый адаптер:

| Провайдер | Значение `VISION_PROVIDER=` | Требует |
|-----------|----------------------------|---------|
| Claude (Anthropic) | `anthropic` | `ANTHROPIC_API_KEY` |
| OpenAI GPT-4o | `openai` | `OPENAI_API_KEY` |
| Groq (Llama Vision) | `groq` | `GROQ_API_KEY` |
| Together AI | `together` | `TOGETHER_API_KEY` |

Переключение провайдера в `.env`:
```env
VISION_PROVIDER=anthropic
VISION_MODEL=claude-haiku-4-5-20251001
```

Подробное сравнение провайдеров: [docs/vision_research.md](docs/vision_research.md)

## Структура проекта

```
vision_cli.py        ← точка входа (--image, --output)
├── image_processor.py  ← загрузка, ресайз до 1200px, base64
├── vision_agent.py     ← адаптер провайдеров (Anthropic / OpenAI-compatible)
├── style_parser.py     ← извлечение StyleAnalysis из ответа LLM
└── exporter.py         ← запись report.json и report.md
```

## Стек

- Python 3.11+
- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python) / [OpenAI SDK](https://github.com/openai/openai-python)
- [Pillow](https://python-pillow.org/) для обработки изображений
- Dev-процесс: [фреймворк TAUSIK](https://github.com/Kibertum/SENAR)

## Статус разработки

| Спринт | Статус | Описание |
|--------|--------|----------|
| Sprint 0 | ✅ Готово | CLI-скаффолд, проверка связи с API |
| Sprint 1 | ✅ Готово | Image pipeline + адаптер провайдеров |
| Sprint 2 | 🔄 В работе | Vision logic + парсинг JSON |
| Sprint 3 | ⏳ Запланировано | Экспорт в JSON + Markdown |

## Лицензия

MIT
