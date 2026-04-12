# VisionStyle — Анализатор визуального стиля

[English](README.md) | **Русский**

> Загрузи фото → получи структурированный паспорт стиля: цвета, настроение, материалы, ключевые слова.

Построен на Python + FastAPI + Next.js + Claude Vision API.

## Что делает

VisionStyle анализирует любое изображение JPG, PNG или WebP и извлекает:

| Поле | Описание |
|------|----------|
| **style** | Стиль одной фразой (например, «Dark moody food photography») |
| **palette** | 5+ доминирующих цветов в виде HEX-образцов |
| **materials** | Определённые материалы (дерево, керамика, лён…) |
| **mood** | Эмоциональный тон изображения |
| **keywords** | Ключевые слова стиля в виде тегов |
| **verdict** | Одно предложение: почему это выглядит именно так |

## Быстрый старт (Веб-приложение)

```bash
# 1. Клонировать
git clone https://github.com/TinaUma/VisionStyle.git
cd VisionStyle
git submodule update --init

# 2. Настроить API-ключ
cp .env.example .env
# Открой .env и вставь ANTHROPIC_API_KEY

# 3. Запустить backend
pip install -r requirements.txt -r backend/requirements.txt
uvicorn backend.main:app --reload
# → http://localhost:8000

# 4. Запустить frontend (новый терминал)
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

Открой **http://localhost:3000**, загрузи фото, нажми **Анализировать стиль**.

## Быстрый старт (CLI)

```bash
python vision_cli.py --image photo.jpg --output report
```

Результат: `report.json` + `report.md`

## Архитектура

```
VisionStyle/
├── backend/             ← FastAPI (REST API)
│   └── main.py          ← POST /analyze, GET /health
├── frontend/            ← Next.js 16 + Tailwind CSS
│   └── app/page.tsx     ← UI загрузки + отображение результатов
├── image_processor.py   ← загрузка, ресайз до 1200px, base64
├── vision_agent.py      ← адаптер провайдеров (мульти-провайдер)
├── style_parser.py      ← извлечение StyleAnalysis из ответа LLM
├── exporter.py          ← запись report.json и report.md
└── vision_cli.py        ← точка входа CLI
```

## Поддержка нескольких провайдеров

| Провайдер | `VISION_PROVIDER=` | Требует |
|-----------|-------------------|---------|
| Claude (Anthropic) | `anthropic` | `ANTHROPIC_API_KEY` |
| OpenAI GPT-4o | `openai` | `OPENAI_API_KEY` |
| Groq (Llama Vision) | `groq` | `GROQ_API_KEY` |
| Together AI | `together` | `TOGETHER_API_KEY` |

Подробное сравнение провайдеров: [docs/vision_research.md](docs/vision_research.md)

## Стек

- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Frontend:** Next.js 16, React, Tailwind CSS, TypeScript
- **AI:** Anthropic Claude Vision API (claude-haiku-4-5-20251001)
- **Обработка изображений:** Pillow
- **Dev-процесс:** [фреймворк TAUSIK](https://gitlab.yumash.ru/tausik/core)

## Статус разработки

| Спринт | Статус | Описание |
|--------|--------|----------|
| Sprint 0 | ✅ Готово | CLI-скаффолд, проверка связи с API |
| Sprint 1 | ✅ Готово | Image pipeline + адаптер провайдеров |
| Sprint 2 | ✅ Готово | Vision logic + парсинг JSON |
| Sprint 3 | ✅ Готово | Экспорт CLI в JSON + Markdown |
| Sprint 4 | 🔄 В работе | Веб-приложение: FastAPI + Next.js |

## Лицензия

MIT
