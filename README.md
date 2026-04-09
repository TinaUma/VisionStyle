# VisionStyle — Visual Style Analyzer

> Feed an image → get a structured style passport in JSON and a Markdown report.

Built with Python + Claude Vision API. No web services, no bloat — pure CLI tool.

## What it does

VisionStyle analyzes any JPG, PNG, or WebP image and extracts:

| Field | Description |
|-------|-------------|
| **style** | One-phrase visual style (e.g. "Scandinavian minimalism") |
| **palette** | 5+ dominant colors as HEX codes |
| **materials** | Detected materials (wood, metal, linen…) |
| **mood** | Emotional tone (calm, bold, playful…) |
| **keywords** | Style descriptors |
| **verdict** | One sentence: why it looks the way it does |

## Quick Start

```bash
# 1. Clone
git clone https://github.com/TinaUma/VisionStyle.git
cd VisionStyle
git submodule update --init

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API key
cp .env.example .env
# Edit .env and set your ANTHROPIC_API_KEY

# 4. Run
python vision_cli.py --image photo.jpg --output report
```

Output: `report.json` + `report.md`

## Multi-provider support

VisionStyle works with multiple vision providers via a unified adapter:

| Provider | Set `VISION_PROVIDER=` | Requires |
|----------|----------------------|---------|
| Claude (Anthropic) | `anthropic` | `ANTHROPIC_API_KEY` |
| OpenAI GPT-4o | `openai` | `OPENAI_API_KEY` |
| Groq (Llama Vision) | `groq` | `GROQ_API_KEY` |
| Together AI | `together` | `TOGETHER_API_KEY` |

Switch providers in `.env`:
```env
VISION_PROVIDER=anthropic
VISION_MODEL=claude-haiku-4-5-20251001
```

See [docs/vision_research.md](docs/vision_research.md) for full provider comparison.

## Project structure

```
vision_cli.py        ← entry point (--image, --output)
├── image_processor.py  ← load, resize to 1200px, base64
├── vision_agent.py     ← VisionProvider adapter (Anthropic / OpenAI-compatible)
├── style_parser.py     ← extract StyleAnalysis from LLM response
└── exporter.py         ← write report.json and report.md
```

## Stack

- Python 3.11+
- [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python) / [OpenAI SDK](https://github.com/openai/openai-python)
- [Pillow](https://python-pillow.org/) for image processing
- Dev workflow: [TAUSIK framework](https://github.com/Kibertum/SENAR)

## Development status

| Sprint | Status | Description |
|--------|--------|-------------|
| Sprint 0 | ✅ Done | CLI scaffold, API connectivity check |
| Sprint 1 | ✅ Done | Image pipeline + multi-provider adapter |
| Sprint 2 | 🔄 In progress | Vision logic + JSON parsing |
| Sprint 3 | ⏳ Planned | Export to JSON + Markdown |

## License

MIT
