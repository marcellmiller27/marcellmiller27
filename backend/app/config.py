"""Centralized runtime settings + production safety validation."""

from __future__ import annotations

import os

DEFAULT_DEV_SECRET = "development-only-change-me"


class Settings:
    def __init__(self) -> None:
        self.app_env = os.getenv("APP_ENV", "development")
        self.auth_secret = os.getenv("AUTH_JWT_SECRET", DEFAULT_DEV_SECRET)
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./john_henry_platform.db")
        self.rate_limit_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", "0") or 0)
        # Gatekeeper: when true, all /api/v1 endpoints require a valid token (except a
        # small public allowlist). Default off so dev/demo stays open; flip on for prod.
        self.enforce_auth = os.getenv("ENFORCE_AUTH", "false").strip().lower() in ("1", "true", "yes")

    @property
    def is_production(self) -> bool:
        return self.app_env.strip().lower() == "production"

    def validate(self) -> "Settings":
        """Fail fast on unsafe production configuration; no-op in dev/test."""
        if not self.is_production:
            return self
        problems: list[str] = []
        if self.auth_secret == DEFAULT_DEV_SECRET:
            problems.append("AUTH_JWT_SECRET must be set to a strong secret in production.")
        elif len(self.auth_secret.encode("utf-8")) < 32:
            problems.append(
                "AUTH_JWT_SECRET must be at least 32 bytes (RFC 7518) for HS256 signing."
            )
        if self.database_url.startswith("sqlite"):
            problems.append("Use a Postgres DATABASE_URL in production (SQLite is dev-only).")
        if problems:
            raise RuntimeError("Unsafe production config: " + "; ".join(problems))
        return self


def get_settings() -> Settings:
    return Settings()
