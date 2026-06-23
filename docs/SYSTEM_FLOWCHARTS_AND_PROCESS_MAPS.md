# John Henry Investments System Flowcharts and Process Maps

## Purpose

This document maps the John Henry Investments platform with flowcharts for the full system, each major module, operating procedures, feedback loops, interface protocols, data movement, and control points.

All diagrams use Mermaid syntax so they can render in GitHub, Cursor, and compatible Markdown viewers.

## Diagram index

1. Entire system map
2. User, tenant, authentication, and billing lifecycle
3. Dashboard process flow
4. Investment discovery engine
5. Business acquisition engine
6. AI due diligence center
7. Global macro dashboard
8. Weekly intelligence reports
9. AI research assistant
10. Portfolio tracking
11. Wealth projection engine
12. Corporate governance center
13. Capital raising center
14. John Henry Opportunity Score
15. Accounting, audit, financial reporting, and CRM backend
16. External banking, vendor, Microsoft Office, and CRM integrations
17. Feedback loops
18. Interface protocol map
19. Data governance, audit, and compliance loop
20. Admin and operations control loop
21. Incident and exception flow

## 1. Entire system map

```mermaid
flowchart TB
  Users["Users and organizations"]
  Auth["Authentication and role access"]
  Billing["Subscription billing and entitlements"]
  UI["Next.js web application"]
  API["FastAPI backend"]
  DB["PostgreSQL or Supabase database"]
  Storage["Object storage for documents and reports"]
  AI["AI provider layer"]
  Market["Market and macro data providers"]
  Bank["Banking providers"]
  Vendor["Vendor and accounting systems"]
  Office["Microsoft Office exports"]
  CRMExt["External CRM systems"]
  Audit["Audit logs and compliance evidence"]
  Admin["Admin operations console"]

  Users --> Auth
  Auth --> UI
  Billing --> UI
  UI --> API
  API --> DB
  API --> Storage
  API --> AI
  API --> Market
  API --> Bank
  API --> Vendor
  API --> Office
  API --> CRMExt
  API --> Audit
  Admin --> API
  Audit --> Admin
  DB --> UI
  Storage --> UI
```

## 2. User, tenant, authentication, and billing lifecycle

```mermaid
flowchart TD
  Start["Visitor opens platform"]
  Register["Register organization and admin user"]
  Verify["Validate email and credentials"]
  CreateTenant["Create organization, membership, subscription"]
  Token["Issue signed access token"]
  Plan["Select subscription plan"]
  Checkout["Create checkout session"]
  Webhook["Billing webhook updates subscription"]
  Entitlements["Plan entitlements loaded"]
  Protected["User enters protected platform"]
  Audit["Write audit log"]
  Deny["Reject request"]

  Start --> Register
  Register --> Verify
  Verify -->|valid| CreateTenant
  Verify -->|invalid| Deny
  CreateTenant --> Token
  Token --> Plan
  Plan --> Checkout
  Checkout --> Webhook
  Webhook --> Entitlements
  Entitlements --> Protected
  Register --> Audit
  Checkout --> Audit
  Webhook --> Audit
  Deny --> Audit
```

Procedure:

1. Capture organization, user, and selected plan.
2. Hash password and create persistent user record.
3. Create organization and membership.
4. Create trialing or incomplete subscription record.
5. Issue bearer token.
6. Start checkout when user selects paid plan.
7. Webhook updates subscription status.
8. Entitlements control access to paid modules.
9. Audit log records registration, login, checkout, and billing changes.

## 3. Dashboard process flow

```mermaid
flowchart TD
  Login["Authenticated user"]
  LoadContext["Load user, organization, plan, role"]
  PullPortfolio["Pull portfolio and watchlist data"]
  PullMarket["Pull market and macro snapshots"]
  PullCRM["Pull CRM and acquisition pipeline"]
  PullAlerts["Pull alerts and recommendations"]
  Score["Run opportunity score refresh"]
  Render["Render dashboard widgets"]
  Action["User acts on recommendation"]
  Feedback["Capture click, save, dismiss, watchlist action"]
  Improve["Improve ranking and alert rules"]

  Login --> LoadContext
  LoadContext --> PullPortfolio
  LoadContext --> PullMarket
  LoadContext --> PullCRM
  LoadContext --> PullAlerts
  PullPortfolio --> Render
  PullMarket --> Render
  PullCRM --> Render
  PullAlerts --> Score
  Score --> Render
  Render --> Action
  Action --> Feedback
  Feedback --> Improve
  Improve --> PullAlerts
```

