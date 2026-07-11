# John Henry Investments Compensation and Professional Services Projections

## Purpose

This document estimates sustainable staffing compensation, professional services costs, in-house conversion costs, and quarterly/annual expenditure impact for the John Henry Investments platform.

These are planning estimates, not compensation, tax, accounting, legal, HR, or investment advice. Actual costs depend on geography, hiring market, benefits, contractor rates, founder compensation, legal scope, regulatory status, customer mix, revenue, and vendor contracts.

Department-level job descriptions and legal/professional staffing requirements are documented in `docs/JOB_DESCRIPTIONS_AND_STAFFING_REQUIREMENTS.md`.

## Planning definitions

Loaded compensation means:

```text
salary or contractor rate + payroll taxes + benefits + equipment + tools + recruiting + management overhead + insurance allocation
```

Professional services means:

```text
outside legal counsel, CPA/bookkeeping, compliance advisory, security review, DevOps contractors, fractional finance, fractional HR, and specialized consultants
```

## Current recommendation

For the next realistic phase:

```text
Founder-led controlled beta with limited contractors and outside counsel.
```

Recommended operating model:

- One founder/operator can manage prototype and limited controlled beta.
- Use outside counsel for legal/compliance review.
- Use CPA/bookkeeper for finance and tax hygiene.
- Use contractor engineering for scoped build items.
- Use contractor security/DevOps review before production launch.
- Do not hire full in-house legal/compliance/security until recurring revenue justifies it.

## Compensation assumptions per person

| Role / unit | Monthly loaded cost | Quarterly loaded cost | Annual loaded cost |
| --- | ---: | ---: | ---: |
| Founder/operator, unpaid or deferred | $0 | $0 | $0 |
| Founder/operator, modest draw | $8,000-$15,000 | $24,000-$45,000 | $96,000-$180,000 |
| Founder/operator, market executive comp | $18,000-$25,000 | $54,000-$75,000 | $216,000-$300,000 |
| Full-stack engineer | $12,000-$25,000 | $36,000-$75,000 | $144,000-$300,000 |
| Backend/data engineer | $14,000-$28,000 | $42,000-$84,000 | $168,000-$336,000 |
| AI/data engineer | $15,000-$35,000 | $45,000-$105,000 | $180,000-$420,000 |
| DevOps/security engineer | $15,000-$35,000 | $45,000-$105,000 | $180,000-$420,000 |
| Product/design | $10,000-$25,000 | $30,000-$75,000 | $120,000-$300,000 |
| Customer support/success | $5,000-$12,000 | $15,000-$36,000 | $60,000-$144,000 |
| Sales/account manager | $8,000-$20,000 | $24,000-$60,000 | $96,000-$240,000 |
| Finance/accounting operations | $8,000-$20,000 | $24,000-$60,000 | $96,000-$240,000 |
| Compliance/legal operations | $10,000-$30,000 | $30,000-$90,000 | $120,000-$360,000 |
| QA/product operations | $7,000-$18,000 | $21,000-$54,000 | $84,000-$216,000 |

## Professional services unit costs

| Professional service | Unit basis | Estimated cost |
| --- | --- | ---: |
| Outside counsel - general business/SaaS | Hourly | $300-$800/hour |
| Outside counsel - fintech/securities | Hourly | $500-$1,200/hour |
| Terms/privacy/disclaimers package | Project | $5,000-$35,000 |
| Securities/investment advisory memo | Project | $10,000-$75,000+ |
| Data privacy review | Project | $5,000-$40,000 |
| Vendor/provider contract review | Per contract | $2,500-$25,000 |
| Fractional compliance officer | Monthly retainer | $2,500-$15,000/month |
| Fractional CFO/controller | Monthly retainer | $2,500-$12,000/month |
| CPA/bookkeeping | Monthly retainer | $300-$3,500/month |
| Security review | Project | $5,000-$25,000 |
| Penetration test | Project | $7,500-$30,000 |
| SOC 2 readiness advisor | Project/monthly | $5,000-$50,000+ |
| DevOps/cloud contractor | Hourly/monthly | $100-$250/hour or $2,500-$15,000/month |
| AI/data science consultant | Hourly/monthly | $150-$350/hour or $5,000-$30,000/month |
| Customer support contractor/VA | Monthly | $500-$5,000/month |

