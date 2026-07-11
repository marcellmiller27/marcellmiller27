# John Henry Investments Next Programming Milestone

## Milestone name

Authentication, Database Persistence, Billing, Security, and Production SaaS Foundation

## Milestone objective

Move the John Henry Investments platform from a prototype into a production-oriented SaaS foundation by adding persistent data, protected user access, subscription billing, secure integrations, audit controls, and operational monitoring.

## Current starting point

The repository already includes:

- Next.js and TypeScript front-end platform application
- Routed screens for dashboard, opportunities, due diligence, portfolio, reports, and AI assistant
- FastAPI backend prototype
- Accounting, audit report, financial report, dashboard, CRM, and integration API contracts
- External integration interfaces for banking, vendor systems, Microsoft Office, accounting systems, and CRM platforms
- Project management checklist and programming script documentation
- SQLAlchemy persistence foundation for organizations, users, memberships, subscriptions, and audit logs
- Authentication endpoints for registration, login, and current-user context
- Subscription billing foundation endpoints for plans, checkout-session contracts, webhooks, and billing audit logs

## Recommended build order

### Phase 1 - Authentication and access control

Priority: highest

Purpose: Users must have secure accounts before the application can safely store financial, CRM, accounting, or document data.

Programming tasks:

- [ ] Add production authentication provider integration
- [x] Add user registration API foundation
- [x] Add login API foundation
- [x] Add signed bearer-token session foundation
- [ ] Add protected front-end route enforcement
- [x] Add protected backend endpoint foundation
- [ ] Add multi-factor authentication support
- [ ] Add role-based access control
- [ ] Add plan-based feature entitlements
- [ ] Add admin, investor, advisor, CPA, attorney, banker, family office, and enterprise roles

Recommended implementation options:

- Supabase Auth
- Auth0
- Clerk
- AWS Cognito

Acceptance checklist:

- [ ] Unauthenticated users cannot access protected dashboards
- [ ] Authenticated users can access their dashboard
- [ ] Admin users can access admin routes
- [ ] Non-admin users cannot access admin routes
- [ ] API endpoints reject unauthorized requests
- [ ] User role and subscription plan are available to front end and backend

Suggested source areas:

- `src/app/(auth)/`
- `src/app/(platform)/`
- `src/middleware.ts`
- `backend/app/auth/`
- `backend/app/dependencies.py`

## Phase 2 - Database persistence

Priority: highest

Purpose: Replace the backend in-memory store with a real database so user, accounting, CRM, report, and integration data survives restarts and can support production workflows.

Programming tasks:

- [x] Add SQLAlchemy database connection foundation
- [ ] Add PostgreSQL or Supabase production database connection
- [ ] Add migration system
- [ ] Add database models
- [ ] Add repository layer
- [ ] Replace in-memory journal entry storage
- [ ] Replace in-memory CRM storage
- [ ] Replace in-memory integration storage
- [x] Add user and organization tables
- [ ] Add team membership tables
- [x] Add subscription and audit log tables
- [ ] Add test database configuration

Recommended implementation options:

- Supabase PostgreSQL
- SQLAlchemy 2.x
- SQLModel
- Alembic migrations

Suggested initial tables:

- `organizations`
- `users`
- `organization_memberships`
- `subscriptions`
- `accounts`
- `journal_entries`
- `journal_lines`
- `audit_logs`
- `crm_contacts`
- `crm_deals`
- `crm_activities`
- `integration_connections`
- `integration_sync_jobs`
- `banking_transactions`
- `vendor_bills`
- `office_exports`
- `documents`
- `reports`
- `ai_research_sessions`
- `opportunity_scores`

Acceptance checklist:

- [ ] Backend starts with database connection
- [ ] Migrations run successfully
- [ ] Journal entries persist in database
- [ ] CRM records persist in database
- [ ] Integration connections persist with secret references only
- [ ] Tests can run against isolated test database or repository mock

