# Completed Platform Programming Scripts

Project: John Henry Investments, LLC Investment Intelligence Platform

Purpose: Save the completed platform programming setup, commands, file map, and source-script locations in one organized reference file.

## 1. Completed platform build status

- Platform type: Subscription investment intelligence SaaS prototype
- Framework: Next.js
- Language: TypeScript
- UI library: React
- Backend framework: FastAPI
- Backend language: Python
- Current build: Routed front-end platform application with backend API prototype and external integration interfaces
- Branch used for platform work: `cursor/compose-ai-agent-work-239d`

## 2. Package programming scripts

The runnable programming scripts are saved in `package.json`.

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint .",
    "typecheck": "next typegen && tsc --noEmit"
  }
}
```

### Script purpose

| Script | Command | Purpose |
| --- | --- | --- |
| Development server | `npm run dev` | Runs the local Next.js development server |
| Production build | `npm run build` | Builds the platform for production |
| Production server | `npm run start` | Starts the built production application |
| Lint check | `npm run lint` | Checks code quality with ESLint |
| Type check | `npm run typecheck` | Generates Next.js route types and checks TypeScript |

## 3. Setup script commands

Use these commands to install and run the saved platform application.

```bash
npm install
npm run dev
```

Then open the local development URL shown in the terminal.

## 4. Verification script commands

Use these commands to verify that the completed platform build is healthy.

```bash
npm run typecheck
npm run lint
npm run build
npm audit --audit-level=moderate
cd backend
python3 -m compileall app tests
python3 -m pytest
python3 -m ruff check .
```

Expected result:

- TypeScript passes
- ESLint passes
- Next.js production build passes
- npm audit reports no moderate-or-higher vulnerabilities
- Backend Python modules compile
- Backend service tests pass
- Backend Ruff lint passes

## 5. Completed route programming files

| Route | Source file | Purpose |
| --- | --- | --- |
| `/` | `src/app/page.tsx` | Public platform overview, subscription plans, modules, scoring model, technology stack, and long-term vision |
| `/dashboard` | `src/app/dashboard/page.tsx` | Investor command center with portfolio metrics, market widgets, market signals, and AI recommendations |
| `/opportunities` | `src/app/opportunities/page.tsx` | Investment and acquisition opportunity engine with scores, recommendations, theses, and metrics |
| `/due-diligence` | `src/app/due-diligence/page.tsx` | AI due diligence center with document intake and sample risk-review queue |
| `/portfolio` | `src/app/portfolio/page.tsx` | Portfolio allocation, cash flow, asset tracking, and wealth projection scenarios |
| `/reports` | `src/app/reports/page.tsx` | John Henry Intelligence Center report generation workflow |
| `/assistant` | `src/app/assistant/page.tsx` | Private AI research assistant workflow examples |

## 6. Shared application programming files

| File | Purpose |
| --- | --- |
| `src/app/layout.tsx` | Root application layout and metadata |
| `src/app/globals.css` | Global platform styling, responsive layouts, app shell styles, cards, dashboards, and route-specific UI classes |
| `src/components/platform-shell.tsx` | Shared platform navigation and page shell component |
| `src/lib/platform-data.ts` | Typed product data for pricing, users, dashboard metrics, market signals, opportunities, diligence, portfolio, reports, assistant workflows, score categories, and technology stack |

## 7. Backend programming files

| File | Purpose |
| --- | --- |
| `backend/pyproject.toml` | Backend package metadata and dependencies |
| `backend/app/main.py` | FastAPI application entrypoint, CORS, health checks, and router registration |
| `backend/app/database.py` | SQLAlchemy database engine and session setup |
| `backend/app/db_models.py` | Persistent organizations, users, memberships, subscriptions, and audit-log tables |
| `backend/app/security.py` | Password hashing and signed bearer token helpers |
| `backend/app/dependencies.py` | Protected endpoint and admin dependencies |
| `backend/app/foundation_models.py` | Auth, account, subscription, billing, and audit-log schemas |
| `backend/app/foundation_services.py` | Registration, login, subscription, checkout, webhook, and audit-log services |
| `backend/app/models.py` | Pydantic models for accounting, reports, dashboards, and CRM |
| `backend/app/store.py` | In-memory prototype repository with seeded chart of accounts, journal entries, and CRM data |
| `backend/app/services.py` | Accounting, reporting, dashboard, and CRM service logic |
| `backend/app/routers/accounting.py` | Chart of accounts, journal entry, and trial balance endpoints |
| `backend/app/routers/auth.py` | Registration, login, and current-user endpoints |
| `backend/app/routers/billing.py` | Plan, subscription, checkout, webhook, and audit-log endpoints |
| `backend/app/routers/reports.py` | Audit and financial report endpoints |
| `backend/app/routers/dashboards.py` | Executive dashboard endpoint |
| `backend/app/routers/crm.py` | CRM contact, deal, activity, and summary endpoints |
| `backend/app/routers/integrations.py` | Banking, vendor, Microsoft Office, accounting, and CRM integration endpoints |
| `backend/tests/test_services.py` | Backend service tests |
| `backend/tests/test_foundation.py` | Authentication, billing, subscription, and audit-log tests |
| `backend/tests/test_integrations.py` | Backend integration service tests |
| `backend/tests/test_api.py` | Backend API route tests |
| `backend/README.md` | Backend setup, route map, examples, verification, and production next steps |

## 8. Configuration programming files

| File | Purpose |
| --- | --- |
| `package.json` | Project metadata, dependencies, npm scripts, and PostCSS override |
| `package-lock.json` | Locked dependency versions |
| `next.config.mjs` | Next.js configuration |
| `tsconfig.json` | TypeScript configuration |
| `eslint.config.mjs` | ESLint configuration for Next.js and TypeScript |
| `next-env.d.ts` | Next.js generated type references |
| `.gitignore` | Ignores build output, dependencies, environment files, logs, and TypeScript cache files |

## 9. Documentation files saved with the programme

| File | Purpose |
| --- | --- |
| `README.md` | Project overview, route map, setup commands, and documentation links |
| `docs/SRC_CODE_AUDIT.md` | Front-end source-code audit, automated check results, findings, and remediation plan |
| `docs/SYSTEM_FLOWCHARTS_AND_PROCESS_MAPS.md` | End-to-end flowcharts, module process flows, feedback loops, interface protocols, and dependency maps |
| `docs/investor_package/` | Pitch deck, PowerPoint, Excel financial model, DCF, projections, charts, and generator scripts |
| `docs/FIVE_STAGE_VALUATION_MODEL.md` | Five-stage valuation ranges, market-cap/equity-value scenarios, probabilities, and milestone valuation requirements |
| `docs/PRODUCT_BLUEPRINT.md` | Full SaaS platform product blueprint and route map |
| `docs/PROJECT_MANAGEMENT_CHECKLIST.md` | Completed work checklist, remaining launch tasks, MVP checklist, and the Founder action items |
| `docs/CLOUD_STORAGE_AND_CAPACITY_PLAN.md` | Cloud storage, database, network, processing, cache, and monitoring estimates |
| `docs/ESTIMATED_PLATFORM_COSTS.md` | Estimated monthly, annual, provider, AI, integration, compliance, and operating costs |
| `docs/PROJECTED_EBITDA_MODEL.md` | Projected EBITDA, margin, break-even, and sensitivity scenarios |
| `docs/STAFFING_LEGAL_PRO_FORMA.md` | Staffing, one-person operation, legal expenditure, compliance, and adjusted EBITDA projections |
| `docs/COMPENSATION_AND_PRO_SERVICES_PROJECTIONS.md` | Per-person compensation, professional services, in-house conversion, quarterly and annual projections |
| `docs/JOB_DESCRIPTIONS_AND_STAFFING_REQUIREMENTS.md` | Department-level job descriptions, skill requirements, legal personnel, and staffing requirements |
| `docs/NEXT_ACTION_ITEMS_TO_DEFINE.md` | Decision checklist for the next platform programming phase |
| `docs/AUTH_DATABASE_BILLING_FOUNDATION.md` | Authentication, database persistence, and billing foundation details |
| `docs/NEXT_PROGRAMMING_MILESTONE.md` | Recommended next implementation sequence and add-on programming backlog |
| `docs/FAILED_PROGRAMMING_CODES.md` | Failed commands, error messages, causes, and fixes from platform programming |
| `docs/COMPLETED_PLATFORM_PROGRAMMING_SCRIPTS.md` | This saved programming-script reference file |
| `AI_AGENT_WORK_SUMMARY.md` | Summary of AI-agent-created application work in the repository |
| `backend/README.md` | Backend API setup and route documentation |

## 10. Dependency setup

The platform currently uses these main dependencies:

```json
{
  "dependencies": {
    "next": "^16.2.9",
    "react": "^19.2.7",
    "react-dom": "^19.2.7"
  },
  "devDependencies": {
    "@types/node": "^26.0.0",
    "@types/react": "^19.2.17",
    "@types/react-dom": "^19.2.3",
    "eslint": "^9.39.4",
    "eslint-config-next": "^16.2.9",
    "typescript": "^6.0.3"
  }
}
```

The project also includes this override to keep the dependency audit clean:

```json
{
  "overrides": {
    "postcss": "^8.5.15"
  }
}
```

Backend dependencies are saved in `backend/pyproject.toml`:

```toml
dependencies = [
  "fastapi",
  "uvicorn[standard]",
  "pydantic"
]
```

## 11. One-command local verification bundle

Run this full command when checking the saved platform:

```bash
npm install && npm run typecheck && npm run lint && npm run build && npm audit --audit-level=moderate && python3 -m pip install -e "backend[dev]" && cd backend && python3 -m compileall app tests && python3 -m pytest && python3 -m ruff check .
```

## 12. Backend API commands

Install backend dependencies:

```bash
python3 -m pip install -e "backend[dev]"
```

Run backend API:

```bash
cd backend
python3 -m uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## 13. Deployment preparation commands

After choosing the hosting provider, use the production build script as the required deployment check:

```bash
npm install
npm run build
```

Recommended production environment variables to define in the future:

```bash
NEXT_PUBLIC_APP_URL=
DATABASE_URL=
SUPABASE_URL=
SUPABASE_ANON_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
MARKET_DATA_API_KEY=
```

These variables are placeholders for the next backend, billing, database, and AI integration phases. Do not commit real secret values to the repository.

## 14. Next programming milestones

- Add authentication and protected routes
- Add Supabase/PostgreSQL database schema
- Add Stripe subscription billing
- Add AI assistant backend endpoint
- Add market and macro data integrations
- Add document upload and secure storage
- Add report PDF generation
- Add role-based permissions and team accounts
- Add automated tests for critical workflows
- Replace backend in-memory store with PostgreSQL/Supabase persistence
- Add journal entry approval workflow and immutable audit logs
- Connect Plaid or MX for live banking sync
- Connect QuickBooks, NetSuite, or Bill.com for live vendor/accounting sync
- Connect Microsoft Graph for Excel and Word file generation and storage
- Connect Salesforce for enterprise CRM sync if required
