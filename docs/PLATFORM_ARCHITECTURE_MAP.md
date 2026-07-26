# JHI Platform — Architecture, Structure & Layout Map

**Owner:** Cy Henry (VP Software Engineering — AI) · **Signature:** `69M2705M` · **Status:** living map
**Purpose:** The clear mental model of *what the platform is* — two demand-sides on one shared spine,
connected by a differentiating loop — so structure, layout, and future build all sequence from it.

---

## 1. The one-line model
**Value anything, and know what to do about it.** JHI serves two jobs on one spine:
watch the **public markets** (research), and **acquire private businesses** (diligence) — with a
loop that turns market context into deal decisions.

## 2. The two pillars

### Pillar A — Markets & Research *(public world)*
*Job: understand the world, surface ideas, tell the story.*
- **Economics** (rates, inflation, growth, labor — FRED/BEA/BLS), **Market tickers** (equities, commodities, crypto, forex), **Screener**, **Reports**, **Newsletters** (Ellery Vance / Bedrock), **Ask JHI**.
- Data source: **live public feeds** (+ EDGAR for company fundamentals).

### Pillar B — Acquire & Diligence *(private world)*
*Job: buy a private business well.*
- **Scope** (Deal X-Ray — Business Quality Assessment + curbed-DCF cross-check) → **Earnings** (QoE — normalized/adjusted EBITDA) → **DCF** (full valuation) → **Document Review** → **Pipeline** → **Portfolio**.
- Data source: the target's **CIM / seller financials** (+ EDGAR where public).

## 3. The shared spine *(serves both pillars)*
- **Data layer** — FRED · BEA · BLS · market quotes · EDGAR; provider adapters; polling/scheduling.
- **AI layer** — Bedrock/Claude editorial (Ellery), fact-locked; Ask-JHI assistant; document Q&A (future RAG).
- **Identity & commerce** — accounts, roles (public/free/subscriber/staff), subscriptions/billing (Stripe), per-seat model.
- **Back-office (staff)** — Accounting/COA/GL, CRM, System Admin (the firm's own operations).
- **Entity graph** — companies ↔ deals ↔ people ↔ filings; the connective data model.
- **Governance** — provenance/`JHI-SIG`, "not advice" disclosures, NASDAQ **no-spillage** isolation.

## 4. The connective tissue — *the loop* (our differentiator)
Competitors do **one** pillar (a data terminal *or* a deal tool). JHI's edge is the **loop between them**:
1. **Markets → Diligence:** the macro regime feeds the deal — e.g., the **rate environment sets the DCF discount rate**; inflation/credit colors the thesis.
2. **Idea → Close:** **Screener → Scope → QoE → DCF → Pipeline → Portfolio** is one continuous flow — find it, vet it, value it, track it, close it.
3. **Everything → Editorial:** both pillars feed the **AI newsletters** (the owned-media funnel) and the **Opportunity Score** (transparent 0–100 decision-support).

## 5. Layout / IA implications
- The app menu already reflects the structure: **Research & Intelligence** · **Diligence a Target** · **Deal Workflow** · **Outputs & AI** · **Firm Operations (staff)**.
- **Refinements to make the model unmistakable:**
  - Make the **two pillars** legible at the top level (a subscriber should instantly see "research" vs. "acquire").
  - **Surface the loop** in the UI — one-click **Screener → Scope → Pipeline** on a target; show the macro read *inside* the DCF (why the discount rate is what it is).
  - Keep **public-ticker valuation** (Pillar A) and **private-deal valuation** (Pillar B) as distinct siblings so the two worlds stay clean (see `docs/CROSS_ASSET_VALUATION_ENGINE_SPEC.md`).

## 6. How current work maps
| Built / in-flight | Pillar | Spine |
|---|---|---|
| Economics, market tickers, Screener, Reports | A | data |
| Newsletters + Ellery (Bedrock, activated) | A | AI |
| Deal X-Ray (Scope), QoE (Earnings), curbed DCF | B | — |
| Pipeline, Portfolio | B | entity graph |
| Accounts/roles/billing, Accounting, Domain, PDF engine | — | spine |

## 7. What this map drives next
- **Cross-Asset Valuation & Action Engine** (Pillar A) — value every asset class with the *right* method + an action write-up. Spec: `docs/CROSS_ASSET_VALUATION_ENGINE_SPEC.md`.
- **AWS enhancements** — reliability/scale/delivery for a superb experience. Roadmap: `docs/AWS_ENHANCEMENT_ROADMAP.md`.
- **Launch gates** — per `docs/LAUNCH_READINESS_MAP.md` (5H, Stripe, per-plan gating, copy, DNS/SES).

*This map is the reference for all layout and build sequencing decisions. Update it when a pillar, spine component, or the loop materially changes.*
