# Stage 1: Build Next.js static files
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
# API URL пустой = тот же сервер (FastAPI)
ENV NEXT_PUBLIC_API_URL=""
RUN npm run build

# Stage 2: Python backend + статика
FROM python:3.11-slim
WORKDIR /app

# Python зависимости
COPY requirements.txt ./
COPY backend/requirements.txt ./backend_requirements.txt
RUN pip install --no-cache-dir -r requirements.txt -r backend_requirements.txt

# Исходники проекта
COPY image_processor.py vision_agent.py style_parser.py exporter.py ./
COPY backend/ ./backend/

# Статика Next.js
COPY --from=frontend-builder /app/frontend/out ./frontend/out

# HuggingFace Spaces требует порт 7860
EXPOSE 7860

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
