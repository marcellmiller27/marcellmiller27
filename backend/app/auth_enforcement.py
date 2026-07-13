# JHI-SIG: 69M2705M | Auth enforcement middleware | John Henry Investments (proprietary)
"""Gatekeeper: when ENFORCE_AUTH is on, require a valid access token for every
/api/v1 endpoint except a small public allowlist. Default-off so dev/demo stays
open; flip ENFORCE_AUTH=true in production to close the currently-open endpoints.

Per-endpoint permission checks (via require_permission) still apply on top of this;
this middleware only enforces "authenticated" as the baseline gate.
"""

from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.config import get_settings
from app.security import decode_access_token

# Public paths under /api/v1 that must remain reachable without a token.
_PUBLIC_PREFIXES: tuple[str, ...] = (
    "/api/v1/auth/login",
    "/api/v1/auth/register",
    "/api/v1/billing/webhook",  # Stripe calls this with a signature, not a user token
    "/api/v1/leads",            # public waitlist / lead capture
)


def _is_public(path: str, method: str) -> bool:
    if method == "OPTIONS":  # CORS preflight
        return True
    return any(path.startswith(prefix) for prefix in _PUBLIC_PREFIXES)


class AuthEnforcementMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if get_settings().enforce_auth:
            path = request.url.path
            if path.startswith("/api/v1") and not _is_public(path, request.method):
                auth = request.headers.get("Authorization", "")
                token = auth[7:].strip() if auth[:7].lower() == "bearer " else ""
                try:
                    decode_access_token(token)
                except Exception:  # noqa: BLE001 - any decode failure => unauthenticated
                    return JSONResponse(
                        {"detail": "Authentication required."}, status_code=401
                    )
        return await call_next(request)
