# Licensed Point-in-Time Fundamentals — Definitions, Vendors, Integration Plan

This is the data-procurement guide for closing H5 (Opportunity Score predictive
validity). It defines the required data, ranks the top vendors, and specifies how
the platform will consume the API key once purchased.

## Definitions

- **Point-in-time (PIT) fundamentals.** Data stored *as it was actually known on
  each historical date* — original/unrestated filings tagged with their real
  report and effective dates. A back-test only uses information available at that
  moment, removing **look-ahead bias** (using later restatements) and **filing-lag
  bias** (using figures before they were public). Must also be
  **survivorship-bias-free** (include delisted/bankrupt names).
- **Larger/longer sample (power target).** Breadth **≥1,000–3,000 names**
  (e.g., Russell 3000 / global developed) and **≥20 years** of monthly history,
  survivorship-bias-free. Power scales with breadth × periods, so an IC ≈ 0.03–0.04
  (already observed) would clear **|t| ≥ 2.0** at this depth (vs t = 0.87 on the
  free 30-name / 44-month sample).
- **Fundamentals-data API key.** Authenticated credential for programmatic
  (REST/bulk) access to a vendor's PIT fundamentals, tiered by coverage/history.

## Top five providers (point-in-time fundamentals)

| # | Provider | PIT dataset | Access | Coverage / history | Tier |
| --- | --- | --- | --- | --- | --- |
| 1 | **S&P Global Market Intelligence** | Compustat Point-in-Time (Snapshot) | S&P APIs / WRDS | US ~1980s+, global; gold standard | Enterprise |
| 2 | **FactSet** | Fundamentals (PIT / as-reported) + estimates | FactSet API | Global, deep | Enterprise |
| 3 | **LSEG / Refinitiv** | Worldscope + I/B/E/S (point-in-time) | Refinitiv Data Platform / Datastream | Global | Enterprise |
| 4 | **Bloomberg** | Data License PIT fundamentals (BLPAPI) | Terminal / Data License | Global | Enterprise |
| 5 | **Nasdaq Data Link — Sharadar (SF1)** | Core US Fundamentals, true PIT, survivorship-free | Simple REST API | ~5,000+ US equities, ~20y | **Affordable / self-serve** |

**Affordable API-first runners-up:** Tiingo Fundamentals, Financial Modeling Prep
(FMP), Intrinio, EOD Historical Data (EODHD).

## Do NOT confuse: market-data feeds vs fundamentals

These are different products — only fundamentals close H5:

- **Nasdaq Depth Data / TotalView (depth-of-book, Level 2)** — the live order book
  (all bids/asks at every price level). Priced as a market-data license (e.g.,
  "External Distribution ~$4,230/firm/month" plus per-user/exchange fees). Used for
  execution / routing / HFT / TCA. **NOT fundamentals — wrong data for factor
  research, and not needed anywhere in this platform.**
- **Nasdaq Data Link (formerly Quandl)** — a data *marketplace* that hosts
  **Sharadar SF1**, the point-in-time fundamentals we actually need. Same parent
  brand ("Nasdaq"), completely different product. **This is the correct one.**
- The platform's live price widgets need only last-price quotes (CoinGecko/Yahoo/
  Twelve Data) — never depth-of-book.

## Recommendation