Interface protocol:

- Front end calls backend dashboard endpoint.
- Backend checks role and plan.
- Backend aggregates database records, market data, CRM records, portfolio records, and score outputs.
- Dashboard displays only data allowed by organization, role, and plan.

## 4. Investment discovery engine

```mermaid
flowchart TD
  Universe["Asset universe: stocks, ETFs, bonds, real estate, private equity, crypto"]
  DataIngest["Ingest market, financial, macro, and user preference data"]
  Normalize["Normalize and validate data"]
  Filters["Apply screening filters"]
  Score["Calculate John Henry Opportunity Score"]
  Rank["Rank opportunities"]
  Explain["Generate score explanation and risk factors"]
  Output["Output buy, watch, pass, or research"]
  UserFeedback["User saves, rejects, or requests deeper analysis"]
  ModelTune["Tune filters and ranking rules"]

  Universe --> DataIngest
  DataIngest --> Normalize
  Normalize --> Filters
  Filters --> Score
  Score --> Rank
  Rank --> Explain
  Explain --> Output
  Output --> UserFeedback
  UserFeedback --> ModelTune
  ModelTune --> Filters
```

Procedure:

1. Define asset class and screening universe.
2. Pull market and financial data.
3. Apply valuation, growth, risk, income, and macro filters.
4. Score each opportunity from 0 to 100.
5. Return ranked list with explanation.
6. Feed user behavior into future ranking.

## 5. Business acquisition engine

```mermaid
flowchart TD
  Sources["SBA, business listings, franchises, distressed assets, referrals"]
  DealIngest["Ingest target business data"]
  Normalize["Normalize revenue, EBITDA, SDE, asking price, industry"]
  Finance["Calculate DSCR, leverage, cash flow, SBA fit"]
  Valuation["Run valuation models"]
  Risk["Assess industry, customer, owner, financing, and diligence risk"]
  Score["Calculate acquisition score"]
  Decision{"Recommendation"}
  Buy["Buy"]
  Watch["Watch"]
  Pass["Pass"]
  Diligence["Send to due diligence center"]

  Sources --> DealIngest
  DealIngest --> Normalize
  Normalize --> Finance
  Finance --> Valuation
  Valuation --> Risk
  Risk --> Score
  Score --> Decision
  Decision --> Buy
  Decision --> Watch
  Decision --> Pass
  Buy --> Diligence
  Watch --> Diligence
```

Procedure:

1. Capture acquisition target.
2. Normalize seller-provided data.
3. Estimate debt service coverage.
4. Test SBA qualification.
5. Run valuation and risk model.
6. Output Buy, Watch, or Pass.
7. Route viable targets to due diligence.

## 6. AI due diligence center

```mermaid
flowchart TD
  Upload["Upload tax returns, P&L, balance sheet, bank statements"]
  Classify["Classify document type"]
  Store["Store in secure object storage"]
  Extract["Extract financial fields"]
  Reconcile["Reconcile statements and bank deposits"]
  RiskFlags["Generate fraud and risk indicators"]
  CashFlow["Normalize cash flow and EBITDA"]
  Checklist["Create diligence checklist"]
  HumanReview["Human reviewer approves or requests clarification"]
  Report["Generate diligence report"]
  Feedback["Reviewer outcome improves rules"]

  Upload --> Classify
  Classify --> Store
  Store --> Extract
  Extract --> Reconcile
  Reconcile --> RiskFlags
  Reconcile --> CashFlow
  RiskFlags --> Checklist
  CashFlow --> Checklist
  Checklist --> HumanReview
  HumanReview --> Report
  HumanReview --> Feedback
  Feedback --> Extract
```

Control points:

- Virus scan before processing.
- Role-based document access.
- Audit log for upload, view, export, and deletion.
- Human review before high-risk recommendations.
- Legal disclaimer on AI-generated conclusions.

## 7. Global macro dashboard

