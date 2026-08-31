# Aegira — AWS-Native Always-On Deployment Construct

**JHI-SIG:** `69M2705M` · Product = **Aegira** · Publisher = **JHI Research &
Analytics Firm, Inc.** · **Region:** `us-east-1` (same as Bedrock/SES).
**Companions:** [`.github/workflows/deploy.yml`](../.github/workflows/deploy.yml) ·
[`deploy/aws/`](../deploy/aws/) · supersedes the "pick a deploy target" open item
in `docs/AWS_TIER1_ACTIVATION.md` / `docs/AWS_ENHANCEMENT_ROADMAP.md`.

> This is the board-ready construct for turning Aegira into an **AWS-native,
> always-on** product — **no Render**, no self-managed servers. It is a
> **config + docs** plan: it changes nothing in the application code. The app is
> already deploy-ready (same-origin proxy, `DATABASE_URL`, `/health` + `/ready`
> probes, production config validation).

---

## 1. Architecture at a glance

```
 Developer ──PR──> main ──(GitHub Actions, OIDC)──┐
                                                  │ build backend + frontend
                                                  │ push to private ECR
                                                  ▼
   ┌─────────────────────── AWS (us-east-1) ───────────────────────┐
   │  Amazon ECR (private)      AWS Secrets Manager (runtime secrets)│
   │      backend img  frontend img       DATABASE_URL, AUTH_JWT_...  │
   │          │            │                    │                     │
   │          ▼            ▼                    │ injected at start    │
   │   ┌─App Runner──────────────────┐          │                     │
   │   │ frontend (Next.js) :3000  ◄──┼─browser (same-origin /api/v1) │
   │   │      │ server-side proxy     │          │                     │
   │   │      ▼                       │          ▼                     │
   │   │ backend (FastAPI) :8000  ────┼──VPC connector──► RDS Postgres │
   │   └──────────────────────────────┘         (PRIVATE subnets,     │
   │                                              not public)          │
   │   Route 53  ──► aegiraenterprise.com ──► frontend service        │
   └────────────────────────────────────────────────────────────────┘
```

**Building blocks:**

| Concern | AWS service | Why |
|---|---|---|
| Image registry | **Amazon ECR** (private) | Versioned, scanned, private image repos. |
| Compute (always-on) | **AWS App Runner** ×2 (backend + frontend) | Managed always-on container services with auto-scaling, TLS, and **auto-deploy on new image** — no cluster to run. |
| Database | **Amazon RDS for PostgreSQL** | Managed, encrypted, backed-up Postgres in a **private** subnet. |
| CI/CD | **GitHub Actions** | build → push → deploy, authenticated by **OIDC** (no static keys). |
| Runtime secrets | **AWS Secrets Manager** | Encrypted secret storage; injected into App Runner at start. |
| DNS / custom domain | **Amazon Route 53** | `aegiraenterprise.com` → frontend service. |

**Why App Runner (vs. ECS/Fargate or Render):** it is the lowest-operational-
overhead way to run two always-on containers with built-in TLS, health checks,
auto-scaling, and image-push auto-deploy, while keeping **everything inside our
AWS account** (aligns with the NASDAQ no-spillage governance story) and next to
Bedrock/SES in `us-east-1`. It removes Render from the stack entirely.

**How the app already fits:**
- The frontend serves the browser and **proxies `/api/v1` server-side** to the
  backend (`next.config.mjs` rewrites → `API_PROXY_TARGET`). The browser only
  ever talks to the frontend origin, so there is **no CORS** and the backend's
  localhost-only CORS config is a non-issue in this topology.
- The backend reads **`DATABASE_URL`** (→ RDS) and validates production config on
  boot (`APP_ENV=production` requires a ≥32-byte `AUTH_JWT_SECRET` and a Postgres
  URL — see `backend/app/config.py`).
- Health probes already exist: backend `GET /health` (liveness) and `GET /ready`
  (DB reachability); frontend `GET /`.

---

## 2. Three-environment model

