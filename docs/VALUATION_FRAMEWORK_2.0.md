# Valuation Framework 2.0 — Fundamentals + Innovation + Management + Optionality

**Date:** 2026-08-11 · **JHI-SIG:** `69M2705M`
**Product:** Aegira · **Publisher:** JHI Research & Analytics Firm, Inc. (proprietary)
**Owner:** Cy Henry (VP, Software Engineering — AI) · **Status:** construct of record (Founder-approved) · **Phase 1 building now**

> The valuation **revamp** that fixes Aegira's systematic under-valuing of innovators (TSLA, CAT and
> peers). Trailing-earnings DCF punishes companies that invest heavily in R&D and carry real
> optionality; Valuation 2.0 corrects this by treating R&D as investment, modeling
> reinvestment-driven growth, and pricing technology optionality in a **bounded, disclosed** way.
> Feeds the **L1 Fundamental/Value layer** of the Aegira Signal Engine. Companion docs:
> `docs/AEGIRA_SIGNAL_ENGINE.md`, `docs/CROSS_ASSET_VALUATION_ENGINE_SPEC.md`,
> `docs/FIVE_STAGE_VALUATION_MODEL.md`, `docs/H5_SF1_VALIDATION_RESULTS.md`,
> `docs/DATA_FOUNDATION_CONSTRUCT.md`. **Research, not investment advice.**

---

## 1. Diagnosis — why the current model under-values innovators

The legacy valuation leans on **trailing-earnings DCF and trailing multiples**. That is
structurally wrong for high-reinvestment innovators, for three compounding reasons:

1. **R&D is expensed, not capitalized.** GAAP forces R&D through the income statement as a cost.
   A company that spends heavily to build future products therefore shows **depressed trailing
   earnings and margins** — the model reads *investment* as *weakness* and marks the company down.
2. **Trailing earnings ignore the reinvestment engine.** A DCF anchored on today's low/negative FCF
   never credits the **ROIC × reinvestment** flywheel that drives future cash flows. High-growth
   compounders look "expensive" because the numerator is temporarily suppressed by choice.
3. **Optionality is unpriced.** New platforms, new markets, and technology bets (autonomy, robotics,
   energy, AI) are **real options** with convex payoffs. A single-point trailing DCF assigns them
   ~zero value, so genuine innovators (**TSLA, CAT**) screen as chronically overvalued.

**Net effect:** the model is biased against exactly the companies our audience most wants a credible,
disciplined read on. Valuation 2.0 removes the bias without inventing numbers or abandoning rigor.

---

## 2. The 8 components

| # | Component | Fixes | Core inputs |
| --- | --- | --- | --- |
| **C1** | **R&D-as-investment** | R&D expensed → understated earnings | Capitalize & amortize R&D over a useful-life window; restate adjusted earnings, margins, invested capital. SF1 `rnd`. |
| **C2** | **ROIC / reinvestment-driven growth** | Trailing FCF ignores the compounding engine | Growth = **ROIC × reinvestment rate**; project cash flows from the engine, not from a suppressed base. SF1 `roic`, `fcf`, margins. |
| **C3** | **Scenario / sum-of-parts DCF** | Single-point DCF hides distribution & mixed businesses | Bear/base/bull scenarios (probability-weighted); **SoP** for multi-segment firms (core vs. emerging). |
| **C4** | **Innovation & Moat score** | No credit for durable advantage | R&D intensity, patents (later), gross-margin durability, share-gain, switching costs → 0–100 moat/innovation score. |
| **C5** | **Management / capital-allocation quality** | Poor capital allocation destroys value silently | ROIC trend, buyback/dividend discipline, M&A track record, **insider ownership** (SEC Form 4, later); **AI/editorial overlay — labeled** as qualitative. |
| **C6** | **Technology optionality premium** | Convex platform bets priced at ~zero | **Bounded** real-options / scenario value for identifiable optionality; capped, disclosed, and always shown as a *separate* line — never blended silently. |
| **C7** | **Sector re-tagging** | Wrong peer set → wrong multiples/expectations | Re-tag firms by *what they actually are* (e.g. TSLA as tech-mobility platform, not pure auto; CAT with services/energy exposure) for peer/expectation context. |
| **C8** | **Blended signal** | Components must resolve to one honest call | Combine C1–C7 into a fair-value **range** + conviction; output in the Signal Engine common schema (L1). |