```mermaid
flowchart TD
  Sources["Fed, ECB, BOJ, PBOC, Treasury, CPI, PPI, M2, GDP, oil, gold, Bitcoin"]
  Ingest["Ingest macro data"]
  Validate["Validate and timestamp data"]
  Indicators["Calculate inflation, liquidity, rates, recession probability"]
  Signals["Generate macro signals"]
  PortfolioImpact["Map signals to asset classes"]
  Alerts["Create alerts"]
  Reports["Feed weekly intelligence reports"]
  Feedback["User reads, saves, or dismisses signals"]

  Sources --> Ingest
  Ingest --> Validate
  Validate --> Indicators
  Indicators --> Signals
  Signals --> PortfolioImpact
  PortfolioImpact --> Alerts
  Signals --> Reports
  Alerts --> Feedback
  Feedback --> Signals
```

## 8. Weekly intelligence reports

```mermaid
flowchart TD
  Schedule["Report schedule"]
  DataPull["Pull macro, market, opportunity, portfolio, CRM, and acquisition data"]
  Draft["Generate report draft"]
  Review["Human review and compliance check"]
  Approve{"Approved?"}
  Revise["Revise report"]
  Export["Export PDF, Word, Excel, email"]
  Distribute["Distribute to subscribers"]
  Analytics["Track opens, downloads, feedback"]
  Improve["Improve templates and topics"]

  Schedule --> DataPull
  DataPull --> Draft
  Draft --> Review
  Review --> Approve
  Approve -->|no| Revise
  Revise --> Review
  Approve -->|yes| Export
  Export --> Distribute
  Distribute --> Analytics
  Analytics --> Improve
  Improve --> Schedule
```

## 9. AI research assistant

```mermaid
flowchart TD
  Prompt["User prompt"]
  Auth["Check user role, plan, and data access"]
  Classify["Classify request type"]
  Retrieve["Retrieve permitted data and sources"]
  Redact["Redact sensitive data if needed"]
  Model["Call AI provider or model router"]
  Guardrails["Apply disclaimers, source requirements, and risk checks"]
  Response["Return charts, report, risk score, recommendation"]
  Save["Save research session"]
  Feedback["User rating and follow-up prompts"]
  Improve["Improve prompts and retrieval"]

  Prompt --> Auth
  Auth --> Classify
  Classify --> Retrieve
  Retrieve --> Redact
  Redact --> Model
  Model --> Guardrails
  Guardrails --> Response
  Response --> Save
  Response --> Feedback
  Feedback --> Improve
  Improve --> Classify
```

Interface protocol:

- Front end sends prompt and context ID.
- Backend verifies token, organization, role, and plan.
- Backend retrieves allowed records only.
- AI response includes disclaimer, sources, risk level, and output type.
- Audit log records sensitive research activity.

## 10. Portfolio tracking

```mermaid
flowchart TD
  Connect["Connect brokerage, bank, crypto, real estate, private equity records"]
  Sync["Sync balances and holdings"]
  Normalize["Normalize asset classes and cost basis"]
  Metrics["Calculate ROI, IRR, Sharpe, income, cash flow"]
  Risk["Calculate concentration and volatility risk"]
  Dashboard["Display portfolio dashboard"]
  Alerts["Generate rebalancing and risk alerts"]
  UserAction["User updates holdings or watchlist"]
  Feedback["Update assumptions and future alerts"]

  Connect --> Sync
  Sync --> Normalize
  Normalize --> Metrics
  Metrics --> Risk
  Risk --> Dashboard
  Risk --> Alerts
  Dashboard --> UserAction
  Alerts --> UserAction
  UserAction --> Feedback
  Feedback --> Sync
```

## 11. Wealth projection engine

```mermaid
flowchart TD
  Inputs["User inputs: assets, income, savings, goals, trusts, family office needs"]
  Assumptions["Return, inflation, tax, liquidity, and spending assumptions"]
  Scenarios["Build bull, base, and bear cases"]
  Projection["Project wealth, retirement, cash flow, and estate outcomes"]
  Stress["Stress test drawdowns and liquidity"]
  Output["Return charts and recommendations"]
  Review["User adjusts assumptions"]
  Loop["Recalculate projection"]

  Inputs --> Assumptions
  Assumptions --> Scenarios
  Scenarios --> Projection
  Projection --> Stress
  Stress --> Output
  Output --> Review
  Review --> Loop
  Loop --> Assumptions
```

