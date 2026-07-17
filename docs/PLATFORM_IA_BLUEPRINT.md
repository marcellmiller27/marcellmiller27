# JHI Platform — Information Architecture & Navigation Blueprint

**Status:** v0.1 — DRAFT FOR DISCUSSION (Day 1 of the Mergr dissection). Nothing here
is built or final; this is the working artifact we edit as we decide together.
**Date:** 2026-07-16. **Owner:** Founder/CEO. **Steward:** Cy (VP Eng).
**Governed by:** `docs/ENGINEERING_POLICY.md` (foundation-first; you review & merge).

> Goal of Day 1: reverse-engineer Mergr's IA, diagnose our current structure, and
> draft JHI's table-of-contents / navigation model + function-first language.

---

## Decisions Log (Founder-approved)
| Date | Item | Decision |
|---|---|---|
| 2026-07-16 | F.1 — Application entry point name | **Dashboard** (matches Mergr convention) |
| 2026-07-17 | K.3 — Nomenclature process & bar | prepare → vet → select → approve; institutional-grade, parallel to Mergr, not elementary |
| 2026-07-17 | **C.1 — Two-zone shell split** | **APPROVED** — separate public Storefront vs authenticated Application shells |
| 2026-07-17 | **Strategic objective** | Audience-first: follow institutional-grade peer standards; goal = conversion into long-term subscriptions by solving subscribers' decision-lag pain-points (Board Minutes §1) |
| 2026-07-17 | **Nomenclature CORE RULE** | Every term = **name + disclosed definition** (Functional Output); disclosure is hierarchical (Sector → Group → Item) |
| 2026-07-17 | **MIRROR PRINCIPLE** | Adopt peers' (Mergr) terms + definitions **verbatim**; **no inventions**; rationale = audience already speaks this jargon → no confusion, no lost conversions |
| 2026-07-17 | **Two-sector product model (L.0)** | Core TOC = (A) Search the Database + (B) Tools & Insights; storefront segments are a separate marketing layer |
| 2026-07-17 | **Outliers = team decision** | JHI-only capabilities (Securities & Markets, Macro Series, SEC Filings; Deal X-Ray/QoE/Valuation/Risk Score; Research & Analysts segment) discussed together — OPEN |

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

### C.1 Two zones (recommend a hard split) — ✅ APPROVED (Founder, 2026-07-17)
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

### F.4 Dashboard anatomy (from a clear straight-on capture) — FOUNDATIONAL
The Dashboard = **two-tier action launchpad (left) + live at-a-glance rail (right)**,
inside the persistent shell (top: Search · logo · user · ☰ MENU/TOC).

