# Sales Commission Model — ground-floor rep (Tier 1 & 2)

> JHI-SIG: 69M2705M · Internal planning model — illustrative, not a forecast or comp guarantee.
> Interactive workbook: `scripts/sales_commission_model.py` → `JHI_Sales_Commission_Model.xlsx`.

## Structure
A **100%-commission** ground-floor rep (the "face of the brand") earns a **residual = % of MRR, paid monthly while each subscription stays active**, carved from gross margin. No base salary; the residual builds a "book of business" that rewards retention — an equity-like loyalty hook **without** giving up stock (keeps the company 100% private).

## Tiers
| Tier | $/mo | Segment | Sales motion |
|---|---|---|---|
| Tier 1 | $1,500 | Enterprise / Family Office | Human rep |
| Tier 2 | $299 | Professional | Human rep |
| Tier 3 | $50 | Consumer | Self-serve / affiliate (no human rep) |

## Year-1 commission — closing 100/mo (1,200 subs), 10% residual, no churn
Ramp basis: sub-months = 100 × (1+2+…+12) = **7,800**; Year-1 commission = 10% × avg MRR × 7,800.

| Mix (T1 / T2) | Avg MRR | Year-1 commission | Year-2 run-rate |
|---|---|---|---|
| **0% / 100%** | $299 | **~$233,220** (≈ the "$236K") | ~$430,560/yr |
| 10% / 90% | $419 | ~$326,898 | ~$603,504/yr |
| 20% / 80% | $539 | ~$420,576 | ~$807,552/yr |

## Honest notes
- **The residual compounds:** Year-1 (~$236K all-Tier-2) is a *ramping* book; the Year-2 run-rate is ~$430K+ as those subs keep paying. Budget for it.
- **Protect long-term margin:** recommend a **residual cap / step-down** (e.g., 24–36 mo) and a **<90-day churn clawback**; pay on **collected** revenue only.
- **Realism:** 1,200 premium subs in Year 1 from one rep on a brand-new product is a **stretch/ceiling** scenario — also model a conservative ramp (20–40/mo).
- **No stock:** the residual delivers the loyalty effect; if more upside is wanted, use a **vesting residual (10%→12%→15%)** or phantom bonus — not equity.

## Year-1 EBITDA by mix (same 100/mo ramp)
Lean bootstrapped opex: payment processing 3% + infra/support 2% + SF1 $18k (COGS); sales commission (10% of revenue) + marketing $36k + legal/accounting $18k + software/AI $12k + founder/ops $60k (opex). All editable.

| Line (Year-1) | 0% / 100% | 10% / 90% | 20% / 80% |
|---|---|---|---|
| Revenue | $2,332,200 | $3,268,980 | $4,205,760 |
| COGS | $134,610 | $181,449 | $228,288 |
| **Gross profit** | $2,197,590 | $3,087,531 | $3,977,472 |
| Sales commission | $233,220 | $326,898 | $420,576 |
| Marketing / Legal / Software / Founder | $126,000 | $126,000 | $126,000 |
| **Total OpEx** | $359,220 | $452,898 | $546,576 |
| **EBITDA** | **~$1,838,370** | **~$2,634,633** | **~$3,430,896** |
| EBITDA margin | ~79% | ~81% | ~82% |

**Reality check:** these EBITDA figures assume the *aggressive* 1,200-premium-sub Year-1 ramp — a ceiling, not a base case. At a conservative 20–40 closes/mo the picture is far smaller (and near the fixed-opex breakeven early on). The model's inputs let you dial the ramp down.

## Regenerate
`python scripts/sales_commission_model.py [output.xlsx]` — editable inputs (tier prices, mix %, closes/mo, residual %, churn, gross margin) drive a live 24-month schedule + Year-1-by-mix table. Every sheet carries the legal/`69M2705M`/entity footer.
