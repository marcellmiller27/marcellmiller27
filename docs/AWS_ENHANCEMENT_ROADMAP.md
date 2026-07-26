# AWS Enhancement Roadmap — Toward a Superb Subscriber Experience

**Owner:** Cy Henry (VP Software Engineering — AI) · **Signature:** `69M2705M` · **Status:** roadmap for review
**Purpose:** Prioritized AWS services that make the JHI platform reliable, fast, secure, and delightful at
subscription scale — with clear subscriber benefit, rough effort, and dependencies. Everything stays
**in our AWS account** (aligns with the NASDAQ no-spillage governance story). Pairs with
`docs/PLATFORM_ARCHITECTURE_MAP.md`.

> Principle: adopt by **impact**, not novelty. Ship the reliability/delivery basics first; add
> intelligence and personalization second; harden security/analytics third. We don't need all of it.

---

## Already in use
- **Amazon Bedrock (Claude Sonnet 4.5)** — the AI editorial engine (Ellery), fact-locked, activated on-screen + PDF.

## 🥇 Tier 1 — Reliability & delivery (biggest, near-term UX wins)
| Service | What it does for subscribers | Effort | Depends on |
|---|---|---|---|
| **Amazon SES** | **Emails the newsletters** to inboxes (the "Step B" send) + transactional email (receipts, alerts) | S–M | verified sender **domain** (johnhenrycapital.com) |
| **EventBridge + Lambda** | **Auto-generates & sends** editions on a schedule — the AI writer runs itself, no manual step | M | SES, editorial engine |
| **CloudFront (CDN) + S3** | **Fast load anywhere** + scalable delivery of pages, PDFs, and downloads; holds up under load | M | deploy target |
| **RDS (managed Postgres)** | **Automatic backups + reliability** for the database; no data loss, minimal downtime | M | migrate from self-managed PG |

## 🥈 Tier 2 — Intelligence & differentiation (premium feel)
| Service | What it does for subscribers | Effort | Depends on |
|---|---|---|---|
| **Bedrock — expanded** | Smarter **Ask JHI** assistant; **document Q&A** over CIMs/filings (Bedrock **Knowledge Bases** / RAG); personalized digests | M–L | Bedrock (have), doc store (S3) |
| **Bedrock Guardrails** | Enforced safety/"not advice" + PII/spillage checks on any generated text | S | Bedrock |
| **Amazon OpenSearch** | Fast, relevant **search** across companies/filings/deals (snappy Screener & directory) | M | entity graph |

## 🥉 Tier 3 — Scale, security & institutional trust
| Service | What it does for subscribers | Effort | Depends on |
|---|---|---|---|
| **Amazon Cognito** | Managed **sign-in + MFA** that scales to a million users (or complements our JWT) | M | auth migration plan |
| **WAF + Shield** | **Protects the app** from attacks/bots (uptime + trust) | S–M | CloudFront |
| **KMS + Secrets Manager** | Encrypt data/secrets; **guarantee no data-set spillage** (NASDAQ credibility) | S–M | — |
| **GuardDuty / CloudTrail** | Threat detection + full audit trail (institutional diligence readiness) | S | — |
| **Kinesis/Firehose + QuickSight** | Engagement analytics → dashboards; know what subscribers value | M | event instrumentation |
| **Amazon Personalize** | **Recommends** the right opportunities/reports per subscriber | L | engagement data |

## Recommended first three (highest impact / lowest risk)
1. **SES** — subscribers actually *receive* the editions (turns owned-media into a real funnel).
2. **CloudFront + S3** — the whole product feels instant and holds up at scale.
3. **RDS** — the data is safe and always up.
*(These three alone make it feel like a polished, professional product to every subscriber.)*

## Sequencing notes
- Tier 1 pairs naturally with **launch** (SES needs the domain; hosting/CDN/RDS = the deploy footprint).
- Tier 2 is the **retention/differentiation** layer post-launch.
- Tier 3 rides alongside as scale + institutional sales require it.
- **Payments stay on Stripe** (AWS isn't a payment processor); AWS handles everything around it.

## Dependencies to confirm (Founder)
- **Deploy target** (ECS/Fargate, App Runner, or Amplify/Lightsail) — determines CloudFront/RDS wiring.
- **Domain DNS** pointed at the deploy target; **SES sender-domain** verification (or Google Workspace for send).
- Budget posture for managed services (all usage-based; start small).

*Next step on Founder go-ahead: pick the deploy target + the first three (SES/CloudFront-S3/RDS) and I'll produce the concrete setup plan + wiring.*
