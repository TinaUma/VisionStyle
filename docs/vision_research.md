# Vision Model Research — VisionStyle

Сравнение провайдеров для задачи анализа визуального стиля изображений.

## Сравнительная таблица

| Модель | Провайдер | Цена (вход / выход, 1M tok) | Контекст | Image input | Python SDK | Надёжность JSON | Примечания |
|--------|-----------|----------------------------|----------|-------------|------------|-----------------|------------|
| **claude-sonnet-4-5** | Anthropic | $3 / $15 | 200K | base64, URL, Files API | `anthropic` (official) | Отличная (native JSON schema) | Лучший баланс качество/цена для анализа стиля |
| **claude-haiku-4-5** | Anthropic | $1 / $5 | 200K | base64, URL, Files API | `anthropic` (official) | Отличная | Дешевле, чуть слабее для сложных сцен |
| **gpt-4o** | OpenAI | $2.50 / $10 | 128K | base64, URL, Files API | `openai` (official) | Отличная (Pydantic) | Зрелая экосистема, хорошо для стиля |
| **gpt-4o-mini** | OpenAI | $0.15 / $0.60 | 128K | base64, URL | `openai` (official) | Хорошая | Самый дешёвый вариант с vision |
| **gemini-1.5-flash** | Google | $0.35 / $1.05 | 1M | base64, URL, File API | `google-genai` (official) | Хорошая (JSON Schema) | Огромный контекст, стриминг |
| **gemini-1.5-pro** | Google | $1.25 / $3.75 | 2M | base64, URL, File API | `google-genai` (official) | Хорошая (JSON Schema) | Лучший для мультиизображений |
| **llama-3.2-90b-vision** | Meta / Groq | ~$0.27 / $0.27 | 8K | base64, URL | OpenAI-compatible | Требует промпт-инженерии | Сверхбыстрый (Groq), открытый |
| **llama-3.2-11b-vision** | Meta / Together AI | Free tier | 8K | base64, URL | OpenAI-compatible | Требует промпт-инженерии | Хорош для разработки/тестов |
| **qwen-vl** | Alibaba / Together AI | $0.41 / — | 32K–260K | base64, URL | OpenAI-compatible | Требует промпт-инженерии | Силён в графиках и схемах |

## Выводы

**Рекомендованный провайдер по умолчанию:** `claude-sonnet-4-5` — лучшее структурированное JSON-извлечение и качество анализа стиля.

**Резервный / дешёвый:** `gpt-4o-mini` — совместим с OpenAI SDK, простая замена.

**Для разработки/тестов (бесплатно):** `llama-3.2-11b-vision` через Together AI.

## Архитектурное решение

Все провайдеры подключаются через единый адаптер `VisionProvider`:
- **Anthropic** — нативный SDK
- **OpenAI-compatible** (OpenAI, Groq, Together AI) — один адаптер на всех через `openai` SDK
- **Google** — нативный `google-genai` SDK

Переключение провайдера — через флаг `--provider` или переменную `VISION_PROVIDER` в `.env`.