## Outsourced vs in-house professional services

### Legal

| Option | Monthly cost | Quarterly cost | Annual cost | Best use |
| --- | ---: | ---: | ---: | --- |
| Outside counsel as needed | $1,000-$10,000 | $3,000-$30,000 | $12,000-$120,000 | Prototype, beta, MVP |
| Fractional general counsel | $5,000-$25,000 | $15,000-$75,000 | $60,000-$300,000 | Paid MVP, enterprise pilots |
| In-house counsel | $20,000-$45,000 | $60,000-$135,000 | $240,000-$540,000 | Growth or regulated enterprise scale |

In-house legal becomes more rational when:

```text
legal spend consistently exceeds ~$20K-$40K/month or the business has constant contracts, compliance, provider negotiations, and regulatory work.
```

### Compliance

| Option | Monthly cost | Quarterly cost | Annual cost | Best use |
| --- | ---: | ---: | ---: | --- |
| Outside compliance advisor | $1,000-$10,000 | $3,000-$30,000 | $12,000-$120,000 | Prototype, beta |
| Fractional CCO/compliance lead | $5,000-$25,000 | $15,000-$75,000 | $60,000-$300,000 | MVP, regulated workflows |
| In-house compliance lead | $15,000-$35,000 | $45,000-$105,000 | $180,000-$420,000 | Growth, regulated advisory risk |
| Compliance team | $50,000-$200,000+ | $150,000-$600,000+ | $600,000-$2.4M+ | Scale/enterprise |

### Finance/accounting

| Option | Monthly cost | Quarterly cost | Annual cost | Best use |
| --- | ---: | ---: | ---: | --- |
| Bookkeeper/CPA retainer | $300-$3,500 | $900-$10,500 | $3,600-$42,000 | Prototype, beta, MVP |
| Fractional controller/CFO | $2,500-$12,000 | $7,500-$36,000 | $30,000-$144,000 | MVP, investor reporting |
| In-house finance/accounting ops | $8,000-$20,000/person | $24,000-$60,000/person | $96,000-$240,000/person | Growth |
| Finance team | $40,000-$150,000+ | $120,000-$450,000+ | $480,000-$1.8M+ | Scale/enterprise |

### Security/DevOps

| Option | Monthly cost | Quarterly cost | Annual cost | Best use |
| --- | ---: | ---: | ---: | --- |
| Security review project | $5,000-$25,000 one-time | Variable | Variable | Before beta/MVP launch |
| DevOps contractor | $2,500-$15,000 | $7,500-$45,000 | $30,000-$180,000 | MVP |
| In-house DevOps/security engineer | $15,000-$35,000/person | $45,000-$105,000/person | $180,000-$420,000/person | Growth |
| Security/DevOps team | $60,000-$250,000+ | $180,000-$750,000+ | $720,000-$3.0M+ | Scale/enterprise |

### Engineering

| Option | Monthly cost | Quarterly cost | Annual cost | Best use |
| --- | ---: | ---: | ---: | --- |
| Part-time contractor | $2,500-$15,000 | $7,500-$45,000 | $30,000-$180,000 | Prototype/beta |
| Full-time contractor | $15,000-$35,000 | $45,000-$105,000 | $180,000-$420,000 | MVP build speed |
| In-house engineer | $12,000-$28,000/person | $36,000-$84,000/person | $144,000-$336,000/person | Durable product development |
| Engineering team | $100,000-$1.5M+ | $300,000-$4.5M+ | $1.2M-$18M+ | Growth/scale |

## Sustainable staffing by stage

### Stage 1 - Founder-led controlled beta

Target:

```text
25-100 beta users, limited uploads, no broad paid launch
```

Sustainable personnel:

| Role/service | Unit | Monthly cost |
| --- | ---: | ---: |
| Founder/operator | 1 | $0-$15,000 |
| Part-time engineering contractor | 0.25-0.5 FTE | $2,500-$12,500 |
| Outside legal/compliance | Retainer/project average | $1,000-$7,500 |
| CPA/bookkeeping | Retainer | $300-$2,000 |
| Security/DevOps review | Part-time/project average | $500-$5,000 |
| Support contractor/VA | Optional | $0-$2,500 |
| Total personnel/pro services |  | $4,300-$44,500/month |

