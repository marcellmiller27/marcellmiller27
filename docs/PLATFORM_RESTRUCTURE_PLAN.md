# JHI Platform — Day 4 Synthesis & Phased Restructure Plan

> JHI-SIG: 69M2705M · JHI Research & Analytics Firm, Inc. (proprietary)
> **The executable plan** to restructure JHI from a "website" into an institutional,
> Mergr-parallel, deep-dive intelligence platform. Consolidates the analysis in
> `docs/PLATFORM_IA_BLUEPRINT.md` (the "what/why") into a phased build (the "how").
> **Planning artifact — no code is built until the Founder approves a phase.**

## Approved foundational decisions (Founder, 2026-07-19)
1. **App navigation:** **left-sidebar TOC** (SEARCH + TOOLS & INSIGHTS + Utility) + top bar
   (global search · Ask JHI · account). *(Mergr uses a top menu; we go left-sidebar for a
   broad module set — CapIQ/PitchBook pattern.)*
2. **Data foundation:** **Postgres relational** entity/relationship graph (no new infra).
3. **Approach:** **incrementally refactor** the current Next.js + FastAPI app (reuse the
   21 backend routers + existing modules); no rewrite.
4. **Phase 1 = the structural spine** (shell split + TOC + workspace Dashboard) — make it
   *feel* like a product first, then layer depth.
5. **Merge/base:** merge the foundational PRs first to form a clean base.
6. **Module consolidation:** map/retire overlapping pages into the canonical set.

## Governing principles (carried into every phase)
**Depth Principle** (win on true deep-dive, not aggregate-shallow) · **Mirror Principle**
(peers' institutional language verbatim) · **Core Rule** (name + disclosed definition) ·
**Context Principle** (judge from the subscriber's POV) · **Foundation-first** (every PR is
a draft the Founder reviews/approves/merges; DoD = pytest + lint + build green + evidence).

---

## Target architecture (consolidated)
- **Two shells:** public **Storefront** (marketing, segments, pricing) vs authenticated
  **Application** (the product).
- **Application spine:** left-sidebar **TOC** → **Dashboard** (launchpad + at-a-glance
  workspace) → **SEARCH** (entities) and **TOOLS & INSIGHTS** (grouped tools) → **record
  pages** (deep-dive) → cross-entity **pivot** (graph traversal).
- **Data core:** Postgres **entity/relationship graph** (Company · Firm · Advisor · Person ·
  Transaction[keystone] · Security · Filing · Macro Series) with edges (acquired/invested/
  advised/employed/connected).
- **Depth layer:** every record drills to bedrock — Financials & Ratios, Valuation, Filings,
  Risk & Governance (the "Fundamentals" facets), + macro overlay.

---

## Current-state inventory (what we reuse)
- **Backend:** 21 FastAPI routers (auth, market, bea, public_macro, edgar, deal_xray,
  financial_diligence, valuations, research, pipeline, crm, leads, accounting, agents,
  integrations, billing, reports, dashboards, mobile_auth, support). Postgres in Docker.
- **Frontend:** Next.js pages (dashboard, opportunities, deal-xray, diligence-suite,
  due-diligence, portfolio, pipeline, reports, assistant, accounting, mobile, account,
  team, pricing, about, downloads). Design tokens (PR #77). Stranded Macro UI (PR #75).
- **Deliverables engine:** EDGAR workbook (#76), models/workbooks in `public/downloads`.

---

## Phased PR plan
*(Each phase = one or more draft PRs; Founder reviews/approves/merges. Sequential unless noted.)*

### Phase 0 — Foundation base (merges only; Founder action)
**Dependency-correct order** (#77/#80/#81 are stacked on #76's branch; #74/#75/#76 target main):
1. **#76** — Company workbook *(base of the stack — merge FIRST; auto-retargets #77/#80/#81 to main)*
2. **#81** — entity-name rename
3. **#77** — design tokens
4. **#80** — Tier-3 pricing
5. **#75** — Macro Dashboard UI
6. **#74** — JH monogram logo *(optional/brand)*

*Conflict note:* #77/#80/#81 are siblings off #76 and touch some overlapping files
(`src/app/downloads/page.tsx`, header comments) — minor conflicts possible. Cy can pre-rebase
#81/#77/#80 onto main after #76 so each is a clean one-click merge (Founder still merges).
*DoD: main builds green with tokens + macro UI + correct pricing/naming.*

### Phase 1 — Structural spine ("product, not website")
- **1.1** Split **Storefront** vs **Application** shells/layouts.
- **1.2** **Left-sidebar TOC** (two-sector model) + top bar (global search · Ask JHI · account);
  route TOC items to module workspaces.
- **1.3** Apply **function-first nomenclature** (mirror terms + approved outliers) across nav/labels.
*DoD: authenticated app has a real TOC→module spine; storefront separate; lint/build/tests green;
before/after screenshots.*

### Phase 2 — Dashboard workspace (launchpad + at-a-glance)
- **2.1** Dashboard **launchpad**: SEARCH (entities) + TOOLS & INSIGHTS groups incl.
  **"Diligence a Target."**
- **2.2** **At-a-glance rail** (coverage stats · saved screens/watchlist · insight widgets) +
  workspace layout (filter rail · results grid · record detail).

### Phase 3 — Entity graph + records (the depth foundation)
- **3.1** Postgres **entity/relationship schema** (nodes + edges; Transaction keystone).
- **3.2** **Company record** page — flat tabs (option C): Overview · Financials & Ratios ·
  Valuation · Filings · Risk & Governance · Transactions · Relationships · Advisors · News · Analytics.
- **3.3** **Firm** & **Advisor** record pages (their node schemas).
- **3.4** **Cross-entity search + pivot** (graph traversal — no dead ends).

### Phase 4 — Tools & Insights (the "answers" layer)
- **4.1** **"Diligence a Target"** group with **shared engines** (BQS · Valuation · Risk;
  QoE separate) — anti-duplication: rename `deal-xray` → **Limited Scope Review**; consolidate
  `diligence-suite` + `due-diligence`.
- **4.2** **Buyer Match** + the two-sided loop (LSR ↔ Buyer Match).
- **4.3** **Market Intelligence** tools: Origination/Screening (from `opportunities`),
  Prospector, Rankings, **Analytics with macro overlay** (our depth edge).

### Phase 5 — Data & depth (Depth Principle)
- **5.1** Recover **Macro Dashboard UI** as the **Macro Series** entity; macro overlay on Analytics.
- **5.2** **Securities & Markets** + **SEC Filings** entities; EDGAR-powered Financials/Valuation
  depth on records.
- **5.3** **Client-upload / accounting-integration** data path (private-company depth; QuickBooks/Xero).

### Phase 6 — Launch gates & polish
- **6.1** Component polish on tokens (tables/cards/charts density) + fix the **mobile dark-on-dark
  headline** (P0 from the audit).
- **6.2** Seat/billing enforcement end-to-end; RBAC on every premium route; empty/error states.
- **6.3** **Mobile parity** decision executed (companion-plus vs native).

---

## Dependencies & risks
- **Data availability:** EDGAR doesn't expose every line item cleanly; private companies need
  client-provided data (Phase 5.3) — set "n/a" gracefully until mapped.
- **Sequencing:** Phase 3 (entity graph) underpins Phases 4–5; do not start records/tools before
  the schema lands.
- **Scope realism:** this is a multi-phase program; each phase ships independently so value lands
  early (Phase 1 alone kills the "website" feel).

## Next action
Founder to **approve Phase 0 merges + Phase 1 scope**; then I open Phase 1 draft PRs. Nothing is
built before that approval.
