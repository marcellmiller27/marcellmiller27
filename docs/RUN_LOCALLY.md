# Run Aegira locally (Docker Desktop)

A concise, step-by-step guide to run the full Aegira platform (Postgres +
FastAPI backend + Next.js frontend) on a laptop with Docker Desktop.

> Product: **Aegira** · Publisher: **JHI Research & Analytics Firm, Inc.** ·
> JHI-SIG 69M2705M

## 1. Prerequisites

- **Docker Desktop** installed and **running** (whale icon steady in the menu
  bar / system tray). That is the only thing you need to install — the
  containers bring their own Node, Python, and Postgres.
- This repository cloned to your laptop.

## 2. Get the code and create your `.env`

```bash
cd path/to/Aegira          # the repo root (contains docker-compose.yml)
cp .env.example .env       # .env is git-ignored — safe for your secrets
```

Open `.env` and fill in at least the **required** values:

- `AUTH_JWT_SECRET` — generate a strong random value:
  ```bash
  openssl rand -hex 32
  ```
  Paste the output as the value.
- `FRED_API_KEY` — free key from <https://fredaccount.stlouisfed.org> (required
  for the macro dashboard).
- `NASDAQ_DATA_LINK_API_KEY` — from <https://data.nasdaq.com> (Sharadar SF1
  fundamentals).
- `JHI_STAFF_EMAILS` — the email you plan to register with. Listing it here is
  what grants staff / **God-Eye** (back-office) access, e.g.
  `JHI_STAFF_EMAILS=you@aegiraenterprise.com`.
- `NEXT_PUBLIC_SITE_URL` — keep `http://localhost:3000` for local use.

Everything else in `.env.example` is optional; leave blank values as-is.

## 3. Build and start

```bash
docker compose up --build
```

The first build pulls base images and compiles both apps, so it takes a few
minutes. Compose starts three services: `db` (Postgres), `backend`, and
`frontend`, with healthchecks.

## 4. Open the app

- Frontend: <http://localhost:3000>
- Backend API docs: <http://localhost:8000/docs>

## 5. First login = Register

1. Go to <http://localhost:3000> and choose **Register**.
2. Register with an email that is listed in `JHI_STAFF_EMAILS`. That account
   gets staff / God-Eye access to the back-office modules (Accounting, Admin,
   etc.).
3. Log in and explore: `/dashboard`, `/opportunities`, `/reports`, `/account`.

## 6. Stop and start again

```bash
docker compose down      # stop and remove containers (Postgres data persists in a volume)
docker compose up -d     # start again in the background (detached)
docker compose logs -f   # follow logs when running detached
```

## 7. Troubleshooting

- **"port is already allocated" / "address already in use"** — something else is
  using port `3000` or `8000`. Stop other local dev servers (or whatever holds
  the port), then run `docker compose up` again.
- **Pulled new code and it looks stale** — rebuild the images:
  ```bash
  docker compose up -d --build
  ```
- **First newsletter / chart call is slow (~20s)** — cold calls warm caches and
  fetch upstream data on first use. Subsequent calls are fast. This is expected.

## 8. Note on the paid Docker Hub account

The paid Docker Hub account is only needed **later**, for the server deploy flow
(build the image → push to Docker Hub → the server pulls it). It is **not**
required for running locally — everything above builds and runs on your laptop.