| Environment | Where | Lifecycle | Deploys from |
|---|---|---|---|
| **local** | Docker Desktop (`docker compose up`) | throwaway | your laptop (see `docs/RUN_LOCALLY.md`) |
| **staging** | App Runner (always-on) | persistent | **auto** on every merge to `main` |
| **production** | App Runner (always-on) | persistent | **promoted** via tag/manual approval |

**Promote flow (numbered):**

1. Cut a **feature branch**, commit, open a **PR** to `main`.
2. **Merge** the PR → the `deploy.yml` `deploy-staging` job auto-builds both
   images, pushes to ECR, and rolls the **staging** App Runner services.
3. **Verify on staging** (the pipeline runs a `/health` + `/` smoke check; do
   manual QA on the staging URL).
4. **Promote to production**: either push a `v*` tag or run the
   `promote-production` workflow (`workflow_dispatch`). This is gated by the
   GitHub **`production` Environment** (manual approval).
5. Promotion copies the **tested backend image by digest** to the `:production`
   tag (byte-identical artifact) and **rebuilds the frontend** for prod (its
   proxy target is baked at build time — see §4), then rolls the **production**
   services and smoke-checks them.

Local uses SQLite by default and is never wired to AWS; staging and production
each get their **own** RDS instance, secrets, VPC, and App Runner services
(`EnvironmentName` parameter in the CloudFormation stacks).

---

## 3. Security mitigations (each mapped to the risk it closes)

| Risk it closes | Mitigation | Where |
|---|---|---|
| **Long-lived static AWS keys leaking from CI** | **GitHub OIDC → IAM role.** CI assumes a role via a short-lived web-identity token; no `AWS_ACCESS_KEY_ID`/`SECRET` are stored in GitHub. Trust policy pins the exact org/repo. | `deploy/aws/02-github-oidc-deploy-role.yaml`, `deploy.yml` |
| **Publicly reachable / attackable database** | **RDS private + locked SG.** `PubliclyAccessible=false`, private subnet group, security group accepts `5432` **only** from the App Runner VPC connector SG (no CIDR, no `0.0.0.0/0`). | `deploy/aws/04-network.yaml`, `05-rds-postgres.yaml` |
| **Plaintext secrets in the image/repo/CI logs** | **Secrets Manager for runtime secrets.** Encrypted at rest; injected into App Runner via `RuntimeEnvironmentSecrets` at start. Never baked into images or committed. RDS master password is generated + stored by RDS. | `deploy/aws/03-secrets.yaml`, `06-apprunner-services.yaml` |
| **Over-privileged deploy role (blast radius)** | **Least-privilege IAM deploy role.** Grants only ECR push and App Runner `StartDeployment`/`Describe` — no create/delete, no IAM, no RDS. App Runner instance role reads only `aegira/<env>/*` secrets. | `deploy/aws/02-...yaml`, `06-...yaml` |
| **Anonymous/public image pulls** | **Private ECR** with scan-on-push and lifecycle expiry. | `deploy/aws/01-ecr.yaml` |
| **Insecure production config shipped by accident** | App enforces prod safety on boot (`Settings.validate()`): rejects the dev JWT secret, sub-32-byte secrets, and SQLite in production. | `backend/app/config.py` (existing) |

Additional hardening available as a follow-on (out of scope here, tracked in
`docs/AWS_ENHANCEMENT_ROADMAP.md`): CloudFront + WAF/Shield in front of the
frontend, GuardDuty/CloudTrail, and KMS CMKs for Secrets/RDS.

---

## 4. The frontend↔backend wiring gotcha on App Runner

App Runner gives each service its **own stable URL**
(`https://<id>.us-east-1.awsapprunner.com`). The catch:

> **Next.js bakes `rewrites()` at *build* time.** The same-origin `/api/v1`
> proxy target (`API_PROXY_TARGET`) is a **Docker build arg** (see the root
> `Dockerfile` and `next.config.mjs`), **not** a runtime env. So the frontend
> image must be built **knowing the backend's URL**.

Because the backend and frontend get **separate** URLs, the frontend image is
**environment-specific** (staging's proxy target ≠ production's). Two supported
patterns:

