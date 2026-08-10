# Data Foundation Construct — Always-Deliver · Cadence-Aware · As-Of-Disclosed

**Date:** 2026-08-10 · **JHI-SIG:** `69M2705M`
**Product:** Aegira · **Publisher:** JHI Research & Analytics Firm, Inc. (proprietary)
**Owner:** Cy Henry (VP, Software Engineering — AI) · **Status:** construct of record (Founder-approved data doctrine)

> The data-supply doctrine for every Aegira function — dashboards, valuation, opportunity scans,
> Excel/PDF exports, and newsletters. Companion docs: `docs/MARKET_DATA_SOURCES.md`,
> `docs/CROSS_ASSET_VALUATION_ENGINE_SPEC.md`, `docs/legal/nasdaq/FOUNDER_RESOLUTION_2026-07-20.md`.
> Not investment advice.

---

## Principles (the doctrine)

| # | Principle | What it means in practice |
| --- | --- | --- |
| **P1** | **Always-deliver** | No task, page, chart, score, or newsletter is ever blocked because a single input is missing. Every function degrades gracefully to what *is* available. |
| **P2** | **Never-fabricate** | We never invent a number. Missing/stale inputs are **labeled** — `pending`, `as-of <date>`, `estimated`, or `unavailable` — never silently backfilled or guessed. |
| **P3** | **As-of transparency** | Every figure we show carries its **actual data date**, its **cadence**, and its **source**. The user always knows how fresh a number is and where it came from. |
| **P4** | **Daily + on-demand refresh** | Series refresh on a **scheduled daily** cycle *and* can be **pulled on demand** (user action, newsletter build, valuation run). |
| **P5** | **Resilient** | Fetch failures **retry with backoff**, then fall back to the **last-good cache**. A provider outage degrades a single element, never the request. |
| **P6** | **Governed** | Licensing class, derived-only isolation, mandatory attribution, and **fact-lock** are enforced at the data layer, not bolted on downstream. |

These six principles are **binding across all functions**. Everything below is the mechanism that makes them true.

---

## 1. Source & series registry

The registry is the single catalog of every series Aegira consumes. Each entry declares its identity, cadence,
unit, license class, release calendar, and fallback chain. This is the contract the rest of the platform reads.

### 1.1 Source classes

| Source | Domain | License class | Notes |
| --- | --- | --- | --- |
| **FRED** (Federal Reserve, St. Louis) | Rates, inflation, macro aggregates | Public-domain / redistributable | Primary macro spine. |
| **US BLS** | CPI, PPI, employment, wages | Public-domain / redistributable | CPI series `CUUR0000SA0`; YoY computed from index levels. |
| **US BEA** | GDP, PCE, national accounts | Public-domain / redistributable | Quarterly + annual national accounts. |
| **SEC EDGAR** | Company fundamentals (raw line-items) | Public-domain / redistributable | **Fallback** fundamentals + the only source allowed to surface **raw** line-items in workbooks/LSR. |
| **Sharadar SF1** (via Nasdaq Data Link) | Point-in-time company fundamentals | **Licensed — derived-only, no-spillage** | **PRIMARY** point-in-time fundamentals (Agreement 00151172.0). Raw rows stay internal; only derived outputs surface. |
| **Market / prices** (CoinGecko, Yahoo Finance, BLS) | Crypto, equities, indices, commodities, treasury yields, inflation | Public / free-tier | Live quotes via `GET /api/v1/market/quotes` (`backend/app/market_services.py`). |

### 1.2 Per-series descriptor

Every series carries:

- **`series_id`** — canonical Aegira id (e.g., `macro.cpi_yoy`, `rate.ust10y`, `fund.aapl.revenue`).
- **`source`** — the provider (FRED / BLS / BEA / EDGAR / SF1 / market).
- **`cadence`** — one of `daily` · `weekly` · `monthly` · `quarterly` · `annual` · `irregular`.
- **`unit`** — `%`, `USD`, `index`, `bps`, `ratio`, `count`, etc.
- **`license_class`** — `public` · `licensed-derived-only` · `free-tier`.
- **`last_release`** — the actual data date of the most recent observation we hold.
- **`next_release`** — the scheduled next publication (from the release calendar; `irregular` = event-driven).
- **`fallback_chain`** — ordered list of substitute sources/series if the primary is unavailable.

### 1.3 Representative registry rows

| series_id | source | cadence | unit | license | fallback chain |
| --- | --- | --- | --- | --- | --- |
| `macro.cpi_yoy` | BLS | monthly | % | public | BLS index → FRED `CPIAUCSL` → last-good cache |
| `macro.gdp_qoq` | BEA | quarterly | % | public | BEA → FRED `GDPC1` → last-good cache |
| `rate.ust10y` | market (Yahoo `^TNX`) | daily | % | free-tier | Yahoo → FRED `DGS10` → last-good cache |
| `rate.fed_funds` | FRED | daily | % | public | FRED `DFF` → last-good cache |
| `price.spx` | market (Yahoo `^GSPC`) | daily | index | free-tier | Yahoo → last-good cache |
| `price.btc` | market (CoinGecko) | daily | USD | free-tier | CoinGecko → Yahoo `BTC-USD` → last-good cache |
| `price.gold` | market (Yahoo `GC=F`) | daily | USD | free-tier | Yahoo → last-good cache |
| `fund.<ticker>.*` | **SF1 (primary)** | quarterly | USD/ratio | licensed-derived-only | **SF1 → SEC EDGAR → last-good cache** |

