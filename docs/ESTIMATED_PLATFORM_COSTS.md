# John Henry Investments Estimated Platform Costs

## Purpose

This document estimates monthly and annual costs for the John Henry Investments platform based on the current product scope, backend services, integration requirements, and capacity plan.

These are planning ranges, not vendor quotes. Actual costs depend on selected providers, negotiated contracts, user behavior, AI usage, document volume, data retention rules, compliance requirements, and support expectations.

Projected EBITDA scenarios based on these cost ranges are documented in `docs/PROJECTED_EBITDA_MODEL.md`.

Realistic staffing, one-person operation limits, legal expenditures, compliance costs, and staffing-adjusted EBITDA are documented in `docs/STAFFING_LEGAL_PRO_FORMA.md`.

Per-person compensation assumptions, outsourced versus in-house professional-services comparisons, and quarterly/annual staffing projections are documented in `docs/COMPENSATION_AND_PRO_SERVICES_PROJECTIONS.md`.

## Cost tiers

| Tier | Users | Description |
| --- | ---: | --- |
| Prototype | 100 | Internal testing and demos |
| Paid MVP | 1,000 | First production customers |
| Growth | 10,000 | Active B2C/B2B platform |
| Scale | 50,000 | Large subscription network |
| Enterprise scale | 100,000 | Major financial technology platform |

## Executive cost summary

Estimated operating cost ranges:

| Tier | Estimated monthly cost | Estimated annual cost |
| --- | ---: | ---: |
| Prototype | $100-$750/month | $1,200-$9,000/year |
| Paid MVP | $2,500-$12,000/month | $30,000-$144,000/year |
| Growth | $25,000-$125,000/month | $300,000-$1.5M/year |
| Scale | $150,000-$650,000/month | $1.8M-$7.8M/year |
| Enterprise scale | $400,000-$1.5M+/month | $4.8M-$18M+/year |

Primary cost drivers:

- AI usage
- Document storage and processing
- Database scale
- Background workers
- Banking/vendor integrations
- Compliance and security tooling
- Support and operations
- Enterprise reporting and file generation

## Prototype cost estimate

Target:

```text
100 users, demos, internal testing, no regulated production data
```

| Category | Estimated monthly cost |
| --- | ---: |
| Front-end hosting | $0-$50 |
| Backend API hosting | $20-$100 |
| Development database | $0-$50 |
| Object storage | $0-$25 |
| AI API usage | $25-$250 |
| Email/domain/basic tools | $10-$50 |
| Monitoring/logging | $0-$50 |
| Payment processor fixed costs | $0-$50 |
| Miscellaneous buffers | $25-$125 |
| Total | $100-$750/month |

Recommended setup:

- Vercel free/pro starter tier
- Small FastAPI container/app service
- SQLite for local development or small managed PostgreSQL
- Low AI quota
- No live bank/vendor integrations

## Paid MVP cost estimate

Target:

```text
1,000 users, first paid customers, 1-2 TB storage, 100 GB database
```

| Category | Estimated monthly cost |
| --- | ---: |
| Front-end hosting/CDN | $50-$500 |
| Backend API compute | $150-$800 |
| Background workers | $100-$700 |
| Managed PostgreSQL | $100-$700 |
| Object storage, 1-2 TB | $25-$150 |
| Backup storage | $25-$150 |
| Redis/cache | $30-$250 |
| AI API usage | $500-$5,000 |
| Email delivery | $20-$200 |
| Stripe/payment processing platform costs | $0-$100 fixed plus transaction fees |
| Monitoring/logging/error tracking | $50-$500 |
| Security tooling | $50-$500 |
| Banking/vendor integration sandbox or starter plans | $0-$1,000 |
| Microsoft/Office integration costs | $0-$300 |
| Miscellaneous buffers | $300-$1,250 |
| Total before payment processing variable fees | $2,500-$12,000/month |

Payment processing variable fees:

```text
Often around 2.9% + $0.30 per card transaction in standard US card pricing, but verify current Stripe terms and negotiated rates.
```

If MVP reaches $50,000/month in subscription revenue:

```text
Estimated card fees may be roughly $1,500-$2,000/month before chargebacks, taxes, and international fees.
```

## Growth cost estimate

Target:

