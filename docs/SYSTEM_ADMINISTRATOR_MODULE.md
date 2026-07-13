# System Administrator Module — Design Write-Up

> JHI-SIG: 69M2705M · Design/architecture document for founder review. **No build in this pass** —
> layout + concerns only; implementation proceeds on your command. Grounded in the current
> codebase (`backend/app/dependencies.py`, `foundation_models.py`, `foundation_services.py`,
> `db_models.py`) so the "current state" is accurate, not aspirational.

---

## 1. Purpose & scope
A single, audited place to **grant and revoke access**, manage who can do what, and see who did what — for both JHI staff and customer organizations. It is the control plane for identity, roles/permissions, entitlements (incl. licensed market data), and security policy.

Two distinct audiences (both belong in the module, at different tiers):

| Tier | Who | What they administer |
|---|---|---|
| **Platform Administration** (super-admin) | JHI founder / internal staff | The whole system: all orgs & users, role definitions, data entitlements, security policy, feature flags, billing overrides, audit. |
| **Organization Administration** (org-admin) | A customer's account owner/admin | Only their own org: invite/remove their users, assign in-org roles, see their org's activity. |

The founder's immediate ask ("granting access, etc.") is primarily the **Platform Administration** super-admin surface. Org-admin is the natural second tier and is designed in here so we don't repaint later.

**Both tiers can be staffed by humans *or* AI agents.** An administrator is a *principal with an admin permission set* — that principal may be a human user or an AI agent (service identity). AI-agent administrators are a first-class part of this design (see §5A), governed by the same RBAC engine plus stricter autonomy/approval controls.

---

## 2. Current state (as-built) — what exists vs. what's missing
**Already in place (good foundation):**
- **Identity & auth:** `POST /auth/register`, `/auth/login`, `GET /auth/me`; JWT access tokens (PyJWT, HS256), PBKDF2 password hashing, scoped challenge tokens.
- **Roles:** `UserRole` enum — `admin, investor, advisor, cpa, attorney, banker, family_office, enterprise` (single role per principal, carried as a JWT claim).
- **Tenancy:** `OrganizationDB` + `MembershipDB(role)` + `SubscriptionDB(plan/status)`; `Principal` = user_id + organization_id + role + email.
- **Account lifecycle:** `UserDB.is_active` (soft-deactivate) already checked on every request and at login.
- **MFA:** TOTP 2FA (encrypted at rest) and WebAuthn/biometric (mobile) with real ES256 verification.
- **Audit trail:** `AuditLogDB` is **written** for auth events and **readable org-scoped** (`foundation_services`), and read for a login KPI.
- **One real guard:** `require_admin` dependency exists and is enforced (currently on a single billing endpoint).
- **Rate limiting:** env-gated per-IP middleware.

**Missing / the gap this module closes:**
- **Enforcement is thin.** `require_admin` guards **one** endpoint. Most product routers (accounting, CRM, Deal X-Ray, pipeline, reports, dashboards, valuations, financial diligence, integrations, market, support) currently have **no auth dependency at all** — they are effectively open. *This is the #1 concern (see §9).*
- **No admin UI** and **no user-management API** (list users, invite, deactivate, reset MFA, change role).
- **No permission granularity** — a principal has exactly one coarse role; there is no permissions table, no capability checks, no per-module access matrix.
- **No access-request / invitation / grant workflow**, no impersonation ("view as"), no API keys/service accounts, no feature flags, no session/token revocation, no separation-of-duties or approvals for sensitive grants.
- **No data-entitlement control** for licensed data (who may access SF1/NASDAQ-derived output) — a real obligation under the data license.

---

## 3. Proposed capabilities (feature set)
Grouped by function; priority in §11.