Quarterly and annual:

| Period | Cost range |
| --- | ---: |
| Quarterly | $12,900-$133,500 |
| Annual | $51,600-$534,000 |

### Stage 2 - Lean paid MVP team

Target:

```text
Up to 1,000 users or roughly $50K-$150K MRR
```

Sustainable personnel:

| Role/service | Unit | Monthly cost |
| --- | ---: | ---: |
| Founder/operator | 1 | $8,000-$20,000 |
| Full-stack engineer | 1 | $12,000-$25,000 |
| Backend/data engineer | 0.5-1 | $7,000-$28,000 |
| Customer support/operations | 0.5-1 | $2,500-$12,000 |
| Outside legal/compliance | Retainer | $2,000-$10,000 |
| CPA/bookkeeping/controller | Retainer | $1,000-$6,000 |
| Security/DevOps contractor | 0.25-0.5 | $2,500-$15,000 |
| Total personnel/pro services |  | $35,000-$116,000/month |

Quarterly and annual:

| Period | Cost range |
| --- | ---: |
| Quarterly | $105,000-$348,000 |
| Annual | $420,000-$1.392M |

### Stage 3 - Growth team

Target:

```text
10,000 users or roughly $500K-$2M+ MRR depending on mix
```

Sustainable personnel:

| Function | Headcount | Monthly cost |
| --- | ---: | ---: |
| Leadership/product | 2-4 | $30,000-$100,000 |
| Engineering | 6-12 | $90,000-$336,000 |
| AI/data | 2-5 | $30,000-$175,000 |
| DevOps/security | 2-4 | $30,000-$140,000 |
| Support/success | 4-10 | $20,000-$120,000 |
| Sales/account management | 3-8 | $24,000-$160,000 |
| Finance/accounting | 1-2 | $8,000-$40,000 |
| Legal/compliance ops | 1-3 | $10,000-$90,000 |
| QA/product ops | 1-3 | $7,000-$54,000 |
| Outside professional services | Retainer/project average | $25,000-$100,000 |
| Total personnel/pro services | 22-51 | $274,000-$1.315M/month |

Quarterly and annual:

| Period | Cost range |
| --- | ---: |
| Quarterly | $822,000-$3.945M |
| Annual | $3.288M-$15.78M |

### Stage 4 - Scale team

Target:

```text
50,000 users or roughly $3M-$10M+ MRR depending on mix
```

Sustainable personnel:

| Function | Headcount | Monthly cost |
| --- | ---: | ---: |
| Executive/product leadership | 5-8 | $100,000-$250,000 |
| Engineering | 20-45 | $300,000-$1.26M |
| AI/data/research | 8-20 | $120,000-$700,000 |
| DevOps/security/compliance engineering | 6-15 | $90,000-$525,000 |
| Support/success | 15-40 | $75,000-$480,000 |
| Sales/account management | 10-25 | $80,000-$500,000 |
| Finance/accounting/legal ops | 5-12 | $50,000-$360,000 |
| QA/product operations | 5-12 | $35,000-$216,000 |
| Outside professional services | Retainer/project average | $100,000-$300,000 |
| Total personnel/pro services | 74-177 | $950,000-$4.591M/month |

Quarterly and annual:

| Period | Cost range |
| --- | ---: |
| Quarterly | $2.85M-$13.773M |
| Annual | $11.4M-$55.092M |

### Stage 5 - Enterprise scale

Target:

```text
100,000 users or enterprise/family-office platform scale
```

Sustainable personnel:

| Function | Headcount | Monthly cost |
| --- | ---: | ---: |
| Executive leadership | 8-15 | $180,000-$500,000 |
| Product/design | 10-25 | $100,000-$625,000 |
| Engineering | 50-120 | $750,000-$3.36M |
| AI/data/research | 20-60 | $300,000-$2.1M |
| Security/compliance/devops | 15-40 | $225,000-$1.4M |
| Support/success | 40-100 | $200,000-$1.2M |
| Sales/account management | 25-75 | $200,000-$1.5M |
| Finance/accounting/legal ops | 10-30 | $100,000-$900,000 |
| QA/release/product operations | 10-30 | $70,000-$540,000 |
| Outside professional services | Retainer/project average | $250,000-$800,000 |
| Total personnel/pro services | 188-495 | $2.375M-$12.925M/month |