```text
10,000 users, 12-24 TB object storage, 500 GB-1 TB database
```

| Category | Estimated monthly cost |
| --- | ---: |
| Front-end hosting/CDN | $500-$3,000 |
| Backend API autoscaling | $2,000-$10,000 |
| Background worker pools | $2,000-$15,000 |
| Managed PostgreSQL | $1,000-$8,000 |
| Read replica/analytics replica | $500-$5,000 |
| Object storage, 12-24 TB | $300-$1,500 |
| Backup/archive storage | $300-$2,000 |
| Redis/cache | $500-$3,000 |
| AI API usage | $10,000-$60,000 |
| Document extraction/OCR | $1,000-$15,000 |
| Email/report delivery | $500-$3,000 |
| Monitoring/logging/security | $1,000-$8,000 |
| Banking/vendor provider fees | $1,000-$10,000 |
| Microsoft Graph/Office storage and licensing | $500-$5,000 |
| Payment processing fixed/variable platform costs | $500-$5,000 fixed plus card fees |
| Support, compliance, and operational tooling | $2,000-$15,000 |
| Miscellaneous buffers | $2,000-$10,000 |
| Total before payment processing variable fees | $25,000-$125,000/month |

Major warning:

```text
At this tier, AI and document processing can exceed infrastructure cost if usage is not limited by plan.
```

## Scale cost estimate

Target:

```text
50,000 users, 60 TB/year object storage growth, 2.5-5 TB database
```

| Category | Estimated monthly cost |
| --- | ---: |
| Front-end hosting/CDN/WAF | $3,000-$20,000 |
| Backend API autoscaling | $15,000-$75,000 |
| Background workers | $15,000-$100,000 |
| Managed PostgreSQL primary | $8,000-$35,000 |
| Read replicas and analytics systems | $5,000-$40,000 |
| Object storage and lifecycle storage | $1,500-$8,000 |
| Backup and retention storage | $2,000-$15,000 |
| Redis/cache cluster | $3,000-$15,000 |
| AI API usage | $50,000-$250,000 |
| Document extraction/OCR | $10,000-$75,000 |
| Report generation and email delivery | $5,000-$30,000 |
| Monitoring, logging, tracing, SIEM | $10,000-$60,000 |
| Banking/vendor integration provider fees | $10,000-$75,000 |
| Microsoft/Salesforce/enterprise integration fees | $5,000-$50,000 |
| Security/compliance tooling | $10,000-$75,000 |
| Support and operations tooling | $10,000-$75,000 |
| Miscellaneous buffers | $20,000-$100,000 |
| Total before payment processing variable fees | $150,000-$650,000/month |

## Enterprise-scale cost estimate

Target:

```text
100,000 users, 120 TB/year object storage growth, 5-10 TB transactional database plus analytics warehouse
```

| Category | Estimated monthly cost |
| --- | ---: |
| Front-end/CDN/WAF/multi-region delivery | $10,000-$75,000 |
| Backend API multi-region/autoscaling | $50,000-$250,000 |
| Background worker fleets | $50,000-$300,000 |
| Transactional databases | $25,000-$150,000 |
| Analytics warehouse/data lake | $25,000-$200,000 |
| Object storage/archive/backup | $10,000-$75,000 |
| Redis/cache clusters | $10,000-$50,000 |
| AI API usage | $150,000-$700,000+ |
| Document extraction/OCR/AI diligence | $25,000-$250,000 |
| Report generation/email/distribution | $15,000-$100,000 |
| Integration provider fees | $25,000-$200,000 |
| Microsoft/Salesforce/enterprise systems | $10,000-$150,000 |
| Monitoring/logging/SIEM/security | $50,000-$250,000 |
| Compliance, audit, GRC tooling | $25,000-$200,000 |
| Support, operations, customer success tools | $50,000-$250,000 |
| Miscellaneous buffers | $50,000-$250,000 |
| Total before payment processing variable fees | $400,000-$1.5M+/month |

## Payment processing cost estimates

Payment processing depends on subscription revenue, card mix, country, chargebacks, taxes, and negotiated rates.

Planning formula:

```text
Monthly payment processing cost = monthly card revenue * 2.9% + transaction_count * $0.30
```

Example scenarios:

