# Contribution Margin & Cost-Volume-Profit (CVP) Analysis

**Owner:** Cy Henry (VP Software Engineering — AI) · **Signature:** `69M2705M`
**Purpose:** Set up the **Unit Contribution Margin** and **CVP / break-even** framework for the sales
force and pricing tiers. Grounds `docs/GTM_LAUNCH_STRATEGY.md` and pairs with the sales-commission and
consolidated-projections models. Figures use the verified unit costs in `docs/PRICING_BILLING_SCHEMA.md`.

> **Core identity:** Unit Contribution Margin **C = P − V** (Unit Price − Unit Variable Cost).
> **CM ratio = C / P.** **Profit = C·Q − F.** **Break-even Q = F / C.** **Break-even revenue = F / CM ratio.**

## 1. Unit variable cost (V) — definition
Two variable components per unit:
- **Delivery variable cost** (scales with each seat/sale): `V_delivery = $3.00 + 3% × P`
  - $3.00 = NASDAQ ~$1.50 + cloud ~$1.50 per seat; 3% = payment processing on price P.
- **Variable selling cost** (only on a **new** sale): sales commission per the **prepaid-MSA** plan ≈ **15% of contract value** upfront (+ year-end MSA bonus). This is a variable cost **per unit sold** and belongs in the sales-force contribution margin.

## 2. Table A — Delivery contribution margin (per seat-month, ongoing)
`V = $3.00 + 3%·P` → this is the **steady-state** margin on an active subscription (excludes one-time commission).

