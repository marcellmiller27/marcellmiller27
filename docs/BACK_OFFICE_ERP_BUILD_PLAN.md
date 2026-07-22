# Back-Office / ERP — Build Plan (for Founder review)

> JHI-SIG: 69M2705M · JHI Research & Analytics Firm, Inc. (proprietary)
> **Planning artifact — no code is built until the Founder authorizes a phase.**
> Scope: System Administrator, Accounting (+ sub-modules), CRM, Sales, AP, AR, Billing,
> and month-end close — the firm's back office. Companion: `docs/SYSTEM_ADMINISTRATOR_MODULE.md`,
> `docs/SALES_COMMISSION_MODEL.md`, `docs/CHART_OF_ACCOUNTS*`.

## 0. Guiding principles
- **Extend, don't duplicate.** We already have a working GL core, CRM backend, billing + Stripe webhook, and integration scaffolding — build on those.
- **RBAC first.** The back office is staff-only and touches money. Secure access (roles + permissions + endpoint lockdown) is the **prerequisite** for every module below.
- **Sub-ledgers roll up to the GL.** AP, AR, fixed assets, and billing each post to journal entries — one source of truth (the trial balance), enabling real month-end close.
- **One module per PR**, phased, each tested with evidence, for your review/merge.

## 1. What exists today (so we extend it)
| Domain | State | Foundation to reuse |
|---|---|---|
| **Accounting — core GL** | Functional | `AccountingService` (COA ~130 accounts, JE post + balanced validation, trial balance), `/api/v1/accounting/*`, `live-accounting.tsx` UI |
| Accounting — reports | Partial | `ReportingService` (P&L/BS/CF from trial balance), `/reports/*` (no UI yet) |
| Accounting — close / bank rec / D&A | **Stub/missing** | COA has the accounts; no schedules, no rec workflow, no period close |
| **System Admin / RBAC** | Stub | `foundation_services` (auth/org/membership/audit), `AuditLogDB`, `dependencies.py` (`require_admin`), `docs/SYSTEM_ADMINISTRATOR_MODULE.md` design |
| **CRM** | Backend partial, **no UI** | `crm_services` + `/crm/*` (contacts, deals, activities), `CRMDealDB` (lead→closed) |
| **Sales / commissions** | Docs only | `docs/SALES_COMMISSION_MODEL.md`, CRM deals, billing tiers |
| **AP / AR** | Stub | COA (AR 1100 / AP 2000), integrations `VendorBillDB` + `suggested_journal_entry`, bank feed `BankingTransactionDB` |
| **Billing / Stripe** | Partial | `/billing/*`, `SubscriptionDB`, verified webhook (checkout is mock) |

**Critical gap flagged by the audit:** most ERP APIs (accounting, reports, CRM, dashboards, pipeline) currently have **no auth** — anyone can call them. Lockdown is P0.

## 2. Target module map
- **System Administrator** — identity, roles→permissions (RBAC), org management, entitlements, feature flags, audit viewer, API keys, system health. (JHI super-admin + customer org-admin.)
- **Accounting** — the hub, with sub-modules:
  - **Chart of Accounts (COA)** — manage accounts + hierarchy.
  - **Journal Entries (JE)** — draft → review → post lifecycle, reversals, recurring.
  - **Reports** — full P&L, Balance Sheet, Cash Flow, Trial Balance, GL detail (by COA category), with UI + export.
  - **Bank Reconciliation** — match imported bank transactions to GL, clear, post adjustments.
  - **Depreciation** — fixed-asset register + schedules → automated periodic JEs.
  - **Amortization** — intangibles / prepaids / loan schedules → automated JEs.
  - **Month-End Close** — checklist, accruals, period lock, reconciliation status, retained-earnings roll.
- **CRM** — contacts, deal pipeline (board), activities; links to AR + billing.
- **Sales** — reps, quotas, **commission engine** (from `SALES_COMMISSION_MODEL` + Stripe MRR), payout tracking.
- **Accounts Payable (AP)** — vendor master, bill entry/approval, payment runs, aging, 1099; posts to GL.
- **Accounts Receivable (AR)** — customer master, invoices, credit memos, cash receipts, aging; Stripe invoice sync; posts to GL.
- **Billing** — live Stripe (checkout + customer portal), entitlement enforcement, automatic revenue-recognition JEs (billing → AR/deferred revenue).

