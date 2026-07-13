# John Henry Investments Projected EBITDA Model

## Purpose

This document estimates projected EBITDA for the John Henry Investments platform using the subscription revenue assumptions, operating cost ranges, and growth tiers already documented for the project.

These projections are planning estimates, not financial advice, valuation advice, accounting advice, or a guarantee of performance. Actual EBITDA will depend on pricing, customer mix, churn, payment methods, AI usage, document volume, support cost, compliance requirements, provider contracts, staffing, and sales efficiency.

The internal company & platform overview, PowerPoint, Excel workbook, and DCF source files are saved in `docs/internal_valuation_package/` (internal use by default; retained for optional external presentation). Five-stage probability-weighted market-cap and equity-value scenarios are documented in `docs/FIVE_STAGE_VALUATION_MODEL.md`.

## EBITDA definition used

For this planning model:

```text
Projected EBITDA = subscription revenue - recurring operating expenses
```

Included in recurring operating expenses:

- Cloud hosting
- Backend compute
- Database and object storage
- Backups
- Cache
- AI usage
- Document processing
- Monitoring/logging/security tools
- Integration provider costs
- Payment processing variable fees
- Support and operational SaaS tools

Excluded from EBITDA:

- Taxes
- Interest
- Depreciation
- Amortization
- One-time build costs
- One-time legal formation costs
- Founder compensation decisions
- Fundraising costs
- Acquisition costs
- Non-recurring advisory or consulting fees

## Subscription pricing assumptions

| Plan | Monthly price used |
| --- | ---: |
| Consumer | $50 |
| Professional | $299 |
| Enterprise / Family Office | $1,500 |

Enterprise pricing may be higher in practice. This model uses $1,500/month for conservative planning.

## Operating cost assumptions

Operating cost ranges come from `docs/ESTIMATED_PLATFORM_COSTS.md`.

| Tier | Users | Monthly operating cost range before payment processing |
| --- | ---: | ---: |
| Prototype | 100 | $100-$750 |
| Paid MVP | 1,000 | $2,500-$12,000 |
| Growth | 10,000 | $25,000-$125,000 |
| Scale | 50,000 | $150,000-$650,000 |
| Enterprise scale | 100,000 | $400,000-$1.5M+ |

Payment processing estimate:

```text
3.0% of subscription revenue
```

This is a planning simplification for card payments. Enterprise ACH, wire, or invoicing could reduce payment processing cost.

## Scenario A - Conservative consumer-heavy mix

Assumptions:

- 95% Consumer
- 4% Professional
- 1% Enterprise

| Tier | Users | Monthly revenue | Operating costs incl. processing | Projected monthly EBITDA | Projected annual EBITDA |
| --- | ---: | ---: | ---: | ---: | ---: |
| Prototype | 100 | $7,446 | $323-$973 | $6,473-$7,123 | $77.7K-$85.5K |
| Paid MVP | 1,000 | $74,460 | $4,734-$14,234 | $60,226-$69,726 | $722.7K-$836.7K |
| Growth | 10,000 | $744.6K | $47,338-$147,338 | $597K-$697K | $7.17M-$8.37M |
| Scale | 50,000 | $3.723M | $261,690-$761,690 | $2.961M-$3.461M | $35.5M-$41.5M |
| Enterprise scale | 100,000 | $7.446M | $623,380-$1.723M | $5.723M-$6.823M | $68.7M-$81.9M |

Interpretation:

Consumer-heavy growth can still produce strong EBITDA at scale, but it requires high subscriber count, disciplined AI limits, and strong self-service support.

## Scenario B - Base blended SaaS mix

Assumptions:

- 85% Consumer
- 13% Professional
- 2% Enterprise

| Tier | Users | Monthly revenue | Operating costs incl. processing | Projected monthly EBITDA | Projected annual EBITDA |
| --- | ---: | ---: | ---: | ---: | ---: |
| Prototype | 100 | $11,137 | $434-$1,084 | $10.1K-$10.7K | $120.6K-$128.4K |
| Paid MVP | 1,000 | $111,370 | $5,841-$15,341 | $96K-$106K | $1.15M-$1.27M |
| Growth | 10,000 | $1.114M | $58,411-$158,411 | $955K-$1.055M | $11.46M-$12.66M |
| Scale | 50,000 | $5.569M | $317,055-$817,055 | $4.751M-$5.251M | $57.0M-$63.0M |
| Enterprise scale | 100,000 | $11.137M | $734,110-$1.834M | $9.303M-$10.403M | $111.6M-$124.8M |

Important note:

Small tiers are extremely sensitive to customer mix. The Paid MVP, Growth, Scale, and Enterprise rows are more useful for planning than the 100-user prototype row.

