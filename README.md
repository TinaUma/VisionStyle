---
title: VisionStyle
emoji: 🎨
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
---

# VisionStyle — Visual Style Analyzer

**English** | [Русский](README.ru.md)

> Upload a photo → get a structured visual style passport: colors, mood, materials, keywords.

## Live Demo

**[https://tinauma-visionstyle.hf.space](https://tinauma-visionstyle.hf.space)**

![VisionStyle demo — fruit board analysis](printscreen/avocado%20deployHuggingface.PNG)

Built with Python + FastAPI + Next.js + Claude Vision API.

## What it does

VisionStyle analyzes any JPG, PNG, or WebP image and extracts:

| Field | Description |
|-------|-------------|
| **style** | One-phrase visual style (e.g. "Dark moody food photography") |
| **palette** | 5+ dominant colors as HEX swatches |
| **materials** | Detected materials (wood, ceramic, linen…) |
| **mood** | Emotional tone of the image |
| **keywords** | Style descriptors as tags |
| **verdict** | One sentence: why it looks the way it does |

## Quick Start (Web App)

```bash
# 1. Clone
git clone https://github.com/TinaUma/VisionStyle.git
cd VisionStyle
git submodule update --init

# 2. Configure API key
cp .env.example .env
# Edit .env → set ANTHROPIC_API_KEY

# 3. Start backend
pip install -r requirements.txt -r backend/requirements.txt
uvicorn backend.main:app --reload
# → http://localhost:8000

# 4. Start frontend (new terminal)
cd frontend
npm install
npm run dev
# → http://localhost:3000
```

Open **http://localhost:3000**, drop a photo, click **Analyze**.

## Quick Start (CLI)

```bash
python vision_cli.py --image photo.jpg --output report
```

Output: `report.json` + `report.md`

## Architecture

```
VisionStyle/
├── backend/             ← FastAPI (REST API)
│   └── main.py          ← POST /analyze, GET /health
├── frontend/            ← Next.js 16 + Tailwind CSS
│   └── app/page.tsx     ← Upload UI + results display
├── image_processor.py   ← load, resize to 1200px, base64
├── vision_agent.py      ← VisionProvider adapter (multi-provider)
├── style_parser.py      ← extract StyleAnalysis from LLM response
├── exporter.py          ← write report.json and report.md
└── vision_cli.py        ← CLI entry point
```

## Multi-provider support

| Provider | `VISION_PROVIDER=` | Requires |
|----------|--------------------|---------|
| Claude (Anthropic) | `anthropic` | `ANTHROPIC_API_KEY` |
| OpenAI GPT-4o | `openai` | `OPENAI_API_KEY` |
| Groq (Llama Vision) | `groq` | `GROQ_API_KEY` |
| Together AI | `together` | `TOGETHER_API_KEY` |

See [docs/vision_research.md](docs/vision_research.md) for full provider comparison.

## Stack

- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Frontend:** Next.js 16, React, Tailwind CSS, TypeScript
- **AI:** Anthropic Claude Vision API (claude-haiku-4-5-20251001)
- **Image processing:** Pillow
- **Dev workflow:** [TAUSIK framework](https://gitlab.yumash.ru/tausik/core)

## Development status

| Sprint | Status | Description |
|--------|--------|-------------|
| Sprint 0 | ✅ Done | CLI scaffold, API connectivity |
| Sprint 1 | ✅ Done | Image pipeline + multi-provider adapter |
| Sprint 2 | ✅ Done | Vision logic + JSON parsing |
| Sprint 3 | ✅ Done | CLI export to JSON + Markdown |
| Sprint 4 | 🔄 In progress | Web app: FastAPI + Next.js |

## License

MIT
