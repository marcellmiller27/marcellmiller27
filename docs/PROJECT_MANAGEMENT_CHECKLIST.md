# John Henry Investments Platform Programme Checklist

## Programme summary

Project: John Henry Investments, LLC Investment Intelligence Platform

Objective: Build a subscription SaaS platform for investors, business buyers, family offices, and professional advisors that provides opportunity discovery, due diligence, macro intelligence, portfolio tracking, AI research, and proprietary scoring.

Current repository status: Front-end application prototype completed as a routed Next.js and TypeScript build, with a FastAPI backend prototype for accounting, reports, dashboards, CRM, and external integrations.

## Status legend

- `[x]` Complete in current repository
- `[ ]` Required before production launch
- `[~]` Partially defined; requires business, legal, design, or engineering follow-up

## Completed application build

| Area | Status | Deliverable |
| --- | --- | --- |
| Public platform overview | [x] | `/` landing page with positioning, subscription plans, modules, scoring model, technology stack, and long-term vision |
| Platform dashboard | [x] | `/dashboard` investor command center with portfolio metrics, market widgets, market signals, and AI recommendations |
| Opportunity engine | [x] | `/opportunities` screen with investment and acquisition opportunities, scores, recommendations, theses, and metrics |
| Due diligence center | [x] | `/due-diligence` screen with document intake categories and sample AI risk-review queue |
| Portfolio management | [x] | `/portfolio` screen with holdings, allocation, cash flow, and bull/base/bear wealth projections |
| Intelligence reports | [x] | `/reports` screen with branded macro, acquisition, crypto, and dividend report workflows |
| AI research assistant | [x] | `/assistant` screen with private research workflow examples and structured outputs |
| Shared product data | [x] | Typed data model for pricing, users, modules, opportunities, diligence, portfolio, reports, assistant workflows, score factors, and stack layers |
| Shared application shell | [x] | Navigation and layout shell for routed platform screens |
| Product documentation | [x] | Product blueprint, route map, setup instructions, and AI work summary |
| Investor package | [x] | Pitch deck, PowerPoint, Excel financial model, DCF, projections, charts, and hierarchy materials in `docs/investor_package/` |
| Programming scripts reference | [x] | Saved programming setup, commands, source file map, and verification commands in `docs/COMPLETED_PLATFORM_PROGRAMMING_SCRIPTS.md` |
| Cloud capacity plan | [x] | Storage, database, network, compute, cache, AI, and monitoring estimates in `docs/CLOUD_STORAGE_AND_CAPACITY_PLAN.md` |
| Estimated platform costs | [x] | Monthly, annual, and tiered cost estimates in `docs/ESTIMATED_PLATFORM_COSTS.md` |
| Projected EBITDA model | [x] | Revenue, expenditure, EBITDA, margin, and break-even scenarios in `docs/PROJECTED_EBITDA_MODEL.md` |
| Staffing/legal pro forma | [x] | One-person feasibility, staffing plan, legal expenditures, compliance costs, and staffing-adjusted EBITDA in `docs/STAFFING_LEGAL_PRO_FORMA.md` |
| Compensation/professional-services projections | [x] | Per-person compensation, outsourced versus in-house services, quarterly/annual staffing, and expenditure comparisons in `docs/COMPENSATION_AND_PRO_SERVICES_PROJECTIONS.md` |
| Job descriptions/staffing requirements | [x] | Department-level job descriptions, skill requirements, education/experience expectations, legal personnel, and law firm requirements in `docs/JOB_DESCRIPTIONS_AND_STAFFING_REQUIREMENTS.md` |
| Next action items to define | [x] | Decision checklist for business, legal, provider, integration, billing, AI, and engineering inputs in `docs/NEXT_ACTION_ITEMS_TO_DEFINE.md` |
| Next programming milestone | [x] | Recommended next implementation sequence in `docs/NEXT_PROGRAMMING_MILESTONE.md` |
| Backend API prototype | [x] | FastAPI service for accounting journal entries, audit reports, financial reports, dashboards, and CRM in `backend/` |
| External integration interfaces | [x] | Banking, vendor, Microsoft Office, accounting, and CRM connector contracts in `/api/v1/integrations/*` |
| Auth/database/billing foundation | [x] | SQLAlchemy persistent organizations, users, memberships, subscriptions, audit logs, auth endpoints, billing contracts, and account/pricing screens |
| Verification | [x] | Typecheck, lint, production build, and npm audit completed successfully |

