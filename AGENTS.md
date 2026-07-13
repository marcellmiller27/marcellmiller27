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
- **Docker uses a same-origin API proxy (browser only needs `:3000`).** In the Compose stack the frontend is built with `NEXT_PUBLIC_API_BASE_URL=/api/v1` and Next.js proxies those calls server-side to the backend (`next.config.mjs` `rewrites()`, target from `API_PROXY_TARGET`). So in Docker the browser never talks to `:8000` directly (this is what makes pages like `/accounting` work behind port forwarding) and there is no CORS. Gotcha: **Next bakes `rewrites()` at build time**, so `API_PROXY_TARGET` must be passed as a Docker **build arg** (see `Dockerfile`), not just a runtime env — changing it requires rebuilding the frontend image. In plain `npm run dev` (no `NEXT_PUBLIC_API_BASE_URL`), pages still call `http://localhost:8000/api/v1` directly, unchanged.
- **`docker-compose.override.yml` is a local sandbox helper** (pins static IPs and points the backend at the db / the frontend proxy at the backend by IP) to work around the docker-in-docker embedded-DNS quirk where service names like `db`/`backend` don't resolve. On a normal Docker host service names resolve and this override is unnecessary.
- The backend test extra uses `httpx2` (not `httpx`); it is already declared in `backend/pyproject.toml` under the `dev` optional dependencies.
