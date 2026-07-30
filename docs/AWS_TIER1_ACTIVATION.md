# AWS Tier‑1 Activation Runbook — SES · CloudFront+S3 · RDS

**JHI-SIG:** `69M2705M` · Companion to `docs/AWS_ENHANCEMENT_ROADMAP.md`.
Product = **Aegira**; legal entity/publisher = **JHI Research & Analytics Firm, Inc.**

This is the concrete, ordered plan to turn on the Tier‑1 stack. **Application code that can
ship now is already in place** (see §1). Live provisioning is gated on three Founder/AWS
prerequisites (§0).

---

## 0. Prerequisites the Founder/AWS must provide (why this can't be fully auto‑exec'd)
1. **AWS deployment credentials** — an IAM user/role with `ses:*`, `cloudfront:*`, `s3:*`,
   `rds:*` (least‑privilege scoped) as `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` (or a
   role). *(The environment currently has only the Bedrock bearer token, which is scoped to
   Bedrock and cannot provision SES/CloudFront/S3/RDS.)*
2. **Deploy target** — pick one: **App Runner**, **ECS/Fargate**, or **Amplify/Lightsail**.
   This determines the CloudFront origin and RDS/VPC wiring.
3. **DNS + SES sender domain** — `aegiraenterprise.com` (in Route 53, registration in
   progress): verify the **SES sender domain** (DKIM + SPF + DMARC) and point app DNS at the
   deploy target.

---

## 1. SES — email the newsletters (Step‑B send)  ·  CODE READY ✅
The application layer is implemented and flag‑gated (safe dry‑run by default):
- `backend/app/email_service.py` — Aegira‑branded, inline‑styled HTML email (JHI legal
  footer + `JHI-SIG`); Amazon SES via lazy `boto3`; **dry‑run** when unconfigured.
- `POST /api/v1/newsletters/{edition}/send` — **staff‑only**; builds the full edition
  (E2‑elevated when enabled) and sends via SES, else returns a dry‑run preview. Defaults to a
  test send to the requesting staff member.

**Go live:**
1. Verify the SES sender domain for `aegiraenterprise.com` (console or IaC); move out of the
   SES sandbox for external recipients.
2. Set Secrets: `ENABLE_EMAIL_SEND=1`, `SES_SENDER="Aegira <newsletters@aegiraenterprise.com>"`,
   plus AWS credentials with `ses:SendEmail`.
3. Recreate the backend **from a shell that carries the Secrets** (see `AGENTS.md`), then test:
   `POST /newsletters/economic-brief/send` → expect `status: "sent"`, `provider: "ses"`.
4. **Scheduled auto‑send** (roadmap EventBridge+Lambda) and a **subscriber list +
   unsubscribe/CAN‑SPAM** are the next increment on top of this endpoint.

## 2. CloudFront + S3 — fast, scalable delivery  ·  NEEDS DEPLOY TARGET
- S3 bucket for static assets + generated PDFs/workbooks; CloudFront distribution in front of
  the app origin (the chosen deploy target) and the S3 bucket; HTTPS via ACM cert for
  `aegiraenterprise.com`.
- App is already **same‑origin‑proxy** configured (`next.config.mjs` rewrites), so CloudFront
  sits on top with no app code change.
- Blocked on: deploy target (origin) + ACM/DNS.

## 3. RDS (managed Postgres) — durable, backed‑up DB  ·  CODE READY ✅ (needs provisioning)
- The backend already reads **`DATABASE_URL`** (currently the Compose `db` service). Migrating
  to RDS is **config‑only**: provision RDS Postgres in the VPC, then set `DATABASE_URL` to the
  RDS endpoint. `init_db()` creates tables on first boot; enable automated backups + Multi‑AZ.
- Blocked on: AWS provisioning + VPC (tied to the deploy target).

---

## Recommended order
**SES first** (subscribers receive editions — code is ready, just needs domain + creds) →
**RDS** (config‑only once provisioned) → **CloudFront+S3** (after the deploy target is chosen).

## Status
- ✅ SES **application layer** shipped (dry‑run verified); flip on with domain + creds.
- ✅ RDS **app‑readiness** confirmed (`DATABASE_URL`).
- ⏳ CloudFront+S3 and live SES/RDS provisioning await the deploy target + DNS + AWS creds.
