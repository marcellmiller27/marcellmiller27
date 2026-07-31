# Aegira — Build Queue (living backlog)

**JHI-SIG:** `69M2705M` · Product = **Aegira** · Publisher = **JHI Research & Analytics Firm, Inc.**
Working process (2026‑07‑31): we **batch related builds** and **hold** until the Founder says
"execute the batch." Locked decisions are recorded in the board minutes. **Corrections to an
in‑scope item (bug/integration/review fixes, merge‑conflict resolution, the activating container
rebuild, green‑CI) are part of that same build; only NEW scope becomes a new queue item.**

Status key: 🟢 built (PR open) · 🔵 queued (spec ready) · 🟣 queued (needs a Founder decision) ·
⏳ blocked on a Founder/AWS dependency · ✅ done/live on `main`.

---

## A. Built — pending merge / activation
- 🟢 **#142 — Salvage deliverables** (5‑Yr projections, prepaid‑MSA, Company Book, DD audit + board minutes 07‑03). *Merge → then close #83/#82/#79/#35.*
- 🟢 **#143 — Discovery‑driven equity Opportunity Scan** (data finds → Ellery writes, fact‑locked; free SEC EDGAR). *Merge → rebuild containers to activate.*
- 🔵 **Container rebuild off `main`** — activates all merged work (Aegira brand, Home story + team, editorial, Opportunity Scan, SES code). *Run from a shell carrying Secrets (see AGENTS.md).*

## B. Newsletter depth (Founder vision, 2026‑07‑31)
- 🔵 **Phase 1 — prose depth (no new AWS):** expand the deterministic **analytical‑facts** layer (trend, level‑vs‑history, vs‑target/threshold, cross‑links like real rates = 10Y − CPI) and restructure the edition into an analytical arc — **executive thesis → analytical sections → cross‑asset implications → forward watch** (~600–900 words). Ellery writes the deep analysis, **fact‑locked**, interpretation‑not‑forecast.
- ⏳ **Phase 2 — depth multipliers (needs AWS):** **Bedrock Knowledge Bases / RAG** over a historical macro corpus (S3) for grounded "keen insight from history"; **charts/visual layer** (QuickSight or server‑rendered → S3); **Bedrock Agents** to orchestrate research → compute → retrieve → draft.

## C. Pricing / access (decisions LOCKED)
- 🔵 **Pricing page mechanics:** Monthly/Annual **toggle** — annual shows discounted /mo **+** annual total; monthly shows /mo. Needs annual prices for Professional & Enterprise (Consumer = $99/mo · $1,188/yr).
- 🔵 **7‑day trial (card required, auto‑converts)** with transparent disclosure + pre‑charge reminder + one‑click cancel. **Stripe SaaS‑subscriptions architecture:** hosted Checkout + Subscriptions + `trial_period_days` + Customer Portal + webhooks. *(Live charge = Purchase Flow Phase B; needs Stripe account/keys.)*
- ✅ **No free user accounts (decided).** Funnel = **anonymous limited browse** + **free newsletter email list**; an account exists only for paid/trial.
- 🟣 **Open‑browse shift:** login‑wall → anonymous **limited browse + upgrade gates**. Needs Founder's "limited‑view depth" instinct (structure+taste vs a few real results then gate); backend must serve safe sample data to anonymous.
- 🔵 **Purchase Flow — Phase A** (radio tiers → mock checkout → success) → **Phase B** live Stripe.

## D. Newsletter distribution (free list)
- ⏳ **Free‑subscriber email list + auto‑broadcast + limited‑edition variant + live SES.** Email‑capture (no account, double opt‑in) → stored list → SES broadcast of the limited edition (+ unsubscribe/CAN‑SPAM). Gated on SES sender‑domain validation.

## E. Platform UX
- 🔵 **Current User Setting (gear):** **Language** dropdown (browser default → English; full i18n added incrementally) + **Visual Mode (beta):** Browser Default / Light / Dark (dark palette on our CSS tokens).
- 🔵 **AI headshots:** regenerate Cy & Ellery (esp. Ellery).
- 🟣 **Pending titles:** finalize "Insider Briefs (Coming soon)" + the mobile "command center" wording.
- 🟣 **Storefront copy rewrite** (institutional voice) — needs Founder voice/scope.

## F. Data / research depth
- ✅ **FRED, SEC EDGAR, BLS — live** (free, redistributable government data).
- 🔵 **Prioritize SEC/EDGAR for fundamentals** to reduce paid‑Sharadar reliance.
- 🟣 **Cross‑Asset Valuation & Action Engine — Phase 1:** equity **DCF + IRR** in the Excel workbook + AI enter/sideline write‑up. Needs decisions (thresholds, US‑only/EDGAR, workbook‑vs‑screen).
- 🔵 **Wire "Generate report preview"** to the render/PDF engine — needs report→output mapping.
- ⏳ Optional keys: `BLS_API_KEY` (v2 limits), TwelveData, NASDAQ/Sharadar (Founder emailing NASDAQ 2026‑08‑03).

## G. Reliability / launch hardening
- 🔵 **Green CI** — fix the 10 pre‑existing accounting tests (staff‑auth).
- 🔵 **Prod hardening** — `APP_ENV=production`, dedicated `APP_ENCRYPTION_KEY`, rate limiting on.
- ⏳ **EDGAR User‑Agent swap** → `@aegiraenterprise.com` contact (on domain validation; using johnhenrycapital meanwhile).
- ⏳ **AWS Tier‑1 infra:** SES go‑live (verified domain), CloudFront+S3 (CDN), RDS (managed Postgres — app already reads `DATABASE_URL`). Needs deploy target + AWS creds + DNS.

## Founder external dependencies (unblock the above)
- 🔴 **Bank account** · 🔴 **DBA "Aegira"** · **register `aegiraenterprise.ai/.io/.dev/.app`** (script #141) · **AWS deploy creds + deploy target + DNS/SES validation** (Google↔AWS pending) · **Stripe account + keys/price IDs** (after bank) · optional data keys.