Quarterly and annual:

| Period | Cost range |
| --- | ---: |
| Quarterly | $7.125M-$38.775M |
| Annual | $28.5M-$155.1M |

## Professional services brought in-house

### In-house conversion summary

| Function | Outsourced monthly range | In-house monthly range | When in-house becomes realistic |
| --- | ---: | ---: | --- |
| Legal | $1K-$25K | $20K-$45K per counsel | Consistent legal spend above $20K-$40K/month |
| Compliance | $1K-$25K | $15K-$35K per lead | Regulated workflows, enterprise contracts, or recurring review burden |
| Finance/controller | $300-$12K | $8K-$20K per person | Recurring revenue, audits, investor reporting, or complex billing |
| Security/DevOps | $2.5K-$25K | $15K-$35K per engineer | Live user data, integrations, uptime requirements |
| Engineering | $2.5K-$35K | $12K-$28K per engineer | Continuous product roadmap and support burden |
| Customer support | $500-$5K | $5K-$12K per person | Daily customer volume and service-level expectations |

### Example: professional services remain outsourced

Paid MVP monthly cost:

```text
Founder + 1-2 engineers + contractor support + outside legal/CPA/security
Estimated personnel/pro services: $35K-$116K/month
Quarterly: $105K-$348K
Annual: $420K-$1.392M
```

### Example: professional services brought in-house early

If the MVP adds in-house legal, compliance, finance, and security too early:

| Added in-house role | Monthly cost |
| --- | ---: |
| In-house counsel | $20K-$45K |
| Compliance lead | $15K-$35K |
| Finance/controller | $8K-$20K |
| Security/DevOps engineer | $15K-$35K |
| Additional monthly cost | $58K-$135K |

Revised paid MVP personnel/pro services:

```text
$93K-$251K/month
Quarterly: $279K-$753K
Annual: $1.116M-$3.012M
```

Interpretation:

```text
Bringing professional services in-house too early can double or triple MVP personnel cost. It is usually better to outsource until workload is recurring, specialized, and high volume.
```

## Comparison with overall platform expenditures

This table combines:

- Platform operating costs from `docs/ESTIMATED_PLATFORM_COSTS.md`
- Personnel/professional services from this document
- Excludes customer acquisition cost, taxes, interest, depreciation, amortization, and one-time build cost

| Stage | Platform ops monthly | Personnel/pro services monthly | Total monthly expenditure | Quarterly total | Annual total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Prototype | $100-$750 | $4.3K-$44.5K | $4.4K-$45.25K | $13.2K-$135.75K | $52.8K-$543K |
| Paid MVP | $2.5K-$12K | $35K-$116K | $37.5K-$128K | $112.5K-$384K | $450K-$1.536M |
| Growth | $25K-$125K | $274K-$1.315M | $299K-$1.44M | $897K-$4.32M | $3.588M-$17.28M |
| Scale | $150K-$650K | $950K-$4.591M | $1.1M-$5.241M | $3.3M-$15.723M | $13.2M-$62.892M |
| Enterprise scale | $400K-$1.5M | $2.375M-$12.925M | $2.775M-$14.425M | $8.325M-$43.275M | $33.3M-$173.1M |

## Quarterly staffing ramp example for paid MVP

Assumption:

```text
Founder-led start, then contractor and employee support added as revenue and customer volume grow.
```

| Quarter | Staffing model | Personnel/pro services | Platform ops | Total quarterly expenditure |
| --- | --- | ---: | ---: | ---: |
| Q1 | Founder + legal setup + contractor engineering | $75K-$250K | $7.5K-$36K | $82.5K-$286K |
| Q2 | Founder + engineer + support contractor + CPA/legal | $105K-$300K | $7.5K-$36K | $112.5K-$336K |
| Q3 | Founder + 1-2 engineers + support + security/devops | $150K-$450K | $7.5K-$36K | $157.5K-$486K |
| Q4 | Lean MVP team + recurring legal/compliance | $180K-$550K | $7.5K-$36K | $187.5K-$586K |
| First-year total |  | $510K-$1.55M | $30K-$144K | $540K-$1.694M |

