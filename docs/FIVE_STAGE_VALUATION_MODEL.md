# John Henry Investments Five-Stage Valuation Model

## Purpose

This document estimates company valuation for John Henry Investments across five realistic growth stages, including market-cap/equity-value ranges, enterprise-value logic, probability of reaching each stage, and probability-weighted outcomes.

This is a planning model only. It is not valuation advice, investment advice, accounting advice, legal advice, or a guarantee of future market value. Actual valuation will depend on revenue quality, churn, gross margin, growth rate, customer concentration, capital structure, legal/compliance status, investor demand, market conditions, and execution risk.

## Valuation terminology

For a private company:

```text
Enterprise value = value of operating business before cash and debt adjustments
Equity value / implied market cap = enterprise value - debt + cash
```

This document uses:

```text
Market cap = implied equity value
```

Planning simplification:

```text
Assume no material debt and neutral cash balance unless otherwise stated.
Therefore, enterprise value and implied market cap are treated as approximately equal.
```

## Five valuation stages

| Stage | Business state | Users | Approximate annual recurring revenue |
| --- | --- | ---: | ---: |
| Stage 1 | Prototype / concept validation | 100 beta users | $0-$250K |
| Stage 2 | Paid MVP / first revenue | 1,000 users | $1M-$2M |
| Stage 3 | Growth / repeatable SaaS | 10,000 users | $10M-$25M |
| Stage 4 | Scale / category contender | 50,000 users | $50M-$90M |
| Stage 5 | Enterprise-scale fintech platform | 100,000 users | $90M-$150M+ |

## Valuation methods used

This model triangulates valuation using:

1. ARR multiple method
2. EBITDA multiple method
3. DCF reference from the investor package
4. Stage probability weighting
5. Execution-risk adjustment

General SaaS planning ranges:

| Company quality | ARR multiple range |
| --- | ---: |
| Very early / pre-revenue | Not meaningful |
| Low-growth or high-risk SaaS | 2x-5x ARR |
| Healthy private SaaS | 5x-10x ARR |
| High-growth strategic SaaS | 10x-15x ARR |
| Exceptional category leader | 15x+ ARR |

EBITDA multiple planning ranges:

| Company profile | EBITDA multiple range |
| --- | ---: |
| Early, risky, low predictability | 5x-8x |
| Profitable niche SaaS | 8x-12x |
| High-quality recurring revenue SaaS | 12x-18x |
| Strategic platform / category leader | 18x-25x+ |

## Stage 1 - Prototype / concept validation

Description:

- Product prototype exists.
- Backend and front-end foundations exist.
- Documentation, investor package, financial model, and process maps exist.
- No meaningful recurring revenue yet.
- Legal/compliance position still needs confirmation.

Typical valuation logic:

- Based on assets created, founder execution, prototype quality, IP potential, and investor belief.
- Revenue multiples are not meaningful until revenue exists.

Estimated valuation range:

| Case | Implied market cap / equity value |
| --- | ---: |
| Conservative | $0-$250K |
| Base | $250K-$1.5M |
| Upside | $1.5M-$5M |

Probability of reaching this stage:

```text
Already substantially achieved from a planning/prototype standpoint.
```

Probability-weighted planning value:

```text
$250K-$1.5M
```

Key value drivers:

- Demonstrable prototype
- Complete technical/business documentation
- Investor package
- Clear module architecture
- Founder commitment

Key risks:

- No validated paying customers
- No live compliance review
- No production infrastructure
- No proven retention

## Stage 2 - Paid MVP / first revenue

Description:

- First production users.
- Authentication, database, billing, and core dashboard working.
- Stripe or equivalent billing live.
- Professional plan or enterprise pilots create recurring revenue.
- Legal disclaimers, privacy policy, and terms reviewed.

Assumption:

```text
ARR: $1M-$2M
```

Valuation range:

| Method | Conservative | Base | Upside |
| --- | ---: | ---: | ---: |
| ARR multiple | 3x ARR = $3M-$6M | 5x ARR = $5M-$10M | 8x ARR = $8M-$16M |
| Strategic early-stage premium | $2M-$5M | $5M-$12M | $12M-$20M |

Estimated market cap / equity value:

```text
$3M-$20M
```

Probability of reaching this stage from current state:

```text
35%-55%
```

Probability-weighted value:

```text
$1.1M-$11M
```

Key value drivers:

- Paying customers
- Subscription retention
- Compliance-safe positioning
- Working billing and database
- Clear professional customer value

Key risks:

- Payment conversion
- Legal/compliance uncertainty
- Customer support burden
- Need for real product usage

## Stage 3 - Growth / repeatable SaaS

Description:

- Repeatable acquisition of Consumer, Professional, and early Enterprise customers.
- AI assistant, opportunity score, reports, due diligence, CRM, and billing are usable.
- Initial integrations are live or in pilot.
- Customer feedback loop improves product.