**Left, Tier 1 — SEARCH THE DATABASE** ("Pick a data type… each built for that record
type"): the raw **entities**, each with a **facet descriptor** = its filter dimensions:
- Private Equity — "By AUM, sector focus, geography & activity"
- Companies — "By ownership, size & sector"
- Transactions — "By date, value, deal type & sector"
- M&A Advisors — "Banks & law firms by deal experience"
- M&A Professionals — "Deal-team members by firm & role"
- M&A Press Releases — "Full announcement archive…"

**Left, Tier 2 — TOOLS & INSIGHTS** ("Pre-built tools that turn the database into
**focused answers**"), grouped by **job-to-be-done**, second person:
- *Working a Live Deal* → Buyer Match · Investor Match · Advisor Match
- *Find New Opportunities* → Prospector · Roll-Up Tracker · Shed · Investor Lookalikes

**Right rail — at-a-glance:** SAVED SEARCHES (persistence) · STATS (live coverage with
faceted breakdowns) · Insight widget (Top PE Firms by acquisitions, '25 vs '26).

**Three lessons locked into JHI's foundation:**
1. **Data vs. Answers is a designed split** — Tier 1 = raw entities; Tier 2 = pre-built
   answers. This is what makes it an intelligence platform, not a database. JHI's
   macro→company integration lets Tier 2 go further than Mergr.
2. **Consistent taxonomy end-to-end** — STATS facets == Search facets == data-model
   categories == "one graph, many lenses."
3. **Name for the job, not the feature** — Buyer Match, Prospector, Roll-Up Tracker, Shed.

**JHI Dashboard (DRAFT for discussion):**
- *Tier 1 — Search/Research entities:* Companies · Securities & Markets · Transactions/
  Deals · Investors & PE · Advisors · SEC Filings · Macro Series · Executives
- *Tier 2 — Tools & Insights (by JTBD):*
  - Analyze a Target → Deal X-Ray · Quality of Earnings · Valuation (DCF/LBO/Search-Fund) · Risk Score
  - Find Opportunities → Opportunity Screener · Prospector · Roll-Up/Consolidation finder
  - Understand the Market → Macro Dashboard · Industry Outlook · Newsletter
- *Right rail:* Saved Screens/Watchlist · Live Coverage Stats · Insight widget
  (market movers · macro highlights · most-active acquirers)

### F.5 Complete Tools taxonomy + embedded dashboard widgets (from full scroll)
**Tools & Insights = 15 tools in 4 job-to-be-done groups** (the "answers" layer):
1. **Working a Live Deal** — Buyer Match · Investor Match · Advisor Match
2. **Find New Opportunities** — Prospector · Roll-Up Tracker · Shed · Investor Lookalikes
3. **Research a Firm or Company** ("build context on a known entity") — Dossier
   (full M&A profile) · Lineage (PE alumni/talent network) · Ownership Graph (ownership
   eras, holds & exit signals) · Trading Partners (recurring buyer-seller pairings +
   timeline) · Compare (side-by-side firms)
4. **Market Intelligence** ("macro view across the database") — Rankings (sortable
   leaderboards) · Analytics (market activity & sector trends) · Deal Flow Map
   (cross-border flows by country/time/keyword)

**KEY VALIDATION:** Group 3 is entirely **graph views** (ownership, people lineage,
buyer↔seller edges, dossiers, compare) → confirms JHI must be built on an
**entity + relationship graph**; downstream tools are queries over that graph.

**Dashboard also embeds live insight widgets (not just a launchpad):**
- **Largest Acquisitions** table with time-window toggle (Last 30 Days / YTD):
  row = `Date · Target (name+geo) · Value · Acquirer (name+logo+geo, PE badge) · Deal
  Article / Deal Link`.
- **Right-rail leaderboard stack**: "TOP PE Firms / Corporates / Law Firms / Investment
  Banks," segmented by **Acquisitions vs Exits vs M&A Engagements**, with year-over-year
  columns ('25 | '26).

**Reusable templates extracted:**
- *Transaction row:* date · target (name+geo) · value · counterparty (name+logo+geo+type badge) · source links.
- *Leaderboard widget:* "Top [entity]" × [activity dimension] × [time comparison].
- *Tool card:* icon · name-for-the-job · one-line value prop · open affordance.

**JHI Tools draft — refined to 4 JTBD groups (for discussion):**
1. *Analyze a Target* — Deal X-Ray · Quality of Earnings · Valuation (DCF/LBO/Search-Fund) · Risk Score
2. *Find Opportunities* — Opportunity Screener · Prospector · Roll-Up/Consolidation finder · Lookalikes
3. *Research a Company* — Company Dossier · Ownership/Relationship Graph · Comparables (Compare) · Filings/Trading relationships
4. *Market Intelligence* — Macro Dashboard · Sector Rankings · Analytics/Trends · (geographic) Deal/Market Flow
- *Embedded widgets:* Market Movers · Macro Highlights · Most-Active Acquirers · Top Movers (time-window toggle + YoY).

### F.3 Still to capture for precise modeling (need clearer/straight-on shots)
- Company & PE-firm profile **section order** (their facet taxonomy = our record template).
- **Ownership/relationship graph** presentation (visual graph vs linked records vs table).
- **Search results row** columns/metadata.
- **AI Connection** query + answer presentation.

## Part G — Day 3: Entity graph & record templates (in progress)
*Source: authenticated Company record (Berkshire Hathaway), read straight-on.*

### G.1 Company record template (observed on Mergr)
- **Header (identity):** name · legal name · address · phone · website.
- **Tabbed facet bar with live counts** + Analytics + print/export:
  - **Profile**
  - **M&A Activity (N)** — transactions: `Date · Target (name, sector, location,
    website, description, Revenue, EBITDA, Advisors) · Value + multiples (EBITDA x,
    Revenue x) · Transaction Type · Acquirer · Seller · Source`;
    filters: Sector · Type · Country · Year · ALL/BUY/SELL.
  - **M&A Connections (N)** — "Invested With": `Name · Total · Most Recent · Date`;
    filters: ALL / INVESTORS / CORPORATES.
  - **M&A Advisors (N)** — `Name · Type (Legal/Financial) · # Transactions · Vol`;
    sub-tabs Advisors vs **Opposing Advisors**; filters ALL/FINANCIAL/LEGAL.
- **Consistent interaction pattern per tab:** filter chips + sortable columns + counts.

### G.2 Entity–relationship model (decoded — JHI foundation)
Each Company tab = an edge type. The graph:
- **Nodes:** Company · Firm/Investor · Advisor (Legal|Financial) · Person/Professional ·
  **Transaction/Deal** (atomic connector). *JHI adds:* Security(ticker) · Filing(SEC) ·
  Industry/Sector · MacroSeries.
- **Edges:** Company —acquired/divested→ Company (via Transaction) · Firm —invested-in→
  Company · Company —advised-by→ Advisor (buy/sell side) · Advisor —opposed→ Advisor ·
  Person —employed-by→ Firm (Lineage) · Company —connected-to→ Investor/Corporate.
  *JHI adds:* Company —has→ Filing · Company —has→ Security · Company —in→ Industry ·
  Industry —tracked-by→ MacroSeries.
- **Transaction attributes:** date · value · EBITDA multiple · Revenue multiple · type
  (Add-on / Buyout / Divestiture / Investment) · target · acquirer · seller · advisors ·
  source. **Transaction is the keystone entity.**

### G.3 JHI Company record template (SUPERSET — our differentiation)
Keeps Mergr's M&A/relationship tabs AND adds integrated financial/macro intelligence
(from EDGAR + market + macro adapters we already have):
1. Overview (identity, description, key facts, ticker, sector/NAICS)
2. **Financials & Ratios** (EDGAR: IS/BS/CF + ratios) ← *not in Mergr*
3. **Valuation** (DCF / LBO / comps multiples) ← *not in Mergr*
4. M&A Activity / Transactions (with multiples)
5. Ownership & Relationships (connections graph)
6. Advisors (incl. opposing)
7. Comparables (Compare)
8. **Filings** (SEC) ← *not in Mergr*
9. News / Press
10. **Risk & Governance** (risk score, ESG) ← *not in Mergr*
11. Analytics
- Same interaction pattern: filter chips + sortable tables + counts.

**Moat note:** Mergr's Company record is deal/relationship-centric (hand-curated, no deep
financials). JHI's superset = relationship graph **+** financials + valuation + filings +
risk = integrated intelligence, not a deal database.

### G.5 Entity search interfaces (all record types) + cross-entity pivot — FOUNDATIONAL
Consistent skeleton for every entity: **search form (entity criteria) → cross-entity
result tabs → toolbar (Sort · Save to List · Save Search · Download) → results table
(entity columns + badges + sparklines) → faceted filter rail.**

Per entity (totals observed):
- **M&A Announcements (121,887):** full-text scoped by Titles/Bodies/Acquirers/Advisors;
  filter rail Acquirer Category (Company/Investor), Value bands, Year counts; results =
  announcement cards + Target sidebar.
- **Transactions (222,791):** Invest/Exit Situation, date range, Deal Value + Target
  criteria (Sector/Geo/Revenue). Columns: Date · Target · Type+Value · Acquirer · Seller.
- **Companies (224,043):** Names/Tickers · Descriptions · Sector · Revenue · Geo. Rows:
  badges (PE Backed, ticker e.g. NYSE:AJG, Acquired) · Sector · Revenue · M&A Activity
  (Total/Buy/Sell) · 5-yr sparkline.
- **Advisors (3,308):** Financial/Legal · Size · Geo · Main Office. Rows: type · founded ·
  team-member avatars ("See all N") · Investor/Corporate client counts · deal-count sparkline.
- **Professionals/People (85,936):** Bio · Title · Works-for · Email · Geo. Rows: photo ·
  title · firm · office · email · joined year · full bio.

**BIG MECHANIC — cross-entity result tabs = graph traversal.** Every search pivots from
the primary entity to connected entity result-sets (Company → Company M&A / PE Investors /
Company Investors / Advisors; Advisor → Team Members / Transactions / PE Clients / Company
Clients). No dead ends — every entity is a launch point into its relationships. **JHI must
replicate this pivot** (it's the UI expression of the entity graph in G.2).

**Node nuance:** "Investor" is a role held by both **PE firms** and **companies**
(PE Investors vs Company Investors) — model Investor as a role/edge, not a rigid type.

**Reusable patterns:** Save to List · Save Search · Download/Export (monetization);
sparkline micro-viz in rows (JHI adds revenue/price trends from EDGAR + market data).

### G.6 PE-Firm record (Petra Capital Partners) — Firm node schema COMPLETE
**Tabs:** Profile · M&A Activity (N) · Portfolio (N) · Team (N) · Offices (N) ·
M&A Connections (N) · Analytics.

**Firm node attributes:**
- **Identity:** name · legal name · address · phone · website · email · LinkedIn.
- **Investor Summary:** Investor Type · Ownership · Size · **AUM/PE Assets** · Established ·
  Specialist/Generalist.
- **Investment Criteria ("buy box"):** Sectors of Interest · Target Transaction Types ·
  Geographic Preferences · **Transaction Criteria (MIN/MAX: Target Revenue, Target EBITDA,
  Investment Size, Enterprise Value)**.
- **Team/Leadership** (people + roles + photos → Person node).
- **Portfolio** (holdings; active vs exited; "Sold to X").
- **M&A Connections:** Acquired-from / Exited-to, split Investors vs Strategics.
- **Team lineage:** "current team worked at" / "past team now works at" (Lineage edges).
- **Analytics:** Buy-vs-Sell over time · Deal Values by band · by Deal Type · by Sector ·
  by Geo (Current # vs All-Time #).

**Key:** the firm's **buy box** is a structured statement of *what it wants* — this is the
attribute that powers Buyer Match (Part H). *Investor* = role held by PE firms AND
companies (confirmed).

### G.7 Ownership Graph tool — captured (Day 3 COMPLETE)
"Ownership history, acquisition activity, sponsor patterns, exit signals for a company."
An **era/timeline model with a derived-intelligence layer** (not a visual node-web):
- **Summary card:** Ownership Eras · Acquisitions · Divestitures · **Current Status**
  (Core Holding / Independent / PE-owned).
- **Tabs:** *Deal Topology* (ownership eras + **hold period** + add-on/divestiture per era) ·
  *Maturity* (scoring, "designed for PE-owned platforms") · *Exit Signals* (exit-likelihood;
  gracefully N/A for independents) · *Advisor Relationships* (advisors per era, buy/sell side).
- **Lesson:** the value is the **derived layer** (hold period, status classification,
  maturity, exit signals) computed over raw edges — where JHI analytics can differentiate.

### G.8 Advisor node schema (Boxwood Partners) — bonus
Parallels the Firm node: identity + **Advisor Summary** (Size · Established · Ownership ·
Type) + **Advisor Criteria** (Sector/Geo coverage · Services) + Team · Offices · M&A
Advisory (transactions) · Clients · Advisory Connections · Analytics (Buyside vs Sellside).

### G.9 Records scale by data availability
Same record template gracefully degrades: a small private company (Monster Tree Service)
shows only Profile + Investors(1) + ownership timeline, vs a 74-deal Berkshire record.
Design principle for JHI: one template, render only the facets with data.

## Part H — Tool anatomy: Buyer Match (the flagship AI/matching engine)
"Rank likely buyers for a target — by sector, specialty, deal size, geography, activity
fit. Financial and Strategic." Flow:
1. **Describe target in plain English** (or pick an existing company) → **PARSE**.
2. **NLP → structured criteria WITH shown reasoning** (e.g. "EBITDA $1M banded to
   $0.8–1.2M; stage null → mature default") — explainability = trust.
3. **Editable criteria chips** (Sector · Specialty · Size EV/Revenue/EBITDA · Geography ·
   Stage; Financial Buyer Pool: HQ Region · Buyer Size) — "click X / + Add; re-runs auto."
4. **Find Matches → ranked, scored results** (PE Firms / Strategic tabs), **match score
   /100** + **evidence badges** ("2 specialty deals · active 3 in last 24m · 1 active
   platform") + plain-English rationale + CSV export.

**JHI implications (high priority):**
- This is the concrete form of "Ask JHI / AI Connection": **NLP parse → editable chips →
  explainable scored ranking → export.**
- **Pairs with Deal X-Ray** as a two-sided loop: X-Ray analyzes a target's CIM; Buyer
  Match finds who would buy it.
- Explainable parse + evidence-badge scoring aligns with JHI's **published-methodology /
  Opportunity Score** ethos.
- Powered by the **Firm buy box (G.6) + transaction graph (G.2)** — both now modeled.

## Part I — JHI differentiation vs Mergr (synthesis input for Day 4)
Where JHI deliberately goes beyond the case study:
1. **Integrated financials/macro on every record** — Mergr records are deal/relationship
   only; JHI adds Financials & Ratios, Valuation (DCF/LBO), Filings, Risk (EDGAR + market
   + macro adapters we already have). See G.3.
2. **Two-sided intelligence loop** — Deal X-Ray (analyze a target's CIM) ↔ Buyer Match
   (find its buyers). See Part H.
3. **SMB / search-fund bridge (unserved by Mergr).** Mergr stops at mid-market+ PE/M&A.
   The real SMB deal world (broker teasers, **SDE = EBITDA + owner comp**, **SBA**
   pre-approval, **DSCR** financing fit) is JHI's home turf via Deal X-Ray. JHI can bridge
   the institutional ownership graph *down* to SMB deal flow — a connection nobody else
   makes. (Illustration: Monster Tree franchise broker teaser ↔ Mergr's Authority Brands
   ownership record.)
4. **Derived-intelligence layer** — hold period, maturity, exit signals, opportunity/risk
   scores computed over the graph (G.7), aligned with JHI's published-methodology ethos.

### I.1 SMB deal-flow input for Deal X-Ray (capability note — no confidential data here)
- The firm has **active business-broker access to live CIMs** (e.g., via Benjamin Ross
  Group), i.e. real SMB offering memoranda for sale.
- A CIM's structure maps 1:1 to **Deal X-Ray inputs**: SDE/add-back schedule, terms &
  financing (SBA/DSCR), franchise economics, business background, org, facilities,
  marketing, reason for sale.
- **Pipeline:** CIM → Deal X-Ray (score financial quality, add-back legitimacy, valuation
  multiple, SBA/DSCR fit) → Buyer Match (find likely buyers). Bridges franchisor-level
  institutional ownership data with franchise-territory SMB deal flow — a connection Mergr
  does not make.
- **COMPLIANCE:** CIMs are confidential/NDA material. Never commit CIM specifics
  (financials, price, seller identity) to the repo or any artifact. Handle only in secure,
  access-controlled contexts.

## Part J — Data-sourcing strategy for detailed financials (draft for discussion)
**Problem:** CIMs don't scale — a single regional broker (BRG, East-Coast only) is a
sample, not a supply chain. How to get detailed financials for a "detailed outlook"?

**Principle:** for a specific company, detailed financials come from either (a) the
subject's own data, or (b) a modeled estimate from benchmarks/comps. No third option.
CIMs are just one (limited) form of (a) — do not build the strategy around them.

**Tiered model:**
1. **Public companies → SEC EDGAR (built).** Full statements/ratios/history; no upload.
2. **Private deep-dive → client-provided data (PRIMARY).** Manual upload (P&L, BS, tax
   returns, trial balance, CIM) **and accounting-system integrations (QuickBooks Online,
   Xero, NetSuite, Sage)** for direct, recurring, scalable linkage. Client authorizes
   their own data → **sidesteps third-party licensing** (the moat). Powers QoE/Deal X-Ray.
3. **Private screening/outlook (no direct data) → modeled estimates.** Industry benchmarks
   (NAICS margins/ratios via Census, BLS, BEA, IRS SOI), public comparables + multiples
   (Deal X-Ray comp benchmark already does this), registry/alt data (Secretary of State,
   UCC, bankruptcy, CRE, FDIC/FFIEC). Output = clearly-labeled **estimate**, not audited.
4. **CIMs → opportunistic supplement**, not the backbone.

**Moat:** client-uploaded/integrated data + JHI institutional analytics on top —
recurring, defensible, licensing-clean.

**Honest limit:** a private company that won't share and isn't public can only get a
benchmarked estimate, never exact statements. Set client expectations (fits transparency
ethos).

**Security (non-negotiable):** client financials are the most sensitive data held —
encryption in transit/at rest, per-org isolation, RBAC (leverages prior P0 hardening).
Never commingle or expose.

## Part K — Nomenclature & Functional-Output Disclosures (NOTATION + draft)
**NOTATION / STANDING TASK (Founder directive 2026-07-17):** Create and maintain a
**single controlled nomenclature list** for the TOC, and write a **Functional-Output
disclosure paragraph for every segment** (what it performs). This vocabulary is the
source of truth for nav labels, UI copy, docs, and code identifiers.

**K.0 Nomenclature standard (rules):**
- One **canonical name** per TOC entry — function-first, institutional, name-for-the-job.
- **No job-title language** (no CPA/Attorney as labels); clarity over cleverness.
- Each entry carries: canonical label · route id · one-line · full functional-output
  paragraph.
- Applies at every level: **segments, TOC groups, modules, dashboard tools, search
  entities, and record facets.**

**K.1 Top-level application TOC — nomenclature + functional output (DRAFT):**
| Canonical name | Route id | Functional output (what it performs) |
|---|---|---|
| **Dashboard** | `/app` | Command center on login: launchpad (entity search + tools) + live at-a-glance intelligence (coverage stats, saved screens/watchlists, market movers, macro highlights, most-active acquirers); routes into any module. |
| **Macro & Industry** | `/app/macro` | Top-down view: live macro indicators (GDP, inflation, rates, employment, credit) from federal/global sources + sector/industry outlooks that frame company-level work. |
| **Screening & Discovery** | `/app/screen` | Surfaces and ranks opportunities by criteria and Opportunity Score; finds targets resembling a reference company (Prospector) and consolidation candidates. |
| **Company Intelligence** | `/app/company` | Company record hub: identity, financials & ratios (EDGAR), valuation, filings, ownership/relationship graph, acquisition history, comparables, news — one profile, drill-down facets. |
| **Diligence & Deal Analysis** | `/app/diligence` | Analyzes a specific target: Deal X-Ray (CIM), Quality of Earnings, valuation (DCF/LBO/Search-Fund), document review, risk scoring → decision-grade assessment. |
| **Deal Workflow** | `/app/deals` | Manages deals across the lifecycle: pipeline (sourcing→close) and portfolio monitoring of held positions. |
| **Research & Outputs** | `/app/research` | Produces client-ready deliverables: institutional Excel workbooks, PDF reports, data-driven newsletters/market outlooks. |
| **Ask JHI** | `/app/ask` | Natural-language intelligence over the entity graph + integrated data: explainable, sourced answers and target→buyer matching (Buyer Match). |
| **Firm Operations** *(role-gated)* | `/app/ops` | Internal firm operations: accounting/GL, CRM/leads, system administration, AI-agent oversight. |
| **Account & Support** | `/app/account` | Subscriber account: profile, roles & seats, billing, security settings, help/support. |

**K.2 Lower-level nomenclature (TO COMPLETE — functional output per item):**
- **Search entities (Tier 1):** Companies · Securities & Markets · Transactions ·
  Investors & Firms · Advisors · Executives · Filings · Macro Series. *(each needs a
  functional-output line — see F.5/G for source patterns.)*
- **Dashboard tools (Tier 2):** the 4 JTBD groups + tools drafted in F.5 — finalize
  canonical names + functional-output lines.
- **Record facets:** Company/Firm/Advisor tabs (Parts G) — each facet gets a one-line
  functional output.
- **Segments (C.2):** each "JHI for [segment]" gets range descriptor + facets (C.2a) —
  functional-output framing already drafted; finalize.

### K.3 Nomenclature process + candidate slate (for vetting)
**Process (Founder-approved 2026-07-17):** (1) Prepare candidate list → (2) vet + open
discussion → (3) final selection → (4) submit for Founder approval.

**The institutional-grade bar:** every name must read as precise trade terminology a PE MD
or M&A advisor recognizes instantly (like Mergr's *Private Equity / Transactions /
M&A Advisors* for sections; *Buyer Match / Prospector / Ownership Graph / Lineage* for
tools). Reject anything that reads as a consumer app ("elementary"). Note: some standard
terms (e.g. *Dashboard*) ARE the institutional convention — Mergr uses them — so "standard"
≠ "elementary" when it's the industry norm.

**⚠️ SUPERSEDED by the MIRROR PRINCIPLE + two-sector model (L.0).** The invented names
below (Origination, Diligence Suite, etc.) are retracted. JHI's TOC mirrors Mergr's
structure — (A) Search the Database + (B) Tools & Insights (see L.0/L.3/L.4) — plus
account/support chrome. Kept here only as a record of the corrected approach.

**Top-level TOC candidate slate (DRAFT — RETRACTED, do not use):**
| Function | Candidates | Cy's lean |
|---|---|---|
| Entry point | Dashboard · Command Center · Terminal | Dashboard (matches Mergr; keeps F.1) |
| Top-down macro | Macro Intelligence · Market & Macro · Economic Intelligence | Macro Intelligence |
| Finding targets | Origination · Deal Origination · Opportunity Screener · Sourcing | Origination |
| Company hub | Company Intelligence · Entity Intelligence · Company Dossier | Company Intelligence |
| Target analysis | Diligence Suite · Due Diligence · Deal Analysis | Diligence Suite |
| Lifecycle mgmt | Pipeline & Portfolio · Deal Management · Execution | Pipeline & Portfolio |
| Deliverables | Research & Reporting · Publications · Research Desk | Research & Reporting |
| NL query / AI | Intelligence Query · Ask JHI · JHI Copilot | Ask JHI / Intelligence Query |
| Internal ops | Firm Operations · Back Office · Operations Console | Firm Operations |
| Account | Account · Account & Access · Settings & Support | Account |

*Still to prepare (same process): candidate names for search entities, dashboard tools,
record facets, and the 8 segments.*

**NEXT SESSION METHOD (Founder-directed 2026-07-17, tabled to tomorrow):** Build the
nomenclature list by going through Mergr's platform **screenshot by screenshot**,
extracting each canonical name verbatim as the institutional-grade reference, then map to
JHI equivalents. Ground the vocabulary in observed terminology — do not invent from
scratch. (This K.3 candidate slate is the starting draft to refine against those screens.)

## Part L — Mergr Nomenclature Master List (verbatim) → JHI candidate mapping
*Extracted from captured Mergr screenshots. Left column = Mergr's exact institutional
terms (the reference bar). Right column = JHI candidate (DRAFT — to vet/approve per K.3).*

> **CORE RULE (Founder-directed 2026-07-17):** Nomenclature = **name + disclosed
> definition (Functional Output)**, never a name alone. Mergr discloses a definition for
> *every* term (segment, entity, tool group, tool, facet) so paid users understand what it
> does. JHI must do the same: every canonical name ships with its own disclosed definition
> written to the same institutional standard. Capture Mergr's definitions verbatim as the
> reference; write JHI's definitions during vetting.
>
> **MIRROR PRINCIPLE (Founder-directed 2026-07-17):** Do NOT reinvent the wheel. JHI
> **adopts Mergr's institutional terms and definition style verbatim** (parallel language
> context). **No new inventions.** The only exceptions are **legitimate outliers** —
> capabilities JHI has that Mergr does not (integrated financials/valuation/macro/SMB) —
> which are flagged and **discussed together as a team**, not invented unilaterally.
>
> **RATIONALE (why we mirror — Founder, 2026-07-17):** the target audience (institutional
> PE/M&A practitioners, advisors, search funders) **already speaks this jargon.** Standard
> terminology = zero learning curve, instant credibility, and **no confusion**. Invented
> terms create hesitation, and hesitation = **missed opportunities / lost conversions.**
> Familiar language is a conversion and trust decision, not just a style choice.

### L.0 The two-sector product model (MASTER FRAMEWORK — disclosure is hierarchical)
The application's core nomenclature is organized into **two sectors**, each disclosing its
own definition. Disclosure is **hierarchical: Sector → Group → Item**, every level with its
own definition. This is the template for JHI's TOC.

| Sector | Mergr disclosed definition (verbatim) | Contents |
|---|---|---|
| **(A) Search the Database** | "Pick a data type to open its dedicated search interface — each is built for that record type." | record-type entities → see L.3 |
| **(B) Tools & Insights** | "Pre-built tools that turn the database into focused answers." | tools grouped by job-to-be-done → see L.4 |

- **Group-level disclosure (inside B), verbatim:** Working a Live Deal — "You have a mandate
  — find the right counterparties." · Find New Opportunities — "Surface candidates you don't
  know about yet." · Research a Firm or Company — "Build context on a known entity." ·
  Market Intelligence — "Macro view across the database."
- **JHI build target:** two parallel sectors, each with a disclosed sector definition; then
  groups (with taglines) and items (with definitions), all written to the institutional bar.
- **NOTE:** the storefront "Solution for [segment]" pages (L.1) are a **separate marketing
  layer**, NOT the product TOC. Core product nomenclature = Sectors A + B above.

### L.1 Storefront — "Solution for [segment]" (marketing layer; name + disclosed definition + facets)
Each Mergr segment page discloses a **range descriptor** + a **facet list** (its
definition). Capture all 8 verbatim, then build JHI parallels. Confirmed so far:
- **M&A Advisors** — *"Legal & Financial, Boutique to Multinational"* → M&A Analytics ·
  M&A Client Lists · Advisory Connections · Sector Coverage · M&A Contacts.
- **Private Equity** — *"Small to Mega, Generalist & Specialist"* → Investment Criteria ·
  M&A History · Portfolio Breakdown · M&A Analytics · Professionals w/ Contact Info ·
  Office Locations · M&A Connections.
- **NEEDED (capture segment pages):** Acquirers/Investors · Lenders · Corporate ·
  Recruiters · Service Providers · Wealth Advisors (range descriptor + facet list each).

JHI mirrors Mergr's segment names verbatim (only the brand prefix changes: "JHI for [X]"):
| JHI segment (= Mergr, "JHI for …") | Range descriptor + facets (adopt from Mergr segment page) |
|---|---|
| Acquirers / Investors | _capture from Mergr page_ |
| M&A Advisors | "Legal & Financial, Boutique to Multinational" → M&A Analytics · Client Lists · Advisory Connections · Sector Coverage · Contacts |
| Private Equity | "Small to Mega, Generalist & Specialist" → Investment Criteria · M&A History · Portfolio Breakdown · M&A Analytics · Professionals w/ Contacts · Office Locations · M&A Connections |
| Lenders | _capture from Mergr page_ |
| Corporate | _capture from Mergr page_ |
| Recruiters | _capture from Mergr page_ |
| Service Providers | _capture from Mergr page_ |
| Wealth Advisors | _capture from Mergr page_ |

**OUTLIER (JHI-added segment — DISCUSS AS A TEAM):** Research & Analysts (JHI's research
identity has no direct Mergr segment). To decide together whether to add + how to frame.

### L.2 Storefront — Product menu (Mergr) → JHI
| Mergr | JHI candidate |
|---|---|
| Pricing · Free Trial · Log In | Pricing · Free Trial · Log In |
| Custom Exports / API | Data Exports & API |
| AI Connection | Ask JHI / Intelligence Query |
| Browse | Browse |
| Support Docs · Search Guides · Search Examples | Support Docs · Guides · Examples |
| PitchBook Alternative | (positioning line — TBD) |

### L.3 Dashboard Tier 1 — "Search the Database" entities (MIRRORED verbatim)
JHI adopts Mergr's names AND definitions verbatim:
| JHI term (= Mergr) | Definition (adopted verbatim) |
|---|---|
| Private Equity | "By AUM, sector focus, geography & activity." |
| Companies | "By ownership, size & sector." |
| Transactions | "By date, value, deal type & sector." |
| M&A Advisors | "Banks & law firms by deal experience." |
| M&A Professionals | "Deal-team members by firm & role." |
| M&A Press Releases | "Full announcement archive across PE and strategic M&A." |

**OUTLIERS (JHI-added — DISCUSS AS A TEAM, not yet adopted):** Securities & Markets ·
Macro Series · SEC Filings (EDGAR). Rationale: JHI integrates market/macro/filing data
Mergr lacks. Names/definitions to be decided together, in Mergr's style.

### L.4 Dashboard Tier 2 — "Tools & Insights" (name + disclosed definition, verbatim)
**Group taglines (disclosed):** Working a Live Deal — "You have a mandate — find the right
counterparties." · Find New Opportunities — "Surface candidates you don't know about yet." ·
Research a Firm or Company — "Build context on a known entity." · Market Intelligence —
"Macro view across the database."

JHI adopts Mergr's tool names AND definitions verbatim:
| JHI tool (= Mergr) | Definition (adopted verbatim) |
|---|---|
| Buyer Match | "Rank likely PE & strategic buyers for a target." |
| Investor Match | "Score growth equity & PE investors that fit a company's profile." |
| Advisor Match | "Banks & law firms that fit a deal mandate." |
| Prospector | "Find targets or clients that look like a reference company." |
| Roll-Up Tracker | "Active roll-ups ranked by add-on cadence, with full lifecycle history." |
| Shed | "Inherited add-ons least likely to fit the new owner's thesis." |
| Investor Lookalikes | "Find PE firms similar to a reference — bigger, smaller, or same tier." |
| Dossier | "Full M&A profile: history, advisors, key people." |
| Lineage | "PE alumni network — where talent came from and went." |
| Ownership Graph | "Ownership eras, holds & exit signals." |
| Trading Partners | "Recurring buyer-seller pairings with activity timeline & sector mix." |
| Compare | "Side-by-side comparison of firms." |
| Rankings | "Sortable M&A leaderboards." |
| Analytics | "Market activity & sector trends." |
| Deal Flow Map | "Cross-border M&A flows by country, time window & keyword." |

**OUTLIERS (JHI-added tools — DISCUSS AS A TEAM):** Deal X-Ray · Quality of Earnings ·
Valuation (DCF/LBO/Search-Fund) · Risk Score. Rationale: JHI's integrated financials/SMB
diligence engine has no Mergr equivalent. Placement (which group) + Mergr-style
definitions to be decided together.

### L.5 Dashboard right rail (Mergr) → JHI
| Mergr | JHI candidate |
|---|---|
| Saved Searches | Saved Screens / Watchlist |
| Stats | Coverage Stats |
| Acquisitions — Top PE Firms; Exits — Top Corporates; M&A Engagements — Top Law Firms / Investment Banks | Insight widgets (Top Acquirers / Movers / Macro) |

### L.6 Record tabs (Mergr, verbatim) → JHI facets
| Record | Mergr tabs | JHI candidate facets |
|---|---|---|
| Company | Profile · M&A Activity · M&A Connections · M&A Advisors · Analytics | Overview · Financials & Ratios* · Valuation* · Transactions · Relationships · Advisors · Filings* · News · Risk* · Analytics (*JHI-added) |
| Firm/Investor | Profile · M&A Activity · Portfolio · Team · Offices · M&A Connections · Analytics | Profile · Investment Criteria · Activity · Portfolio · Team · Offices · Connections · Analytics |
| Advisor | Profile · M&A Team · Offices · M&A Advisory · M&A Clients · M&A Advisory Connections · Analytics | Profile · Team · Offices · Advisory · Clients · Connections · Analytics |
| Ownership Graph | Deal Topology · Maturity · Exit Signals · Advisor Relationships | Deal Topology · Maturity · Exit Signals · Advisor Relationships |

### L.7 Cross-entity pivot tabs (Mergr) → JHI
Company results pivot: Company M&A · PE Investors · Company Investors · Advisors →
JHI: Transactions · Investors · Advisors · (Filings/Comps). *(Preserve the pivot mechanic.)*

**TO VET:** the JHI candidates above (per K.3 process). Flag any "elementary" terms for
upgrade; confirm which Mergr terms to keep verbatim (Buyer Match, Prospector, Ownership
Graph, Lineage, Dossier read institutional and may carry over).

## Next (Day 4 preview, not started)
Synthesis: consolidate IA (nav + segments + language) + dashboard model + entity graph +
record templates + tool patterns + differentiation (Part I) + data sourcing (Part J) +
nomenclature & functional-output disclosures (Part K) into one restructure blueprint;
scope into reviewed, phased PRs.
