# Authentication, Database Persistence, and Billing Foundation

## Scope

This document describes the John Henry Investments platform foundation added for:

- User registration and login
- Organization accounts
- Role and protected-route context
- Persistent database tables
- Subscription billing contracts
- Billing and account audit logs

## Backend source files

| File | Purpose |
| --- | --- |
| `backend/app/database.py` | SQLAlchemy engine, session factory, and table initialization |
| `backend/app/db_models.py` | Persistent ORM models for organizations, users, memberships, subscriptions, and audit logs |
| `backend/app/security.py` | Password hashing, password verification, signed bearer token creation, and token validation |
| `backend/app/dependencies.py` | Protected API dependencies and admin guard |
| `backend/app/foundation_models.py` | Pydantic request/response models for auth, billing, subscriptions, and audit logs |
| `backend/app/foundation_services.py` | Registration, login, current-user context, billing plan, checkout, webhook, and audit-log logic |
| `backend/app/routers/auth.py` | Authentication API routes |
| `backend/app/routers/billing.py` | Billing and subscription API routes |
| `backend/tests/test_foundation.py` | Tests for auth, billing, subscription updates, and audit logs |

## Persistent tables

Current SQLAlchemy tables:

- `organizations`
- `users`
- `organization_memberships`
- `subscriptions`
- `audit_logs`

Default development database:

```text
sqlite:///./john_henry_platform.db
```

Production target:

```text
PostgreSQL or Supabase PostgreSQL
```

## Authentication endpoints

Base path:

```text
/api/v1
```

| Method | Route | Purpose |
| --- | --- | --- |
| `POST` | `/auth/register` | Create organization, admin user, membership, trial subscription, access token, and audit log |
| `POST` | `/auth/login` | Validate credentials and return signed bearer token |
| `GET` | `/auth/me` | Return authenticated user, organization, role, and subscription |

## Billing endpoints

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/billing/plans` | List Consumer, Professional, and Enterprise plan definitions |
| `GET` | `/billing/subscription` | Return current authenticated subscription context |
| `POST` | `/billing/checkout-session` | Create checkout-session contract and record billing intent |
| `POST` | `/billing/webhook` | Update local subscription status from billing event |
| `GET` | `/billing/audit-logs` | Return organization audit logs for admin users |

## Front-end source files

| Route | File | Purpose |
| --- | --- | --- |
| `/register` | `src/app/register/page.tsx` | Registration workflow overview |
| `/login` | `src/app/login/page.tsx` | Login and session contract overview |
| `/pricing` | `src/app/pricing/page.tsx` | Plan packaging and billing API contract overview |
| `/account` | `src/app/account/page.tsx` | User, organization, subscription, role, and audit context overview |

## Environment variables

```bash
DATABASE_URL=
AUTH_JWT_SECRET=
AUTH_TOKEN_TTL_MINUTES=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_CONSUMER_PRICE_ID=
STRIPE_PROFESSIONAL_PRICE_ID=
STRIPE_ENTERPRISE_PRICE_ID=
```

## Verification

```bash
python3 -m compileall backend/app backend/tests
python3 -m pytest backend/tests
python3 -m ruff check backend
npm run typecheck
npm run lint
npm run build
npm audit --audit-level=moderate
```

## Remaining production-hardening tasks

- Replace default SQLite development database with PostgreSQL or Supabase.
- Add Alembic migrations.
- Move accounting, CRM, reporting, and integration modules from in-memory prototype storage into database repositories.
- Replace development token secret with managed secret storage.
- Add MFA.
- Add Stripe SDK checkout session creation.
- Verify Stripe webhook signatures.
- Add plan entitlement middleware for route and feature access.
- Add secure front-end session storage strategy.
