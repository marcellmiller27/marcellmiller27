# Enterprise Architecture — Review & Adjustments

> JHI-SIG: 69M2705M · JHI Research & Analytics Firm, Inc. (proprietary)
> Review of the proposed enterprise backend (30+ modules, six suites, ~180–250 modules /
> 1,500–2,500 tables / 6,000–10,000 endpoints, 600–1,000-page SRS). **Planning artifact —
> no build until the Founder authorizes.** Companion: `docs/BACK_OFFICE_ERP_BUILD_PLAN.md`,
> `docs/SYSTEM_ADMINISTRATOR_MODULE.md`.

## 0. Verdict
The **vision is right** and the module taxonomy is comprehensive — this is a genuine
enterprise ERP + research platform. My adjustments are about **how to get there without
sinking the firm**: build the moat, integrate commodity back-office, phase by revenue, and
replace the giant upfront SRS with a living spec. The full 250-module count is a **10-year
ceiling**, not a near-term build target.

## 1. Four adjustments that matter most
### A. Build vs. Buy vs. Configure (the biggest one)
Building all ~250 modules from scratch — including payroll, HRIS, tax provisioning, BI
tools, SSO — would take **hundreds of engineer-years** and dwarf the actual product. Split
every module three ways:
- **BUILD (our moat — this *is* JHI):** Research Operations, AI Analytics Engine, Market/Economic Data ingestion, the subscriber product (dashboards, screener, entity records, diligence tools), the **Editorial** system, and the proprietary scoring/models. Never outsource these.
- **CONFIGURE / extend (we've started; finish in-house):** RBAC/System Admin, Accounting GL, AP/AR, Bank Reconciliation, Subscription, Billing, CRM, Sales/commissions, Fixed Assets/Depreciation/Amortization, Support. These run the firm and are tightly coupled to our data — worth owning.
- **BUY / INTEGRATE (commodity — do NOT rebuild):** Payroll + payroll tax (Gusto/Rippling/ADP), HRIS/benefits, SSO/IdP (Okta/Auth0/WorkOS), e-signature (DocuSign/Dropbox Sign), Cap table/equity (Carta/Pulley), Tax provision (CPA + Avalara for sales tax), Treasury/banking (bank + Mercury/Brex), BI tools (Metabase/Power BI/Tableau), advertising/email marketing (existing SaaS). Integrate via API; don't reinvent.

*Why:* every engineer-hour spent rebuilding payroll is an hour not spent on the research edge that customers actually pay for.

### B. Scale numbers — right-size the target
180–250 modules / 1,500–2,500 tables / 6,000–10,000 endpoints is **Workday/NetSuite/SAP class**. Keep it as the **long-horizon ceiling**, but set the **first 12–18 months** at roughly **15–25 modules** that (1) drive revenue and (2) run the firm — everything else is deferred or integrated. Grow the surface as headcount and revenue justify, not before.

### C. Replace the 600–1,000-page upfront SRS with a *living* spec
A giant waterfall SRS written before code is **usually obsolete before it ships** and is where budgets die. Recommended instead:
- **A durable core spec (~40–80 pages, living):** the module registry, the canonical **data model**, the **RBAC/permissions** model, API conventions, the accounting/GL rules, and naming standards.
- **Thin per-module specs (5–15 pages each), written just-in-time** right before that module is built.
This prevents costly redesign *better* than a monolith, because each spec is current when engineering uses it.

### D. Internal ops vs. subscriber product — draw the line
Most of these modules run **JHI the company** (internal: HR, Payroll, Legal, Treasury, our own GL). Only a subset is the **customer-facing product** (Research, Analytics, Editorial, records, screening). Keep two planes:
- **Corporate/back-office plane** — staff-only, single-tenant (JHI's books/ops).
- **Product plane** — multi-tenant, subscriber-facing.
This split drives tenancy, RBAC, and where each of the six suites lives.

## 2. Adjusted suite structure (your six, mapped + tagged)
Your six suites are sound. Each module tagged **[Build]**, **[Configure]**, or **[Buy/Integrate]**.

**1. Corporate Operations** (internal, staff-only)
Executive Dashboard [Build] · HR [Buy: HRIS] · Payroll [Buy] · Legal + Corporate Secretary + Cap Table [Buy: Carta] · Compliance [Configure] · Procurement [Configure] · Administration [Configure] · Investor Relations [Configure].

**2. Finance & Accounting ERP** (internal)
General Ledger [Configure ✅ core exists] · AP [Configure] · AR [Configure] · Bank Reconciliation [Configure] · Banking/Treasury [Buy + Configure] · Budgeting/Forecasting [Configure] · Tax [Buy: CPA/Avalara + Configure provision] · Fixed Assets [Build/Configure] · Depreciation [Build] · Amortization [Build] · Intangibles [Configure] · Financial Reporting [Configure ✅ partial].

**3. Commercial Platform** (revenue engine)
CRM [Configure ✅ backend exists] · Sales + Commissions [Build/Configure] · Subscription Management [Configure ✅] · Billing [Configure ✅ + live Stripe] · Customer Success [Configure] · Marketing [Buy/Integrate] · Customer Support [Configure ✅ backend].

**4. Research & Analytics** (THE MOAT — build)
Market/Economic Data ingestion [Build ✅ FRED/BEA/BLS live] · Research Library/Notes [Build] · AI Analytics Engine + LLM [Build] · Model Portfolios/Screening/Records [Build ✅ partial] · Editorial/Newsletters [Build ✅ live] · Watchlists/Alerts [Build].

**5. Technology Platform**
Software Engineering/DevOps [Configure] · IT Operations/Cloud [Buy: AWS + Configure] · Cyber Security/SSO [Buy: IdP + Configure] · API Management [Configure].

**6. Enterprise Intelligence**
Data Warehouse/Lake [Buy: Snowflake/BigQuery] · BI/Dashboards [Buy: Metabase/Power BI] · Exec Reporting/Forecast models [Build on top].

**Cross-cutting (every module):** Workflow automation, approvals, notifications, e-signature, versioning, **RBAC**, and **complete audit trail** — build these **once** as shared platform services, not per module.

## 3. What already exists (extend, don't restart)
From the codebase inventory: functional **GL** (COA, JE, trial balance), **CRM backend**, **billing + verified Stripe webhook**, **integration scaffolding** (vendor bills + bank feed that already *suggest* journal entries), **research/market data** (FRED/BEA/BLS live), and the **editorial** system. The near-term ERP work is mostly **finishing** these + the RBAC lockdown — not greenfield.

## 4. Recommended sequencing (revenue + foundation first)
Reconciles this blueprint with `BACK_OFFICE_ERP_BUILD_PLAN.md` (A–F) and revenue priority:
1. **Foundation — System Admin / RBAC P0** *(prerequisite for all staff-only modules)*: roles/permissions, endpoint lockdown, staff gate, `/admin`, audit, shared workflow/audit services.
2. **Revenue engine — Commercial Platform**: Subscription + **live Billing (Stripe)** + CRM UI + Sales/commissions + Support. (Drives cash; validates the funnel.)
3. **Firm books — Finance & Accounting ERP**: Accounting depth (statements, close) + AP/AR + Bank Reconciliation + Fixed Assets/Depreciation/Amortization. (Real month-end close.)
4. **Moat (parallel, ongoing) — Research & Analytics**: keep advancing the product (records/entity graph, AI, editorial visuals).
5. **Integrate commodity** as needed — Payroll, HRIS, Cap table, SSO, BI, Tax (via SaaS), rather than building.
6. **Enterprise Intelligence + the long tail** — once scale justifies (data warehouse, BI, IR, advanced Treasury/Tax provision).

## 5. Risks if we build it all in-house up front
- **Focus dilution** — the research/AI edge (why customers pay) starves while we rebuild payroll/BI.
- **Maintenance drag** — 2,000 tables and 8,000 endpoints is a permanent ops/security burden for a lean team.
- **Compliance exposure** — payroll/tax/HR done wrong is legal risk; specialized SaaS is safer + cheaper.
- **Time-to-revenue** — a 600–1,000-page SRS + 250 modules delays the cash-generating pieces by years.

## 6. Open questions for the Founder
1. **Confirm Build/Buy posture** — OK to **integrate** commodity back-office (Payroll, HRIS, SSO, Cap table, BI, Tax) and **build** only the moat + revenue/finance core? (My strong recommendation.)
2. **First 12–18 months scope** — target ~15–25 modules; confirm the **revenue-engine-first** sequence (RBAC → Commercial → Finance) after the Phase-A foundation.
3. **SRS format** — agree to the **living core spec + just-in-time per-module specs** instead of the 600–1,000-page upfront SRS?
4. **Internal vs. product tenancy** — confirm the two-plane split (staff-only corporate/back-office vs. multi-tenant subscriber product).
5. **Priority within the revenue engine** — Billing-go-live first, or CRM/Sales UI first?

**Bottom line:** keep the grand blueprint as the north star; execute it as a **revenue-first, build-the-moat / integrate-the-commodity, phase-by-phase** program with living specs. That gets JHI to a real enterprise platform without betting the firm on a multi-year big-bang.