## 12. Corporate governance center

```mermaid
flowchart TD
  Entity["Entity profile: LLC, corporation, shareholders, members"]
  Template["Select document template"]
  Data["Collect required governance data"]
  Generate["Generate operating agreement, minutes, resolutions, certificates"]
  LegalReview["Optional legal review"]
  Approve["User approval"]
  Store["Store signed or final document"]
  Calendar["Create renewal and meeting reminders"]
  Audit["Write audit log"]

  Entity --> Template
  Template --> Data
  Data --> Generate
  Generate --> LegalReview
  LegalReview --> Approve
  Generate --> Approve
  Approve --> Store
  Store --> Calendar
  Store --> Audit
```

## 13. Capital raising center

```mermaid
flowchart TD
  Company["Company profile and funding need"]
  Package["Build investor deck, loan package, SBA package, financial model"]
  CRM["Create investor and lender CRM pipeline"]
  Outreach["Track outreach and status"]
  Diligence["Provide diligence documents"]
  Feedback["Investor or lender feedback"]
  Revise["Revise deck, model, or package"]
  Close["Close funding or mark lost"]
  Report["Generate funding status report"]

  Company --> Package
  Package --> CRM
  CRM --> Outreach
  Outreach --> Diligence
  Diligence --> Feedback
  Feedback --> Revise
  Revise --> Package
  Feedback --> Close
  Close --> Report
```

## 14. John Henry Opportunity Score

```mermaid
flowchart TD
  Asset["Asset or business opportunity"]
  Factors["Collect factors"]
  Valuation["Valuation score"]
  Growth["Growth score"]
  Risk["Risk score"]
  Macro["Macro overlay"]
  Liquidity["Liquidity and financing score"]
  Weight["Apply model weights"]
  Score["Overall score 0-100"]
  Explain["Explain score and factor contribution"]
  Decision["Buy, Watch, Pass, or Research"]
  Outcome["Track realized outcome"]
  Tune["Tune scoring model"]

  Asset --> Factors
  Factors --> Valuation
  Factors --> Growth
  Factors --> Risk
  Factors --> Macro
  Factors --> Liquidity
  Valuation --> Weight
  Growth --> Weight
  Risk --> Weight
  Macro --> Weight
  Liquidity --> Weight
  Weight --> Score
  Score --> Explain
  Explain --> Decision
  Decision --> Outcome
  Outcome --> Tune
  Tune --> Weight
```

## 15. Accounting, audit, financial reporting, and CRM backend

```mermaid
flowchart TD
  Journal["General journal entry"]
  Validate["Validate balanced debits and credits"]
  Post["Post entry"]
  Trial["Generate trial balance"]
  Financial["Generate financial report"]
  AuditReport["Generate audit report"]
  CRM["CRM contacts, deals, activities"]
  Dashboard["Executive dashboard"]
  Billing["Subscription billing"]
  AuditLog["Audit log"]

  Journal --> Validate
  Validate -->|balanced| Post
  Validate -->|not balanced| AuditLog
  Post --> Trial
  Trial --> Financial
  Trial --> AuditReport
  CRM --> Dashboard
  Financial --> Dashboard
  Billing --> Dashboard
  Post --> AuditLog
  Financial --> AuditLog
  CRM --> AuditLog
  Billing --> AuditLog
```

## 16. External integration protocol map

```mermaid
flowchart LR
  User["Admin user"]
  Connect["Create integration connection"]
  Secret["Store credential reference only"]
  SyncJob["Create sync job"]
  Provider["External provider API"]
  Normalize["Normalize provider payload"]
  Suggest["Create accounting or CRM suggestions"]
  Review["Human review"]
  Post["Post approved records"]
  Audit["Audit log"]

  User --> Connect
  Connect --> Secret
  Secret --> SyncJob
  SyncJob --> Provider
  Provider --> Normalize
  Normalize --> Suggest
  Suggest --> Review
  Review --> Post
  Connect --> Audit
  SyncJob --> Audit
  Post --> Audit
```

Supported interface groups:

