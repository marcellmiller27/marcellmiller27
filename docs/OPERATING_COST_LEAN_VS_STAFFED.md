# Paid‑MVP Operating Cost Map — Lean (Cloud + AI) vs Hiring Personnel

Objective: a clear, precise expenditure map for running the **paid MVP** lean —
cloud hosting (AWS‑class) + AI agents for customer service/email — versus hiring
real personnel and office space, **without sacrificing outstanding customer service**.

> All figures are monthly USD estimates with low / typical / high ranges and explicit
> assumptions. They are planning estimates, not quotes; variable costs (Stripe %, LLM
> usage) scale with volume. Complements `docs/ESTIMATED_PLATFORM_COSTS.md` and
> `docs/PROJECTED_EBITDA_MODEL.md`.

## Stage assumption — "Paid MVP"

- Billing live (Stripe). **~300–3,000 paying users.**
- Support volume: **~300–1,500 tickets/month** (email/chat), bursty, needs 24/7 cover.
- Requirements: reliable hosting, real auth/security, fast support, room to scale.

---

## Option A — Lean (cloud + AI agents)

### A.1 Cloud hosting (AWS‑class), monthly

| Item | Low | Typical | High | Notes |
| --- | ---: | ---: | ---: | --- |
| Compute (Fargate/App Runner/EC2) | $40 | $120 | $300 | API + Next.js; 1–3 small containers |
| Database (RDS Postgres / Supabase Pro) | $25 | $75 | $200 | Managed Postgres + backups |
| Storage + CDN (S3 + CloudFront) | $10 | $30 | $80 | Static assets, documents |
| Email send (SES) | $5 | $15 | $40 | ~$0.10 / 1,000 emails |
| Load balancer + data transfer | $20 | $45 | $120 | ALB + egress |
| Monitoring/logging (CloudWatch/Sentry) | $0 | $30 | $90 | Errors, metrics, alerts |
| Backups / misc | $10 | $25 | $70 | Snapshots, secrets, DNS |
| **Cloud subtotal** | **$110** | **$340** | **$900** | |

### A.2 AI + data services, monthly

| Item | Low | Typical | High | Notes |
| --- | ---: | ---: | ---: | --- |
| AI support agent (LLM for email/chat) | $20 | $60 | $200 | See per‑ticket math below |
| Market data (CoinGecko/Yahoo free; vendor optional) | $0 | $0 | $80 | Twelve Data optional |
| Fundamentals (Sharadar SF1) — optional | $0 | $120 | $120 | Only if running research |
| Embeddings / misc AI | $0 | $20 | $60 | FAQ retrieval, summaries |
| **AI/data subtotal** | **$20** | **$200** | **$460** | |

### A.3 SaaS / tooling, monthly

| Item | Low | Typical | High |
| --- | ---: | ---: | ---: |
| Error tracking, uptime, analytics | $0 | $50 | $150 |
| Help‑desk inbox (shared) / domain / misc | $10 | $40 | $120 |
| **Tooling subtotal** | **$10** | **$90** | **$270** |

### A.4 Minimal human oversight

Founder or **1 fractional/part‑time** person for escalations: **$0–$2,000/mo**.

### Lean total (excluding Stripe %)

| | Low | Typical | High |
| --- | ---: | ---: | ---: |
| Infra + AI + tooling | ~$140 | ~$630 | ~$1,630 |
| + fractional human (optional) | $140 | ~$1,600 | ~$3,600 |

**Headline: a paid MVP can run lean for roughly $600–$1,600/mo** in infra+AI+tooling
(~$7k–$19k/yr), or ~$1,600–$3,600/mo with a part‑time human for escalations.
Stripe processing (~2.9% + $0.30/txn) is a separate, revenue‑proportional cost.

---

## Option B — Hiring personnel + office

