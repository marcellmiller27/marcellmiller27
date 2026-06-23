# John Henry Investments Intelligence Platform

John Henry Investments, LLC is a subscription-based investment intelligence platform concept for B2C and B2B customers.

The prototype in this repository turns the SaaS application blueprint into a runnable Next.js and TypeScript application with a FastAPI backend. It presents subscription plans, platform modules, opportunity scoring, macro intelligence, due diligence workflows, portfolio management, AI assistant workflows, accounting workflows, reporting, dashboards, CRM, and the recommended technology stack.

## Application focus

- AI-powered opportunity discovery
- Business acquisition analysis
- AI due diligence center
- Global macro dashboard
- Weekly intelligence reports
- Portfolio tracking
- Wealth projection
- Corporate governance and capital raising tools
- John Henry Opportunity Score
- General journal accounting entries
- Audit and financial reports
- Executive dashboards
- CRM pipeline management
- External banking, vendor, Microsoft Office, and CRM integrations

## Tech stack

- Next.js
- React
- TypeScript
- Python
- FastAPI
- Future backend target: PostgreSQL, Supabase, OpenAI, Anthropic, AWS or private cloud

## Application routes

- `/` - Public platform overview and subscription positioning
- `/dashboard` - Investor command center with portfolio metrics, market widgets, and AI recommendations
- `/opportunities` - Investment and acquisition opportunity engine with John Henry Opportunity Scores
- `/due-diligence` - AI due diligence center for document upload and risk review workflows
- `/portfolio` - Portfolio management and wealth projection scenarios
- `/reports` - John Henry Intelligence Center report generation workflow
- `/assistant` - Private AI research assistant workflow examples

## Backend API

The backend application is saved in:

```text
backend/
```

It includes API modules for:

- Accounting journal entries
- Chart of accounts
- Trial balance
- Audit reports
- Financial reports
- Executive dashboards
- CRM contacts, deals, activities, and pipeline summary
- External banking connectors such as Plaid and MX
- Vendor/accounting connectors such as QuickBooks, NetSuite, and Bill.com
- Microsoft 365 Excel and Word export package interfaces
- Salesforce CRM sync interface

Backend documentation:

```text
backend/README.md
```

## Getting started

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Build for production:

```bash
npm run build
```

Run static checks:

```bash
npm run lint
npm run typecheck
```

Run backend checks:

```bash
cd backend
python3 -m compileall app tests
python3 -m pytest
python3 -m ruff check .
```

## Product blueprint

The full product specification, project management checklist, next programming milestone, and saved programming-script reference are available in:

```text
docs/PRODUCT_BLUEPRINT.md
docs/PROJECT_MANAGEMENT_CHECKLIST.md
docs/NEXT_PROGRAMMING_MILESTONE.md
docs/COMPLETED_PLATFORM_PROGRAMMING_SCRIPTS.md
```
