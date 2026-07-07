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
- **SQLite gotcha:** deleting `backend/john_henry_platform.db` while a `--reload` dev server is running triggers `sqlite3.OperationalError: attempt to write a readonly database` on the next write (the process holds a deleted inode). If you must reset the DB (e.g. a stale schema after switching branches with new columns), delete the file **and restart the backend** so `init_db()` recreates it.
- **Ports:** frontend dev server runs on `3000`, backend on `8000`. The backend CORS config only allows origins `http://localhost:3000` and `http://127.0.0.1:3000`.
- The backend test extra uses `httpx2` (not `httpx`); it is already declared in `backend/pyproject.toml` under the `dev` optional dependencies.