Suggested source areas:

- `backend/app/database.py`
- `backend/app/repositories/`
- `backend/app/db_models/`
- `backend/migrations/`

## Phase 3 - Subscription billing and plan entitlements

Priority: highest

Purpose: Convert the platform into a revenue-generating SaaS system with Consumer, Professional, and Enterprise plans.

Programming tasks:

- [ ] Add Stripe products and prices
- [x] Add checkout session endpoint contract
- [ ] Add billing portal endpoint
- [x] Add Stripe webhook endpoint contract
- [x] Persist subscription status
- [x] Map subscription plans to feature entitlements foundation
- [ ] Add trial, cancellation, and failed payment handling
- [ ] Add admin revenue dashboard data

Initial plan mapping:

| Plan | Billing scope | Entitlements |
| --- | --- | --- |
| Consumer | $50/month | Dashboard, market intelligence, watchlists, AI assistant, opportunity scanner |
| Professional | $299/month | Consumer features plus acquisition engine, due diligence, business analysis, reports |
| Enterprise | Custom or $1,500+/month | Professional features plus team accounts, advanced CRM, integrations, branded reports |

Acceptance checklist:

- [ ] User can start checkout
- [ ] Stripe webhook updates subscription record
- [ ] Subscription status controls feature access
- [ ] Canceled users lose paid access after entitlement period
- [ ] Admin can view active subscriptions and revenue summary

Suggested source areas:

- `backend/app/routers/billing.py`
- `backend/app/services_billing.py`
- `backend/app/models_billing.py`
- `src/app/pricing/`
- `src/app/account/billing/`

## Phase 4 - Security, audit logs, and compliance controls

Priority: high

Purpose: Financial applications require strong access control, traceability, and data protection.

Programming tasks:

- [ ] Add immutable audit logging
- [ ] Log journal entry creation and approval events
- [ ] Log CRM changes
- [ ] Log report generation
- [ ] Log integration sync events
- [ ] Add request ID tracking
- [ ] Add security headers
- [ ] Add rate limiting
- [ ] Add secrets management pattern
- [ ] Add financial disclaimers to AI and report outputs
- [ ] Add terms, privacy, and compliance pages

Acceptance checklist:

- [ ] Every sensitive write creates an audit log
- [ ] Raw external provider secrets are never persisted in database
- [ ] Integration connections store only secret-manager references
- [ ] AI outputs include financial disclaimer metadata
- [ ] Protected routes require authenticated sessions

Suggested source areas:

- `backend/app/audit.py`
- `backend/app/security.py`
- `backend/app/middleware.py`
- `src/app/legal/`

## Phase 5 - AI assistant backend and John Henry Opportunity Score engine

Priority: high

Purpose: Convert the prototype AI concepts into backend services with repeatable scoring, explainability, and guardrails.

Programming tasks:

- [ ] Add AI assistant chat endpoint
- [ ] Add provider abstraction for OpenAI and Anthropic
- [ ] Add prompt templates
- [ ] Add source citation structure
- [ ] Add saved research sessions
- [ ] Add financial disclaimer guardrails
- [ ] Add John Henry Opportunity Score formula v1
- [ ] Add score explanation endpoint
- [ ] Add score history
- [ ] Add risk factor outputs

Initial scoring modules:

- Stocks: valuation, growth, margin quality, balance sheet, dividend quality, risk
- Businesses: EBITDA, seller discretionary earnings, DSCR, industry, customer concentration, competition
- Crypto: adoption, liquidity, volatility, institutional activity, cycle position
- Macro overlay: inflation, rates, liquidity, recession probability

Acceptance checklist:

- [ ] Backend can generate a structured AI research response
- [ ] Response includes disclaimer and sources field
- [ ] Opportunity Score returns numeric score from 0 to 100
- [ ] Score includes factor breakdown
- [ ] Score results can be saved and retrieved

