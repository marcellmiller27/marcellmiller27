# JHI-SIG: 69M2705M | Platform spine | John Henry Investments (proprietary)
"""Lightweight, dependency-free, per-IP rate limiting middleware.

Disabled by default (RATE_LIMIT_PER_MINUTE=0). Set it to a positive number in
production to throttle abusive clients on the API. Fixed 60s window per client IP.
"""

from __future__ import annotations

import os
import threading
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

_HITS: dict[str, list[float]] = {}
_LOCK = threading.Lock()
_WINDOW = 60.0


def reset() -> None:
    with _LOCK:
        _HITS.clear()


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        limit = int(os.getenv("RATE_LIMIT_PER_MINUTE", "0") or 0)
        if limit > 0 and request.url.path.startswith("/api/v1/"):
            client = request.client.host if request.client else "unknown"
            now = time.time()
            with _LOCK:
                recent = [t for t in _HITS.get(client, []) if t > now - _WINDOW]
                if len(recent) >= limit:
                    _HITS[client] = recent
                    return JSONResponse(
                        {"detail": "Rate limit exceeded. Please slow down and retry shortly."},
                        status_code=429,
                    )
                recent.append(now)
                _HITS[client] = recent
        return await call_next(request)