| Tier (unit) | Price P | Variable cost V | **CM  C = P − V** | CM ratio |
|---|---:|---:|---:|---:|
| Consumer (seat) | $110.00 | $6.30 | **$103.70** | 94.3% |
| Professional (seat) | $299.00 | $11.97 | **$287.03** | 96.0% |
| Enterprise (per-seat-equiv) | $300.00 | $12.00 | **$288.00** | 96.0% |
| Enterprise (plan, 5 seats) | $1,500.00 | $60.00 | **$1,440.00** | 96.0% |
| Enterprise (add'l seat) | $99.00 | $5.97 | **$93.03** | 94.0% |

**Read:** software-style CM ratios (94–96%). Nearly every incremental dollar of price is contribution — the engine of the model.

## 3. Table B — Sales contribution per NEW subscription (Year 1, incl. commission)
Unit = **one new annual subscription**; V now includes annual delivery **and** the 15% upfront commission. (Illustrative; renewals carry little/no commission → Year-2+ CM ≈ Table A annualized.)

| Tier (new annual sub) | ACV (P) | Annual delivery | Commission (15%) | Total V | **CM  C = P − V** | CM ratio |
|---|---:|---:|---:|---:|---:|---:|
| Consumer (prepaid) | $1,188 | $71.64 | $178.20 | $249.84 | **$938.16** | 79.0% |
| Professional | $3,588 | $143.64 | $538.20 | $681.84 | **$2,906.16** | 81.0% |
| Enterprise (5-seat plan) | $18,000 | $720.00 | $2,700.00 | $3,420.00 | **$14,580.00** | 81.0% |

**Read:** even after paying the rep 15% upfront, Year-1 contribution is ~79–81%; it steps up to ~94–96% on renewal. Enterprise throws off the largest CM per deal → prioritize it in the sales motion.

## 4. Break-even (CVP) — how many units to cover fixed costs
`Break-even units Q* = F / C` where **F = monthly fixed operating cost** (staff, tooling, overhead).
Using **Table A** monthly CM. *(Confirm F from `scripts/consolidated_projections_model.py`; shown here for three illustrative F levels.)*

| Monthly fixed cost F | Consumer-only (C=$103.70) | Professional-only (C=$287.03) | Enterprise-plan-only (C=$1,440) |
|---|---:|---:|---:|
| $50,000 | 483 subs | 175 subs | 35 plans |
| $100,000 | 965 subs | 349 subs | 70 plans |
| $150,000 | 1,447 subs | 523 subs | 105 plans |

- **Break-even revenue = F / CM ratio.** At ~95% CM ratio, break-even revenue ≈ **1.05 × F** — i.e., revenue only needs to clear fixed costs by ~5% because variable costs are tiny.
- **Blended** break-even needs a tier-mix assumption; compute `C_blended = Σ(mix_i × C_i)` then `Q* = F / C_blended`.

## 5. CVP toolkit (formulas for the workbook / planning)
- **Target-profit volume:** `Q = (F + target profit) / C`
- **Margin of safety:** `(actual sales − break-even sales) / actual sales` — cushion before losses.
- **Degree of operating leverage:** `DOL = total CM / operating income` — with high CM and rising volume, profit accelerates fast (and is sensitive on the downside).
- **CVP profit line:** `Profit = (P − V)·Q − F` — plot profit vs. volume Q per tier to see the crossover.

## 6. Sales-force implications
- **Commission is a variable cost per unit** — kept inside CM (Table B), so quotas and comp never erode unit economics.
- **Lead with Enterprise** (largest CM per deal, $14.6k Year-1 / ~$17.3k on renewal) while Consumer/Professional scale via product-led funnel.
- **Renewals are the profit engine:** Year-1 CM 79–81% → renewal CM 94–96% once commission rolls off. Retention is worth more than a marginal new sale.
- **Gate rep hiring to break-even math:** add reps as incremental CM covers their fully-loaded cost (ties to the EBITDA-gated staffing plan in the consolidated projections).

## 7. Editorial AI (E2) production spend — how it hits Contribution Margin
The LLM editorial spend (Claude Sonnet 5 / Nova Pro / Llama on Bedrock — evaluation open) is a
**shared production cost, not a per-seat variable cost.** One edition is generated **once** and served
to **every** subscriber, so it does **not** scale per unit like data/cloud/processing. Correct CVP
treatment: it sits in **Fixed Costs (F)** (content production), and its **cost-per-subscriber falls as
we scale.** (If we ever want a per-unit view, it's the amortized figure below — but it is technically fixed/shared.)

### Recommended monthly budget (a *cap*, pick one)
Set as a **hard cap** in the drafting service (stop / fall back to the deterministic edition when hit),
so spend cannot run away. Estimated steady-state at our cadence (daily/monthly/quarterly/annual, tiered
models + a fact-check pass) is **only ~$25–$75/mo**; the cap adds headroom for iteration, the bake-off,
and growth.

| Option | Monthly cap | Covers |
|---|---:|---|
| Starter | **$100** | Production at current cadence + light iteration |
| **Recommended** | **$250** | Production + fact-check pass + bake-off iteration + buffer |
| Growth | **$500** | Heavy experimentation, multi-model in parallel, scaling cadence |

*(Range to choose from: **$100–$500/mo**. True spend likely lands well under the cap.)*

### CM impact is negligible (amortized per subscriber, at a $250 cap)
| Subscribers | Editorial $/sub/mo | Consumer CM after editorial (from $103.70) |
|---:|---:|---:|
| 100 | $2.50 | $101.20 (92%) |
| 1,000 | $0.25 | $103.45 (94%) |
| 10,000 | $0.025 | $103.68 (94%) |
| 50,000 | $0.005 | $103.70 (94%) |

- **Break-even effect:** a $250/mo cap raises fixed costs by `F/CM` ≈ **2–3 Consumer subs** to cover — a rounding error against 94–96% margins.
- **Takeaway:** the AI editorial budget is **immaterial to unit economics at any real scale**; it's a fixed production line, and the fact-lock keeps quality without quality-risk. Fold the chosen cap into **F** in the consolidated projections.

## 7a. Next step (optional build)
On authorization, I'll generate an **Excel CVP workbook** (`scripts/contribution_margin_cvp.py`) — editable P/V/F/mix inputs, per-tier CM, break-even chart, target-profit and margin-of-safety calculators — matching our other institutional workbooks. Say the word.

---
*Inputs to confirm:* monthly fixed cost **F** (from the consolidated projections), the commission schedule (15% upfront + year-end bonus), and whether Professional/Enterprise get annual-prepaid SKUs.
