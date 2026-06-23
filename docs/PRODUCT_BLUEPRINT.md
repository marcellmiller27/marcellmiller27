# John Henry Investments SaaS Application Blueprint

## Objective

John Henry Investments, LLC is designed as a subscription-based investment intelligence platform that can support consumer, professional, and enterprise customers.

The primary mission is to provide investors, business owners, family offices, and acquisition entrepreneurs with AI-powered opportunity discovery, financial analysis, valuation tools, macroeconomic intelligence, and portfolio management capabilities.

## Subscription model

| Plan | Price | Target users | Example revenue target |
| --- | --- | --- | --- |
| Consumer Plan | $50/month | Retail investors | 50,000 subscribers, $2.5M/month |
| Professional Plan | $299/month | Business buyers and advisors | 5,000 subscribers, $1.495M/month |
| Enterprise / Family Office Plan | $1,500+/month | Family offices, investment firms, CPAs, attorneys, bankers | 500 subscribers, $750K+/month |

## Product phases

### Phase 1 - Core Platform

#### Module 1: User Management

- User registration
- Multi-factor authentication
- Profile management
- Team accounts
- Role permissions

User types:

1. Retail Investor
2. Accredited Investor
3. Business Buyer
4. Family Office
5. Investment Firm
6. CPA
7. Attorney
8. Banker

#### Module 2: Dashboard

The home screen displays portfolio value, watch lists, market alerts, economic indicators, acquisition opportunities, and AI recommendations.

Widgets include BTC, gold, S&P 500, treasury rates, inflation, and real estate trends.

### Phase 2 - AI Opportunity Engine

#### Module 3: Investment Discovery Engine

Finds opportunities across stocks, ETFs, bonds, real estate, private equity, small businesses, and cryptocurrency.

Screening filters include revenue growth, EBITDA, debt ratios, dividend yield, insider buying, and valuation metrics.

Output: Investment Score from 0 to 100.

#### Module 4: Business Acquisition Engine

Searches SBA opportunities, business listings, franchise opportunities, distressed assets, and family-owned businesses.

Analysis includes EBITDA, seller discretionary earnings, SBA qualification, debt service coverage ratio, and valuation models.

Output: Buy, Watch, or Pass.

#### Module 5: AI Due Diligence Center

Accepts uploads for tax returns, P&L statements, balance sheets, and bank statements.

Produces risk assessments, cash flow analysis, fraud indicators, and opportunity scores.

### Phase 3 - John Henry Intelligence Center

#### Module 6: Global Macro Dashboard

Tracks the Federal Reserve, ECB, BOJ, PBOC, treasury markets, oil, gold, Bitcoin, money supply, CPI, PPI, M2, GDP, and unemployment.

Forecasting includes recession probability, inflation outlook, and liquidity trends.

#### Module 7: Weekly Intelligence Reports

Automated branded newsletter and PDF report generation.

Examples:

- John Henry Weekly Macro Report
- Crypto Intelligence Report
- Business Acquisition Report
- Dividend Opportunities Report

#### Module 8: AI Research Assistant

A private AI assistant for questions like:

- Analyze Tesla
- Evaluate this business
- Compare SBA loans
- Build dividend portfolio
- Analyze Bitcoin cycle

Returns charts, reports, risk scores, and recommendations.

### Phase 4 - Portfolio Management

#### Module 9: Portfolio Tracking

Connects banks, brokerages, and crypto exchanges.

Tracks stocks, ETFs, crypto, real estate, and private equity.

Metrics include ROI, IRR, Sharpe ratio, and cash flow.

#### Module 10: Wealth Projection Engine

Calculates retirement, family office growth, trust planning, and generational wealth outcomes.

Scenarios include bull case, base case, and bear case.

### Phase 5 - Business Owner Platform

#### Module 11: Corporate Governance Center

Generates LLC and corporation documents including operating agreements, meeting minutes, stock certificates, board resolutions, and shareholder agreements.

#### Module 12: Capital Raising Center

Helps businesses prepare investor decks, loan packages, SBA packages, and financial models.

Tracks investors, lenders, and funding status.

### Phase 6 - AI Scoring System

#### Module 13: John Henry Opportunity Score

A proprietary 0 to 100 scoring model across asset classes.

Stocks:

- Valuation
- Growth
- Risk

Businesses:

- EBITDA
- Industry
- Competition

Crypto:

- Adoption
- Liquidity
- Institutional activity

## Technology stack