## Scenario C - Professional/enterprise-heavy mix

Assumptions:

- 70% Consumer
- 25% Professional
- 5% Enterprise

| Tier | Users | Monthly revenue | Operating costs incl. processing | Projected monthly EBITDA | Projected annual EBITDA |
| --- | ---: | ---: | ---: | ---: | ---: |
| Prototype | 100 | $18,475 | $654-$1,304 | $17.2K-$17.8K | $206K-$214K |
| Paid MVP | 1,000 | $184,750 | $8,043-$17,543 | $167K-$177K | $2.01M-$2.12M |
| Growth | 10,000 | $1.848M | $80,425-$180,425 | $1.667M-$1.767M | $20.0M-$21.2M |
| Scale | 50,000 | $9.238M | $427,125-$927,125 | $8.310M-$8.810M | $99.7M-$105.7M |
| Enterprise scale | 100,000 | $18.475M | $954,250-$2.054M | $16.421M-$17.521M | $197.1M-$210.3M |

Interpretation:

This mix produces the strongest EBITDA, but it also requires higher enterprise support, stronger compliance, more integrations, better onboarding, and more reliable reporting workflows.

## Original target-plan scenario

The product blueprint lists these target counts:

- 50,000 Consumer users at $50/month
- 5,000 Professional users at $299/month
- 500 Enterprise users at $1,500/month

Projected revenue:

| Plan | Users | Monthly revenue | Annual revenue |
| --- | ---: | ---: | ---: |
| Consumer | 50,000 | $2.500M | $30.0M |
| Professional | 5,000 | $1.495M | $17.94M |
| Enterprise | 500 | $750K | $9.0M |
| Total | 55,500 | $4.745M | $56.94M |

Estimated operating cost range:

```text
Use Scale-tier cost range because total user count is near 50,000 users.
```

Payment processing estimate:

```text
$4.745M * 3.0% = ~$142K/month
```

Projected EBITDA:

| Metric | Conservative cost case | Higher cost case |
| --- | ---: | ---: |
| Monthly revenue | $4.745M | $4.745M |
| Operating costs before payment processing | $150K | $650K |
| Payment processing estimate | $142K | $142K |
| Projected monthly EBITDA | $4.453M | $3.953M |
| Projected annual EBITDA | $53.44M | $47.44M |
| EBITDA margin | 93.8% | 83.3% |

Interpretation:

The target-plan scenario is highly profitable on paper because software gross margins can be high. In practice, EBITDA may be lower after staffing, compliance, enterprise support, customer acquisition, chargebacks, refunds, taxes, and additional provider costs.

## ARR valuation scenario from product blueprint

The product blueprint includes:

```text
100,000 users * $75 average monthly revenue per user = $7.5M/month
ARR = $90M/year
```

Using Enterprise-scale cost assumptions:

| Metric | Lower cost case | Higher cost case |
| --- | ---: | ---: |
| Monthly revenue | $7.5M | $7.5M |
| Operating costs before payment processing | $400K | $1.5M |
| Payment processing estimate at 3.0% | $225K | $225K |
| Projected monthly EBITDA | $6.875M | $5.775M |
| Projected annual EBITDA | $82.5M | $69.3M |
| EBITDA margin | 91.7% | 77.0% |

Potential valuation range from the product blueprint:

```text
8x-15x ARR on $90M ARR = $720M-$1.35B enterprise value
```

EBITDA-based view:

```text
At $69M-$82.5M projected EBITDA, valuation outcomes would depend on growth rate, churn, margins, market conditions, compliance risk, customer concentration, and defensibility of proprietary data.
```

## EBITDA sensitivity table

This table shows how EBITDA margin changes depending on operating cost load and payment processing.

| Monthly revenue | Monthly operating costs | Payment processing at 3% | Projected monthly EBITDA | EBITDA margin |
| ---: | ---: | ---: | ---: | ---: |
| $50K | $12K | $1.5K | $36.5K | 73.0% |
| $100K | $15K | $3K | $82K | 82.0% |
| $500K | $75K | $15K | $410K | 82.0% |
| $1M | $150K | $30K | $820K | 82.0% |
| $5M | $650K | $150K | $4.2M | 84.0% |
| $10M | $1.5M | $300K | $8.2M | 82.0% |

## Break-even subscriber examples

Using estimated MVP operating costs of:

```text
$5,000-$15,000/month
```

Plus estimated payment processing:

```text
3.0% of revenue
```

Approximate break-even:

| Revenue mix | Approximate break-even volume |
| --- | --- |
| Consumer only at $50/month | 104-310 subscribers |
| Professional only at $299/month | 18-52 subscribers |
| Enterprise only at $1,500/month | 4-11 subscribers |
| Blended base mix | Usually below 150 total paid users if professional/enterprise users are included |

