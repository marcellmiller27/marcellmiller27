# Cross-Asset & Distribution Construct — Global Opportunity + Editorial Distribution

**Date:** 2026-08-10 · **JHI-SIG:** `69M2705M`
**Product:** Aegira · **Publisher:** JHI Research & Analytics Firm, Inc. (proprietary)
**Owner:** Cy Henry (VP, Software Engineering — AI) · **Status:** construct of record (Phase 1 buildable now; global held pending Founder vendor decision)

> Two coupled systems: (1) a **cross-asset opportunity engine** that produces a **common signal schema** across all
> asset classes, and (2) the **editorial distribution** system that delivers it on cadence. Global in-scope by design.
> Builds on the data doctrine in `docs/DATA_FOUNDATION_CONSTRUCT.md`; extends the valuation methods in
> `docs/CROSS_ASSET_VALUATION_ENGINE_SPEC.md`; distribution companion `docs/NEWSLETTER_DISTRIBUTION_STEP_B.md`.
> Not investment advice.

---

## Principles (inherits P1–P6 from the Data Foundation)

The six data-foundation principles (**always-deliver, never-fabricate, as-of transparency, daily+on-demand refresh,
resilient, governed**) apply in full. This construct adds three:

| # | Principle | What it means |
| --- | --- | --- |
| **P7** | **Cross-asset consistency** | Every asset class emits the **same opportunity signal schema** (below), regardless of the underlying method. The *shape* of the output is unified; the *math* is asset-appropriate. |
| **P8** | **Global-by-design** | Coverage is worldwide from the architecture up — currency normalization, regional disclaimers, and vendor-agnostic adapters are built in, not retrofitted. |
| **P9** | **Rigor-disclosed** | Each signal declares whether it is **`validated`** (full method on licensed/PIT data) or **`directional`** (lighter method / limited data). The reader always knows the analytical weight. |

### The common opportunity signal schema (P7)

```
{
  score:            0–100,
  signal:           Enter | Accumulate | Sideline,
  margin_of_safety: %  (fair value vs. price),
  expected_return:  %  (modeled, with horizon),
  rationale:        text (fact-locked to the model),
  as_of:            date + cadence + source,
  rigor:            validated | directional
}
```

Every asset — a US equity, a global equity, gold, EUR/USD, BTC — resolves to this one object. That is what makes the
cross-asset comparison honest and the distribution templating uniform.

---

## A. Distribution & cadence

### A.1 Editorial cadence

| Edition | Cadence | Content |
| --- | --- | --- |
| **Daily / Weekly Pulse** | daily + weekly | Short cross-asset read: what moved, what tripped a threshold, the top signals. |
| **Monthly Deep-Dive** | monthly | An Insider-Brief-style analytical essay on a theme/sector/asset, with charts + historical context. |
| **Quarterly Global Outlook** | quarterly | Cross-asset regime read across regions; positioning framework. |
| **Annual Outlook** | annual | The year-ahead thesis across asset classes and geographies. |

### A.2 Scheduler

Cadence-driven scheduler (shares the next-release calendar from the Data Foundation): each edition has a build window;
the pulse builds daily/weekly, deep-dives on their monthly/quarterly/annual cycle. On-demand rebuild supported.

### A.3 Channels

- **On-platform** — rendered at `/newsletters` (live today), exportable to **PDF**.
- **PDF** — deterministic, provenance-stamped export.
- **SES email** — AWS SES send service (gated on verified sender domain — see runbook in board minutes / STEP_B).

### A.4 Subscriber lists

| List | Entry | Notes |
| --- | --- | --- |
| **Free** | **Double opt-in** email capture (no account) | Limited-edition variant; growth funnel to paid. |
| **Paid** | Tier-1/Tier-2 subscribers | Full editions. |

### A.5 Broadcast & compliance

- **Broadcast** send with per-recipient **unsubscribe** (one-click), physical address, **CAN-SPAM** footer on every send.
- **Bounce/complaint handling** → suppression list; sender-reputation protection.
- **Archive** — every issue archived (on-platform + stored) for reference and audit.

---

## B. Cross-asset opportunity engine

Each class uses its own appropriate method (per `CROSS_ASSET_VALUATION_ENGINE_SPEC.md`) but emits the **common signal
schema** (P7) with a **rigor** flag (P9).

| Asset class | Method | Data | Rigor at Phase 1 |
| --- | --- | --- | --- |
| **US equities** | **Validated** — SF1 factor decomposition + **DCF** (+ multiples cross-check) | SF1 (primary, PIT) → EDGAR fallback | **validated** |
| **Global equities** | DCF/multiples via commercial vendor fundamentals | global vendor (Phase 2) | directional → validated |
| **Commodities** | Futures **curve / carry / cost-curve**, real rates, supply/demand | market + macro | directional |
| **Forex** | **Rate-differential / carry / PPP / REER** | policy rates, inflation, real rates | directional |
| **Crypto** | **Network / liquidity** + scarcity, volatility-scaled (labeled speculative) | on-chain/adoption proxies, liquidity | directional |
| **Cross-asset relative value** | Ranked comparison across the common score | all of the above | as per inputs |

