# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-07-12 · **Type:** Founder working session · **Recorder:** Cy (VP, Software Engineering — AI teammate)
**Present:** Founder.

> NOT legal/tax/accounting/investment/security-audit advice. Prior session: `docs/board/BOARD_MINUTES_2026-07-11.md`.
> Companion design doc: `docs/SYSTEM_ADMINISTRATOR_MODULE.md` (PR #55).

---

## 1. Context
- PRs #51, #53, #54, #52 merged to `main` (accounting module: proxy + view + journal posting; Documents/downloads page; full GAAP chart of accounts; finance model + verified competitor deep-dive).
- Founder commissioned a **dual System Administrator module** design (platform gatekeeper + per-subscription org gatekeeper). Write-up delivered as PR #55. Agreed it is a **P0**.
- Founder's governing priority: **make the platform robust and complete before any launch.** Question tabled: *when* to build the dual admin.

## 2. Decision of record — sequencing principle
**"Pour the security foundation first; layer the admin experience just-in-time."**
- **Authorization is plumbing, not a feature.** Auth/permission enforcement is a cross-cutting concern; retrofitting it across N modules costs ≈ N×, enforcing it as a gate once costs ≈ 1×. Therefore the **enforcement layer is the next foundational workstream**, *before* more product surface is added on top of currently-open endpoints.
- **The admin UX is layered by need:**
  - **Now / next (foundation):** enforce `auth + permission` across all product endpoints; admin MFA; expand audit coverage; session/token revocation model. (This *is* the gatekeeper skeleton.)
  - **Before ANY external users (private beta):** platform super-admin + user management (invite / deactivate / role change) — you cannot safely run even a closed beta on open endpoints, and you'll be manually granting access.
  - **Before public/paid launch:** org-admin self-serve tier + data entitlements + invitations/approvals — customers must self-manage their own users.
- **Rationale:** this avoids the two failure modes — (a) building lots of features on open endpoints and paying a large retrofit later, and (b) over-building admin workflow before there are users to administer.

## 3. Launch-readiness gates (where admin fits)
"Robust & complete" is objective when tracked as go/no-go gates. Dual-admin is **one of ~8**:
1. **AuthZ enforcement + System Admin (P0 foundation)** — this workstream.
2. **Opportunity/Deal Score validation** (H5) — no predictive claim until it clears the pre-registered bar.
3. **NASDAQ/Sharadar derived-data rights** (addendum) — gates client-facing data + entitlements.
4. **Security hardening in prod** — rate-limit ON, secrets manager, security headers/CORS, dependency scanning.
5. **Data safety** — Postgres backups + tested restore, tenant-isolation tests.
6. **Observability** — error tracking, structured logs, uptime/status, alerting.
7. **Legal/compliance** — ToS, Privacy Policy, DPA, acceptable-use, AI-output "research not advice" disclaimers, data-subject export/delete.
8. **Billing↔access coupling** — subscription status drives entitlement (past_due/canceled → auto-downgrade).

## 4. Blind spots flagged (things not yet anticipated)
- **Transactional email/identity infra** (SES/Postmark + SPF/DKIM/DMARC) — invitations, password reset, and MFA recovery are *blocked* without it. Frequently missed; it gates the admin invite flow.
- **Immediate revocation** — current JWTs can't be revoked before expiry, so "remove access" isn't truly instant. Needs refresh tokens + a revocation list (or very short TTLs).
- **Billing-driven entitlement** — access should follow subscription status automatically; otherwise churned accounts keep access.
- **Data-license entitlement enforcement** — the admin module must be the single enforcement point for who can access SF1/NASDAQ-derived output (license risk otherwise).
- **Backups/DR with tested restore** before real customer data exists.
- **Admin break-glass / recovery** — losing the sole super-admin must not brick administration (a sealed second recovery admin).
- **Seed/demo-data hygiene** — seeded accounting/demo data must never mingle with real tenant data.
- **Incident-response & breach plan**, **data-subject rights (export/delete)**, **rate-limiting ON in prod**, **staging environment + CI-run tests**.

## 5. Bright ideas / suggestions
- **Enforcement behind a feature flag ("enforcement mode").** Land auth on every endpoint but flip it on per-cohort — keeps the current open demo working while removing big-bang risk and enabling instant rollback.
- **Audit-from-day-one.** Turn on full mutation auditing now, before customers arrive — cheap insurance and a strong enterprise-sales/trust artifact.
- **Entitlements built once, used twice.** The same engine that satisfies the NASDAQ license also powers plan gating (Consumer/Pro/Enterprise feature tiers). One build, two payoffs.
- **The admin grant flow unlocks a private design-partner beta.** Building super-admin invite/grant *first* is what lets you run a controlled beta with ~5–10 search funds — real usage to harden the platform pre-launch.
- **Dogfood the admin module internally** (manage staff + AI-agent access) before exposing to customers.
- **Living launch-readiness scorecard** (the §3 gates as a tracked checklist/dashboard) so "are we ready?" is objective, not a feeling.
- **Lightweight threat-model / pre-launch pen-test** once endpoints are locked down.
- **Per-module kill switches** (feature flags) for safe, reversible rollout.

## 6. Recommendation
Proceed to **P0 (auth+permission enforcement, user management, audit, admin MFA)** as the next foundational workstream — ideally landed **behind an enforcement feature flag** so the open demo is undisturbed until you flip it. Defer org-admin self-serve, approvals, and feature-flag/impersonation tooling to just-in-time (private beta → public launch). Track the eight gates in §3 as the objective definition of "ready."

---

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | Review System Admin write-up (PR #55) + these minutes; answer the 6 open decisions in the doc | Founder | 🔴 |
| 2 | On command: build P0 — enforce auth+permission across endpoints (behind enforcement flag), user management, audit coverage, admin MFA | Cy | 🔴 (gated on founder cmd) |
| 3 | Decide session model: refresh tokens + revocation now vs. short-TTL JWT for v1 | Founder + Cy | 🟠 |
| 4 | Stand up transactional email + domain auth (SPF/DKIM/DMARC) to unblock invites/reset | Founder | 🟠 |
| 5 | Create a living launch-readiness scorecard (the 8 gates) | Cy | 🟡 |
| 6 | Confirm entitlement engine also drives plan gating + data-license enforcement | Founder + Cy | 🟡 |

**Next review:** next working session.
**Recorded by:** Cy · signature of record `69M2705M`.
