# JHI Code Signature — `69M2705M`

The founder's unique provenance signature **`69M2705M`** is stamped as a header comment
on every source file in the John Henry Investments (JHI) codebase, labeled by subsystem.

## Signature format

Each file carries a single header comment (language-appropriate):

```
# JHI-SIG: 69M2705M | <Subsystem> | John Henry Investments (proprietary)     (Python)
// JHI-SIG: 69M2705M | <Subsystem> | John Henry Investments (proprietary)    (TS/TSX/JS)
/* JHI-SIG: 69M2705M | <Subsystem> | John Henry Investments (proprietary) */ (CSS)
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