**Validation per class:** a class is promoted from `directional` to `validated` only when its method runs on
sufficient, appropriately-licensed, point-in-time data. US equities are `validated` now (SF1 live); other classes
carry `directional` until their data/method are validated (Phases 2–3).

---

## C. Global data sourcing

- **Vendor candidates:** **EODHD / FMP / Intrinio** — chosen for **commercial / redistribution rights + point-in-time
  (PIT)** history. Final selection is a **Founder-gated decision** (license + cost).
- **Global prices** — worldwide equities/indices/FX via the selected vendor; free feeds (Yahoo/CoinGecko) remain for
  the classes they already cover.
- **Vendor-agnostic adapters** — a normalized adapter interface (as in `market_services.py`) so a vendor can be added
  or swapped without changing downstream contracts.
- **Currency normalization** — every value carried in **USD + local currency**, with the FX as-of disclosed.
- **Coverage map** — an explicit map of which regions/classes are covered by which source, surfaced for transparency.
- **Licensing / attribution** — global vendor license class recorded in the registry; mandatory attribution +
  redistribution/end-user-cap terms honored (see §F).

---

## D. Integration with the Data Foundation

This engine is a **consumer** of `docs/DATA_FOUNDATION_CONSTRUCT.md`:

- Every input arrives through the **registry** with its cadence, license class, and fallback chain.
- Every signal inherits **as-of + cadence + source** (P3) and **freshness state** (current/overdue/fetch-failed).
- **Always-deliver** applies: a signal computes on available factors; missing factors are disclosed, not fabricated.
- **Governance** (derived-only / no-spillage / fact-lock) is enforced upstream at the data layer.

---

## E. Editorial layer

- **Ellery Vance — VP of Editorial (AI)** authors the essays; support agents are **not** editorial
  (`docs/EDITORIAL_CHARTER.md`).
- **Essays + charts** — Fed "Economic Research" style: analytical essays WITH charts and cited historical context
  (Newsletter Depth Phase 2).
- **RAG** — Bedrock Knowledge Base / RAG over a historical macro corpus for grounded historical context.
- **Fact-lock** — all narrative is locked to the engine's signal outputs; no invented figures.

---

## F. Governance & compliance

- **Commercial-tier trap** — before onboarding any global vendor, confirm the tier grants **commercial +
  redistribution** rights (many "free/personal" tiers forbid redistribution — the trap). Recorded per-vendor in the
  registry.
- **Derived-only** — licensed vendor raw data isolated server-side; only derived signals surface (mirrors the SF1
  no-spillage rule).
- **Attribution** — mandatory-attribution rendered where required; external-distribution/end-user-cap terms honored.
- **Regional disclaimers** — jurisdiction-appropriate disclaimers on global content; research/education only, never
  personalized advice.

---

## G. Testing

1. **Schema conformance** — every asset class emits the full common signal schema with a valid `rigor` flag.
2. **Rigor labeling** — `validated` only where method+data qualify; everything else `directional`.
3. **Always-deliver** — signals compute on partial factors; missing inputs labeled, edition still ships.
4. **Currency normalization** — USD + local present with FX as-of on every global value.
5. **Distribution** — cadence scheduler builds each edition; double opt-in + unsubscribe + CAN-SPAM footer verified;
   bounce → suppression.
6. **Governance** — no licensed vendor raw row surfaces; attribution present where required.

---

## H. Rollout phases

- **Phase 1 (now):** **Distribution** (cadence scheduler, on-platform + PDF, free double-opt-in list, unsubscribe /
  CAN-SPAM, archive) **+ validated US equities** (SF1 factor decomposition + DCF). Other classes emit `directional`
  signals from data we already poll.
- **Phase 2:** **Global equities** via the selected commercial vendor (DCF/multiples on PIT global fundamentals),
  currency normalization, coverage map.
- **Phase 3:** **Full per-class valuation** — commodities (curve/carry/cost-curve), forex (rate-diff/carry/PPP/REER),
  crypto (network/liquidity) promoted toward `validated` as data/methods qualify; cross-asset relative value ranking.
- **Phase 4:** **Depth** — deeper editorial (RAG-grounded historical context), quarterly/annual global outlooks, and
  broader regional coverage.

> **Held pending Founder decision:** commodities / FX / crypto full valuation **and** global equities depend on the
> **global-vendor license decision** (§C). Phase 1 (distribution + validated US) ships without it.

---

*Inherits P1–P6; adds P7 cross-asset consistency, P8 global-by-design, P9 rigor-disclosed. Not investment advice.*
