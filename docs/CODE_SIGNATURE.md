# JHI Code Signature — `69M2705M`

The founder's unique provenance signature **`69M2705M`** is stamped as a header comment
on every source file in the John Henry Investments (JHI) codebase, labeled by subsystem.

## Signature format

Each file carries a single header comment (language-appropriate):

```
# JHI-SIG: 69M2705M | <Subsystem> | JHI Research & Analytics Firm, Inc. (proprietary)     (Python)
// JHI-SIG: 69M2705M | <Subsystem> | JHI Research & Analytics Firm, Inc. (proprietary)    (TS/TSX/JS)
/* JHI-SIG: 69M2705M | <Subsystem> | JHI Research & Analytics Firm, Inc. (proprietary) */ (CSS)
```

Placement rules:
- **Python / TS / CSS:** first line of the file.
- **Next.js `"use client"` files:** the signature is placed **immediately after** the
  `"use client";` directive (the directive must remain the first line for Next.js).

## Coverage

83 source files signed across backend (`backend/app`, `backend/tests`), frontend (`src`),
and `next.config.mjs`. Non-code/config files that cannot carry comments (e.g. JSON) are
intentionally excluded.

## Signature registry by subsystem

| Subsystem | Files |
| --- | --- |
| Platform spine | `backend/app/{main,config,rate_limit,database,db_models,dependencies,models,store,services,__init__}.py`, `backend/app/routers/__init__.py`, `backend/tests/{test_services,test_hardening}.py` |
| Identity, Auth & Security | `backend/app/{security,foundation_services,foundation_models,mobile_services,mobile_models}.py`, `backend/app/routers/{auth,mobile_auth}.py`, `backend/tests/{test_foundation,test_mobile_auth}.py`, `src/app/{login,register,mobile}/page.tsx` |
| Billing & Subscriptions | `backend/app/routers/billing.py`, `src/app/{pricing,account}/page.tsx` |
| Accounting & Reporting | `backend/app/{accounting_services,reporting_services}.py`, `backend/app/routers/{accounting,reports,dashboards}.py`, `backend/tests/{test_accounting_db,test_reports_db,test_api}.py`, `src/app/reports/page.tsx` |
| CRM | `backend/app/crm_services.py`, `backend/app/routers/crm.py`, `backend/tests/test_crm.py` |
| Market Data | `backend/app/{market_services,market_models}.py`, `backend/app/routers/market.py`, `backend/tests/test_market.py`, `src/components/live-market.tsx`, `src/app/dashboard/page.tsx` |
| Research & Opportunity Score | `backend/app/{research_services,research_models,opportunity_score}.py`, `backend/app/routers/research.py`, `backend/tests/test_research.py`, `src/app/{opportunities,assistant}/page.tsx` |
| Valuations | `backend/app/{valuation_services,valuation_models}.py`, `backend/app/routers/valuations.py`, `backend/tests/test_valuations.py`, `src/app/{portfolio,due-diligence}/page.tsx` |
| Support & AI Agents | `backend/app/{support_services,support_models,agents_services,agents_models}.py`, `backend/app/routers/{support,agents}.py`, `backend/tests/{test_support,test_agents}.py`, `src/app/{support,team}/page.tsx` |
| Growth / Leads | `backend/app/lead_models.py`, `backend/app/routers/leads.py`, `backend/tests/test_leads.py`, `src/components/waitlist-form.tsx`, `src/app/{join,page}.tsx` |
| External Integrations | `backend/app/routers/integrations.py`, `backend/tests/test_integrations.py` |
| Frontend shell | `src/app/{layout,globals.css}`, `src/components/{platform-shell,logo}.tsx`, `src/lib/platform-data.ts` |
| Build & Deploy | `next.config.mjs` |

## Maintaining the signature

When adding a **new source file**, include the signature header for its subsystem as the
first line (or immediately after `"use client";`). The token `JHI-SIG: 69M2705M` makes
the provenance greppable:

```bash
rg -l "JHI-SIG: 69M2705M"        # list all signed files
rg -c "JHI-SIG: 69M2705M" | wc -l  # count
```

> The signature is a provenance/authorship marker. It is **not** a security control and
> does not replace license headers or copyright registration; pair it with a `LICENSE`
> and formal IP records (see `docs/IP_INTANGIBLES_AMORTIZATION.md`).

## Reconciliation status (updated 2026-07-03)

This initial stamp was a **point-in-time** pass. Files created afterward (on separate,
unmerged feature branches) were stamped individually and still need a final consolidated
sweep once the feature PRs merge into the base.

**Stamped since the initial pass (on their branches):**
- `src/components/{live-reports,live-opportunities,live-valuations,live-assistant,live-account}.tsx` (PR #34)
- `backend/app/integration_services.py` (PR #33)
- `backend/app/fundamentals.py` (PR #30)
- `backend/app/{webauthn,billing_webhook}.py` (PR #17)

**Still to stamp in the consolidated sweep** (new since the initial pass):
- `src/components/live-market.tsx` (predates the initial stamp)
- New backend tests: `test_security_encryption.py`, `test_security_tokens.py`,
  `test_billing_webhook.py`, `test_webauthn.py`, `test_fundamentals.py`, `test_reports_db.py`
- Any file added on a branch not covered above.

**Recommended:** after the feature PRs merge, re-run the stamping (idempotent — it skips
files already containing `JHI-SIG: 69M2705M`) so the whole tree is covered in one pass.

## Entity attribution — pending (JHI Research & Analytics Firm, Inc.)

The founder mark `69M2705M` is **entity-agnostic** and stays on every file. The **copyright
/ entity attribution** currently reads `JHI Research & Analytics Firm, Inc. (proprietary)` in headers and
`John Henry Investments, LLC` in `LICENSE`. Per the two-entity decision
(`docs/COMPANY_POSTURE_AND_COMPLIANCE.md`), the **platform IP will belong to
JHI Research & Analytics Firm, Inc.** — so the attribution should change to that entity, but
**only after** (1) the Wyoming corporation is **formed** and (2) the **platform IP is
assigned** to it. Renaming to a not-yet-formed entity would be premature/inaccurate.

**Plan:** form entity → assign IP → then one consolidated pass updates the entity name in all
`JHI-SIG` headers **and** the `LICENSE` from "John Henry Investments" to
"JHI Research & Analytics Firm, Inc." (keeping the `69M2705M` mark unchanged).