- Front end: React, Next.js, TypeScript
- Mobile: Flutter or React Native
- Backend: Python, FastAPI
- Database: PostgreSQL and Supabase
- AI layer: OpenAI, Anthropic, custom financial models
- Cloud: Amazon Web Services, Vercel, or private cloud hosting

Estimated cloud storage, database capacity, network throughput, and processing requirements are documented in `docs/CLOUD_STORAGE_AND_CAPACITY_PLAN.md`.

Estimated platform costs, projected EBITDA scenarios, staffing/legal pro forma assumptions, and compensation/professional-services projections are documented in `docs/ESTIMATED_PLATFORM_COSTS.md`, `docs/PROJECTED_EBITDA_MODEL.md`, `docs/STAFFING_LEGAL_PRO_FORMA.md`, and `docs/COMPENSATION_AND_PRO_SERVICES_PROJECTIONS.md`.

The investor package, pitch deck, PowerPoint presentation, Excel financial model, DCF model, revenue/expenditure/marketing projections, and personnel hierarchy materials are saved in `docs/investor_package/`.

## Back-end application build map

The current repository includes a FastAPI backend prototype in `backend/` for internal operating workflows:

| Area | Routes | Purpose |
| --- | --- | --- |
| Authentication | `/api/v1/auth/*` | Organization registration, login, bearer token, and current-user context |
| Billing | `/api/v1/billing/*` | Plan catalog, checkout-session contract, subscription status, webhook updates, and audit logs |
| Accounting | `/api/v1/accounting/*` | Chart of accounts, balanced general journal entries, and trial balance |
| Audit reports | `/api/v1/reports/audit` | Period-based audit findings, controls summary, scope, and risk score |
| Financial reports | `/api/v1/reports/financial` | Income statement, balance sheet summary, cash-flow summary, and KPIs |
| Dashboards | `/api/v1/dashboards/executive` | Cash position, CRM pipeline, accounting controls, and operating notes |
| CRM | `/api/v1/crm/*` | Contacts, deals, activities, and weighted pipeline summary |
| Integrations | `/api/v1/integrations/*` | Banking, vendor, Microsoft Office, accounting, and CRM connector interfaces |

The backend currently uses an in-memory development repository with seeded data. The production target is PostgreSQL/Supabase persistence with authentication, approvals, audit logs, billing integration, document storage, secret-manager-backed provider credentials, and webhook verification.

The authentication, database persistence, and billing foundation is documented in `docs/AUTH_DATABASE_BILLING_FOUNDATION.md`.

External interfaces currently represented:

- Banking applications: Plaid and MX style bank account and transaction sync
- Vendor/accounting applications: QuickBooks Online, NetSuite, and Bill.com style vendor bill and accounting workflow sync
- Microsoft Office: Microsoft 365 Excel workbook, Word document, CSV, and PDF export package manifests
- CRM: Salesforce style contacts, accounts, opportunities, and activities sync

## Current application build map

The current repository implements the first front-end build as a routed Next.js application:

| Route | Purpose |
| --- | --- |
| `/` | Public platform overview, subscription positioning, modules, scoring model, stack, and vision |
| `/dashboard` | Investor command center with portfolio metrics, market widgets, signals, and AI recommendations |
| `/opportunities` | Investment and acquisition discovery engine with scores, thesis summaries, and metrics |
| `/due-diligence` | Financial document intake and sample AI diligence findings |
| `/portfolio` | Holdings allocation, cash-flow tracking, and bull/base/bear wealth projections |
| `/reports` | Branded macro, acquisition, crypto, and dividend report generation workflow |
| `/assistant` | Private AI research assistant workflow examples |

The organized project-management checklist for completed work and remaining launch tasks is available in `docs/PROJECT_MANAGEMENT_CHECKLIST.md`. The recommended next programming milestone and add-on backlog are available in `docs/NEXT_PROGRAMMING_MILESTONE.md`.

## Long-term vision

The long-term strategy is to transform John Henry Investments from an investment company into a financial technology company with:

1. Investment Research Platform
2. Business Acquisition Marketplace
3. AI Due Diligence Platform
4. Family Office Operating System
5. Wealth Intelligence Network

At 100,000 users and average revenue per user of $75/month, annual recurring revenue could reach approximately $90M/year. At SaaS valuation ranges of 8x to 15x ARR, enterprise value could potentially range from approximately $720M to more than $1.3B, depending on growth, retention, margins, and market conditions.

The most defensible advantages are expected to be the John Henry Opportunity Score, AI Due Diligence Engine, and Business Acquisition Intelligence Platform because they create proprietary data and decision-support capabilities.
