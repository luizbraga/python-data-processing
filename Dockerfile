# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    MODULE=app.main \
    APP_VAR=app

WORKDIR /app

COPY . /app
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["sh", "-c", "uvicorn ${MODULE}:${APP_VAR} --host 0.0.0.0 --port ${PORT}"]