## Quarterly staffing ramp example for growth stage

| Quarter | Staffing model | Personnel/pro services | Platform ops | Total quarterly expenditure |
| --- | --- | ---: | ---: | ---: |
| Q1 | 20-25 person team | $822K-$1.5M | $75K-$375K | $897K-$1.875M |
| Q2 | 25-32 person team | $1.0M-$2.2M | $75K-$375K | $1.075M-$2.575M |
| Q3 | 32-40 person team | $1.5M-$3.0M | $75K-$375K | $1.575M-$3.375M |
| Q4 | 40-51 person team | $2.0M-$3.945M | $75K-$375K | $2.075M-$4.32M |
| Annual total |  | $5.322M-$10.645M | $300K-$1.5M | $5.622M-$12.145M |

## Quarterly staffing ramp example for scale stage

| Quarter | Staffing model | Personnel/pro services | Platform ops | Total quarterly expenditure |
| --- | --- | ---: | ---: | ---: |
| Q1 | 75-90 person team | $2.85M-$5.0M | $450K-$1.95M | $3.3M-$6.95M |
| Q2 | 90-115 person team | $3.5M-$7.5M | $450K-$1.95M | $3.95M-$9.45M |
| Q3 | 115-140 person team | $5.0M-$10.5M | $450K-$1.95M | $5.45M-$12.45M |
| Q4 | 140-177 person team | $6.5M-$13.773M | $450K-$1.95M | $6.95M-$15.723M |
| Annual total |  | $17.85M-$36.773M | $1.8M-$7.8M | $19.65M-$44.573M |

## Impact on EBITDA planning

Compared with platform-only EBITDA, realistic compensation and professional services reduce early-stage EBITDA substantially.

Key implications:

- Prototype and controlled beta can be operated lean, but only with limited risk and limited user volume.
- Paid MVP may be close to break-even or negative if hiring and legal costs arrive before recurring revenue.
- Professional and enterprise revenue materially improves ability to support staffing.
- Bringing legal/compliance/security in-house before recurring workload exists can materially reduce EBITDA.
- Growth and scale can support strong EBITDA if revenue grows faster than headcount.

## Recommended staffing budget guardrails

| Stage | Recommended personnel/pro services cap |
| --- | ---: |
| Controlled beta | $5K-$20K/month excluding founder salary |
| Paid MVP before $50K MRR | $25K-$60K/month |
| Paid MVP at $50K-$150K MRR | $35K-$116K/month |
| Growth at $500K+ MRR | Keep total personnel/pro services below 40%-55% of revenue |
| Scale at $3M+ MRR | Keep total personnel/pro services below 25%-45% of revenue |

## Recommended decision before hiring

Before converting outside professional services to in-house roles, define:

- [ ] Is the workload recurring every week?
- [ ] Is outside professional spend consistently above in-house cost?
- [ ] Does the role reduce legal, compliance, uptime, or customer risk?
- [ ] Does the role directly accelerate revenue or retention?
- [ ] Can the platform afford at least 6-12 months of loaded compensation?
- [ ] Would a fractional role solve the need at lower risk?

## Practical near-term recommendation

For John Henry Investments, the most sustainable near-term model is:

```text
Founder/operator + contractor engineering + outside legal/compliance + CPA/bookkeeper + fractional security/devops.
```

Do not bring all professional services in-house until:

```text
The platform has recurring revenue, live customer support volume, live integrations, and ongoing legal/compliance workload.
```

Suggested first-year paid MVP staffing budget:

```text
$540K-$1.694M total including platform operations, excluding customer acquisition and one-time product build cost.
```

Suggested first-year professional/legal/security setup reserve:

```text
$50K-$200K
```

Suggested one-person beta budget:

```text
$5K-$20K/month excluding founder salary, with strict usage and risk limits.
```
