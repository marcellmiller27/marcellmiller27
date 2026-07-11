# AWS Hosting Cost — Provision for up to 10,000 Users (Initial Procurement)

Estimated AWS infrastructure cost to deploy and host the John Henry Investments
platform (Next.js frontend + FastAPI backend + Postgres + supporting services) for
**up to 10,000 registered users**. Same low / typical / high breakdown format as
`docs/OPERATING_COST_LEAN_VS_STAFFED.md`. Monthly USD, on‑demand pricing.

> Reality check: 10,000 users is **small** for AWS — this is a data/dashboard SaaS,
> not video/streaming. Costs scale sub‑linearly; the lean thesis holds.

## Sizing assumptions (for 10k users)

- ~10,000 registered users; ~1,000–3,000 monthly active; low‑hundreds concurrent at peak.
- Workload: API + SSR pages + Postgres reads/writes; market data is cached server‑side.
- Region: us‑east‑1. Reliability: **single‑AZ for MVP**, **Multi‑AZ for production**.
- No large upfront capex (AWS is pay‑as‑you‑go); "procurement" = monthly run‑rate, with
  a 1‑year Savings Plan to lock discounts once steady (see optimized view).

## Itemized monthly breakdown

| AWS service | Purpose | Low | Typical | High |
| --- | --- | ---: | ---: | ---: |
| **ECS Fargate — backend** | FastAPI API, 2–4 autoscaled tasks (~1 vCPU/2 GB) | $60 | $120 | $260 |
| **Frontend hosting** | Next.js SSR (Fargate) or Amplify; or S3+CF if static | $30 | $70 | $150 |
| **RDS PostgreSQL** | db.t4g.medium, gp3 50 GB (single‑AZ) | $70 | $110 | $180 |
| **Application Load Balancer** | ALB base + LCUs | $20 | $30 | $45 |
| **CloudFront (CDN)** | Asset + API egress (~200–400 GB) | $15 | $40 | $80 |
| **S3** | Static assets, documents, backups | $5 | $15 | $35 |
| **SES (email)** | Transactional + lifecycle (~50k–200k/mo) | $5 | $15 | $30 |
| **ElastiCache (Redis)** | Sessions / rate‑limit / data cache (t4g.small) | $0 | $35 | $60 |
| **CloudWatch** | Logs, metrics, dashboards, alarms | $15 | $40 | $80 |
| **Secrets Manager / SSM** | API keys, DB creds | $5 | $10 | $20 |
| **AWS WAF** | Web‑app firewall (recommended for fintech) | $0 | $30 | $60 |
| **NAT Gateway** | Egress from private subnets (1×) | $35 | $45 | $70 |
| **Route 53 + ECR + misc** | DNS, container registry, data | $10 | $15 | $30 |
| **Subtotal (single‑AZ)** | | **~$270** | **~$575** | **~$1,100** |

### Single‑AZ (MVP) vs Multi‑AZ (production)

| Posture | Monthly (typical) | Annual (typical) | What changes |
| --- | ---: | ---: | --- |
| **Single‑AZ (MVP)** | **~$575** | **~$6,900** | One AZ; fine to launch and validate |
| **Multi‑AZ (production)** | **~$950** | **~$11,400** | RDS Multi‑AZ (+~$110), 2× NAT, extra task headroom (+~$265) |

## Cost‑optimized view (1‑year Savings Plan / Reserved)

Committing a 1‑year **Compute Savings Plan** + **RDS Reserved Instance** (no upfront)
typically cuts compute + database **~30–40%**:

- Single‑AZ optimized: **~$400–450/mo** (~$5,000/yr).
- Multi‑AZ optimized: **~$650–700/mo** (~$8,000/yr).

Use **Graviton (t4g/Fargate ARM)** for ~20% better price/performance (already assumed).

## Not included (separate, non‑AWS)

These are external APIs/data, not AWS infrastructure:

- Market/fundamentals data: CoinGecko/Yahoo/BLS **$0**; optional Twelve Data/FRED;
  Sharadar fundamentals **~$120/mo**.
- LLM for AI agents (if upgraded from the free retrieval engine): **~$25–150/mo**.
- Stripe processing: ~2.9% + $0.30/txn (revenue‑proportional).

## What drives the bill (and levers to control it)

- **Biggest line items:** Fargate compute, RDS, NAT Gateway, CloudFront egress.
- **Levers:** ship the frontend as **static export on S3 + CloudFront** (drop SSR
  Fargate → saves ~$50–120/mo); **VPC endpoints** instead of NAT for AWS‑bound traffic;
  **single‑AZ** until production; **Savings Plan/Reserved** once steady; right‑size with
  CloudWatch + autoscaling; S3 lifecycle policies for backups.

## Bottom line

To host the platform for **up to 10,000 users**, budget roughly:

- **MVP launch (single‑AZ): ~$270–$1,100/mo, ~$575 typical (~$6.9k/yr).**
- **Production (Multi‑AZ): ~$950/mo typical (~$11.4k/yr).**
- **With a 1‑year Savings Plan: ~$400–700/mo.**

This stays well inside the lean operating envelope from
`docs/CASHFLOW_PROJECTION_12MO.md` — at 10k users the platform is comfortably
self‑funding, and AWS is a small fraction of revenue.