## Project management workstreams

### 1. Business strategy and product scope

- [x] Define subscription model: Consumer, Professional, Enterprise / Family Office
- [x] Define target user groups: retail investors, accredited investors, business buyers, family offices, firms, CPAs, attorneys, bankers
- [x] Define initial product modules across dashboard, opportunity engine, diligence, macro intelligence, reports, assistant, portfolio, governance, capital raising, and scoring
- [x] Define first front-end route map
- [ ] Approve MVP scope for first paid release
- [ ] Confirm final subscription pricing and packaging
- [ ] Define success metrics: signups, paid conversions, churn, ARPU, report usage, opportunity scans, assistant usage
- [ ] Define launch market: consumer investors, acquisition entrepreneurs, advisors, or family offices

### 2. Legal, compliance, and risk management

- [ ] Engage legal counsel for investment advisory, securities, and financial promotion review
- [ ] Determine whether the platform requires SEC, state, FINRA, or other regulatory registration
- [ ] Draft financial disclaimer: not investment, tax, legal, or accounting advice
- [ ] Draft terms of service
- [ ] Draft privacy policy
- [ ] Draft data processing and retention policy
- [ ] Review AI-generated financial analysis risk disclosures
- [ ] Review third-party data licensing requirements
- [ ] Review legal-document generation risk for governance center features

### 3. Brand, content, and customer experience

- [ ] Finalize John Henry Investments logo
- [ ] Finalize brand colors, typography, and visual identity
- [ ] Approve homepage copy and product claims
- [ ] Create customer onboarding flow copy
- [ ] Create pricing-page copy
- [ ] Create sample report templates
- [ ] Create support and contact workflows
- [ ] Define enterprise sales collateral

### 4. Application engineering

- [x] Create Next.js application scaffold
- [x] Create routed front-end prototype
- [x] Add reusable platform shell
- [x] Add typed mock data model
- [x] Add responsive styling for platform screens
- [x] Add project scripts for development, typecheck, lint, build, and audit
- [x] Add FastAPI backend prototype
- [x] Add accounting journal entry and trial balance APIs
- [x] Add audit report and financial report APIs
- [x] Add dashboard and CRM APIs
- [x] Add external integration API contracts for banking, vendor apps, Microsoft Office, accounting systems, and CRM
- [x] Add authentication foundation
- [ ] Add multi-factor authentication
- [x] Add role-based permissions foundation
- [ ] Add team accounts
- [x] Add billing and subscription management foundation
- [x] Add persistent database schema foundation
- [x] Add API layer prototype
- [ ] Add document upload and secure storage
- [ ] Add AI assistant backend integration
- [ ] Add market data integrations
- [ ] Add economic data integrations
- [ ] Add portfolio account integrations
- [ ] Add production banking provider integration such as Plaid or MX
- [ ] Add production vendor/accounting provider integration such as QuickBooks, NetSuite, or Bill.com
- [ ] Add Microsoft Graph integration for Excel and Word exports
- [ ] Add Salesforce integration if enterprise CRM sync is required
- [ ] Add report generation and PDF export
- [ ] Add admin dashboard
- [ ] Add observability, logging, and error monitoring
- [ ] Migrate accounting, CRM, reports, and integrations from in-memory store to database repositories

### 5. Data and AI systems

- [x] Define John Henry Opportunity Score concept
- [x] Define sample factors for stocks, businesses, and crypto
- [x] Define sample opportunity output: Buy, Watch, Pass
- [x] Define sample AI assistant workflows
- [ ] Select AI providers: OpenAI, Anthropic, or multi-provider architecture
- [ ] Design prompt and evaluation framework
- [ ] Define proprietary scoring formula version 1
- [ ] Define confidence scoring and human-review rules
- [ ] Add source citations for AI research outputs
- [ ] Add data-quality checks
- [ ] Add hallucination and financial-risk guardrails
- [ ] Add audit logs for AI recommendations

### 6. Infrastructure and DevOps

