"""VisionStyle FastAPI backend.

Endpoints:
    GET  /health        — health check
    POST /analyze       — анализ изображения, возвращает StyleAnalysis JSON

В продакшене также раздаёт статику Next.js из frontend/out/.
"""

from __future__ import annotations

import sys
import os
import tempfile
from pathlib import Path

# Импортируем модули из корня проекта
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

# Загружаем .env из корня проекта (игнорируем если не найден — в продакшене не нужен)
from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from fastapi import FastAPI, File, Header, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from image_processor import prepare_image
from vision_agent import analyze_style
from style_parser import parse_response, ParseError


app = FastAPI(
    title="VisionStyle API",
    description="Анализатор визуального стиля изображений",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


class AnalyzeResponse(BaseModel):
    image: dict
    analysis: dict


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    file: UploadFile = File(...),
    x_api_key: str | None = Header(default=None),
):
    # Ключ: из заголовка запроса или из .env
    api_key = x_api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API ключ не передан. Укажи свой ANTHROPIC_API_KEY в настройках.",
        )

    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый формат: {file.content_type}. Используйте JPG, PNG или WebP.",
        )

    suffix = "." + (file.filename.rsplit(".", 1)[-1] if "." in file.filename else "jpg")
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        image_b64, meta = prepare_image(tmp_path)
        raw = analyze_style(image_b64, meta.media_type, api_key=api_key)
        analysis = parse_response(raw)
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (ValueError, ParseError) as e:
        raise HTTPException(status_code=502, detail=f"Ошибка анализа: {e}")
    finally:
        os.unlink(tmp_path)

    from dataclasses import asdict
    return AnalyzeResponse(
        image=asdict(meta),
        analysis=asdict(analysis),
    )


# Раздаём статику Next.js (только если сборка существует)
_static = ROOT / "frontend" / "out"
if _static.exists():
    app.mount("/_next", StaticFiles(directory=str(_static / "_next")), name="next-assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        return FileResponse(_static / "index.html")