- **(A) Two-phase build — pipeline default.** Create/deploy the backend service
  first (its URL is stable across deployments), then in CI read it with
  `aws apprunner describe-service ... --query 'Service.ServiceUrl'` and pass it
  as `--build-arg API_PROXY_TARGET=https://<backend-url>` when building the
  frontend. This is exactly what `deploy.yml` does for both staging and prod.
- **(B) Stable custom domain.** Assign `api.aegiraenterprise.com` to the backend
  App Runner service (Route 53 + App Runner custom domain) and always build the
  frontend with `API_PROXY_TARGET=https://api.aegiraenterprise.com`. This makes
  the frontend build arg constant and decouples it from the generated URL.

Consequences for promotion (§2): the **backend** image is environment-agnostic
(all config comes from runtime secrets) and is promoted **by digest**; the
**frontend** image must be **rebuilt per environment** with that environment's
backend URL.

**Database wiring:** the backend gets `DATABASE_URL` from Secrets Manager
(`aegira/<env>/DATABASE_URL`), composed from the RDS endpoint + the RDS-managed
master credential secret. The backend reaches RDS **only** through the App
Runner VPC connector into the private subnets.

The build args map 1:1 to the root `Dockerfile` ARGs:

| Build arg | Value | Source |
|---|---|---|
| `NEXT_PUBLIC_API_BASE_URL` | `/api/v1` | constant (same-origin) |
| `API_PROXY_TARGET` | `https://<backend App Runner URL>` (or custom domain) | resolved in CI |
| `NEXT_PUBLIC_SITE_URL` | `https://aegiraenterprise.com` (prod) / staging URL | GitHub var |

---

## 5. Runbook — Founder actions vs. Cy actions

### Founder (AWS account owner) — one-time enablement
1. **Confirm region** = `us-east-1` (Bedrock/SES parity) and the AWS account id.
2. **Set up GitHub OIDC → IAM deploy role.** Deploy `02-github-oidc-deploy-role.yaml`
   (or create a scoped IAM role manually) with your `GitHubOrg`/`GitHubRepo`.
   Copy the role ARN into the GitHub secret `AWS_DEPLOY_ROLE_ARN`.
3. **Put runtime secret *values* in Secrets Manager.** After `03-secrets.yaml`
   creates the empty keys, paste real values (at minimum `AUTH_JWT_SECRET` via
   `openssl rand -hex 32`, and `DATABASE_URL` composed from the RDS endpoint).
   Never commit these.
4. **Populate GitHub secrets/vars** from the §"GitHub secrets & vars" table.
5. **Add Route 53 records later** — point `aegiraenterprise.com` (and optionally
   `api.aegiraenterprise.com`) at the App Runner services once staging is green.

### Cy (VP Software Engineering — AI) — pipeline + wiring + verification
1. Author/maintain the **pipeline** (`.github/workflows/deploy.yml`) and the
   **CloudFormation** (`deploy/aws/*`).
2. Deploy the **infra stacks** in order (ECR → OIDC → secrets → network → RDS →
   App Runner) per environment (`deploy/aws/README.md`).
3. Wire **RDS/VPC**: private subnet group, connector SG, RDS SG locked to the
   connector; compose and store `DATABASE_URL`.
4. Wire the **frontend↔backend** build arg (§4) and confirm the same-origin proxy
   resolves on App Runner.
5. **Verify**: `/health` + `/ready` on the backend URL, `/` and a real user flow
   on the frontend URL (register a staff email → log in → load `/dashboard`).
6. Manage **promotion** to production behind the Environment gate.

---

## 6. Cost notes (rough, us-east-1, monthly)

Order-of-magnitude for an always-on staging + production footprint (list price;
usage-based, starts small):

| Item | Rough monthly |
|---|---|
| App Runner — 4 services (2 envs × backend+frontend), ~1 vCPU/2 GB, low traffic | ~$25–60/service active; **provisioned/idle** billed lower — budget ~$120–200 total |
| RDS — 2× `db.t4g.micro`/`small` (staging + prod), gp3, single-AZ staging | ~$25–90 |
| NAT gateway — per env (hourly + data) | ~$32/env + data |
| ECR storage + Secrets Manager (~$0.40/secret) + Route 53 hosted zone ($0.50) | ~$5–15 |
| **Total (both envs, low traffic)** | **~$250–450/mo** |

