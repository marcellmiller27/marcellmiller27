# JHI Platform — Information Architecture & Navigation Blueprint

**Status:** v0.1 — DRAFT FOR DISCUSSION (Day 1 of the Mergr dissection). Nothing here
is built or final; this is the working artifact we edit as we decide together.
**Date:** 2026-07-16. **Owner:** Founder/CEO. **Steward:** Cy (VP Eng).
**Governed by:** `docs/ENGINEERING_POLICY.md` (foundation-first; you review & merge).

> Goal of Day 1: reverse-engineer Mergr's IA, diagnose our current structure, and
> draft JHI's table-of-contents / navigation model + function-first language.

---

## Part A — Mergr, reverse-engineered (our case study)

### A.1 Two clearly separated zones
Mergr keeps **marketing/storefront** and **product** distinct:

- **Storefront (public):** positioning + conversion.
- **Product (authenticated):** the actual working tool (browse/search/analyze/export).

### A.2 Storefront IA (from the menu snapshots)
- **Solution for [segment]** (primary framing — market/function, not job title):
  Acquirers/Investors · M&A Advisors · Private Equity (Fund/Suite) · Lenders ·
  Corporate · Recruiters · Service Providers · Wealth Advisors
- **Product:** Pricing · Free Trial · Log In · Custom Exports/API · AI Connection ·
  Browse · Support Docs · Search Guides · Search Examples · *PitchBook Alternative*
- **Company:** About · Contact · LinkedIn
- **Legal:** Terms · Privacy
- **Persistent CTA:** "Search Free" / "Free for 7 days — cancel anytime"

### A.3 Credibility pattern
Dataset scale shown as trust signal, with **facets that double as filters**:
- 4,867 PE firms · 223,608 companies (middle-market / large / private / acquired /
  PE-backed) · 3,914 advisors (law firms / investment banks / middle-market / multi-sector)

### A.4 Positioning pillars
Updated Daily (in-house research) · Fast to Use (no onboarding) · Built for PE & M&A (focus)

### A.5 Product model (inferred)
- **Entities:** PE Firms · Companies · Advisors · Transactions/Deals
- **Core interactions:** Search + Browse → filterable results grid → record profile →
  related records via the **ownership graph** (buyer ↔ target ↔ advisor ↔ timeline)
- **AI Connection:** natural-language questions over the graph
  (e.g. *"Who has 3M bought from and divested to, and which advisors did they use?"*)
- **Exports/API:** custom data out

### A.6 The real lesson
Mergr's moat is **normalization + relationship modeling** of *public* data into a
searchable graph — not proprietary raw feeds. **JHI's data model must therefore be an
entity + relationship graph, not just tables of filings.**

---

## Part B — JHI today (honest diagnosis)

- **App navigation is a flat 16-link bar** (`src/components/platform-shell.tsx`):
  Home, Dashboard, Opportunities, Reports, AI Assistant, Deal X-Ray, Quality of
  Earnings, Pipeline, Document Review, Portfolio, Accounting, Documents, Plans,
  Account, Help, Team. → **No hierarchy, no table-of-contents, mixes marketing +
  app + account.** This is "website," not "product."
- **No separation** between storefront and application shells.
- **Job-title language** used as audience segments (`src/app/page.tsx`): "CPAs",
  "Attorneys", "Business Brokers", "Executive Recruiters", etc.
  (The "CPA-signed QoE" *feature* wording is legitimate and stays.)
- **Dashboard is a static page**, not a filter/grid/detail workspace.

---

## Part C — Proposed JHI IA (draft for discussion)

### C.1 Two zones (recommend a hard split)
1. **Storefront shell** (public): Home · Solutions (by segment) · Pricing · About ·
   Team · Log in · Start free.
2. **Application shell** (authenticated): the **Table of Contents** navigation +
   module workspaces.

### C.2 Segment language — "JHI for [segment]" (replaces job titles)
| Old (job-title / mixed) | New (function/market segment) |
|---|---|
| Search-Fund & SMB Acquirers, Independent Sponsors, Self-Directed | **Acquirers & Investors** |
| (new) | **Private Equity** |
| Business Brokers | **M&A Advisors & Brokers** |
| (new) | **Corporate Development** |
| (new) | **Lenders & Credit** |
| Investment Advisors (RIAs), Family Offices | **Wealth & Asset Managers** |
| CPAs, Attorneys | **Service Providers** (accountants, attorneys, consultants) |
| (new) | **Research & Analysts** |
| Executive Recruiters | **Recruiters** *(keep? — see open questions)* |