- Banking: Plaid, MX, direct bank APIs.
- Vendor and accounting: QuickBooks, NetSuite, Bill.com.
- Microsoft Office: Excel, Word, CSV, PDF, OneDrive, SharePoint.
- CRM: Salesforce or equivalent enterprise CRM.
- Payments: Stripe checkout, billing portal, webhooks.

## 17. Microsoft Office export flow

```mermaid
flowchart TD
  Request["User requests export"]
  Auth["Check role and plan"]
  Template["Select Excel, Word, CSV, or PDF template"]
  Data["Pull report, accounting, CRM, portfolio, or audit data"]
  Map["Apply field map"]
  Generate["Generate export package"]
  Review["Optional review and approval"]
  Store["Store or send to Microsoft Graph"]
  Download["User downloads or shares file"]
  Log["Audit log"]

  Request --> Auth
  Auth --> Template
  Template --> Data
  Data --> Map
  Map --> Generate
  Generate --> Review
  Review --> Store
  Store --> Download
  Generate --> Log
  Download --> Log
```

## 18. Feedback loops

```mermaid
flowchart TB
  UserAction["User actions: save, dismiss, buy, watch, pass, export, ask AI"]
  ProductAnalytics["Product analytics"]
  ScoringFeedback["Score outcome feedback"]
  SupportFeedback["Support tickets and success notes"]
  ReportAnalytics["Report opens, downloads, shares"]
  ModelTuning["Model and prompt tuning"]
  Roadmap["Product roadmap updates"]
  ComplianceReview["Compliance and risk review"]

  UserAction --> ProductAnalytics
  UserAction --> ScoringFeedback
  UserAction --> ReportAnalytics
  SupportFeedback --> Roadmap
  ProductAnalytics --> Roadmap
  ScoringFeedback --> ModelTuning
  ReportAnalytics --> ModelTuning
  ModelTuning --> ComplianceReview
  ComplianceReview --> Roadmap
  Roadmap --> UserAction
```

Feedback procedures:

1. Capture explicit and implicit user behavior.
2. Separate product analytics from regulated advice workflows.
3. Track score outcomes by asset class.
4. Route sensitive AI or recommendation changes through compliance review.
5. Update score factors, prompts, templates, and UI flows.

## 19. Interface protocol map

```mermaid
sequenceDiagram
  participant UI as Next.js Front End
  participant API as FastAPI Backend
  participant DB as PostgreSQL
  participant Store as Object Storage
  participant AI as AI Provider
  participant Ext as External Provider
  participant Audit as Audit Log

  UI->>API: HTTPS request with bearer token
  API->>API: Validate token, role, plan
  API->>DB: Read or write tenant-scoped records
  API->>Store: Read or write documents and reports
  API->>AI: Send approved prompt and permitted context
  AI-->>API: Return structured response
  API->>Ext: Sync provider data through adapter
  Ext-->>API: Return provider payload
  API->>Audit: Write action and metadata
  API-->>UI: Return authorized response
```

Protocol requirements:

- HTTPS only.
- Bearer token for protected backend routes.
- Organization ID on tenant-owned records.
- Secret references only for provider credentials.
- Webhook signature verification.
- Idempotency keys for billing and integration writes.
- Audit logs for sensitive reads, writes, exports, and syncs.

## 20. Data governance, audit, and compliance loop

```mermaid
flowchart TD
  Event["Sensitive platform event"]
  Classify["Classify event type and risk"]
  Policy["Apply policy: access, retention, consent, disclaimer"]
  Audit["Write immutable audit log"]
  Review{"Requires review?"}
  Queue["Compliance review queue"]
  Approve["Approve or remediate"]
  Report["Compliance report"]
  Improve["Update policy or controls"]

  Event --> Classify
  Classify --> Policy
  Policy --> Audit
  Audit --> Review
  Review -->|yes| Queue
  Queue --> Approve
  Approve --> Report
  Review -->|no| Report
  Report --> Improve
  Improve --> Policy
```

## 21. Admin and operations control loop

```mermaid
flowchart TD
  Admin["Admin console"]
  Users["User and organization management"]
  Billing["Subscription and revenue management"]
  Integrations["Integration health"]
  Jobs["Background job queues"]
  Logs["Audit logs and errors"]
  Support["Support tickets"]
  Metrics["KPIs and alerts"]
  Actions["Admin actions"]
  Audit["Audit admin actions"]

  Admin --> Users
  Admin --> Billing
  Admin --> Integrations
  Admin --> Jobs
  Admin --> Logs
  Admin --> Support
  Users --> Metrics
  Billing --> Metrics
  Integrations --> Metrics
  Jobs --> Metrics
  Logs --> Metrics
  Support --> Metrics
  Metrics --> Actions
  Actions --> Audit
```