## 3. Cross-cutting foundation — Phase A (do first)
**System Administrator / RBAC P0** (matches `SYSTEM_ADMINISTRATOR_MODULE.md`):
1. **Roles & permissions:** add internal roles (e.g., Super-Admin/Founder, Controller/Accountant, Sales Manager, Sales Rep, Employee-read-only) + a permission matrix; `require_permission(...)` dependency.
2. **Lock down endpoints:** put every back-office API behind auth + permission (accounting, reports, CRM, AP/AR, admin) behind an `ENFORCE_AUTH` flag → on.
3. **Staff gate:** the "staff/employee" concept from the RBAC work (#104) so the back office is **only** visible/accessible to Founder + employees (subscribers never see it).
4. **Admin UI** (`/admin`): Users (invite/deactivate/role/reset-MFA), Roles, Organizations, Audit Log viewer, Feature flags.
5. **Audit everywhere:** extend `AuditLogDB` writes to all back-office mutations.

*Why first:* every module below is money/PII and staff-only; without this it's exposed.

## 4. Module build detail (extends existing code)
### Accounting
- **COA:** UI to create/edit/deactivate accounts + parent/child hierarchy + account types; reuse `AccountDB`/service.
- **JE lifecycle:** add `status` (draft/pending/posted/void), approval, reversal, recurring templates; keep balanced-entry validation.
- **Reports:** upgrade `ReportingService` to full statements grouped by COA category + comparative periods; build `/reports` + `/dashboards/executive` **UI**; export (PDF via existing reportlab, XLSX via openpyxl).
- **Bank Reconciliation:** new subledger UI — pull `BankingTransactionDB`, match to GL lines, mark cleared, post adjusting JEs; reconciliation report.
- **Depreciation:** `FixedAssetDB` (cost, in-service date, method, life, salvage) → schedule generator → monthly JE (Dr depreciation 6600 / Cr accum 1590).
- **Amortization:** `AmortizationScheduleDB` for intangibles/prepaids/loans → periodic JE (e.g., Cr 1790 / Dr 6610).
- **Month-End Close:** close checklist (accruals, rec status, subledger tie-out), **period lock**, retained-earnings roll to a new period.

### CRM
- Build the **frontend** on the existing backend: pipeline board (lead→closed), contact records, activity timeline; add PATCH (stage, owner), search. Link deals → AR invoices + billing.

### Sales
- `SalesRepDB`, quotas, **commission rules engine** driven by `SALES_COMMISSION_MODEL` (prepaid MSA, 15% + year-end bonus) reading Stripe MRR / CRM closed-won; payout ledger; rep dashboard. (Distinct from the M&A `pipeline`.)

### Accounts Payable
- `VendorDB` + `BillDB` (from the integrations `VendorBillDB` suggestions) → approval → **post to GL** (Dr expense / Cr AP 2000) → payment runs (Cr cash / Dr AP) → AP aging + 1099.

### Accounts Receivable
- `CustomerDB` + `InvoiceDB` + `PaymentDB` → post to GL (Dr AR 1100 / Cr revenue or deferred 2060) → cash receipts/application → AR aging; **sync Stripe invoices/payments** into AR.

### Billing (hardening)
- Live Stripe Checkout + Customer Portal (needs live keys); entitlement enforcement beyond `require_premium`; **automatic revenue-recognition JEs** from webhook events (billing → AR/deferred revenue → month-end recognition).

## 5. Recommended phasing (each = its own tested PR)
- **Phase A — System Admin / RBAC P0** *(prerequisite)*: roles/permissions, endpoint lockdown, staff gate, `/admin` UI, audit.
- **Phase B — Accounting depth**: COA mgmt UI, JE lifecycle/approval, full statements + reports UI, close scaffolding.
- **Phase C — Sub-ledgers**: AP (bills→GL, payments, aging) + AR (invoices, receipts, aging, Stripe sync) + Bank reconciliation.
- **Phase D — Fixed assets**: Depreciation + Amortization schedules → automated JEs.
- **Phase E — CRM + Sales**: CRM frontend; Sales reps + commission engine (MRR-driven).
- **Phase F — Billing + Close automation**: live Stripe, entitlements, revenue-recognition JEs, full month-end close orchestration + reconciliations.

## 6. Access model (who sees what)
- **Staff/employees (Founder + internal roles):** the entire back office (System Admin, Accounting + sub-modules, AP, AR, Sales, CRM), scoped by permission (e.g., a Sales Rep sees Sales/CRM, not the GL).
- **Subscribers (Tier 1–3):** the product only — never the back office.
- Enforced by the Phase-A RBAC (extends #104), not just menu hiding.

## 7. Immediate defect — newsletter Print/PDF crash (separate, small)
- **Cause:** the three editions call `window.print()` (`economic-newsletter.tsx`, `red-alerts.tsx`, `opportunity-scan.tsx`). In the forwarded/desktop viewer that call can crash the app ("shuts down").
- **Robust fix:** replace `window.print()` with a **server-generated PDF** using the existing `backend/app/pdf_export.py` (reportlab) — a `/api/v1/newsletters/{edition}/pdf` endpoint returns a branded, download-safe PDF. No browser print dialog, no crash; consistent output; reusable for the Step-B email attachment.
- **Interim (zero-risk) option:** remove the JS `window.print()` and label the button as "Download PDF" wired to the endpoint (or temporarily hide it) so nothing can crash.
- Small and isolated — **I can hotfix this immediately on your OK**, independent of the ERP phases.

## 8. Dependencies & risks
- **RBAC must land first** (Phase A) — do not expose GL/AP/AR/admin before it.
- **Stripe live keys** needed for Phase F (billing go-live); **bank-feed vendor creds** (Plaid/Bill.com) if we want live AP/AR feeds vs. manual entry.
- `AUTH_JWT_SECRET` — ✅ added.
- **Scope realism:** this is a multi-phase ERP program; each phase ships independently so value lands early (Phase A + B alone give a secure, real accounting back office).

## 9. Open questions for the Founder
1. **Real books vs. product:** Is this JHI's **own** internal accounting/ERP (our firm's books), a **productized** module we sell to subscribers, or **both**? (Changes the data model + tenancy.)
2. **Internal roles:** confirm the internal role set + who sees which sub-module (e.g., Super-Admin, Controller/Accountant, Sales Manager, Sales Rep, Employee-read-only).
3. **Priority after Phase A:** highest-value next — **Accounting depth (B)**, **AP/AR (C)**, or **Sales/CRM (E)**?
4. **Bank feeds:** live (Plaid/Bill.com) or manual entry first?
5. **Stripe:** go live now (Phase F) or keep mock until later?
6. **Print fix:** hotfix now (server-side PDF), or fold into a phase?
7. **Cadence:** confirm one-module-per-PR in the phase order above.