### C.2a Segment-framing language pattern (Mergr's strategic copy) — FOUNDATIONAL
**Principle (Founder directive): language is strategic, intentional, and with purpose —
never generic.** Each segment is framed with a repeatable formula:

> **[Segment]** = a **range/spectrum descriptor** → then a **facet list written in that
> segment's own insider vocabulary**.

Observed on Mergr:
- **M&A Advisors** → *"Legal & Financial, Boutique to Multinational"* →
  M&A Analytics · M&A Client Lists · Advisory Connections · Sector Coverage · M&A Contacts
- **Private Equity** → *"Small to Mega, Generalist & Specialist"* →
  Investment Criteria · M&A History · Portfolio Breakdown · M&A Analytics ·
  Professionals w/ Contact Info · Office Locations · M&A Connections

Why it works (the three intentional moves):
1. **Range descriptor = inclusion.** "Boutique to Multinational," "Small to Mega,"
   "Generalist & Specialist" signal total coverage with both/and framing, so **no reader
   in the segment self-excludes** — everyone thinks "that's me."
2. **Facets in native vocabulary = credibility.** Each audience sees the terms *it* uses,
   proving the platform was built for them.
3. **Facets recur across segments** ("M&A Analytics," "M&A Connections") → they are
   **views of one shared entity/relationship graph, re-labeled per segment lens.**
   → **Language and data model are the same coin: one graph, many segment lenses.**

**JHI action (to fill in together):** every JHI segment gets (a) a range descriptor and
(b) a facet list in that audience's vocabulary, each facet mapping to a view of the
underlying intelligence graph. Starter template (DRAFT — for discussion):

| Segment | Range descriptor (draft) | Facet list (draft, native vocabulary) |
|---|---|---|
| Acquirers & Investors | Search fund to family office | Deal Screening · Target Financials · Valuation & LBO · Ownership Graph · Comparable Transactions |
| Private Equity | Lower-middle-market to mega; generalist & specialist | Investment Criteria · Portfolio Breakdown · Acquisition History · Sector Analytics · Firm Contacts |
| M&A Advisors & Brokers | Boutique to multinational | Buyer/Seller Lists · Advisory Connections · Sector Coverage · Comparable Deals · Contacts |
| Corporate Development | Single-acquirer to serial acquirer | Target Screening · Strategic Fit · Deal History · Comps · Ownership Graph |
| Lenders & Credit | Community to institutional | Credit Profile · Cash-Flow & DSCR · Collateral/CRE · Risk Score · Filings |
| Wealth & Asset Managers | Independent RIA to family office | Macro Outlook · Security Fundamentals · Portfolio Analytics · Research · Newsletter |
| Service Providers | Solo practice to national firm | QoE / Diligence · Financial Analytics · Document Review · Client Intelligence |
| Research & Analysts | Independent to institutional | Macro Dashboard · Industry Outlook · Company Profiles · Data Export/API |

### C.3 Application Table of Contents (module map, grouped by function)
The left-sidebar TOC — pick a group, land in that module's workspace:

1. **Dashboard** — the application entry point after login (DECIDED, see F.1): a hybrid
   **launchpad + at-a-glance workspace** (quick-access groups + summary/metrics rail),
   and the "home base" anchoring the product
2. **Macro & Industry** — Macro Dashboard · Industry/Sector Outlook
3. **Screening & Discovery** — Opportunity Screener · Company Search/Browse
4. **Company Intelligence** — Company Profile hub: Financials & Ratios (EDGAR) ·
   Ownership & Relationship Graph · Acquisition History · Comparable Transactions ·
   Market Data / Securities
5. **Diligence & Deal Analysis** — Deal X-Ray (CIM) · Quality of Earnings ·
   Valuation Models (DCF / LBO / Search-Fund) · Document Review · Risk Score
6. **Deal Workflow** — Pipeline · Portfolio
7. **Research & Outputs** — Reports & Excel Workbooks · Newsletter
8. **Ask JHI (AI)** — natural-language query over the entity graph
9. **Firm Operations** *(internal/role-gated)* — Accounting · Admin Console/Agents · CRM/Leads
10. **Account & Support** — Account · Billing & Seats · Help