## 22. Incident and exception flow

```mermaid
flowchart TD
  Detect["Detect exception: API error, failed sync, billing failure, security alert"]
  Classify["Classify severity"]
  Alert["Notify responsible team"]
  Triage["Triage root cause"]
  Contain["Contain customer or data impact"]
  Resolve["Resolve issue"]
  Communicate["Notify affected users if required"]
  Postmortem["Write incident report"]
  Improve["Add tests, alerts, runbooks, or controls"]

  Detect --> Classify
  Classify --> Alert
  Alert --> Triage
  Triage --> Contain
  Contain --> Resolve
  Resolve --> Communicate
  Resolve --> Postmortem
  Postmortem --> Improve
  Improve --> Detect
```

## 23. End-to-end business acquisition workflow

```mermaid
flowchart LR
  Lead["Deal lead"]
  CRM["CRM record"]
  Acquisition["Acquisition engine"]
  Score["Opportunity score"]
  Diligence["Due diligence center"]
  Finance["Financial model and SBA analysis"]
  Report["Diligence report"]
  Decision["Buy, watch, pass"]
  Capital["Capital raising or loan package"]
  Close["Close or archive"]

  Lead --> CRM
  CRM --> Acquisition
  Acquisition --> Score
  Score --> Diligence
  Diligence --> Finance
  Finance --> Report
  Report --> Decision
  Decision --> Capital
  Decision --> Close
  Capital --> Close
```

## 24. End-to-end investor research workflow

```mermaid
flowchart LR
  Question["Investor question"]
  Assistant["AI research assistant"]
  Market["Market and macro data"]
  Score["Opportunity score"]
  Portfolio["Portfolio context"]
  Output["Charts, risk score, recommendation"]
  Watchlist["Watchlist or portfolio action"]
  Report["Saved research report"]
  Feedback["User feedback"]

  Question --> Assistant
  Assistant --> Market
  Assistant --> Score
  Assistant --> Portfolio
  Market --> Output
  Score --> Output
  Portfolio --> Output
  Output --> Watchlist
  Output --> Report
  Watchlist --> Feedback
  Report --> Feedback
  Feedback --> Assistant
```

## 25. Full module dependency map

```mermaid
flowchart TB
  Auth["Auth and roles"]
  Billing["Billing and entitlements"]
  Data["Database and object storage"]
  Audit["Audit logs"]
  Dashboard["Dashboard"]
  Discovery["Investment discovery"]
  Acquisition["Business acquisition"]
  Diligence["Due diligence"]
  Macro["Macro intelligence"]
  Reports["Reports"]
  Assistant["AI assistant"]
  Portfolio["Portfolio"]
  Wealth["Wealth projection"]
  Governance["Governance"]
  Capital["Capital raising"]
  Score["Opportunity Score"]
  Accounting["Accounting and financial reporting"]
  CRM["CRM"]
  Integrations["External integrations"]
  Admin["Admin console"]

  Auth --> Dashboard
  Billing --> Dashboard
  Data --> Dashboard
  Audit --> Admin
  Dashboard --> Discovery
  Dashboard --> Portfolio
  Discovery --> Score
  Acquisition --> Score
  Score --> Diligence
  Macro --> Reports
  Assistant --> Reports
  Portfolio --> Wealth
  Governance --> Reports
  Capital --> CRM
  Accounting --> Reports
  CRM --> Dashboard
  Integrations --> Accounting
  Integrations --> Portfolio
  Integrations --> CRM
  Reports --> Admin
  Admin --> Audit
```

## Recommended next flowchart additions

- Add detailed database entity relationship diagram after all persistent tables are migrated.
- Add role-based access matrix by plan and user type.
- Add sequence diagrams for Stripe, Plaid, Microsoft Graph, and AI provider calls after production adapters are selected.
- Add data retention lifecycle diagram after legal retention policy is finalized.
- Add deployment architecture diagram after cloud provider is selected.
