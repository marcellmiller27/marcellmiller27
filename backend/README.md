# John Henry Investments Backend

FastAPI backend for the John Henry Investments platform.

This service supports:

- General journal accounting entries
- Chart of accounts
- Trial balance reporting
- Audit report generation
- Financial reports
- Executive dashboards
- CRM contacts, deals, activities, and pipeline summary
- External banking integrations
- Vendor and ERP application integrations
- Microsoft Excel, Word, CSV, and PDF export package interfaces

## Setup

From the repository root:

```bash
python3 -m pip install -e "backend[dev]"
```

## Run the API

```bash
cd backend
python3 -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Health check

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

## API route map

Base path:

```text
/api/v1
```

### Accounting

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/accounting/chart-of-accounts` | List chart of accounts |
| `GET` | `/api/v1/accounting/journal-entries` | List journal entries, optionally filtered by period |
| `POST` | `/api/v1/accounting/journal-entries` | Create a balanced general journal entry |
| `GET` | `/api/v1/accounting/trial-balance` | Generate trial balance for a period |

### Reports

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/reports/audit` | Generate an audit report for a period |
| `GET` | `/api/v1/reports/financial` | Generate financial statements and KPIs for a period |

### Dashboards

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/dashboards/executive` | Generate executive dashboard snapshot |

### CRM

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/crm/contacts` | List CRM contacts |
| `POST` | `/api/v1/crm/contacts` | Create CRM contact |
| `GET` | `/api/v1/crm/deals` | List CRM deals |
| `POST` | `/api/v1/crm/deals` | Create CRM deal |
| `GET` | `/api/v1/crm/activities` | List CRM activities |
| `POST` | `/api/v1/crm/activities` | Create CRM activity |
| `GET` | `/api/v1/crm/summary` | Generate CRM pipeline summary |

### Integrations

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/api/v1/integrations/connectors` | List supported external connectors |
| `GET` | `/api/v1/integrations/connections` | List configured integration connections |
| `POST` | `/api/v1/integrations/connections` | Create integration connection record using a secret-manager reference |
| `GET` | `/api/v1/integrations/sync-jobs` | List integration sync jobs |
| `POST` | `/api/v1/integrations/sync-jobs` | Request an import/export sync job |
| `GET` | `/api/v1/integrations/banking/transactions` | List imported banking transactions |
| `POST` | `/api/v1/integrations/banking/transactions` | Import banking transaction and generate accounting suggestions |
| `GET` | `/api/v1/integrations/vendor/bills` | List imported vendor bills |
| `POST` | `/api/v1/integrations/vendor/bills` | Import vendor bill and generate accounts-payable journal suggestion |
| `POST` | `/api/v1/integrations/office/export-package` | Create Excel, Word, CSV, or PDF export package manifest |

Supported connector categories:

- Banking: Plaid, MX
- Accounting and vendor applications: QuickBooks Online, NetSuite, Bill.com
- Microsoft Office: Microsoft 365 Excel and Word through Microsoft Graph
- CRM: Salesforce

Production integration rule: API requests must pass `credential_reference` values only. Do not send or store raw bank, vendor, Microsoft, or CRM credentials in request bodies or source code.

## Example journal entry

```json
{
  "entry_date": "2026-06-23",
  "memo": "Professional subscription payment",
  "source_module": "billing",
  "created_by": "marcellus.miller",
  "lines": [
    {
      "account_code": "1000",
      "description": "Cash received",
      "debit": "299.00",
      "credit": "0.00"
    },
    {
      "account_code": "4000",
      "description": "Subscription revenue",
      "debit": "0.00",
      "credit": "299.00"
    }
  ]
}
```

## Verification

```bash
cd backend
python3 -m compileall app tests
python3 -m pytest
python3 -m ruff check .
```

## Production next steps

- Replace in-memory store with PostgreSQL/Supabase persistence
- Add authentication and role-based permissions
- Add approval workflow for journal entries
- Add immutable audit logs
- Connect CRM deals to Stripe subscriptions and invoices
- Connect Plaid or MX for bank account and transaction sync
- Connect QuickBooks, NetSuite, or Bill.com for vendor bills and accounting workflow sync
- Connect Microsoft Graph for Excel and Word template export
- Connect Salesforce if enterprise CRM sync is required
- Add report export to PDF
- Add document storage for audit evidence
- Add secret-manager integration for provider tokens
- Add webhook verification for external provider callbacks
- Add CI checks for backend tests and linting