### C.4 Navigation model (the "table of contents → module" flow you described)
- **App shell:** persistent **left sidebar = TOC** (collapsible groups) + top bar with
  **global search + Ask JHI + account menu**. Selecting a TOC item routes to that
  module workspace in the content area.
- **Rationale:** Mergr uses a top-right menu, but institutional analytics tools
  (Capital IQ, PitchBook, Preqin) use a **left TOC sidebar** for dense module sets —
  better for a platform this broad. (Open question C.7.)

### C.5 Dashboard = workspace (the "pivot table" idea)
Standard three-region analytical layout: **filter rail (left) · results grid (center) ·
record detail (right/drawer)**, plus **saved views**. Facets = the data model's
categories (mirrors Mergr A.3).

### C.6 Signature workflow (our differentiator vs Mergr)
`Macro dashboard → industry outlook → company screening → company profile →
{ratios · ownership graph · acquisition history · comps · DCF · LBO · search-fund ·
QoE · risk · ESG/governance · exec bios · litigation · patents · credit · news}`.
Mergr can't do the macro→company drill-down; we can, on data adapters we already have.

### C.7 Open questions to decide (Day 1 discussion)
1. **App nav:** left-sidebar TOC (my rec) vs top menu like Mergr?
2. **Segment list:** confirm the 8 segments in C.2 (keep "Recruiters"? add others?).
3. **Naming:** "Ask JHI" vs "AI Assistant"? ~~"Intelligence Home" vs "Dashboard"~~
   → **DECIDED: "Dashboard"** (see F.1 — matches Mergr; clarity over cleverness)
4. **Shell split:** fully separate storefront vs app shells (my rec: yes)?
5. **Module consolidation:** `deal-xray` vs `diligence-suite` vs `due-diligence`
   overlap — confirm the canonical module set.
6. **Firm Operations** (accounting/admin/CRM): in the same app TOC (role-gated) or a
   separate internal console?

---

## Part D — Mapping current pages → target IA (so nothing is lost)
| Current page/route | Target TOC home |
|---|---|
| `/dashboard` | Dashboard (rebuilt as launchpad + workspace) |
| `/macro` *(stranded, to recover)* | Macro & Industry |
| `/opportunities` | Screening & Discovery |
| `/deal-xray` | Diligence & Deal Analysis |
| `/diligence-suite` (QoE) | Diligence & Deal Analysis |
| `/due-diligence` (Document Review) | Diligence & Deal Analysis |
| `/pipeline` | Deal Workflow |
| `/portfolio` | Deal Workflow |
| `/reports`, `/downloads` | Research & Outputs |
| `/assistant` | Ask JHI (AI) |
| `/accounting` | Firm Operations |
| `/account`, `/support` | Account & Support |
| `/`, `/pricing`, `/about`, `/team` | Storefront shell |

---

## Part F — Day 2: Authenticated-product observations (in progress)
*Source: Founder's logged-in Mergr session (photos of screen — layout read reliably,
fine text pending clearer captures).*

### F.1 Entry point = "Dashboard" (DECIDED)
- After login, Mergr's entry point **is a dashboard, labeled "Dashboard" in the TOC.**
- It is a **hybrid launchpad + at-a-glance workspace**: quick-access groups (entities/
  segments/recent) on the left + a **summary/metrics rail** on the right.
- It lives inside the **persistent product shell** (top search + nav on every screen).
- **JHI decision:** application entry point after login = **"Dashboard"**, first item in
  the TOC, built as launchpad + at-a-glance workspace. (Supersedes the earlier
  "Intelligence Home" idea — keep the proven, clear convention.)

### F.2 Patterns confirmed from authenticated views
- **Search = filter controls + dense results *list*** (right-aligned metadata per row),
  not cards.
- **Record/profile pages = header + sectioned facets + data tables** (financials shown
  as rows × periods).
- **Restrained green/gold accenting**; **data density over whitespace** throughout.

### F.3 Still to capture for precise modeling (need clearer/straight-on shots)
- Company & PE-firm profile **section order** (their facet taxonomy = our record template).
- **Ownership/relationship graph** presentation (visual graph vs linked records vs table).
- **Search results row** columns/metadata.
- **AI Connection** query + answer presentation.

## Next (Day 3 preview, not started)
Data & entity graph: define JHI's entity/relationship model and map each module to its
data sources + licensing constraints (from F.1–F.3 record templates).