## Major EBITDA risks

- AI usage can reduce margins if usage is not capped.
- Due diligence document processing can become expensive.
- Enterprise support can require human staff.
- Compliance, legal review, and insurance can materially reduce EBITDA.
- Customer acquisition costs are excluded from this EBITDA model.
- Churn can reduce revenue faster than costs fall.
- Payment processing can be high if enterprise customers pay by card instead of ACH/wire.
- Banking and vendor integration provider costs can rise with transaction volume.
- Data retention requirements can increase storage and backup costs.

## EBITDA improvement levers

- Use ACH or wire for enterprise plans.
- Add plan-based AI quotas.
- Charge separately for heavy document analysis.
- Put external integrations behind Professional and Enterprise plans.
- Use annual contracts for enterprise customers.
- Add self-service onboarding to reduce support costs.
- Cache AI and macro research outputs.
- Archive old reports and documents.
- Use lower-cost AI models for simple tasks.
- Require human approval only for high-risk workflows.

## Recommended EBITDA target by stage

| Stage | Target EBITDA margin |
| --- | ---: |
| Prototype | Not meaningful |
| Paid MVP | 40%-70% after initial launch stabilization |
| Growth | 60%-80% |
| Scale | 70%-85% |
| Enterprise scale | 65%-85%, depending on compliance/support intensity |

## Next financial action items

- [ ] Define final plan mix assumptions.
- [ ] Define expected churn.
- [ ] Define customer acquisition cost assumptions.
- [ ] Define staffing plan.
- [ ] Define support cost per plan.
- [ ] Define AI usage caps by plan.
- [ ] Define storage caps by plan.
- [ ] Define whether enterprise customers pay by ACH/wire or card.
- [ ] Define one-time implementation budget separate from EBITDA.
- [ ] Build a spreadsheet model using live inputs for revenue, cost, churn, and margins.

## Recommended financial planning baseline

For the next planning cycle, use this baseline:

```text
Paid MVP:
- 1,000 users
- 85% Consumer, 13% Professional, 2% Enterprise
- Monthly revenue: ~$111K
- Monthly operating costs including processing: ~$6K-$15K
- Projected monthly EBITDA: ~$96K-$106K before staffing and customer acquisition
```

Conservative adjustment:

```text
After staffing, customer acquisition, compliance, and legal expenses, early-stage EBITDA may be materially lower or negative until the platform reaches stable paid adoption.
```

## Staffing and legal adjustment to pro forma

The base EBITDA tables above should be treated as platform-level EBITDA before full staffing, customer acquisition, and many legal/compliance services.

Detailed staffing and legal assumptions are documented in `docs/STAFFING_LEGAL_PRO_FORMA.md`. Per-person compensation, outsourced versus in-house professional-services comparisons, and quarterly/annual staffing projections are documented in `docs/COMPENSATION_AND_PRO_SERVICES_PROJECTIONS.md`.

Base blended SaaS mix:

```text
85% Consumer, 13% Professional, 2% Enterprise
```

| Tier | Monthly revenue | Platform operating costs incl. processing | Staffing/professional services | Legal/compliance recurring | Adjusted monthly EBITDA | Adjusted annual EBITDA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Prototype - 100 users | $11K | $434-$1,084 | $0-$15K | $0-$2.5K | ($6.5K)-$10.7K | ($78K)-$128K |
| Paid MVP - 1,000 users | $111K | $5.8K-$15.3K | $35K-$90K | $2K-$10K | ($4K)-$68K | ($48K)-$816K |
| Growth - 10,000 users | $1.114M | $58K-$158K | $250K-$650K | $25K-$100K | $206K-$781K | $2.47M-$9.37M |
| Scale - 50,000 users | $5.569M | $317K-$817K | $1.0M-$2.5M | $100K-$300K | $1.95M-$4.15M | $23.4M-$49.8M |
| Enterprise - 100,000 users | $11.137M | $734K-$1.834M | $2.25M-$6.0M | $250K-$800K | $2.50M-$7.90M | $30.0M-$94.8M |

One-person operation view:

```text
One person can operate prototype and limited controlled beta workflows, but a paid production financial SaaS platform requires contractor support or a team for support, security, compliance, legal review, billing, integrations, and engineering.
```

Near-term planning recommendation:

```text
Founder-led controlled beta + outside counsel + contractor engineering + limited AI/document usage.
Initial monthly operating budget excluding founder salary: $5,000-$20,000.
Initial legal/security budget before broad paid launch: $25,000-$100,000.
Paid MVP staffing budget: $35,000-$90,000/month.
```
