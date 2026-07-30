# Job Aid — Excel Workbook Download: Process, Procedure & Error Recovery

> JHI-SIG: 69M2705M · JHI Research & Analytics Firm, Inc. (proprietary)
> **Purpose:** deliver a generated Excel (`.xlsx`) workbook to the user reliably, and
> recover fast when a download fails — so we never spin our wheels on a solved problem.
> **Audience:** engineering agent (Cy) + Founder. **Scope:** any file in `public/downloads/`.

---

## TL;DR (the 10-second version)
1. File must be **valid & non-zero** in the repo.
2. Get it into the **running app** (rebuild frontend if it's a *new* file).
3. Download from the **Documents page** (`/downloads`).
4. **Check the Size ≈ KB, not "Zero bytes"** before opening. A 0-byte file = the *download*
   failed, not the file.

---

## Part A — Standard delivery procedure (do this EVERY time)

**Step 1 — Generate & verify the file (source of truth = the repo).**
- Generate into `public/downloads/<file>.xlsx`.
- Verify it is a valid, non-empty workbook:
  ```
  ls -l public/downloads/<file>.xlsx          # size must be > 0
  .venv/bin/python -c "import openpyxl; print(openpyxl.load_workbook('public/downloads/<file>.xlsx').sheetnames)"
  ```

**Step 2 — Commit the file to the repo** (so it survives and is on the PR).

**Step 3 — Make it available on the RUNNING app.**
- **If the file already exists** in the frontend container (an update/overwrite):
  ```
  docker cp public/downloads/<file>.xlsx workspace-frontend-1:/app/public/downloads/<file>.xlsx
  ```
  (Next serves existing `public/` files from disk per request — updates immediately.)
- **If it is a NEW file** (never in the container's build): the container **caches its
  public-file list at startup**, so `docker cp` alone still 404s. **Rebuild the frontend:**
  ```
  docker compose build frontend && docker compose up -d frontend
  ```
  (or `docker cp` **then** `docker restart workspace-frontend-1`).

**Step 4 — Verify the app actually serves it:**
```
curl -s -o /dev/null -w "%{http_code} %{content_type} %{size_download} bytes\n" \
  http://localhost:3000/downloads/<file>.xlsx
```
Expect **`200`**, an Excel content-type, and the **real byte size**. A `404` = Step 3 not done.

**Step 5 — Download it (user side):**
- **Documents page:** open `http://localhost:3000/downloads` → click **Download** on the file's card.
- **or Direct URL:** `http://localhost:3000/downloads/<file>.xlsx`.

**Step 6 — VERIFY before opening:** in Finder, the **Size column must read ~KB, not
"Zero bytes."** If 0 bytes → the download didn't complete; delete and re-pull (see Part B).

---

## Part B — Troubleshooting (symptom → cause → fix)

| # | Symptom | Likely cause | Fix |
|---|---|---|---|
| 1 | Downloaded file shows **"Zero bytes"** / won't open in Excel | The *download transport* failed (served a 404/error page or connection dropped) — the file itself is fine | Delete the 0-byte file. Confirm the app serves it (Part A Step 4). Re-download from the Documents page. Check Size ≈ KB. |
| 2 | Browser: **"localhost:3000 refused to connect (-102)"** | Port forwarding to the VM is down | Use **Cursor Explorer → right-click file → Download** (uses Cursor's connection, not localhost). Or the **base64 recovery** (Part C). Or restart the Cloud Agent session to restore forwarding. |
| 3 | File **not listed** on the Documents page | Running frontend is a **stale build** without the new file/page | **Rebuild the frontend** (Part A Step 3, new-file path). |
| 4 | Direct URL returns **404** but old workbooks download fine | New file not in the container's cached public list | `docker cp` the file in **and restart/rebuild** the frontend container. |
| 5 | Editor shows **"Binary file is not supported"** | Normal — code editors can't *preview* binary `.xlsx` | Not an error. Download it (don't try to view in-editor). |
| 6 | Artifact card (chat) not appearing | The `/opt/cursor/artifacts` panel is unreliable in this environment | Do **not** rely on it as the sole path. Use the Documents page or Part C. |
| 7 | Excel says file is **corrupt** | Downloaded an HTML error page saved as `.xlsx` (esp. private GitHub raw without auth) | Re-download from the Documents page / a `200`-verified source; confirm Size ≈ KB. |

---

## Part C — Escalation / alternate delivery (when the app is unreachable)

**C1 — Cursor Explorer download (uses the Cursor connection, not localhost):**
Explorer → `public/downloads/` → **right-click** the file → **Download…** → check Size ≈ KB.

**C2 — Base64 text transport (bulletproof; rebuilds the file locally):**
1. Generate a text copy: `base64 public/downloads/<file>.xlsx > public/downloads/<file>_BASE64.txt` (commit it).
2. Open that `.txt` in the editor (text always opens) → **Cmd+A**, **Cmd+C**.
3. Mac Terminal: `pbpaste | openssl base64 -d > ~/Downloads/<file>.xlsx`
4. `open ~/Downloads/<file>.xlsx`

**C3 — GitHub PR:** open the PR → **Files changed** → the `.xlsx` → **Download** (GitHub serves
the real committed bytes; won't be 0 bytes if you're signed in).

---

## Part D — Root-cause reference (why this happens here)
- **Docker frontend bakes `public/` at build** and **caches its public-file list at startup** →
  newly-added files 404 until a rebuild/restart. (See `AGENTS.md` file-delivery note.)
- **localhost:3000 port forwarding can drop** between the user's browser and the VM.
- **The chat artifact panel** (`/opt/cursor/artifacts`) is unreliable in this environment.
- **A 0-byte download means the transport failed**, not the workbook — always verify size.

## Part E — Definition of Done (delivery)
- [ ] File valid & non-zero in `public/downloads/` and committed.
- [ ] `curl` returns `200` + real byte size from `localhost:3000/downloads/<file>`.
- [ ] File appears on the Documents page with a working Download button.
- [ ] User confirms the downloaded file shows **~KB (not 0 bytes)** and opens in Excel.