**Governance flag on SF1 rows:** raw datatable rows/fields **stay INTERNAL**; only **derived** outputs (valuations,
opportunity scores, ratios, margins) surface. Consumers that must show raw line-items (EDGAR financials
endpoint/workbook, LSR public-comp benchmark) deliberately stay on **SEC EDGAR**.

---

## 2. Acquisition & refresh

| Mode | Trigger | Behavior |
| --- | --- | --- |
| **Daily scheduled** | Cron/worker (per-cadence policy) | Refresh series whose `next_release` is due; skip series not yet due (avoids wasted calls). |
| **On-demand** | User action, newsletter build, valuation run, export | Pull the specific series a task needs; serve cache if fresh, else fetch. |
| **Rate-limit-aware** | All fetches | Respect per-provider limits; batch where possible (e.g., crypto symbols batched into one CoinGecko call); token-bucket/backoff to stay under caps. |
| **Bulk** | Initial load / backfill / SF1 datatable sync | Bulk fetch on cold start and for licensed bulk endpoints; write to cache with full provenance. |

Acquisition is **idempotent** and **provenance-first**: every write records value + actual-data-date + fetched-at +
source + cadence (see §3). Scheduled refresh is cadence-driven — a `quarterly` series is not polled daily.

---

## 3. Caching, freshness & as-of

### 3.1 The cache record (provenance envelope)

Every cached observation stores:

```
{ value, actual_data_date, fetched_at, source, cadence, license_class, freshness_state }
```

- **`value`** — the datum.
- **`actual_data_date`** — the real date the data pertains to (the "as-of").
- **`fetched_at`** — when *we* retrieved it.
- **`source`** / **`cadence`** / **`license_class`** — from the registry.

### 3.2 Last-good cache

The last successfully fetched observation is always retained. If a live fetch fails, the last-good value is served
**with its original `actual_data_date`** and a `fetch-failed` freshness flag — never presented as current.

### 3.3 Freshness states

| State | Meaning | Surface treatment |
| --- | --- | --- |
| **current** | Latest observation within its cadence window | Shown normally with as-of stamp. |
| **overdue** | `next_release` passed but no newer observation retrieved yet | Shown with as-of + "awaiting <cadence> release" note. |
| **fetch-failed** | Live fetch errored; serving last-good cache | Shown with as-of + "last good; refresh failed" note. |

### 3.4 As-of disclosure everywhere

Every figure — on-screen, in PDF, in the Excel workbook, in a newsletter — renders its **as-of date + cadence +
source**. No number is ever displayed without its provenance. This is the visible expression of **P2 + P3**.

---

## 4. Always-deliver & graceful degradation

Degradation is **element-level**, not request-level.

- **Charts** render whatever series are available; missing series are omitted with a labeled gap, not a blank chart.
- **Scores / valuation** compute on the available factors; a missing factor is disclosed and the score notes reduced
  coverage rather than failing (see the factor-decomposition pattern in the Cross-Asset engine).
- **Newsletters always ship.** A section whose data is pending renders with an as-of/"pending" label; the edition is
  never blocked. (This mirrors the live editorial pipeline in `docs/EDITORIAL_CHARTER.md`.)
- **No-fabrication guardrail.** The degradation path may only **label and omit** — it may never **invent** a value to
  fill a gap. AI-authored text is **fact-locked** to model/data outputs (never invents figures).

**Contract:** a single provider outage or an unreleased monthly print degrades exactly the elements that depend on it,
and nothing else.

---

## 5. Cadence categorization & next-release calendar

Each series is categorized by cadence so the scheduler, freshness logic, and UI copy can reason about it uniformly.

| Cadence | Examples | Refresh policy | "Overdue" trigger |
| --- | --- | --- | --- |
| **daily** | prices, treasury yields, fed funds | Poll each business day | No new obs by end of day |
| **weekly** | jobless claims, some Fed H-series | Poll on release weekday | `next_release` passed |
| **monthly** | CPI, PPI, employment | Poll around release date | `next_release` passed |
| **quarterly** | GDP, company fundamentals (SF1/EDGAR) | Poll after filing/print window | `next_release` passed |
| **annual** | annual national accounts, 10-K annuals | Poll after annual print | `next_release` passed |
| **irregular** | ad-hoc filings, event data | Event/on-demand | n/a (event-driven) |

A **next-release calendar** is derived from `next_release` across the registry, driving (a) the scheduler's daily
"what's due" list and (b) user-facing "next update expected <date>" copy.