| Monthly subscription revenue | Approximate card fees |
| ---: | ---: |
| $50,000/month | $1,500-$2,000/month |
| $250,000/month | $7,500-$9,000/month |
| $1,000,000/month | $29,000-$35,000/month |
| $5,000,000/month | $145,000-$175,000/month |
| $10,000,000/month | $290,000-$350,000/month |

Revenue examples from the product plan:

| Plan scenario | Revenue | Estimated card fees |
| --- | ---: | ---: |
| 1,000 Consumer users at $50/month | $50,000/month | $1,500-$2,000/month |
| 5,000 Professional users at $299/month | $1.495M/month | $43,000-$55,000/month |
| 500 Enterprise users at $1,500/month | $750,000/month | $21,750-$27,000/month |

Enterprise invoicing can reduce card fees if customers pay by ACH or wire.

## AI cost estimates

AI cost depends heavily on model choice, prompt size, output size, document analysis, caching, and usage quotas.

Planning range:

| Tier | Estimated monthly AI cost |
| --- | ---: |
| Prototype | $25-$250 |
| Paid MVP | $500-$5,000 |
| Growth | $10,000-$60,000 |
| Scale | $50,000-$250,000 |
| Enterprise scale | $150,000-$700,000+ |

Cost-control recommendations:

- Set plan-based AI request limits.
- Cache common macro and market intelligence answers.
- Use cheaper models for classification and summaries.
- Use premium models only for high-value research.
- Use async jobs for due diligence document analysis.
- Require user confirmation before large AI jobs.
- Track token usage by organization.

## Integration provider cost estimates

Planning ranges:

| Integration type | Prototype | MVP | Growth | Scale |
| --- | ---: | ---: | ---: | ---: |
| Plaid/MX banking | $0-$250 | $250-$2,500 | $2,500-$25,000 | $25,000-$100,000+ |
| QuickBooks/NetSuite/Bill.com | $0-$250 | $250-$2,500 | $2,500-$25,000 | $25,000-$100,000+ |
| Microsoft Graph/Office | $0-$100 | $100-$1,000 | $1,000-$10,000 | $10,000-$50,000+ |
| Salesforce sync | $0-$250 | $250-$2,500 | $2,500-$25,000 | $25,000-$100,000+ |

Notes:

- Many providers require commercial approval before production access.
- Banking data costs may depend on connected accounts, transactions, and refresh frequency.
- NetSuite/Salesforce costs can include customer-owned license costs plus platform integration costs.
- Provider contracts can materially change the range.

## Compliance, legal, and security cost estimates

These are business operating costs rather than pure cloud infrastructure, but they are necessary for a financial platform.

| Category | Prototype | MVP | Growth | Scale/Enterprise |
| --- | ---: | ---: | ---: | ---: |
| Legal review | $1,500-$10,000 one-time | $10,000-$50,000 | $50,000-$250,000/year | $250,000+/year |
| Privacy/terms/compliance docs | $1,000-$7,500 | $5,000-$25,000 | $25,000-$100,000/year | $100,000+/year |
| Security audit / penetration test | $0-$5,000 | $5,000-$25,000 | $25,000-$100,000/year | $100,000+/year |
| SOC 2 / GRC readiness | $0 | $5,000-$30,000 | $30,000-$150,000/year | $150,000+/year |
| Cyber insurance | $0-$2,500/year | $2,500-$15,000/year | $15,000-$100,000/year | $100,000+/year |

## Software and SaaS tools cost estimates

| Tool category | MVP estimate | Growth estimate |
| --- | ---: | ---: |
| Error monitoring | $50-$500/month | $1,000-$10,000/month |
| Logging and observability | $50-$500/month | $1,000-$25,000/month |
| Email delivery | $20-$200/month | $500-$5,000/month |
| Customer support/helpdesk | $50-$500/month | $1,000-$15,000/month |
| Analytics/product tracking | $0-$500/month | $1,000-$15,000/month |
| Secret manager/KMS | $10-$250/month | $500-$10,000/month |
| CI/CD | $0-$250/month | $500-$5,000/month |
| Status page/incident tools | $0-$250/month | $500-$5,000/month |

## Development and engineering cost estimates

If hiring outside development resources, approximate implementation cost ranges:

