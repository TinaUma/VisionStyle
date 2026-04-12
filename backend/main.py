"""VisionStyle FastAPI backend.

Endpoints:
    GET  /health        — health check
    POST /analyze       — анализ изображения, возвращает StyleAnalysis JSON
"""

from __future__ import annotations

import sys
import os
import tempfile
from pathlib import Path

# Импортируем модули из корня проекта
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

# Загружаем .env из корня проекта
from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
async def analyze(file: UploadFile = File(...)):
    # Проверяем тип файла
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Неподдерживаемый формат: {file.content_type}. Используйте JPG, PNG или WebP.",
        )

    # Сохраняем во временный файл
    suffix = "." + (file.filename.rsplit(".", 1)[-1] if "." in file.filename else "jpg")
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        image_b64, meta = prepare_image(tmp_path)
        raw = analyze_style(image_b64, meta.media_type)
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