---

## 6. Resilience & error handling

- **Retry with backoff** on transient errors (network/5xx/rate-limit), bounded attempts.
- **Fallback chain** per series (§1.3): primary → alternate source/series → **last-good cache**.
- **Normalized errors** — provider/parse failures normalize to a single error type; the affected element returns
  `unavailable` with a note (the endpoint never 500s on a provider outage — the pattern already used in
  `backend/app/market_services.py`).
- **Isolation** — a failure in one series/provider cannot cascade to others in the same request.
- **Circuit-awareness** — repeated failures for a provider short-circuit to cache to protect rate limits and latency.

---

## 7. Transparency, monitoring & audit

- **As-of on every figure** (§3.4) — the primary transparency surface.
- **Freshness monitoring** — a health view of series by freshness state (current/overdue/fetch-failed) with
  last-fetch timestamps.
- **Fetch audit log** — every acquisition records source, series, actual-data-date, fetched-at, and outcome
  (ok/retry/fallback/cache) for later review.
- **Source disclosure** — provider catalog + status is discoverable (mirrors `GET /api/v1/market/providers`).
- **Provenance in exports** — workbooks/PDF carry `JHI-SIG`, sources, "as of," and disclaimer watermark
  (consistent with existing exports).

---

## 8. Governance & compliance

- **Licensing class enforced at the data layer** — `licensed-derived-only` series (SF1) are isolated server-side;
  **only derived outputs** may reach users, newsletters, or workbooks (**no spillage**), per
  `docs/legal/nasdaq/FOUNDER_RESOLUTION_2026-07-20.md`.
- **Derived-only** — raw licensed rows never leave the server; raw line-items surface only from **public-domain SEC
  EDGAR**.
- **Attribution** — mandatory-attribution and external-distribution/end-user-cap terms honored wherever a series
  requires it.
- **Fact-lock** — all AI-authored narrative is locked to the underlying data/model outputs; no invented figures.
- **Distributor obligations** — SF1 monthly usage reporting (Nasdaq Data-Client Portal) + EIPP invoicing tracked as
  ops obligations (owner: Founder/ops).

---

## 9. Application matrix (per function)

| Function | Consumes | Degradation behavior | As-of surface |
| --- | --- | --- | --- |
| **Dashboard / market widgets** | daily prices, rates, inflation | Per-symbol `unavailable`; others render | Per-tile as-of + source |
| **Cross-Asset Valuation / DCF** | SF1 (primary) → EDGAR fundamentals; rates | Value on available factors; disclose coverage | Per-input as-of in workbook/screen |
| **Opportunity Scan** | SF1-derived factors, prices | Score on available factors; note reduced coverage | Per-factor as-of |
| **Excel / PDF export** | whichever series the report needs | Missing cells labeled `pending`/`as-of` | Provenance block + per-figure as-of |
| **Newsletters (editorial)** | macro spine + derived metrics | Section renders `pending`; edition always ships | Per-figure as-of in body + methodology |

---

## 10. Testing & acceptance

**Acceptance criteria (the doctrine is met when):**

1. **Always-deliver** — with any single provider forced offline, every page/chart/score/newsletter still renders
   (degraded, labeled), no request 500s.
2. **Never-fabricate** — no code path substitutes a missing value with an invented one; missing inputs render as
   `pending`/`as-of`/`unavailable`.
3. **As-of everywhere** — automated check that every displayed figure has an attached actual-data-date + source.
4. **Refresh** — daily scheduled refresh updates only due series; on-demand pull fetches the requested series.
5. **Resilience** — forced fetch failure retries then serves last-good cache with `fetch-failed` state.
6. **Freshness** — overdue/current/fetch-failed states compute correctly against the release calendar.
7. **Governance** — no licensed raw row appears in any user-facing surface; raw line-items trace only to EDGAR.

**Test types:** unit (registry/freshness/fallback logic) · integration (acquisition + cache + degradation) ·
contract (as-of presence on outputs) · governance (no-spillage assertions).

---

## 11. Rollout phases

- **Phase 1 — Foundation (now):** registry + provenance cache (value/as-of/fetched-at/source/cadence) + last-good
  fallback + freshness states + as-of disclosure on existing surfaces (market widgets, valuation, newsletters).
  Sources live: FRED, BLS, BEA, SEC EDGAR, **Sharadar SF1 (primary)**, market/prices.
- **Phase 2 — Cadence & scheduling:** daily scheduled refresh driven by the next-release calendar + on-demand pulls +
  rate-limit-aware batching + freshness monitoring view + fetch audit log.
- **Phase 3 — Hardening & breadth:** circuit-awareness, expanded fallback chains, bulk/backfill for licensed
  datatables, and application-matrix coverage across all export/newsletter surfaces with full acceptance-test suite.

---

*Locked doctrine: **always-deliver + never-fabricate + as-of disclosure + cadence categorization.** Every Aegira
function inherits P1–P6. Not investment advice.*
