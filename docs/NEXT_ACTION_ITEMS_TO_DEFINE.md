# John Henry Investments Next Action Items to Define

## Purpose

This file lists the decisions and inputs that must be defined before the next programming phase of the John Henry Investments platform.

The current platform now has a front-end application, FastAPI backend, accounting/reporting/CRM APIs, external integration interfaces, and an authentication/database/billing foundation. The next step is to define production choices so engineering work can proceed without ambiguity.

## 1. Business and product decisions

- [ ] Define the first launch customer segment:
  - Consumer investors
  - Acquisition entrepreneurs
  - Family offices
  - CPAs, attorneys, bankers, or investment firms
- [ ] Confirm the first paid MVP package.
- [ ] Confirm whether the launch offer is B2C, B2B, or invite-only enterprise.
- [ ] Confirm plan names and prices:
  - Consumer Plan
  - Professional Plan
  - Enterprise / Family Office Plan
- [ ] Define plan entitlements by feature.
- [ ] Define free trial rules, if any.
- [ ] Define refund, cancellation, and upgrade/downgrade policy.
- [ ] Define the first dashboard metrics that matter most.
- [ ] Define the first reports to ship:
  - Weekly Macro Report
  - Business Acquisition Report
  - Crypto Intelligence Report
  - Dividend Opportunities Report
  - Financial Statement Package
  - Audit Summary Report

## 2. Branding and customer experience inputs

- [ ] Provide final logo.
- [ ] Provide brand colors.
- [ ] Provide company description.
- [ ] Provide contact email.
- [ ] Provide support email.
- [ ] Provide founder/company bio.
- [ ] Define homepage call-to-action.
- [ ] Define onboarding copy.
- [ ] Define pricing page copy.
- [ ] Define enterprise sales message.
- [ ] Define sample screenshots or demo data to show in the platform.

## 3. Legal and compliance items to define

- [ ] Confirm whether legal counsel has reviewed the platform concept.
- [ ] Define initial legal budget using `docs/STAFFING_LEGAL_PRO_FORMA.md`.
- [ ] Define financial disclaimer language.
- [ ] Define AI-output disclaimer language.
- [ ] Define tax/legal/accounting advice disclaimer language.
- [ ] Define privacy policy requirements.
- [ ] Define terms of service requirements.
- [ ] Define data retention policy.
- [ ] Define user consent language for bank/accounting integrations.
- [ ] Define whether investment recommendations will be educational only or advisory.
- [ ] Confirm whether SEC, state, FINRA, or other regulatory review is required.
- [ ] Define who approves published reports before users receive them.

## 4. Authentication and account decisions

- [ ] Choose authentication provider:
  - Supabase Auth
  - Auth0
  - Clerk
  - AWS Cognito
  - Custom FastAPI auth foundation
- [ ] Define whether MFA is required at launch.
- [ ] Define password policy.
- [ ] Define session timeout policy.
- [ ] Define user roles:
  - Admin
  - Investor
  - Advisor
  - CPA
  - Attorney
  - Banker
  - Family Office
  - Enterprise User
- [ ] Define which roles can access accounting data.
- [ ] Define which roles can generate reports.
- [ ] Define which roles can manage billing.
- [ ] Define which roles can manage integrations.
- [ ] Define team account rules.

## 5. Database and infrastructure decisions

- [ ] Choose production database:
  - Supabase PostgreSQL
  - AWS RDS PostgreSQL
  - Neon PostgreSQL
  - Other managed PostgreSQL
- [ ] Choose hosting:
  - Vercel
  - AWS
  - Private cloud
- [ ] Choose file storage:
  - Supabase Storage
  - AWS S3
  - Azure Blob Storage
- [ ] Define backup policy.
- [ ] Define data encryption requirements.
- [ ] Define environment variable management.
- [ ] Define secret-manager provider.
- [ ] Define deployment environments:
  - Development
  - Staging
  - Production
- [ ] Define production domain name.
- [ ] Define monitoring and alerting provider.

## 6. Billing and revenue decisions

- [ ] Choose payment provider, recommended: Stripe.
- [ ] Create Stripe account.
- [ ] Define Stripe products.
- [ ] Define Stripe price IDs.
- [ ] Define whether Enterprise is self-serve checkout or invoiced manually.
- [ ] Define billing portal requirements.
- [ ] Define invoice branding.
- [ ] Define coupon and promotional policy.
- [ ] Define failed-payment policy.
- [ ] Define revenue dashboard requirements.
- [ ] Define who receives billing notifications.