| Workstream | Estimated implementation cost |
| --- | ---: |
| Production auth and role-based access | $10,000-$50,000 |
| PostgreSQL/Supabase persistence and migrations | $15,000-$75,000 |
| Stripe billing and webhooks | $10,000-$50,000 |
| Banking/vendor integrations | $25,000-$150,000+ |
| Microsoft Office export integration | $15,000-$75,000 |
| AI assistant backend | $25,000-$150,000+ |
| Opportunity Score engine v1 | $25,000-$150,000+ |
| Document upload and due diligence workflows | $25,000-$200,000+ |
| Admin dashboard | $15,000-$100,000 |
| CI/CD, monitoring, security hardening | $10,000-$75,000 |
| Full MVP from current prototype | $100,000-$500,000+ |

Internal engineering cost depends on staffing, compensation, and speed of execution.

## MVP budget recommendation

For a credible first paid release:

```text
Cloud and SaaS operating budget: $2,500-$12,000/month
Legal/compliance/security setup: $20,000-$100,000 one-time or first-year
Additional implementation budget: $100,000-$500,000+ if using paid engineering resources
Payment processing: variable, based on subscription revenue
```

Lean MVP option:

```text
$1,000-$3,000/month cloud/SaaS if AI usage, document uploads, integrations, and support are tightly limited.
```

Professional MVP option:

```text
$5,000-$15,000/month cloud/SaaS with production database, storage, monitoring, Stripe, limited AI, and initial integrations.
```

Enterprise-ready MVP option:

```text
$15,000-$50,000/month cloud/SaaS with stronger security, audit logging, integrations, higher storage, and compliance tooling.
```

## Break-even examples

### Consumer plan only

```text
100 subscribers at $50/month = $5,000/month revenue
500 subscribers at $50/month = $25,000/month revenue
1,000 subscribers at $50/month = $50,000/month revenue
```

If MVP operating costs are $5,000-$12,000/month, the platform may need roughly:

```text
100-240 Consumer subscribers to cover operating costs before labor, taxes, refunds, and payment fees.
```

### Professional plan

```text
50 subscribers at $299/month = $14,950/month revenue
100 subscribers at $299/month = $29,900/month revenue
500 subscribers at $299/month = $149,500/month revenue
```

Professional customers can cover MVP operating costs with fewer subscribers, but usually require stronger support, reporting, and compliance quality.

### Enterprise plan

```text
10 subscribers at $1,500/month = $15,000/month revenue
50 subscribers at $1,500/month = $75,000/month revenue
100 subscribers at $1,500/month = $150,000/month revenue
```

Enterprise users can cover infrastructure faster, but require higher security, onboarding, legal review, support, and integration reliability.

## Cost-control recommendations

- Start with one launch segment rather than all segments.
- Limit AI requests by plan.
- Limit document storage by plan.
- Use signed object-storage uploads.
- Archive old documents and reports.
- Use async workers for heavy jobs.
- Cache market data and AI responses.
- Keep enterprise integrations behind higher-tier plans.
- Prefer ACH/wire for enterprise billing where appropriate.
- Separate prototype/demo data from production financial data.
- Review cloud costs weekly during launch.

## Immediate cost decisions to define

- [ ] Monthly MVP infrastructure budget.
- [ ] Maximum acceptable AI cost per user.
- [ ] Storage limit per plan.
- [ ] Report generation limit per plan.
- [ ] Whether Enterprise customers pay by card, ACH, wire, or invoice.
- [ ] Whether document uploads are included or charged separately.
- [ ] Which integration providers are required for launch.
- [ ] Whether compliance/security audit is required before launch.
- [ ] Whether to prioritize Consumer, Professional, or Enterprise revenue first.

## Recommended first budget target

For the next programming and launch phase, plan around:

```text
$5,000-$15,000/month operating budget for a professional MVP
```

This should be enough to support:

- Production PostgreSQL/Supabase
- Object storage
- FastAPI backend hosting
- Vercel or similar frontend hosting
- Stripe billing
- Monitoring/logging
- Limited AI usage
- Limited document uploads
- Initial security tooling
- Early integration testing

For a very lean controlled beta, target:

```text
$1,000-$3,000/month
```

For enterprise-ready launch, target:

```text
$15,000-$50,000/month
```