### 2.1 Optionality guardrails (C6)

Optionality is the highest-risk component and the easiest to abuse. Rules:
- **Bounded:** real-options / scenario value is **capped** as a disclosed % of base fair value.
- **Identified:** each option must be a *named* bet (not a vague "future upside").
- **Separated:** shown as its own line above the fundamentals base — never folded in silently.
- **Scenario-first:** prefer transparent probability-weighted scenarios over opaque option-pricing math; if a real-options model is used, its assumptions are disclosed.

---

## 3. Data plan

Inherits `DATA_FOUNDATION_CONSTRUCT.md` (never-fabricate, as-of, derived-only for licensed data).

| Phase | Data | Feeds |
| --- | --- | --- |
| **Now (P1)** | **Sharadar SF1** (existing): `rnd`, `fcf`, `roic`, margins, invested capital, revenue/EPS history | C1, C2, C3, C4 (partial), C8 |
| **Later (P2)** | **SEC Form 4** insider ownership/transactions | C5 |
| **Later (P2)** | **Segment / KPI** data (10-K/10-Q segments, deliveries, backlog) | C3 (SoP), C7 |
| **Later (P3)** | **Patents** (grants/citations) | C4 (moat/innovation depth) |

Licensed rows (SF1) stay internal (gitignored cache); only **derived** metrics surface (governance).

---

## 4. Validation (H5 on the revamped model)

Valuation 2.0 is not "shipped because it feels fairer." It is **re-validated** with the pre-registered
back-test method of `docs/H5_SF1_VALIDATION_RESULTS.md`:

1. **Pre-register** the revamped factor construction (C1–C8), weights, universe, and success bar
   **before** reading results — no tuning to the outcome.
2. **Compare** Valuation 2.0 vs. the legacy trailing model on the **same pre-registered bar**
   (mean IC ≥ 0.03, |t-stat| ≥ 2.0, hit-rate ≥ 0.55), out-of-sample and survivorship-free where data allows.
3. **Innovator check:** confirm the revamp corrects the specific TSLA/CAT-type mis-ranking without
   degrading breadth performance (no cherry-picking; report the honest full-universe result).
4. **Ship rule:** clears the bar → L1 uses Valuation 2.0 as **`validated`**; misses → **`directional`**
   (or withhold) with the honest result recorded. Never relabel a miss as a pass.

---

## 5. Governance & disclosures

- **Licensed data derived-only + attributed** (SF1, and later SEC/segment/patent sources).
- **AI/editorial overlay labeled** (C5): qualitative management/capital-allocation judgments are
  clearly marked as AI/editorial, fact-locked to the underlying metrics, never presented as hard data.
- **Optionality disclosed** (C6): the premium line, its cap, and its assumptions are always visible.
- **As-of / source** on every figure; **never fabricate** missing inputs.
- **Research, not investment advice** on every surface.

---

## 6. Rollout — Phases 1–3

### Phase 1 — Fundamentals revamp on existing data *(building now)*
- **Components:** C1 (R&D-as-investment), C2 (ROIC/reinvestment growth), C3 (scenario/SoP DCF),
  C4 (Innovation & Moat, from R&D intensity + margins), C8 (blended signal).
- **Data:** existing **SF1** (`rnd`, `fcf`, `roic`, margins).
- **Validate:** re-run **H5** vs. legacy; ship L1 as `validated`/`directional` per result.

### Phase 2 — Management, segments, optionality depth
- **Add:** C5 (SEC **Form 4** insider ownership), C7 (sector re-tagging via segment/KPI),
  deeper C3 SoP for multi-segment firms; formalize C6 optionality scenarios.
- **Data:** SEC Form 4 + segment/KPI.

### Phase 3 — Patents & full optionality
- **Add:** patents into C4 (moat/innovation depth); mature C6 bounded real-options where warranted.
- **Data:** patent grants/citations.

---

*Prepared under JHI-SIG `69M2705M`. Aegira is a product of JHI Research & Analytics Firm, Inc.
Research, not investment advice.*