| Item | Low | Typical | High | Notes |
| --- | ---: | ---: | ---: | --- |
| Support agent (fully loaded: salary+payroll+benefits) | $3,800 | $4,800 | $5,800 | per agent/mo (~$45k–70k/yr) |
| Agents needed for ~24/7 cover | ×2 | ×3 | ×4–5 | shifts/weekend coverage |
| **Support payroll** | **$7,600** | **$14,400** | **$29,000** | |
| Office rent | $1,500 | $3,000 | $5,000 | small office |
| Utilities / internet / insurance | $300 | $600 | $1,000 | |
| Equipment / seat software (amortized) | $200 | $400 | $800 | |
| HR / management overhead | $500 | $1,200 | $2,500 | |
| **Staffed total** | **~$10,100** | **~$19,600** | **~$38,300** | |

(Plus the **same cloud infra** from A.1 — humans don't replace hosting.)

---

## Side‑by‑side

| | Lean (AI‑first) | Staffed + office |
| --- | ---: | ---: |
| Monthly (typical) | **~$1,600** | **~$19,600** |
| Annual (typical) | **~$19k** | **~$235k** |
| 24/7 coverage | ✅ instant, native | ❌ needs shifts |
| Multilingual | ✅ built‑in | ❌ costly |
| **Cost per support ticket** | **~$0.02–$0.05** | **~$5–$7** |

**Per‑ticket math:** an LLM answer ≈ 1.5k in + 0.5k out tokens ≈ **$0.01–0.03**; even
1,500 tickets/mo ≈ **$25–60**. A fully‑loaded human (~$35/hr) handling ~6 tickets/hr ≈
**$5.80/ticket**. AI is roughly **150–300× cheaper per ticket** and answers in seconds,
24/7.

---

## Customer‑service quality — the real decision

Outstanding service is **not** "all humans" — it's *fast, accurate, always‑on, with a
human when it matters*. Pure‑AI risks frustration on complex, emotional, or
high‑value cases; pure‑human is slow and ~12–30× more expensive.

**Recommendation: AI‑first hybrid.**

1. **AI agent handles tier‑1 (24/7):** FAQs, account, billing basics, how‑to — this is
   already built (`/support` + `/api/v1/support/ask`). Upgrade it with an LLM tier for
   free‑form email replies (cost: ~$25–150/mo).
2. **One fractional/part‑time human (or founder)** owns escalations, complaints, and
   high‑value/enterprise relationships — the moments that need empathy.
3. **Safeguards that keep quality high:** confidence threshold with auto‑escalation
   (already in the assistant), human‑in‑the‑loop review of AI email drafts at first,
   clear "talk to a human" path, and SLA on escalations.

This keeps **excellent** service at **~$1.6k–3.6k/mo**, vs ~$20k+/mo for a staffed desk.

## When to add real personnel (scaling triggers)

Add humans when any holds:

- Sustained **> ~1,500–2,000 tickets/mo** that AI + 1 human can't cover within SLA.
- **Enterprise/Family‑Office** clients contractually require named, dedicated reps.
- Escalation rate stays **> ~15–20%** (signals AI gaps or product issues).
- Regulatory/advice interactions requiring **licensed** humans (compliance).

Add in this order: (1) fractional support → (2) first FT support hire (still remote,
no office) → (3) team + tooling → office **only** if a real reason exists (remote‑first
avoids the $2k–6k/mo office line entirely).

## What's already built that enables the lean path

- **AI customer‑service FAQ** (`/support`, `/api/v1/support/ask`) — confidence + auto
  escalation; deterministic today (free), LLM‑upgradeable.
- **Transactional email** is SES‑ready (cheap at MVP volume).
- **Stripe billing foundation**, auth/2FA/biometric, audit logs — no extra staff to run.

## Bottom line

For a paid MVP, **run lean: ~$1.6k–3.6k/mo all‑in** (AI‑first support + cloud), versus
**~$20k+/mo** for a staffed support desk + office — a **~10–15×** difference — while
delivering *faster, 24/7* service. Keep one human in the loop for escalations and
high‑value relationships, and hire ahead of the scaling triggers above, remote‑first.
