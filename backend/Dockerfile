# John Henry Investments — backend (FastAPI) image (production-hardened)
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app
COPY backend/ /app/backend/

# Headless Chromium (Playwright) for exact-as-viewed newsletter PDF rendering.
# Browsers live in a shared path so the non-root runtime user can launch them.
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
RUN pip install -e /app/backend \
    && python -m playwright install --with-deps chromium

# Run as a non-root user.
RUN useradd -m -u 10001 appuser \
    && chown -R appuser:appuser /app /opt/pw-browsers
USER appuser

WORKDIR /app/backend
EXPOSE 8000

# Container healthcheck hits the FastAPI /health endpoint.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health').read()" || exit 1

# Multiple workers in production (override with WEB_CONCURRENCY).
# Set APP_ENV=production (and a real AUTH_JWT_SECRET + Postgres DATABASE_URL) for prod.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers ${WEB_CONCURRENCY:-2}"]
