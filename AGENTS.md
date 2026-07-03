# AGENTS.md

## Cursor Cloud specific instructions

### Repository layout
This repo is the **John Henry Investments** platform prototype with two independent services:

- **Frontend** (repo root): Next.js / React / TypeScript app. Standard commands are in `package.json` and `README.md`.
- **Backend** (`backend/`): FastAPI + SQLAlchemy app. Standard commands are in `backend/README.md`.

Note: the actual application lives on the `cursor/compose-ai-agent-work-239d` branch (open PR #1). The default `main` branch only contains a GitHub profile `README.md` with no application code, so the startup update script guards its commands with file checks and becomes a no-op on `main`.

### Non-obvious caveats
- **Most frontend pages are static, but the mobile app is live.** The marketing/app pages only *document* the `/api/v1/...` routes as on-page text. The mobile companion app at `/mobile` is the exception: it makes real HTTP calls to the backend (sign-in, two-factor, biometric, security status), so the backend must be running on `:8000` for `/mobile` to function. The API base is `http://localhost:8000/api/v1` (overridable via `NEXT_PUBLIC_API_BASE_URL`); backend CORS already allows the `:3000` origin.
- **Dev-only OTP convenience:** mobile two-factor endpoints surface the current TOTP code (`dev_code` / `POST /auth/2fa/dev-code`) for testing. This is gated on `APP_ENV` and is disabled when `APP_ENV=production`.
- **Backend Python deps install into a venv at `.venv`** (repo root), created by the startup update script. Always invoke backend tooling through that interpreter, e.g. `/workspace/.venv/bin/python -m uvicorn app.main:app --reload` (run from `backend/`), `/workspace/.venv/bin/python -m pytest`, `/workspace/.venv/bin/ruff check .`. The `python3-venv` system package is required and is baked into the VM snapshot.
- **No external database is needed.** The backend defaults to SQLite (`sqlite:///./john_henry_platform.db` via `DATABASE_URL`); `init_db()` creates tables on startup. The `.db` file is gitignored.
- **Ports:** frontend dev server runs on `3000`, backend on `8000`. The backend CORS config only allows origins `http://localhost:3000` and `http://127.0.0.1:3000`.
- The backend test extra uses `httpx2` (not `httpx`); it is already declared in `backend/pyproject.toml` under the `dev` optional dependencies.

### Security hardening notes (P0 work)
- **New backend deps** (in `pyproject.toml`, installed into `.venv`): `cryptography` (at-rest field encryption), `PyJWT` (access/scoped tokens), `stripe` (webhook signature verification).
- **TOTP 2FA secrets are encrypted at rest** (`security.encrypt_secret`/`decrypt_secret`, Fernet). The key comes from `APP_ENCRYPTION_KEY` (a urlsafe-base64 32-byte Fernet key) if set, else it is derived from `AUTH_JWT_SECRET`. **Set a dedicated `APP_ENCRYPTION_KEY` in production.** Legacy plaintext rows still decrypt and upgrade on next write.
- **Tokens use PyJWT (HS256).** Scoped (`2fa`/`biometric`) tokens are signed with a scope-specific key; access tokens reject scoped tokens and vice versa. Prod `AUTH_JWT_SECRET` must be ≥ 32 bytes (enforced by `Settings.validate()`).
- **Stripe webhook signatures are verified** when `STRIPE_WEBHOOK_SECRET` is set (`app/billing_webhook.py`); without it, the dev JSON-mock path is used. Verified events map `metadata.organization_id`/`metadata.plan` to the tenant.
- **Biometric assert requires a real WebAuthn ES256 assertion in production** (`app/webauthn.py`: challenge binding + signature + advancing `sign_count`). The presence-only path is dev-only (`APP_ENV != production`).
- **Schema note:** a `sign_count` column was added to `device_credentials`. `init_db()` uses `create_all` (no ALTER), so on a pre-existing **SQLite** dev DB, delete the gitignored `john_henry_platform.db` to pick up the new column. Production Postgres needs a migration (Alembic is still a TODO).