Assumption:

```text
ARR: $10M-$25M
Adjusted EBITDA: $2M-$10M depending on staffing, AI usage, marketing, support, and compliance
```

Valuation range:

| Method | Conservative | Base | Upside |
| --- | ---: | ---: | ---: |
| ARR multiple | 4x = $40M-$100M | 7x = $70M-$175M | 10x = $100M-$250M |
| EBITDA multiple | 8x = $16M-$80M | 12x = $24M-$120M | 16x = $32M-$160M |

Estimated market cap / equity value:

```text
$40M-$200M
```

Probability of reaching this stage from current state:

```text
15%-30%
```

Probability-weighted value:

```text
$6M-$60M
```

Key value drivers:

- Repeatable sales motion
- Low churn
- Professional/enterprise revenue mix
- AI usage controlled by plan
- Early proprietary score data

Key risks:

- Churn
- CAC too high
- AI costs too high
- Compliance constraints
- Competitors copy generic features

## Stage 4 - Scale / category contender

Description:

- Large subscription network.
- Strong professional and enterprise revenue.
- Proprietary scoring and due diligence workflows mature.
- Integrations and reports become sticky.
- Platform becomes a workflow system, not just an information tool.

Assumption:

```text
ARR: $50M-$90M
Adjusted EBITDA: $20M-$50M depending on staffing and support intensity
```

Valuation range:

| Method | Conservative | Base | Upside |
| --- | ---: | ---: | ---: |
| ARR multiple | 6x = $300M-$540M | 10x = $500M-$900M | 15x = $750M-$1.35B |
| EBITDA multiple | 10x = $200M-$500M | 15x = $300M-$750M | 20x = $400M-$1.0B |

Estimated market cap / equity value:

```text
$300M-$1.0B+
```

Probability of reaching this stage from current state:

```text
5%-12%
```

Probability-weighted value:

```text
$15M-$120M
```

Key value drivers:

- Significant ARR
- High gross margin
- Strong retention
- Enterprise contracts
- Proprietary data moat
- Defensible score methodology

Key risks:

- Scaling support and compliance costs
- Regulatory complexity
- Enterprise customer concentration
- Security/data incident risk
- Market multiple compression

## Stage 5 - Enterprise-scale fintech platform

Description:

- 100,000+ users or equivalent high-ARPU enterprise network.
- AI due diligence engine, Opportunity Score, family office OS, and acquisition marketplace become category-defining.
- Platform has meaningful proprietary data and workflow lock-in.
- Strategic acquirer or public-market comparables may become relevant.

Assumption:

```text
ARR: $90M-$150M+
Adjusted EBITDA: $30M-$95M+ depending on staffing, compliance, AI, and sales costs
```

Valuation range:

| Method | Conservative | Base | Upside |
| --- | ---: | ---: | ---: |
| ARR multiple | 8x = $720M-$1.2B | 12x = $1.08B-$1.8B | 15x+ = $1.35B-$2.25B+ |
| EBITDA multiple | 12x = $360M-$1.14B | 18x = $540M-$1.71B | 25x = $750M-$2.375B |

Estimated market cap / equity value:

```text
$750M-$2.0B+
```

Probability of reaching this stage from current state:

```text
1%-5%
```

Probability-weighted value:

```text
$7.5M-$100M
```

Key value drivers:

- Proprietary data network
- Category leadership
- Enterprise adoption
- Acquisition marketplace
- High retention
- Strong EBITDA
- Strategic acquisition interest

Key risks:

- High execution difficulty
- Regulatory and legal exposure
- Enterprise-level security requirements
- Need for large team and capital
- Competitive pressure from incumbents
- Public/private market valuation cycles

## Probability-weighted valuation summary

This table uses broad probability ranges from current prototype state.

| Stage | Market cap / equity value range | Probability of reaching stage | Probability-weighted range |
| --- | ---: | ---: | ---: |
| Stage 1 - Prototype | $250K-$1.5M | 80%-100% | $200K-$1.5M |
| Stage 2 - Paid MVP | $3M-$20M | 35%-55% | $1.1M-$11M |
| Stage 3 - Growth | $40M-$200M | 15%-30% | $6M-$60M |
| Stage 4 - Scale | $300M-$1.0B+ | 5%-12% | $15M-$120M |
| Stage 5 - Enterprise scale | $750M-$2.0B+ | 1%-5% | $7.5M-$100M |

Important interpretation:

```text
Probability-weighted outcomes are not additive in a simple way because stages are sequential and dependent. They are best used to understand risk-adjusted potential, not to claim a present-day valuation.
```

## Realistic current valuation view

Current state:

