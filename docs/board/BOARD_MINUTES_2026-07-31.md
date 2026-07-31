# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-07-31 · **Type:** Founder working session (product + process) · **Recorder:** Cy Henry (VP, Software Engineering — AI teammate)
**Present:** Founder (Galen Marcellus Miller).

> NOT legal/tax/accounting advice. Prior session: `docs/board/BOARD_MINUTES_2026-07-27.md`.
> Signature of record: `69M2705M`. Ethos: *How we do anything is how we do everything.*

---

## 1. Build process — batch + queue (DECIDED)
- We **batch related builds** and **hold** until the Founder says "execute the batch," maintaining a living **Build Queue** (`docs/BUILD_QUEUE.md`); locked decisions are recorded here.
- **Corrections are part of the build (process rule):** fixing an in‑scope item — bugs, integration, review/Bugbot feedback, merge‑conflict resolution, the activating container rebuild, green‑CI — is **the same build**, not a separate one. **Only NEW scope** becomes a new queue item. The line is *scope*, not *whether code changed*.

## 2. Pricing / access — LOCKED
- **No free user accounts.** Funnel = **anonymous limited browse** + **free newsletter email list** (no account); an account exists only for **paid / 7‑day trial**. Rationale: free accounts add hosting/support cost with weak conversion; the email list captures leads far more cheaply.
- **Pricing page:** Monthly/Annual **toggle** — annual shows discounted /mo **+** annual total; monthly shows /mo.
- **7‑day trial, card required, auto‑converts**, with transparent disclosure + pre‑charge reminder + one‑click cancel — honoring our "no auto‑renewal traps" promise. **Stripe architecture = SaaS subscriptions:** hosted Checkout + Subscriptions + `trial_period_days` + Customer Portal + webhooks (per Stripe's "Sell subscriptions as a SaaS startup" guide).
- **Open‑browse** (login‑wall → anonymous limited view + upgrade gates) is queued pending the Founder's "limited‑view depth" call.

## 3. Newsletter vision — depth (DECIDED; Phases 1 & 2 queued)
- Direction: from "summary + percentages" to a **detailed macro brief** — interpret the numbers, connect them, deliver the *"so what"* (executive thesis → analytical sections → cross‑asset implications → forward watch). Discipline holds: **data finds, Ellery writes, fact‑locked, interpretation‑not‑forecast.**
- **Phase 1 (no new AWS):** expand the deterministic analytical‑facts layer (trend, level‑vs‑history, vs‑target, cross‑links) + restructure + richer Bedrock prompt (~600–900 words).
- **Phase 2 (needs AWS):** **Bedrock Knowledge Bases/RAG** over a historical macro corpus (S3) for grounded insight; **charts/visual layer**; **Bedrock Agents** orchestration.
- **AWS mapping recorded:** Bedrock (deep writing, live), Knowledge Bases/RAG (historical grounding — the key insight unlock), Agents (orchestration), QuickSight/S3 (charts + corpus), SES + Lambda + EventBridge (deliver + auto‑generate).

## 4. Free government data — strategy (RECORDED)
- **SEC EDGAR, FRED, BLS, BEA, Treasury** are **free and public‑domain (freely redistributable)** — a margin + redistribution advantage vs. licensed vendors (Sharadar, Twelve Data, Bloomberg).
- **Live now:** **FRED** (macro — Fed Funds 3.63%, etc.), **SEC EDGAR** (company financials — verified on AAPL FY2025), **BLS** (CPI 3.53% YoY, keyless v1).
- **Decision:** prioritize **SEC/EDGAR for fundamentals** to reduce paid‑Sharadar reliance.

## 5. Delivered this session (on PRs)
- **#143 — Discovery‑driven equity Opportunity Scan:** value/quality/growth screen over large/mid‑cap US equities from free SEC EDGAR + prices → 0–100 Opportunity Score → **top 5**; the Scan's full edition gains a "Top equity opportunities" group (teaser gates it). Verified live: **V, CRM, ADBE, MSFT, ORCL**; Bedrock elevation fact‑locked (0 reverts).
- **#142 — Salvage** of the 5‑Yr projections, prepaid‑MSA workbook, Company Book, and the 2026‑07‑03 board minutes (Aegira filenames; JHI internals).

## 6. Domain / email status (RECORDED)
- `aegiraenterprise.com` DNS is **pending Google ↔ AWS validation**. Gated on it: the **EDGAR User‑Agent swap** (using `research@johnhenrycapital.com` meanwhile — fully functional) and **SES** newsletter email. Founder will signal when green.

## Decisions locked
Batch‑build process (+ corrections‑are‑part‑of‑build); no free accounts; pricing toggle + 7‑day Stripe trial; newsletter depth Phases 1 & 2; SEC/EDGAR‑first for fundamentals.

---

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | Bank account · DBA "Aegira" · register `aegiraenterprise.*` (script #141) | Founder | 🔴 |
| 2 | AWS: complete DNS validation → then EDGAR UA swap + SES go‑live | Founder → Cy | 🟡 |
| 3 | Stripe account + keys/price IDs (after bank); annual prices for Pro/Enterprise | Founder | 🟡 |
| 4 | Merge **#142** + **#143**; then rebuild containers to activate | Founder → Cy | 🟡 |
| 5 | On "execute the batch": build the queue (`docs/BUILD_QUEUE.md`) | Cy | 🟡 |

**Next review:** next working session.
**Recorded by:** Cy Henry · signature of record `69M2705M`.