Cost levers: single-AZ + smaller RDS for staging; one shared NAT (or VPC
endpoints to drop NAT for AWS-only egress); scale App Runner min-instances to
zero-idle where acceptable. See `docs/AWS_COST_10K_USERS.md` for scale modeling.

---

## 7. Rollback / redeploy

- **App Runner keeps deployment history.** To roll back, redeploy the previous
  image tag/digest: for the backend, re-point `:production` to the prior
  `:prod-<sha>` (or `:<sha>`) with `docker buildx imagetools create` and
  `aws apprunner start-deployment`; for the frontend, rerun the promote job at
  the previous SHA. A failed deployment auto-rolls-back to the last healthy
  image (App Runner health checks gate the swap).
- **Immutable, digest-addressable artifacts** (`:<sha>` tags) make any past build
  reproducible.
- **Data** is safe across redeploys: RDS is independent of the compute; App
  Runner recreation loses no data.

## 8. Ongoing upgrades

Every future change — app code, dependency bumps, config — flows through the
**same pipeline**: feature branch → PR → merge to `main` → staging auto-deploy →
verify → tag/dispatch → gated production promotion. Infra changes go through the
same PR flow by editing `deploy/aws/*` and re-running `aws cloudformation deploy`
(idempotent). No manual server access is ever required.

---

## GitHub secrets & vars

Set these in **Settings → Secrets and variables → Actions**. Nothing here
contains a real value in the repo — the Founder supplies them.

### Secrets (encrypted)

| Name | Example / shape | Purpose |
|---|---|---|
| `AWS_DEPLOY_ROLE_ARN` | `arn:aws:iam::<acct>:role/aegira-ci-deploy-role` | OIDC `role-to-assume` for CI (from `02-...yaml` output). |

### Variables (non-secret)

| Name | Example | Purpose |
|---|---|---|
| `AWS_REGION` | `us-east-1` | Region for all AWS calls. |
| `AWS_ACCOUNT_ID` | `123456789012` | Builds the ECR registry host. |
| `ECR_BACKEND_REPO` | `aegira/backend` | Backend ECR repo name. |
| `ECR_FRONTEND_REPO` | `aegira/frontend` | Frontend ECR repo name. |
| `APPRUNNER_BACKEND_SERVICE_ARN_STAGING` | `arn:aws:apprunner:us-east-1:<acct>:service/aegira-staging-backend/...` | Staging backend service (deploy + URL lookup). |
| `APPRUNNER_FRONTEND_SERVICE_ARN_STAGING` | `arn:aws:apprunner:...aegira-staging-frontend/...` | Staging frontend service. |
| `APPRUNNER_BACKEND_SERVICE_ARN_PRODUCTION` | `arn:aws:apprunner:...aegira-production-backend/...` | Production backend service. |
| `APPRUNNER_FRONTEND_SERVICE_ARN_PRODUCTION` | `arn:aws:apprunner:...aegira-production-frontend/...` | Production frontend service. |
| `NEXT_PUBLIC_SITE_URL_STAGING` | `https://staging.aegiraenterprise.com` | Canonical/OG base for staging (frontend build arg). |
| `NEXT_PUBLIC_SITE_URL_PRODUCTION` | `https://aegiraenterprise.com` | Canonical/OG base for prod (frontend build arg). |

Also create a GitHub **Environment** named `production` with required reviewers
(the manual approval gate the `promote-production` job depends on).

The runtime application secrets (`DATABASE_URL`, `AUTH_JWT_SECRET`,
`APP_ENCRYPTION_KEY`, `JHI_STAFF_EMAILS`, `FRED_API_KEY`,
`NASDAQ_DATA_LINK_API_KEY`, `DATA_GOV_API_KEY`, `STRIPE_WEBHOOK_SECRET`,
`AWS_BEARER_TOKEN_BEDROCK`, …) live in **Secrets Manager** (`aegira/<env>/*`),
**not** in GitHub — App Runner injects them at start.
