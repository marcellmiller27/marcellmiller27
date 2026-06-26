# John Henry Investments — backend (FastAPI) image
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY backend/ /app/backend/
RUN pip install -e /app/backend

WORKDIR /app/backend
EXPOSE 8000

# Dev-friendly default (enables the 2FA demo code for sandbox testing).
# Set APP_ENV=production to disable dev-only endpoints.
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