- **Highest accuracy:** Compustat PIT (#1) — enterprise contract.
- **Best practical buy-now choice:** **Sharadar SF1 via Nasdaq Data Link** (#5) —
  genuinely PIT, survivorship-bias-free, self-serve API key, integrates fastest.

## Procurement status (updated 2026-06-29)

**Status: AWAITING NASDAQ RESPONSE.** A purchase inquiry for the **Sharadar SF1
single-user/developer** license has been submitted to NASDAQ / Nasdaq Data Link; we are
awaiting their response. No API key yet — the adapter remains **gated/inactive** and
`/research/fundamentals-status` reports `available: false`. Next action: once NASDAQ
responds and the license is purchased, add the key to Secrets and follow the integration
plan below.

## Procurement decision (confirmed 2026-06-25)

**Chosen dataset: Sharadar Core US Fundamentals (SF1) on Nasdaq Data Link.** It meets
every requirement: point-in-time (time-indexed to filing date), survivorship-bias-free
(6k active + 10k delisted), restatement control, ~24y history, ~16k companies, 150
indicators, and a Nasdaq Data Link API. Buy the **single-user/developer** license.

**Critical PIT usage rule (for the adapter):** query the **As-Reported** dimensions
(`ARQ`/`ART`/`ARY`) and align on the **filing date `datekey`** — NOT the
most-recent/restated dimensions (`MRQ`/`MRT`/`MRY`) — to avoid look-ahead bias.
SF1 is US-listed (plus ADRs/Canadian); global coverage would need a separate dataset.

## Integration plan (after purchase)

1. Add the key in the **Secrets** panel. Default env vars the adapter will read:
   `FUNDAMENTALS_VENDOR` (e.g., `sharadar`) and `FUNDAMENTALS_API_KEY`
   (Sharadar/Nasdaq Data Link may also use `NASDAQ_DATA_LINK_API_KEY`).
2. Implement a PIT fundamentals adapter feeding value (E/P, B/P), quality (ROE,
   margins, low accruals), and growth factors into `opportunity_score.py`
   (`/research/fundamentals-status` flips to `available`).
3. Expand the universe + history to the vendor's survivorship-bias-free coverage.
4. Re-run the equity-only, **costed, out-of-sample** protocol
   (`/research/equity-oos-backtest`) and report honestly against a **|t| ≥ 2.0** bar.

## R&D & validation timeline (how long, and can we validate in one week?)

**Blunt answer: yes — we can produce a credible, pre-registered PASS/FAIL within ~1 work
week of getting data access — but "validation" is a process, not a one-time stamp.**

Once the SF1 key is available (single-user/developer is sufficient for this R&D phase):

| Day | Work |
| --- | --- |
| 0 | Key added to Secrets; confirm SF1 access + dimensions. |
| 1–2 | PIT ingestion adapter (As-Reported `ARQ/ART/ARY`, aligned on `datekey`); build value/quality/growth factors. |
| 3–4 | Backtest harness: survivorship-free universe, out-of-sample split, transaction costs, turnover; run. |
| 5 | Robustness (subperiods/sectors), write honest results vs the pre-registered **|t| ≥ 2.0** bar. |

**What one week buys you:** a defensible, *pre-registered* verdict on the Opportunity
Score's predictive validity (the H5 hypothesis) — pass or fail — without p-hacking.

**What it does NOT buy you (be honest with clients):**
- A one-week backtest is **historical evidence**, not a live track record. Forward/paper
  validation continues after launch.
- If it **fails**, we iterate — but every new variant spends statistical credibility;
  disciplined, limited iteration only (no overfitting).
- Passing the backtest ≠ "proven alpha in production." It clears the bar to *honestly
  claim* research-grade signal, nothing more.

## SF1 Licensing & Client-Serving Guardrails

| Phase | License needed |
| --- | --- |
| **R&D / backtesting (now)** | **Single-user/developer** is sufficient — internal research by one developer. |
| **Serving B2C/B2B clients (commercial)** | **NOT** single-user. Requires a **commercial / business / redistribution-class license** with **derived-data display rights confirmed in writing.** |

Hard rules:
- **Single-user/developer = internal R&D only.** Do **not** launch any client-facing
  feature on it.
- **Derived vs. raw:** even showing only *derived* outputs (the 0–100 score, Buy/Watch/
  Pass, rankings) to clients may exceed an internal license — vendors' "derived data"
  clauses vary. **Get derived-data display + redistribution rights in writing.**
- **MSA term ≠ license scope.** A 12-month MSA sets *duration*; the *scope*
  (single-user vs commercial/redistribution) is the limiter. We need the right **scope**.
- The data license is **necessary but not sufficient** to serve clients — also need the
  validated model and the advice-vs-education compliance posture (RIA question).

**Exactly what to procure to serve clients commercially:** a Nasdaq Data Link **commercial
SF1 license** (business/enterprise tier) that explicitly permits **(a) commercial/production
use in a paid SaaS, (b) display of SF1-*derived* analytics to external B2C/B2B end users,
and (c) any redistribution if raw fields are ever shown** — on a 12-month MSA, priced
per-seat/per-user or organizationally. Confirm exact tier name + price with Nasdaq; have
counsel review the MSA/license schedule before signing.

## NASDAQ outreach message (template)

Use while negotiating the MSA. Fill the brackets; keep it short and specific.

```
Subject: SF1 (Sharadar Core US Fundamentals) — commercial license inquiry for a SaaS product

Hello [Nasdaq Data Link / Sharadar team],

I'm [Name], founder of John Henry Investments, LLC. We are currently evaluating the
Sharadar SF1 dataset under a single-user/developer license for internal R&D
(point-in-time factor research and backtesting).

We are preparing to launch a commercial SaaS platform (B2C and B2B) that will present
SF1-DERIVED analytics — a standardized 0–100 "Opportunity Score" and rankings — to
paying clients. To scope the right agreement, please confirm:

1. Which license tier covers COMMERCIAL/production use of SF1 in a paid SaaS serving
   multiple external users (B2C and B2B)?
2. Does that tier permit DISPLAY OF DERIVED DATA (scores/rankings computed from SF1) to
   our end clients? Are there limits on derived works?
3. If we ever display RAW SF1 fields to clients, what REDISTRIBUTION/display license is
   required?
4. Pricing model: per-seat, per-user, or flat commercial? Any usage/API-call limits?
5. Any ATTRIBUTION, caching, or display requirements we must implement?
6. Term: we'd like a 12-month MSA. What is the upgrade path from single-user/developer
   to the commercial tier, and can R&D spend be credited?

Please send the applicable license schedule, MSA, and a quote. Happy to share more about
our use case on a call.

Thank you,
[Name] — John Henry Investments, LLC — [email] — [phone]
```

## NASDAQ engagement guidelines: one-week R&D → commercial MSA

**Goal:** secure a short, low-cost **R&D/evaluation window** on SF1 single-user/developer
to run our pre-registered validation (see `docs/RND_VALIDATION_PROTOCOL.md`, ~1 week of
work), then move directly to a **commercial MSA** for client serving — ideally with the
R&D fee credited.

**Negotiation principles (what to hold firm on):**
1. **Separate the two phases explicitly.** Phase 1 = internal R&D (single-user/developer,
   short term). Phase 2 = commercial production (B2C/B2B) — a different license scope.
2. **Ask for a trial/short eval first.** Many data vendors offer a **free trial or a
   short evaluation** of single-user data. Request a **1–2 week** eval (or the smallest
   single-user term) sufficient to run our backtest — we don't need a 12-month single-user
   commitment just to validate.
3. **Get an upgrade/credit path in writing.** Request that R&D/eval spend be **credited
   toward** the commercial MSA when we upgrade.
4. **Nail derived-data rights for Phase 2.** The commercial MSA must permit **display of
   SF1-derived analytics (scores/rankings) to external clients** (and redistribution if
   raw fields are ever shown). Confirm in writing.
5. **Term ≠ scope.** Accept a 12-month *commercial* MSA term — but only the **commercial
   scope** enables client serving. A 12-month *single-user* term does not.
6. **No client serving on single-user.** We will not deploy any client-facing feature on
   the R&D license; commercial launch waits for the commercial MSA.

> Reality check: if NASDAQ has **no** short trial and only sells single-user annually, the
> single-user annual license is still a low-cost R&D on-ramp — buy it, validate in ~1 week,
> and upgrade to commercial before serving clients (ask for the credit per #3).

### Cover message (one-week R&D → commercial MSA)

```
Subject: SF1 evaluation (1 week) → commercial MSA — John Henry Investments

Hello [Nasdaq Data Link / Sharadar team],

I'm [Name], founder of John Henry Investments, LLC (fintech SaaS). We've selected Sharadar
SF1 and want to move efficiently in two phases:

PHASE 1 — R&D (now): We need a short evaluation/single-user-developer window — ideally
about ONE WEEK — to run an internal, point-in-time backtest validating our derived
"Opportunity Score." Could you provide a free trial or the smallest single-user term that
covers this? No client access during this phase.

PHASE 2 — Commercial (immediately after, if validation passes): We will move to a
COMMERCIAL MSA to serve B2C/B2B clients SF1-DERIVED analytics. Please confirm:
  • the commercial tier that permits production SaaS use + display of derived data to
    external clients (and redistribution if raw fields are shown);
  • a 12-month MSA term and pricing (per-seat/per-user/flat);
  • whether our Phase 1 R&D fee can be CREDITED toward the commercial MSA.

We validate quickly, so we expect a short gap between phases. Please send trial details,
the commercial license schedule, MSA, and a quote.

Thank you,
[Name] — John Henry Investments, LLC — [email] — [phone]
```
