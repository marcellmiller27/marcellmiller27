# R&D Validation Protocol & Go-Live Criteria (JHI)

> The agreed standard for validating the John Henry Opportunity Score on SF1 fundamentals
> before deploying to B2C/B2B clients. Built to give **real confidence without waiting a
> year**. Companions: `docs/FUNDAMENTALS_RESEARCH_PROGRAM.md`,
> `docs/FUNDAMENTALS_DATA_VENDORS.md`, `docs/SECTION_8_VALIDATION_RESULTS.md`.
>
> **NOT investment advice.** This governs internal research quality and go-live gating.

---

## Core principle

**Historical depth substitutes for calendar time.** We do NOT need 12 months of live
data to gain statistical confidence — ~20+ years of point-in-time, survivorship-free SF1
history, tested out-of-sample, delivers far more statistical power in ~weeks than a year
of forward data could. Calendar time is reserved for **trust / live track record**, which
accrues *after* a properly positioned launch — not as a gate on statistical validity.

### Three distinct timescales (don't conflate)
| Time | Meaning | Duration |
| --- | --- | --- |
| **A. Work time** | Building adapter + running tests | ~1 week |
| **B. Historical lookback** | Years of past data in the test | ~20+ yrs (free; it's data) |
| **C. Live/forward track** | Real-time record after deploy | months → ongoing (post-launch) |

---

## Pre-registration (lock BEFORE running — anti p-hacking)

Fix and write down these *before* touching results:
- **Hypothesis (H5):** the Opportunity Score has predictive validity for forward returns.
- **Bar:** out-of-sample **|t| ≥ 2.0** on the long–short factor return (pre-registered).
- **Factors:** value (E/P, B/P), quality (ROE, margins, low accruals), growth — fixed list.
- **Universe:** SF1 survivorship-free US equities; liquidity screen fixed.
- **PIT rule:** As-Reported (`ARQ/ART/ARY`) aligned on filing date `datekey` (no `MRQ` restated).
- **Costs:** transaction costs + turnover modeled (no frictionless fantasy).
- **OOS split:** train/test split (or walk-forward) fixed in advance.
- **Iteration budget:** limited; every re-spec spends statistical credibility (record each attempt).

---

## The ~3–4 week validation gate

| Phase | Time | Work | Gate to pass |
| --- | --- | --- | --- |
| **0 — Historical validation** | Week 1 | Adapter + pre-registered OOS backtest over full SF1 history (PIT, costs) | **OOS |t| ≥ 2.0**; positive net-of-cost long–short |
| **1 — Robustness** | Weeks 2–3 | Subperiods, sectors, regimes, turnover/capacity, drawdown, factor crowding | Holds out-of-sample, not just full-sample; no single-period dependence |
| **2 — Soft launch (research/beta)** | Week 4 | Ship to early B2C/B2B **labeled research/education + disclaimers**; start live paper-track | Clients understand it's analysis, not advice |
| **3 — Live track accrues** | Months 2–6+ | Publish growing live IC/track record while serving | Trust compounds; no return promises |

---

## Go-live criteria (all must be true)

**Statistical**
- [ ] Pre-registered OOS test passes **|t| ≥ 2.0** (net of costs).
- [ ] Robust across subperiods, sectors, and at least one stress regime.
- [ ] Realistic capacity/turnover; drawdowns understood and disclosed.
- [ ] Results reproducible from a tagged commit (`/research/equity-oos-backtest`).

**Positioning & compliance (the real "market risk")**
- [ ] Marketed as **research / education / decision-support — NOT advice or guaranteed returns**.
- [ ] Disclaimers in product + marketing; score shown as **one input**, not a directive.
- [ ] Advice/RIA posture reviewed with counsel (don't drift into personalized advice).
- [ ] Honest methodology + limitations published ("what the score is / isn't").

**Operational**
- [ ] Commercial SF1 license with derived-data rights in place (single-user is R&D only).
- [ ] Monitoring of live signal vs. backtest expectation (drift alerts).

---

## What would RAISE the bar (be honest)
- If JHI ever **manages money** or **promises outcomes**, ~4 weeks is NOT enough — that
  requires a longer live track record **and** RIA registration. As transparent
  **research/decision-support**, the ~3–4 week gate is defensible; as advice/management, it isn't.
- A failed gate → limited, disciplined iteration only; if it keeps failing, **say so
  honestly** and ship the platform's other value (organization, macro, acquisition tools)
  without over-claiming predictive alpha.

---

## Bottom line
**Don't wait a year — but don't ship on Day 5 either.** A ~**3–4 week** pre-registered,
out-of-sample, robustness-checked validation (decades of history doing the heavy lifting)
plus correct **research/education positioning** is the responsible path to live B2C/B2B
deployment, with the live track record accruing alongside real clients.
