# Platform Scope — Locked Decisions (2026-07-22)

> JHI-SIG: 69M2705M · JHI Research & Analytics Firm, Inc. (proprietary)
> The build/buy posture, confirmed by the Founder. Supersedes the heavier ERP scope in
> `docs/BACK_OFFICE_ERP_BUILD_PLAN.md` / `docs/ENTERPRISE_ARCHITECTURE_REVIEW.md`.

## The posture: build the moat + the cash register in-house; rent the rest
### Build in-house
- **The moat (build fully):** Research & Analytics, AI/Analytics engine, market/economic data ingestion, the subscriber product (records, screener, diligence), and the **Editorial** system.
- **The cash register (build just-enough):** RBAC / System-Admin, Subscription, **Billing (Stripe)**, **CRM/Sales** (assists the sales team), Support.
- **Chart of Accounts (KEEP in-house):** our canonical GAAP COA (`AccountDB`, ~130 accounts) stays as the firm's controlled chart + reporting/analysis structure. Day-to-day bookkeeping is mapped to/synced with the third-party accounting app.
- **Revenue analytics + Executive dashboard (build):** poll our own subscription/billing data (Stripe) for MRR/ARR/churn/LTV/CAC + pull financials from the accounting app → unified CEO/KPI dashboard, categorized to our COA.

### Rent (third-party, light API integration — minimize G&A)
AP/AR, bank reconciliation, payroll + payroll tax, HR/HRIS/benefits, income/sales tax, treasury/banking, BI tools, SSO/IdP, cap-table/equity. Start on the cheap tier (e.g., **QuickBooks/Xero → NetSuite**, **Gusto**, **Carta**, **Avalara/CPA**, **Mercury/Brex**, **Metabase/Power BI**, **Okta/WorkOS**), scaling with company growth.

## What this means for the roadmap
- The heavy in-house **Finance-ERP** phases (full AP/AR, bank rec, depreciation/amortization, month-end close automation) are **dropped** in favor of the third-party accounting app + light integrations.
- **KEEP:** COA (in-house), revenue analytics, exec dashboard.
- Near-term build order: **RBAC foundation → revenue engine (Subscription/Billing/CRM/Sales) → moat (ongoing) → thin ops/G&A integrations + exec dashboard.**

## SRS approach
No 600–1,000-page upfront SRS. Maintain a **living core spec** (module registry, data model, RBAC/permissions, API conventions, GL/COA rules, naming) + **thin per-module specs written just-in-time** before each build.

## Founder actions to enable this
- `AUTH_JWT_SECRET` — ✅ added.
- `JHI_STAFF_EMAILS` — add Founder + employee emails to Secrets (grants back-office access under the RBAC foundation).
- Later: third-party app API keys (QuickBooks, Gusto, etc.) when those integrations are built.