- Prototype application exists.
- Backend and investor documents exist.
- No evidence of live paying customers in the repository.
- No production legal/compliance signoff yet.
- No live market validation metrics yet.

Realistic current planning valuation:

| Case | Current implied equity value |
| --- | ---: |
| Asset/documentation value only | $0-$250K |
| Founder/prototype seed value | $250K-$1.5M |
| Strong narrative/strategic seed case | $1.5M-$5M |

Recommended conservative planning range today:

```text
$250K-$1.5M pre-revenue planning value
```

Potential seed fundraising valuation, if investor believes in founder and market:

```text
$2M-$5M pre-money could be possible in a favorable seed environment, but requires investor appetite and credible execution plan.
```

## Valuation milestones required to move upward

### To justify $3M-$10M valuation

- Working production MVP.
- Legal disclaimers and privacy terms reviewed.
- Stripe billing live.
- First paying customers.
- Product demo with real workflows.
- Clear MVP roadmap and support plan.

### To justify $10M-$50M valuation

- $500K-$2M ARR.
- Low churn.
- Repeatable acquisition channel.
- Professional or enterprise users.
- Early evidence of product-market fit.
- Secure database and integration architecture.

### To justify $50M-$200M valuation

- $5M-$20M ARR.
- Strong retention.
- Enterprise contracts or high professional adoption.
- Proprietary scoring data.
- Demonstrated AI/diligence workflow value.
- Clear compliance controls.

### To justify $300M-$1B valuation

- $50M+ ARR or very high strategic value.
- High growth rate.
- Strong EBITDA or credible path to EBITDA.
- Defensible proprietary data moat.
- Large addressable market.
- Enterprise-grade security and compliance.

### To justify $1B+ valuation

- $90M+ ARR or equivalent strategic platform value.
- Category leadership.
- Strong retention and expansion.
- Large proprietary dataset.
- Enterprise and family office adoption.
- Strategic acquirer interest or IPO-quality metrics.

## Market cap sensitivity

| ARR | 4x ARR | 8x ARR | 12x ARR | 15x ARR |
| ---: | ---: | ---: | ---: | ---: |
| $1M | $4M | $8M | $12M | $15M |
| $5M | $20M | $40M | $60M | $75M |
| $10M | $40M | $80M | $120M | $150M |
| $25M | $100M | $200M | $300M | $375M |
| $50M | $200M | $400M | $600M | $750M |
| $90M | $360M | $720M | $1.08B | $1.35B |
| $150M | $600M | $1.2B | $1.8B | $2.25B |

## EBITDA multiple sensitivity

| EBITDA | 8x EBITDA | 12x EBITDA | 18x EBITDA | 25x EBITDA |
| ---: | ---: | ---: | ---: | ---: |
| $1M | $8M | $12M | $18M | $25M |
| $5M | $40M | $60M | $90M | $125M |
| $10M | $80M | $120M | $180M | $250M |
| $25M | $200M | $300M | $450M | $625M |
| $50M | $400M | $600M | $900M | $1.25B |
| $100M | $800M | $1.2B | $1.8B | $2.5B |

## Probability realism by stage

| Stage | Main blocker | Probability-improving evidence |
| --- | --- | --- |
| Prototype | Focus and execution | Completed product demo and clear roadmap |
| Paid MVP | Converting users to paid | First paying customers and low refund/churn |
| Growth | Repeatable acquisition | CAC/LTV proof and retention |
| Scale | Operational complexity | Enterprise contracts, security, compliance, team |
| Enterprise scale | Category leadership | Proprietary data, network effects, strategic demand |

## Recommended valuation position for investor discussions

Recommended framing:

```text
Do not lead with billion-dollar valuation claims. Lead with milestone-based valuation path.
```

Suggested language:

```text
John Henry Investments is currently a prototype-stage fintech platform concept with a built planning/demo foundation. The valuation path depends on achieving paid MVP revenue, validated retention, professional/enterprise adoption, compliance-safe workflows, and proprietary data from the Opportunity Score and due diligence engine.
```

Recommended investor-stage framing:

- Current stage: prototype / seed concept.
- Near-term target: paid MVP and first professional/enterprise customers.
- Medium-term target: $1M-$2M ARR.
- Growth target: $10M-$25M ARR.
- Long-term upside: $90M+ ARR and possible $720M-$1.35B+ enterprise value if category leadership is achieved.

## Next valuation action items

- [ ] Validate first paying customer segment.
- [ ] Define final pricing and plan limits.
- [ ] Obtain legal/compliance review.
- [ ] Build live MVP with billing.
- [ ] Track MRR, ARR, churn, CAC, LTV, gross margin, and AI cost per user.
- [ ] Create investor-ready cap table and raise terms.
- [ ] Add customer pipeline and pilot letters of intent.
- [ ] Update valuation after real revenue exists.