- [ ] Choose production hosting: Vercel, AWS, or private cloud
- [ ] Choose database provider: Supabase/PostgreSQL or managed AWS PostgreSQL
- [ ] Review cloud capacity plan and select MVP infrastructure size
- [ ] Review estimated platform costs and approve MVP budget range
- [ ] Review projected EBITDA model and approve financial planning assumptions
- [ ] Review staffing/legal pro forma and approve one-person beta or staffed MVP plan
- [ ] Review compensation and professional-services projections before converting contractors to in-house roles
- [ ] Review job descriptions and staffing requirements before recruiting or contracting roles
- [ ] Review investor package and add live assumptions, screenshots, demo video, pilot customers, and final use-of-funds ask
- [ ] Configure environment variables
- [ ] Configure CI checks for typecheck, lint, build, and audit
- [ ] Configure preview deployments
- [ ] Configure production deployment
- [ ] Configure backups
- [ ] Configure secrets management
- [ ] Configure uptime monitoring
- [ ] Configure incident response process

### 7. Security and privacy

- [ ] Define authentication security requirements
- [ ] Define MFA policy
- [ ] Define data encryption requirements
- [ ] Define document upload security controls
- [ ] Define access controls by user role and plan
- [ ] Add security headers
- [ ] Add rate limiting
- [ ] Add audit logging
- [ ] Add vulnerability scanning
- [ ] Conduct security review before launch

### 8. Payments and revenue operations

- [ ] Create Stripe account or selected payment processor account
- [ ] Configure Consumer Plan product
- [ ] Configure Professional Plan product
- [ ] Configure Enterprise invoicing workflow
- [ ] Add subscription checkout
- [ ] Add customer portal
- [ ] Add plan entitlement rules
- [ ] Add trial, coupon, and cancellation policies
- [ ] Add revenue reporting dashboard

### 9. Quality assurance and launch readiness

- [x] Verify current front-end prototype builds successfully
- [x] Verify current code passes lint
- [x] Verify current code passes TypeScript checks
- [x] Verify current dependency audit has zero moderate-or-higher findings
- [x] Verify backend code compiles
- [x] Add backend service tests for accounting, reporting, dashboard, and CRM services
- [x] Verify backend code passes Ruff lint
- [ ] Add unit tests for scoring helpers after scoring logic is implemented
- [ ] Add integration tests for authentication, billing, and protected routes
- [ ] Add end-to-end tests for signup, subscription, dashboard, reports, and assistant flows
- [ ] Run accessibility review
- [ ] Run cross-browser review
- [ ] Run mobile responsiveness review
- [ ] Run production readiness review

## Suggested MVP release checklist

The first paid MVP should focus on a smaller production-ready surface:

- [ ] Public homepage
- [ ] User registration and login
- [ ] Subscription checkout
- [ ] Protected dashboard
- [ ] Watch list
- [ ] Market intelligence feed
- [ ] AI research assistant with disclaimers
- [ ] Opportunity score prototype
- [ ] Branded weekly report preview
- [ ] User profile and billing management
- [ ] Terms, privacy policy, and financial disclaimers

## Immediate action items for Marcellus Miller

- [ ] Review the current prototype routes and approve the overall platform direction
- [ ] Decide which customer segment launches first
- [ ] Approve or revise pricing tiers
- [ ] Provide brand assets: logo, colors, contact details, and company description
- [ ] Select hosting, database, AI, and payment providers
- [ ] Engage legal counsel for compliance and disclaimer review
- [ ] Approve MVP scope
- [ ] Provide sample reports, sample opportunities, and sample portfolio data for production-like demos
- [ ] Decide whether to prioritize B2C consumer subscriptions or B2B professional subscriptions
- [ ] Approve next engineering milestone: authentication, database persistence, and subscription billing foundation
- [ ] Review `docs/NEXT_ACTION_ITEMS_TO_DEFINE.md` and define production decisions
- [ ] Review `docs/NEXT_PROGRAMMING_MILESTONE.md` and confirm implementation order

## Current verification record

The current application build has been verified with:

```bash
npm run typecheck
npm run lint
npm run build
npm audit --audit-level=moderate
python3 -m compileall backend/app backend/tests
python3 -m pytest backend/tests
python3 -m ruff check backend
```

All checks passed at the time this checklist was created.
