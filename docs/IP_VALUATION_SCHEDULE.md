# IP Valuation Schedule — platform & mobile software

> JHI-SIG: 69M2705M · Support schedule for the IP contributed to JHI Research &
> Analytics Firm, Inc. in exchange for 10,000,000 founder shares. **NOT a formal
> appraisal** — the official §351 basis is the CPA/appraiser's determination.
> Interactive workbook: `scripts/ip_valuation_schedule.py` → `JHI_IP_Valuation_Schedule.xlsx`.

## Basis
Par value **$0.04 × 10,000,000 shares = $400,000** stated capital. This schedule provides
**defensible, hours-based support** for that figure: completed engineering + professional work,
plus projected work to launch, valued at market rates by workstream and skillset.

## Summary
| Category | Value |
|---|---|
| Completed work (to date) | **$312,725** |
| Projected work (to launch) | **$86,750** |
| **Grand total** | **$399,475** |
| Par-value stated capital | $400,000 |
| Variance | **−$525 (~0.1%)** |

## Completed work (to date)
| Workstream | Skillset | Rate | Hours | Value |
|---|---|---|---|---|
| Backend platform & 17 API modules | Sr. Backend | $140 | 500 | $70,000 |
| Frontend + mobile app | Sr. Frontend | $130 | 360 | $46,800 |
| Research / quant (score, validation, fundamentals) | Data/Quant | $180 | 210 | $37,800 |
| Deal X-Ray / QoE / diligence engines | Sr. Backend + domain | $160 | 230 | $36,800 |
| Interactive Excel + PDF exports | Sr. Backend | $140 | 95 | $13,300 |
| Deal Pipeline + Postgres persistence | Sr. Backend | $140 | 85 | $11,900 |
| DevOps / Docker / infrastructure | DevOps | $150 | 80 | $12,000 |
| Security (auth, 2FA, WebAuthn, encryption) | Security | $160 | 95 | $15,200 |
| Architecture / product / competitive strategy | Product/Strategy | $175 | 175 | $30,625 |
| Finance & legal-adjacent docs | Finance/Legal-adj. | $150 | 160 | $24,000 |
| QA / testing | QA | $110 | 130 | $14,300 |

## Projected work (to launch)
| Workstream | Skillset | Rate | Hours | Value |
|---|---|---|---|---|
| Homepage Phase B + About polish | Sr. Frontend | $130 | 55 | $7,150 |
| Stripe checkout + trial/paywall + Stripe Tax | Sr. Backend | $140 | 90 | $12,600 |
| CI/CD + observability + backups | DevOps | $150 | 75 | $11,250 |
| Production security hardening | Security | $160 | 65 | $10,400 |
| SF1 fundamentals + H5 validation | Data/Quant | $180 | 110 | $19,800 |
| Module UI wiring (accounting/reports/CRM) | Sr. Frontend | $130 | 80 | $10,400 |
| Terms/Privacy/compliance + counsel | Legal-adj. | $150 | 35 | $5,250 |
| E2E testing + launch hardening | QA | $110 | 90 | $9,900 |

## Important note (par value vs. fair value)
**Par value ($400,000) is a stated-capital / legal figure — not the same as fair market value.**
For the IRC **§351** IP-for-stock exchange, the **fair-value basis is determined by a licensed CPA
or qualified appraiser**. This schedule is defensible *support* they can rely on and adjust; rates
and hours in the workbook are editable inputs.

## Regenerate
`python scripts/ip_valuation_schedule.py` — editable Rate/Hours cells drive live Value formulas,
subtotals, grand total, and the par-value reconciliation. Legal/`69M2705M`/entity footer on the sheet.
