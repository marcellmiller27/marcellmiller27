# Outsourcing Plan — Phase 1 Prototype & Paid MVP (Specialized Fintech SaaS Partner)

Objective: use a SaaS company/agency that **specializes in financial‑markets /
economics products** to build and deploy the **Phase 1 prototype** and **paid MVP**,
and to drive **user conversion** toward the company's revenue objectives — while
staying lean (see `docs/OPERATING_COST_LEAN_VS_STAFFED.md` and
`docs/CASHFLOW_PROJECTION_12MO.md`).

## 1. Why outsource (and what to keep in‑house)

| Outsource (speed + specialist skill) | Keep in‑house (control + IP) |
| --- | --- |
| Prototype/MVP build & deployment (front end, APIs, infra) | Product vision, roadmap, brand/mission |
| Market‑data & fundamentals integrations | Architecture decisions & data ownership |
| Growth/conversion (paid, lifecycle, CRO) | Pricing, customer relationships, compliance sign‑off |
| AI customer‑service tuning | Security/regulatory accountability |

Outsourcing buys **time‑to‑market and domain expertise** without a full payroll;
in‑house retention of vision, IP, and compliance protects long‑term value.

## 2. Ideal partner profile (vet against this)

- **Domain:** proven **fintech / capital‑markets / investing SaaS** track record
  (not a generic dev shop) — understands market data, brokerage/portfolio,
  KYC/AML, and investor UX.
- **Security/compliance:** SOC 2 Type II, secure SDLC, willingness to sign DPA/NDA;
  experience with PII and financial data.
- **Full‑stack delivery:** React/Next.js + Python/FastAPI (matches our stack),
  cloud (AWS), CI/CD, observability.
- **Growth capability** (or a paired partner): performance marketing, conversion‑rate
  optimization (CRO), lifecycle/email, analytics.
- **Commercials:** IP assignment to us, source‑in‑our‑repos, documented handover.

## 3. Scope of work

**Phase 1 — Prototype (validate + demo):** polish the existing prototype, wire live
data, instrument analytics, ship a public landing + waitlist. *Target: 4–8 weeks.*

**Paid MVP — Deploy (monetize):** production hosting + reliability, Stripe billing
live, auth/2FA/biometric hardening, AI support agent (LLM tier), onboarding funnel,
and the conversion stack (landing → trial → paid). *Target: 8–16 weeks.*

**Conversion (ongoing):** acquisition + activation + paid‑conversion + retention
loops, tied to revenue targets (Section 6).

## 4. Engagement models & indicative cost

| Model | What it is | Indicative cost | Best for |
| --- | --- | --- | --- |
| **Fixed‑bid project** | Defined prototype/MVP scope, milestone payments | Prototype ~$30k–80k; MVP ~$80k–250k | Clear scope, capped budget |
| **Dedicated squad (staff‑aug)** | 2–4 engineers + PM/designer, monthly | Nearshore ~$18k–45k/mo; US specialist ~$60k–150k/mo | Evolving scope, speed |
| **Growth/CRO retainer** | Fintech growth agency | ~$5k–25k/mo + ad spend | Conversion to revenue |
| **Performance / rev‑share** | Pay per converted user or % of revenue | variable | Aligning incentives, low fixed cost |

**Lean‑aligned recommendation:** a **nearshore specialized squad** for the build
(fixed‑bid for the prototype to cap risk, then a small dedicated squad for the MVP)
**+ a fintech growth partner on a performance basis** for conversion. This keeps fixed
cash low and ties spend to outcomes — consistent with the lean operating model.

## 5. Cost fit vs the lean budget

Build is a **one‑time/【ramp】 capex**; the lean **operating** cost (~$1.6k–3.6k/mo from
the cost analysis) is unchanged by who builds it. Fund the build from the cash the
lean model preserves (~$220k+/yr vs staffed) and/or a seed allocation; avoid a fixed
in‑house dev+support payroll before product‑market fit.

## 6. Conversion strategy → revenue objectives

Map the partner's mandate to the cash‑flow targets (Base scenario):

- **Revenue objective (Base):** ~**1,010 paying users / ~$70k MRR (~$850k ARR run‑rate)
  by month 12**; Conservative ~$21k MRR; Optimistic ~$201k MRR.
- **Funnel math (illustrative, Base):** at a **3–5% visitor→paid** rate, ~1,000 paying
  users needs ~20k–35k qualified visitors over the year (or a trial funnel at ~25%
  trial→paid). The growth partner owns these conversion rates.
- **Unit‑economics guardrails:** ARPU $70/mo; target **LTV/CAC ≥ 3**. At ~18‑month
  lifetime, LTV ≈ $1,260 → **CAC ceiling ≈ $400–420**. Hold the partner to CAC and
  payback (<12 mo) targets, not vanity traffic.
- **Levers:** SEO/content (markets/economics authority), paid search/social, referral,
  lifecycle email, and CRO on pricing/onboarding; the AI assistant lifts activation
  and deflects support cost.

## 7. Risks & safeguards

| Risk | Safeguard |
| --- | --- |
| **IP leakage / ownership** | Written IP assignment; code in *our* repos/cloud accounts; NDA. |
| **Data security & regulation** | SOC 2 partner; DPA; least‑privilege access; no production secrets shared; compliance sign‑off in‑house. |
| **Vendor lock‑in** | Standard stack (Next.js/FastAPI/AWS), documentation + handover, no proprietary black boxes. |
| **Quality / drift** | Milestone acceptance, code review, test coverage gates, our architect oversight. |
| **Misaligned growth spend** | Performance‑based terms; CAC/LTV and payback KPIs; monthly review. |
| **Knowledge loss at exit** | Runbooks, recorded handover, a transition clause. |

## 8. KPIs to hold the partner accountable

- **Delivery:** milestones on time; uptime ≥ 99.9%; test coverage; security review passed.
- **Activation:** signup→activated rate; time‑to‑first‑value.
- **Conversion:** visitor→paid (or trial→paid); CAC; LTV/CAC ≥ 3; payback < 12 mo.
- **Revenue:** MRR vs the scenario targets; net revenue retention.
- **Support quality (AI‑first):** first‑response time, deflection rate, CSAT, escalation rate < 15–20%.

## 9. Recommendation

1. **Outsource the build** to a specialized fintech SaaS squad — fixed‑bid prototype
   to cap risk, then a small dedicated squad for the paid MVP — with IP assigned to us
   and code in our accounts.
2. **Engage a fintech growth partner on performance terms** for conversion, governed
   by the CAC/LTV and MRR KPIs above.
3. **Keep vision, pricing, data ownership, compliance, and customer relationships
   in‑house;** run support AI‑first (already built) with a fractional human.
4. **Fund the build from preserved lean cash / seed;** do not add fixed dev+support
   payroll before product‑market fit. Re‑forecast monthly against
   `docs/CASHFLOW_PROJECTION_12MO.md`.