1. **User management** — list/search users; view profile, org, role, MFA status, last login; **create/invite**, **deactivate/reactivate** (reuse `is_active`), force password reset, **reset/deactivate MFA**, end sessions.
2. **Roles & permissions** — define roles as **named sets of permissions**; assign roles to users (per org); view an effective-permissions preview; protect built-in roles.
3. **Access requests & grants** — a request → review → approve/deny queue for elevated access; time-boxed ("expires in N days") grants; every grant/revoke audited.
4. **Organizations** — list orgs, members, plan/status; suspend an org; transfer ownership.
5. **Data entitlements** — toggle who/which plans may access licensed-data-derived outputs (SF1/NASDAQ), to honor the data license and internal-use vs. distribution boundaries.
6. **Security policy** — enforce MFA for admins; session/token lifetime; password policy; IP allow-list for admin; rate-limit toggles.
7. **API keys / service accounts** — scoped, revocable machine credentials for integrations (never a human's token).
8. **Feature flags** — enable/disable modules per org/plan/user (also the safety switch to lock a module).
9. **Audit log viewer** — filter by actor/action/resource/date; export; tamper-evident.
10. **System health** — read-only: service/DB status, background jobs, data-provider status, error surface.

---

## 4. Proposed layout (information architecture)
A dedicated **Admin** area (super-admin only), separate from the product nav, with a left sub-nav:

```
Admin
├── Overview            KPIs: users, active orgs, pending access requests, MFA coverage, recent admin actions
├── Users               table (search/filter) → user detail drawer (role, MFA, sessions, activity, actions)
│     └── Invite user   email + org + role + optional expiry
├── Roles & Permissions role list → permission matrix editor (role × capability)
├── Access Requests     queue: pending / approved / denied  (approve, deny, set expiry)
├── Organizations       org list → org detail (members, plan, entitlements, suspend)
├── Data Entitlements   licensed-data access by plan/org/user (SF1/NASDAQ guardrails)
├── Security            MFA enforcement, session lifetime, password policy, admin IP allow-list
├── API Keys            scoped keys / service accounts (create, scope, rotate, revoke)
├── Agents & Automation non-human admins: identity, permission scope, autonomy tier,
│                       pending approvals, activity, per-agent KILL SWITCH
├── Feature Flags       module on/off by org / plan / user
├── Audit Log           filterable, exportable event stream
└── System Health       services, DB, jobs, data providers (read-only)
```

**UX principles:** destructive/elevating actions require confirm + reason (captured in audit); everything is filterable and exportable; the admin area is visually distinct (e.g., a banner) so admins always know they're in the control plane; **impersonation** ("view as user"), if built, shows a persistent "You are viewing as …" bar and writes start/stop audit events.

**Entry points:** web `/admin` (guarded), and a slimmer org-admin surface under `/account` for customer org owners (their org only). Mobile: read-only admin views later (P2).

---

## 5. Access-control model
Move from **role-only** to **role → permission** (RBAC), org-scoped, least-privilege.

- **Permission** = a capability string, `resource:action` (e.g. `accounting:read`, `accounting:post_entry`, `users:invite`, `roles:manage`, `entitlements:manage`, `audit:read`).
- **Role** = a named, editable set of permissions. Built-in roles seeded from today's `UserRole` values; keep them but back them with permission sets.
- **Assignment** = user has a role **within an org**; the effective permission set is the union of granted role(s) minus any time-expired grants.
- **Two hard tiers:** a **platform super-admin** flag (JHI internal, can cross orgs) that is *separate* from the customer **org-admin** role (bounded to their org). Org-admins can never grant platform-super-admin or see other orgs.

**Draft capability matrix (illustrative — finalize during build):**

| Capability | Super-Admin (JHI) | Org-Admin | Member (role-based) |
|---|---|---|---|
| Manage all orgs/users | ✅ | ✅ own org only | ❌ |
| Define roles & permissions | ✅ | ❌ | ❌ |
| Invite / deactivate users | ✅ | ✅ own org | ❌ |
| Assign roles | ✅ any | ✅ non-admin, own org | ❌ |
| Manage data entitlements | ✅ | ❌ | ❌ |
| Post journal entries | ✅ | per role | per role |
| View audit log | ✅ all | ✅ own org | ❌ |
| Manage API keys / flags | ✅ | scoped (later) | ❌ |

**Principle:** default-deny. Every product endpoint should require an authenticated principal **and** the specific permission — closing the current open-endpoint gap.

---

## 5A. AI-agent administrators (human + machine admins)
Administration must support **AI agents acting as system administrators**, alongside humans — JHI already runs AI service agents (Ava/Max/Sage/Quinn/Tess with founder escalation), and this extends that pattern into the admin control plane with tighter controls.

**Identity — agents are first-class, non-human principals.**
- Extend the principal with `principal_type` = `human | agent` and an `agent_id`. Agents are **service identities**, never a human's login/session.
- Agents authenticate with **scoped, short-lived, rotatable credentials** (an agent variant of API keys), not passwords/human tokens.
- Every agent has a **human owner/sponsor** and a written **charter** (what it may do, on whose authority).

**Bounded autonomy — the core control.** Each agent-admin operates at a declared tier per capability:
| Tier | Examples | Control |
|---|---|---|
| **Autonomous** (low-risk, reversible) | read/triage, detect anomalies, draft/route, generate reports, *propose* grants | agent acts, everything audited |
| **Human-approved** (sensitive/irreversible) | grant/revoke access, change roles, change entitlements, deactivate users, billing changes | agent **proposes → human approves** (four-eyes); agent cannot self-approve |
| **Forbidden** (never) | grant platform-super-admin, disable/alter audit, change security policy, read raw secrets, cross-tenant export beyond scope | hard-blocked in code, not policy |

**Guardrails.**
- **Least privilege + hard caps:** narrowly scoped permissions; per-agent rate/volume limits so a loop can't cascade.
- **Kill switch:** any human super-admin can **instantly suspend** an agent (revoke its credentials/sessions).
- **Non-repudiation:** every agent action is audited with the agent identity, its human sponsor, the trigger/source, and a machine-readable **reason/citation**.
- **Confused-deputy protection:** when acting on someone's behalf, an agent's effective authority is **capped at the requester's own permissions** (an agent can't be used to exceed the human's rights).
- **Prompt-injection containment:** untrusted input (support tickets, uploaded CIMs/docs, web content) can **never directly trigger a privileged action** — such actions route through the approve queue. Agents treat external text as data, not commands.
- **Time-boxed elevation:** any elevated grant to an agent expires automatically.
- **Data-license aware:** agents obey the same data entitlements as humans (no licensed-data leakage).

**Where it lives:** the **Admin → Agents & Automation** area (identity, scope, autonomy tier per capability, pending approvals, activity feed, kill switch). Reuses the same role→permission engine — an "agent-admin" is a permission set assigned to an agent principal, plus its autonomy policy.

## 6. Data model additions (sketch)
Additive to the existing schema; no rewrite of `UserDB`/`OrganizationDB`/`MembershipDB`.

- `permissions(code, description)`
- `roles(id, name, org_id NULL=built-in, is_system)`
- `role_permissions(role_id, permission_code)`
- `user_roles(user_id, org_id, role_id, granted_by, expires_at NULL)` — supports time-boxed grants
- `invitations(id, email, org_id, role_id, token, status, invited_by, expires_at)`
- `access_requests(id, user_id, requested_permission/role, status, reviewer, decided_at, reason)`
- `api_keys(id, org_id, name, hashed_key, scopes, created_by, last_used_at, revoked_at)`
- `agents(id, name, owner_user_id, charter, status, hashed_credential, created_at, suspended_at)` — non-human admin principals (kill switch = set `suspended_at` + revoke credential)
- `agent_autonomy(agent_id, permission_code, tier)` — `autonomous | human_approved | forbidden` per capability
- `feature_flags(key, scope_type, scope_id, enabled)`
- `sessions` / token-revocation list (for "end session" and rotation)
- Extend `AuditLogDB` usage to **all** admin mutations (already the right shape).

---

## 7. Backend API surface (proposed, all permission-guarded)
`/admin/users` (GET/POST/PATCH), `/admin/users/{id}/deactivate|reactivate|reset-mfa|end-sessions`, `/admin/invitations` (GET/POST/DELETE), `/admin/roles` + `/admin/roles/{id}/permissions`, `/admin/access-requests` (GET/POST/decision), `/admin/organizations` (+ suspend/transfer), `/admin/entitlements`, `/admin/api-keys`, `/admin/feature-flags`, `/admin/audit-logs`, `/admin/health`. Enforced by a new `require_permission("…")` dependency layered on the existing `get_current_principal`/`require_admin`.

---

## 8. Concerns & risks (the "any concerns" ask)
Ordered by severity.

1. **🔴 Open product endpoints today.** Most module routers have no auth. Shipping an admin/grant UI while the endpoints it "protects" are publicly callable is false assurance. **Enforce `get_current_principal` + `require_permission` across all product routers as part of / before P0.** This is the top item.
2. **🔴 Privilege escalation.** Admins granting themselves/others elevated access is the classic risk. Mitigate: platform-super-admin is a separate, tightly-held flag; org-admins can't grant platform scope or cross orgs; **no self-escalation** (can't grant yourself a permission you lack); optional **separation-of-duties / four-eyes approval** for sensitive grants (entitlements, super-admin).
3. **🔴 Admin MFA + session control.** Any admin account must have **MFA enforced**; support immediate **session/token revocation** (today JWTs can't be revoked before expiry — add a revocation list / short TTL + refresh). Consider admin IP allow-listing and a **break-glass** procedure.
4. **🟠 Audit integrity.** Audit must be **append-only** and cover *every* admin mutation with actor, before/after, reason, IP/UA. Protect against deletion; consider periodic export/WORM. (Table exists; coverage must expand.)
5. **🟠 Impersonation ("view as").** Powerful and dangerous. If built: explicit start/stop, persistent banner, full audit, and **never** allow impersonating another super-admin; scope to read-only first.
6. **🟠 Data-license entitlements.** The NASDAQ/Sharadar license constrains who may access derived data and internal-use vs. distribution. The admin module must be the **enforcement point** for data entitlements, or we risk a license breach. Tie to the pending derived-data addendum.
7. **🟠 Multi-tenant isolation.** Every admin query must be org-scoped for org-admins; a missing `WHERE org_id=…` leaks across tenants. Centralize scoping; test it.
8. **🟡 Secrets & API keys.** Store only hashed keys; show the secret once; scope narrowly; rotate/revoke; never reuse a human token for machine access.
9. **🟡 PII & compliance.** Admin views expose user data — minimize fields, log access, support data-subject export/delete. Keep the software/data-publisher posture (NAICS 513210); admin tooling is not investment advice.
10. **🟡 Lockout / recovery.** Don't build a system where losing the sole super-admin bricks administration — define recovery (a second break-glass admin, secured).
11. **🟡 Rate-limit / brute force on admin.** Admin login + sensitive actions should be rate-limited and alerted.
12. **🟠 AI-agent administrators (non-human admins).** Powerful and novel-risk (see §5A). Specific threats: **prompt injection** (an agent tricked by untrusted input into granting access — mitigate by routing all privileged actions through human approval and treating external text as data, never commands); **confused deputy** (agent exceeding the requester's rights — cap agent authority at the requester's permissions); **runaway/looping** actions (hard volume caps + kill switch); **over-permissioning** (least privilege, short-TTL scoped credentials); and **non-repudiation** (every agent action attributable to the agent + its human sponsor). Agents must never self-approve, grant super-admin, or disable audit.

---

## 9. Non-negotiable guardrails (proposed)
- Default-deny; least privilege; every mutation audited with a reason.
- MFA required for all admin/super-admin accounts.
- Super-admin (platform) strictly separate from org-admin (customer).
- No self-escalation; four-eyes for the most sensitive grants.
- Data entitlements enforced centrally, aligned to the data license.
- **AI-agent admins:** propose-only for sensitive actions by default; never self-approve, grant super-admin, or disable audit; always attributable to a human sponsor; instantly suspendable (kill switch).

---

## 10. Phased rollout (when you give the command)
- **P0 — Foundation & safety:** enforce auth+permission across all product endpoints; `require_permission`; seed permissions/roles from current `UserRole`; Users list + deactivate + role change; expand audit coverage; enforce admin MFA. *(Closes the open-endpoint gap and delivers "granting access.")*
- **P1 — Workflow:** invitations, access-requests/approvals (SoD), org management, data-entitlement controls, API keys, session revocation.
- **P2 — Advanced:** feature flags, impersonation (read-only first), system-health board, org-admin self-serve surface, mobile admin views.

---

## 11. Open decisions for you
1. **Primary audience first?** Platform super-admin only for v1 (recommended), or ship org-admin alongside?
2. **RBAC depth:** full role→permission matrix now, or start with the 8 existing roles mapped to fixed permission sets and add the matrix in P1?
3. **Impersonation:** do you want "view as user" at all? (High utility, high risk.)
4. **Approvals (four-eyes):** required for entitlements/super-admin grants, or audit-only given you're currently a solo operator?
5. **Session model:** add refresh tokens + revocation now (needed for real "end session"), or accept short-lived JWTs for v1?
6. **Scope of P0 endpoint lockdown:** lock every module at once, or gate behind a feature flag to avoid disrupting the current open demo?
7. **AI-agent admin autonomy:** which admin capabilities may agents perform **autonomously** vs. **propose-only (human-approved)** for v1? (Recommended v1: agents are *propose-only* for every grant/role/entitlement/deactivation; autonomous only for read/triage/report — then widen per proven track record.)

---

*Provenance: founder signature of record `69M2705M`. © 2026 JHI Research & Analytics Firm, Inc. All rights reserved. Confidential — internal design document; not legal, tax, or security-audit advice.*
