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
- Add report export to PDF
- Add document storage for audit evidence
- Add CI checks for backend tests and linting
