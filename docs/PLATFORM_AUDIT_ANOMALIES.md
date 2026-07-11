# Platform Conditions Audit — All Anomalies

Audit date: 2026-06-24. Scope: repository topology, backend services/security, data
state, frontend, and validation claims. Method: static inspection (`rg`), live test
suite, `ruff`, build, and direct SQLite inspection of the dev database.

## Overall conditions (health)

- ✅ Backend test suite: **48 passed**; ✅ `ruff` clean; ✅ frontend `lint`/`typecheck`/`build` pass.
- ✅ Live market data verified across crypto/equities/indices/commodities/FX/curve/bonds/CPI.
- ⚠️ Several **anomalies** below require corrective action before any production claim.

## Anomalies (with severity, evidence, corrective action)

| # | Severity | Anomaly | Evidence | Corrective action |
| --- | --- | --- | --- | --- |
| 1 | High | **App is not on `main`; work is fragmented across 9 unmerged branches.** `main` contains only `README.md` (a GitHub profile repo). | `git ls-tree origin/main` → `README.md`; 9 `cursor/*` branches | Consolidate the stacked PRs into a single mainline in dependency order and merge. |
| 2 | High | **Opportunity Score predictive validity is unproven (H5 = FALSE).** Back-test IC weak/insignificant. | `docs/SECTION_8_VALIDATION_RESULTS.md` | Define a real score formula; outcome-validate to a pre-registered IC floor. |
| 3 | Medium | **Orphaned `crypto_holdings` table with 18 rows (incl. public wallet addresses) persists in the dev DB** after the feature was removed (PR #5 reverted). | SQLite: `crypto_holdings: 18` on a branch that has no crypto code | Drop the table / rebuild the dev DB; add teardown so removed features leave no data residue. |
| 4 | High | **Default dev token signing secret.** | `security.py`: `AUTH_JWT_SECRET` defaults to `development-only-change-me` | Require `AUTH_JWT_SECRET` (fail closed) outside development. |
| 5 | Medium | **2FA dev-code endpoint returns live TOTP codes.** Gated by `APP_ENV` but enabled by default in dev. | `/api/v1/auth/2fa/dev-code` | Keep strictly disabled when `APP_ENV=production`; never expose in any shared/staging env. |
| 6 | Medium | **2FA verification window widened to ±60s** (`window=2`) for manual-entry latency. | `mobile_services.py` `verify_totp(..., window=2)` | Tighten to ±30s now that the demo code auto-refreshes. |
| 7 | Medium | **Biometric assertion is not cryptographically verified** (presence check only; simulated fallback). | `mobile_services.biometric_assert` | Implement full WebAuthn assertion (challenge + signature + counter) verification. |
| 8 | Medium | **Public, unauthenticated market & research endpoints; no rate limiting.** | `routers/market.py` (all public), `routers/research.py` (only `/adoption` auth), no limiter in `main.py` | Add rate limiting; consider auth/quota for research + heavy endpoints. |
| 9 | Medium | **Live equities/indices/commodities/FX depend on the unofficial Yahoo endpoint** (no ToS/SLA). | `market_services.yahoo_chart` | Set `TWELVEDATA_API_KEY` to switch the licensed vendor to primary (adapter added; Yahoo stays as fallback). |
| 10 | Low | **Macro (FRED) and licensed vendor are key-gated and inactive.** | `/market/providers` → `requires_credentials` | Add `FRED_API_KEY` and/or `TWELVEDATA_API_KEY` secrets. |
| 11 | Medium | **Static (non-live) data still drives most pages.** 8 pages import `platform-data`; e.g. `reports` still renders static `marketSignals`; `opportunities`/`portfolio` are static. | `rg "@/lib/platform-data"` (8 hits); `reports/page.tsx` | Wire remaining pages to live endpoints (`/market/quotes`, `/research/*`). |
| 12 | Low | **Dev DB has accumulated 131 test orgs/users**, skewing the adoption study and inflating the DB. | SQLite counts | Use an isolated/ephemeral test DB; reset seed data; exclude test rows from analytics. |
| 13 | Low | **Unusual test dependency `httpx2`** (a fork, not the standard `httpx`). | `backend/pyproject.toml` | Verify provenance/security; prefer standard `httpx` unless there is a specific reason. |
| 14 | Low | **No CI** runs tests/lint on push (called out as a "next step" in `backend/README.md`). | repo has no CI workflow | Add CI to run `pytest`, `ruff`, `npm run lint/typecheck/build`. |
| 15 | Trivial | **`next-env.d.ts` flips** between `./.next/types` and `./.next/dev/types` depending on dev vs build. | git diff churn | Leave auto-generated; never commit the transient variant. |
| 16 | Info | **Bloomberg/TradingView are advertised but not usable** (paid entitlement / no public API). | `/market/providers` | Integrate only behind provisioned credentials; prefer a licensed vendor. |

## Notable non-anomalies (by design)

- **Non-custodial only:** no private keys/seed phrases are stored anywhere (crypto
  custody was deliberately rejected; see `docs/CRYPTO_HOLDINGS_STORAGE.md`).
- **Graceful degradation:** provider/network failures surface as per-symbol
  `status: "unavailable"`, not 500s.

## Priority remediation order

1. (#1) Consolidate branches into a mainline.
2. (#4, #3) Production secret enforcement; purge orphaned dev-DB data.
3. (#7, #6, #8) Harden auth (WebAuthn verification, tighter 2FA window, rate limits).
4. (#2) Define + validate the score (H5).
5. (#9, #11, #10) Switch to licensed vendor; wire remaining pages to live data; add keys.
6. (#14) Add CI.