## 7. Banking and vendor integration decisions

- [ ] Choose banking provider:
  - Plaid
  - MX
  - Direct bank API
- [ ] Define supported bank account types.
- [ ] Define transaction sync frequency.
- [ ] Define bank reconciliation rules.
- [ ] Choose accounting/vendor providers:
  - QuickBooks Online
  - NetSuite
  - Bill.com
- [ ] Define whether vendor bills sync into John Henry first or external accounting software first.
- [ ] Define approval workflow for imported vendor bills.
- [ ] Define chart-of-accounts mapping rules.
- [ ] Define who can approve journal entries.
- [ ] Define webhook security requirements.

## 8. Microsoft Office and document decisions

- [ ] Choose Microsoft integration path:
  - Microsoft Graph
  - Manual file export
  - Both
- [ ] Define Excel workbook templates.
- [ ] Define Word report templates.
- [ ] Define PDF branding.
- [ ] Define where generated files are stored:
  - Local download
  - OneDrive
  - SharePoint
  - S3/Supabase Storage
- [ ] Define report approval workflow.
- [ ] Define file naming rules.
- [ ] Define document retention rules.

## 9. AI and scoring decisions

- [ ] Choose AI providers:
  - OpenAI
  - Anthropic
  - Both
- [ ] Define whether user data can be sent to AI providers.
- [ ] Define redaction rules before AI processing.
- [ ] Define source citation requirements.
- [ ] Define John Henry Opportunity Score formula version 1.
- [ ] Define asset classes for scoring:
  - Stocks
  - ETFs
  - Businesses
  - Real estate
  - Crypto
- [ ] Define Buy / Watch / Pass thresholds.
- [ ] Define risk score methodology.
- [ ] Define human-review requirement for AI reports.
- [ ] Define saved research history requirements.

## 10. Document upload and due diligence decisions

- [ ] Define supported upload types:
  - Tax returns
  - P&L statements
  - Balance sheets
  - Bank statements
  - Contracts
  - Leases
  - Loan documents
- [ ] Define maximum file size.
- [ ] Define allowed file formats.
- [ ] Define document security classification.
- [ ] Define diligence checklist categories.
- [ ] Define fraud flag rules.
- [ ] Define reviewer roles.
- [ ] Define document deletion policy.

## 11. Admin and operations decisions

- [ ] Define admin dashboard requirements.
- [ ] Define user management requirements.
- [ ] Define subscription management requirements.
- [ ] Define integration health dashboard requirements.
- [ ] Define audit log viewer requirements.
- [ ] Define support workflow.
- [ ] Define whether beta is one-person operated or contractor-supported.
- [ ] Define which professional services stay outsourced versus move in-house using `docs/COMPENSATION_AND_PRO_SERVICES_PROJECTIONS.md`.
- [ ] Review `docs/JOB_DESCRIPTIONS_AND_STAFFING_REQUIREMENTS.md` before posting jobs or signing contractor agreements.
- [ ] Review `docs/SYSTEM_FLOWCHARTS_AND_PROCESS_MAPS.md` before defining detailed implementation tickets.
- [ ] Review `docs/FIVE_STAGE_VALUATION_MODEL.md` before discussing valuation or fundraising terms.
- [ ] Review `docs/SRC_CODE_AUDIT.md` before the next front-end implementation sprint.
- [ ] Define incident response workflow.
- [ ] Define production launch checklist owner.

## 12. Engineering implementation decisions

- [ ] Confirm whether to continue with the current FastAPI backend.
- [ ] Confirm whether to continue with the current Next.js frontend.
- [ ] Decide whether to add Alembic migrations next.
- [ ] Decide whether to migrate accounting/CRM/integration data to SQLAlchemy next.
- [ ] Decide whether Stripe or Supabase should be implemented first.
- [ ] Decide whether front-end forms should connect to live backend endpoints next.
- [ ] Decide whether to add CI/CD next.
- [ ] Decide whether to add end-to-end tests next.

## Recommended immediate decisions

Define these first:

1. Production database provider.
2. Authentication provider.
3. Payment provider and plan pricing.
4. First launch customer segment.
5. Legal disclaimer requirements.
6. Whether to prioritize Stripe billing or database migration next.
7. Whether to connect front-end auth forms to backend auth APIs next.

## Recommended next programming task after definitions

After these items are defined, the recommended next programming task is:

```text
Connect front-end registration, login, pricing, and account pages to the backend auth and billing APIs; add persistent PostgreSQL/Supabase configuration; add Stripe SDK checkout and webhook signature verification.
```