Suggested source areas:

- `backend/app/routers/ai.py`
- `backend/app/routers/scoring.py`
- `backend/app/services_ai.py`
- `backend/app/services_scoring.py`

## Phase 6 - Document upload and due diligence workflow

Priority: high

Purpose: Support business acquisition, lending, and audit workflows by ingesting documents securely.

Programming tasks:

- [ ] Add secure document upload endpoint
- [ ] Add storage provider integration
- [ ] Add document metadata table
- [ ] Add document classification
- [ ] Add P&L, balance sheet, tax return, and bank statement categories
- [ ] Add due diligence checklist generation
- [ ] Add AI extraction pipeline placeholder
- [ ] Add fraud and risk flag structure
- [ ] Add reviewer notes and status workflow

Recommended storage options:

- Supabase Storage
- AWS S3
- Azure Blob Storage

Acceptance checklist:

- [ ] Authenticated user can upload document
- [ ] Document is associated with organization and diligence workspace
- [ ] Document metadata persists
- [ ] Unauthorized users cannot access document metadata
- [ ] Due diligence status can be updated

Suggested source areas:

- `backend/app/routers/documents.py`
- `backend/app/services_documents.py`
- `src/app/due-diligence/upload/`

## Phase 7 - Production integration adapters

Priority: medium-high

Purpose: Replace provider-interface placeholders with live provider adapters for bank feeds, vendor systems, Microsoft Office, and CRM platforms.

Programming tasks:

- [ ] Add Plaid or MX OAuth/link workflow
- [ ] Add bank account sync
- [ ] Add transaction sync
- [ ] Add bank reconciliation workflow
- [ ] Add QuickBooks or NetSuite OAuth/token workflow
- [ ] Add Bill.com vendor bill sync
- [ ] Add Microsoft Graph OAuth flow
- [ ] Add Excel workbook generation
- [ ] Add Word document generation
- [ ] Add Salesforce OAuth flow if required
- [ ] Add provider webhook verification

Acceptance checklist:

- [ ] Integration tokens are stored in secret manager only
- [ ] Sync jobs record status and errors
- [ ] Provider webhook signatures are verified
- [ ] Imported transactions create accounting suggestions
- [ ] Export packages can be sent to Microsoft 365 storage

Suggested source areas:

- `backend/app/integrations/plaid.py`
- `backend/app/integrations/microsoft_graph.py`
- `backend/app/integrations/quickbooks.py`
- `backend/app/integrations/salesforce.py`

## Phase 8 - Admin dashboard and operations console

Priority: medium

Purpose: Give platform operators visibility into users, subscriptions, integrations, CRM, accounting controls, and system health.

Programming tasks:

- [ ] Add `/admin` front-end route group
- [ ] Add admin API endpoints
- [ ] Add user management view
- [ ] Add subscription dashboard
- [ ] Add integration health dashboard
- [ ] Add CRM pipeline dashboard
- [ ] Add audit log viewer
- [ ] Add report generation queue

Acceptance checklist:

- [ ] Only admin users can access admin screens
- [ ] Admin can view subscription and revenue summary
- [ ] Admin can inspect integration sync failures
- [ ] Admin can inspect audit log events

Suggested source areas:

- `src/app/admin/`
- `backend/app/routers/admin.py`

## Phase 9 - Reporting engine and branded exports

Priority: medium

Purpose: Produce investor-ready and advisor-ready reports from backend data.

Programming tasks:

- [ ] Add report template registry
- [ ] Add PDF generation provider
- [ ] Add Excel export writer
- [ ] Add Word document writer
- [ ] Add email delivery integration
- [ ] Add scheduled report generation
- [ ] Add report archive

Report types:

- John Henry Weekly Macro Report
- Business Acquisition Report
- Crypto Intelligence Report
- Dividend Opportunities Report
- Financial Statement Package
- Audit Summary Report
- CRM Pipeline Report

