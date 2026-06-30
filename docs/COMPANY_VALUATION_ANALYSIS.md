# Company Valuation — Honest Assessment (current state)

> **Posture note:** JHI is a **research & analytics firm** that **never manages outside
> funds / client money**, but **is open to outside equity (VC/seed)** to fund the company
> (`docs/COMPANY_POSTURE_AND_COMPLIANCE.md`). This valuation supports **fundraising** as
> well as internal/IP/estate/lending use. (Raising company equity ≠ managing client money.)


What is John Henry Investments worth *today*, based on what's actually built? Short
answer: a **large "market cap" is unwarranted now**, because value in software is
driven by traction (users, revenue, retention) and validated IP — all currently
absent. The defensible value today is essentially the **asset / cost‑to‑duplicate of
the codebase + IP**, plus option value.

> Not a valuation, securities, or investment opinion. Confirm with a qualified
> appraiser/banker for any transaction. This is an internal, honest estimate.

## First, terminology

- **Market capitalization** = shares outstanding × public share price. It applies to
  **public** companies. John Henry Investments is **private**, so there is no market
  cap — the right concept is **private valuation / enterprise value** (or pre‑money
  valuation if raising).

## Current status (the value drivers that are missing)

| Value driver | Status | Effect on value |
| --- | --- | --- |
| Revenue / ARR | **$0** (pre‑revenue) | No income‑ or revenue‑multiple value |
| Users / traction | **0** (pre‑launch) | No market validation |
| Retention / NRR | none | No durability evidence |
| Core IP validated | **No** — Opportunity Score predictive validity (H5) failed back‑test | Key moat unproven |
| Deployed to production | **No** (runs in Docker/dev; code on a feature branch, not `main`) | Not yet operational |
| Functional completeness | Partial (several module pages still prototype) | Reduces realizable value |

When the income and market approaches both yield ~$0 (no revenue, no comparable
multiple to apply), the only defensible basis is **asset/cost**.

## Valuation by method

| Method | Applicable now? | Estimate |
| --- | --- | --- |
| **Income (DCF / ARR multiple)** | ❌ No — $0 revenue | ~$0 |
| **Market (comparable ARR multiples)** | ❌ No — nothing to multiply | ~$0 |
| **Cost‑to‑duplicate (asset‑based)** | ✅ Yes — real codebase + IP exist | **~$120k–$350k** |
| **Pre‑revenue startup methods (Berkus / Scorecard / Risk‑factor)** | ⚠️ Story‑based only | **~$0.5M–$2.5M** *if raising*, heavily caveated |
| **Future scenario (blueprint)** | 🚫 Not current value | $720M–$1.3B *only at ~$90M ARR* |

### Cost‑to‑duplicate (the honest "now" floor)
Rebuilding what exists — a broad Next.js + FastAPI app (auth/2FA/biometric, live
multi‑asset market data, research/valuation engines, 5‑agent AI support with
escalation, durable accounting/CRM, mobile app, Docker, 98 tests) — is roughly
**800–2,000 engineering hours**. At blended market dev rates ($80–150/hr) that's
**~$120k–$350k** of replacement value. This is the most defensible current intrinsic
figure. (Note: actual cash spent was far lower thanks to AI‑assisted build — good for
ROI, but it doesn't inflate market value.)

### Pre‑revenue "story" valuations (if raising capital)
Pre‑seed rounds are priced on narrative, team, and prototype, not intrinsics. Methods
like **Berkus** cap pre‑revenue valuations around **$2–2.5M** and only when there's a
strong team, prototype, and early relationships. Here: idea ✅, prototype ✅, team =
founder + AI (partial), market relationships/traction ❌. A defensible *raise* story
might land **~$0.5M–$1.5M pre‑money** — but that's **investor narrative/optionality,
not realized value**, and would be hard to justify without traction.

### The blueprint's $720M–$1.3B is a *future scenario*, not today
That figure (`docs/PRODUCT_BLUEPRINT.md`) is explicitly conditioned on **reaching
~$90M ARR** at 8–15× ARR. Today's ARR is $0, so applying it now is unwarranted.

## Why a large valuation is unwarranted right now

1. **No revenue and no users** — the two biggest value drivers are zero.
2. **Unvalidated core IP** — the Opportunity Score's predictive edge failed its
   back‑test; until validated it's a feature, not a moat.
3. **Not deployed / not on `main`** — pre‑production, partly prototype modules.
4. **No retention/unit economics** — nothing proves durable value or LTV/CAC.
5. **Easily‑replicable today** — AI tooling lowers the rebuild cost (cuts to the
   cost‑to‑duplicate floor), so the *code alone* isn't a strong moat.

## What unlocks value (milestone → valuation ladder)

| Milestone | Indicative valuation impact |
| --- | --- |
| Ship to production on `main`, modules functional | Establishes a real product asset |
| First paying users + live billing | Enables revenue‑based valuation |
| **Validate the Opportunity Score (H5)** with licensed data | Creates a defensible moat |
| ~$10k–$50k MRR with retention | Seed‑stage valuation on real ARR multiples |
| Scale toward the blueprint's ARR | Approaches the $100M+ scenario range |

## Honest verdict

- **Market cap:** not applicable (private company).
- **Defensible intrinsic value today:** ≈ the **asset/cost‑to‑duplicate (~$120k–$350k)**
  plus option value — **not** millions, and certainly not the blueprint's hundreds of
  millions.
- **A high valuation is unwarranted** until there are **users, revenue, retention, and a
  validated score.** Build those, and the valuation grows into the larger numbers
  honestly.