Acceptance checklist:

- [ ] User can request report generation
- [ ] Report status can be tracked
- [ ] Generated report is stored and downloadable
- [ ] Report is associated with organization and user

## Phase 10 - Production quality, CI, deployment, and monitoring

Priority: high before launch

Purpose: Make the application safe to deploy, monitor, and maintain.

Programming tasks:

- [ ] Add CI workflow for frontend and backend checks
- [ ] Add deployment configuration
- [ ] Add environment variable documentation
- [ ] Add application logging
- [ ] Add error monitoring
- [ ] Add uptime monitoring
- [ ] Add backup and restore documentation
- [ ] Add smoke tests
- [ ] Add accessibility checks
- [ ] Add end-to-end tests

Acceptance checklist:

- [ ] Pull requests run frontend checks
- [ ] Pull requests run backend checks
- [ ] Production deployment requires passing checks
- [ ] Errors are logged with request IDs
- [ ] System health endpoint is monitored

## Recommended immediate next milestone

Build this milestone first:

```text
Authentication + database persistence + subscription billing foundation
```

Current status:

- Foundation implementation has started in `backend/` and front-end account/pricing pages.
- The next implementation step is production hardening: external auth provider or JWT key management, PostgreSQL/Supabase connection, Stripe SDK integration, webhook signature verification, and database repositories for accounting/CRM/reporting/integration modules.

Why this comes first:

- It converts the platform from a prototype into a real SaaS foundation.
- It enables users, organizations, teams, roles, and subscriptions.
- It gives the backend a durable data layer.
- It prepares the system for secure financial data, banking integrations, CRM, and AI workflows.

## Immediate implementation checklist

Start with these concrete programming tasks:

- [ ] Choose authentication provider
- [ ] Choose database stack
- [ ] Choose payment provider
- [x] Add organization and user schema
- [ ] Add session-aware front-end layout
- [ ] Add protected dashboard routes
- [x] Add backend auth dependency
- [x] Add subscription plan model
- [x] Add Stripe checkout endpoint contract
- [x] Add Stripe webhook endpoint contract
- [ ] Add plan entitlement middleware
- [ ] Add admin-only route guard
- [x] Add audit log table and logging helper

Before implementing the remaining unchecked items, review and define the decisions in `docs/NEXT_ACTION_ITEMS_TO_DEFINE.md`.

## Suggested environment variables for next milestone

```bash
NEXT_PUBLIC_APP_URL=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
DATABASE_URL=
AUTH_JWT_SECRET=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_CONSUMER_PRICE_ID=
STRIPE_PROFESSIONAL_PRICE_ID=
STRIPE_ENTERPRISE_PRICE_ID=
SECRET_MANAGER_PROVIDER=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

## Definition of done for next milestone

- [x] Users can register and sign in through backend APIs
- [x] Users belong to an organization
- [ ] Dashboard route is protected
- [x] Backend rejects unauthenticated protected requests
- [ ] Database persists users, organizations, subscriptions, CRM records, journal entries, and audit logs
- [ ] Stripe checkout creates a live hosted checkout session
- [x] Stripe webhook contract updates local subscription status
- [ ] Feature access is controlled by plan
- [ ] Admin can view user and subscription status
- [ ] Frontend and backend tests pass
- [ ] Production deployment checklist is updated

## Longer-term add-on backlog

- [ ] Native mobile app
- [ ] Browser extension for deal capture
- [ ] Email ingestion for vendor bills and acquisition leads
- [ ] AI-generated board packets
- [ ] Tax planning module
- [ ] Trust and estate planning module
- [ ] Capital raising investor portal
- [ ] SBA loan package builder
- [ ] Marketplace for acquisition opportunities
- [ ] Data room for acquisition due diligence
- [ ] White-label enterprise reporting
- [ ] API access for enterprise customers
- [ ] Data warehouse and analytics layer
