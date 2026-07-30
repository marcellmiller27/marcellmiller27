# Domain Registration Runbook — `aegiraenterprise.*` family (Route 53)

**JHI-SIG:** `69M2705M` · Companion to `docs/board/BRAND_NAMING_AEGIRA.md`.
Registers the remaining Aegira domains alongside the already-owned **`aegiraenterprise.com`**.

Domains to register: **`aegiraenterprise.ai`**, **`aegiraenterprise.io`**, **`aegiraenterprise.dev`**, **`aegiraenterprise.app`**.

---

## Prices (Amazon Route 53, USD, excl. taxes — confirm live before running)
| TLD | Registration | Renewal | Notes |
|---|---|---|---|
| `.ai` | **$129 / yr — 2‑year minimum (~$258 up front)** | ~$137 / yr | Anguilla ccTLD; **`DurationInYears` must be `2`** |
| `.io` | $71 / yr | $71 / yr | — |
| `.dev` | $17 / yr | $17 / yr | Google TLD, HSTS‑preloaded (always HTTPS) |
| `.app` | $20 / yr | $20 / yr | Google TLD, HSTS‑preloaded (always HTTPS) |

**Estimated up-front total ≈ $366** (`.ai` at 2 yr + `.io` + `.dev` + `.app`). AutoRenew is enabled by the script.

## Prerequisites
1. **`aws` CLI installed** and **authenticated** to the AWS account that owns `aegiraenterprise.com` (`aws configure`, SSO, or an IAM role) with `route53domains:RegisterDomain` + `route53domains:GetOperationDetail`.
2. **`python3`** (used to assemble each request JSON — no extra packages).
3. Registrant PII ready (name, org, address, phone `+1.XXXXXXXXXX`, email).

## Steps
1. Fill in your contact details (kept local; **gitignored**):
   ```bash
   cp scripts/domains/contact.example.json scripts/domains/contact.json
   # edit scripts/domains/contact.json — replace every REPLACE_* value
   ```
2. Run the registrar (submits all four; `.ai` auto-set to 2 years):
   ```bash
   bash scripts/domains/register-domains.sh
   ```
   It prints an **OperationId** per domain and appends them to `scripts/domains/operations.log`.
3. Track each registration:
   ```bash
   aws route53domains get-operation-detail --region us-east-1 --operation-id <OperationId>
   ```
   Status moves `SUBMITTED → IN_PROGRESS → SUCCESSFUL`.

## TLD-specific notes
- **`.ai`** — 2‑year minimum registration (the script sets `DurationInYears=2`). If it **rejects WHOIS privacy**, edit the `.ai` row in `register-domains.sh` to `:2:false` and re-run just that domain (some ccTLDs don't support privacy protection).
- **`.dev` / `.app`** — on the HSTS preload list; browsers force HTTPS. You'll need valid TLS on any host you point them at (ACM handles this behind CloudFront).
- Route 53 does **not** register **special/premium-priced** names — `aegiraenterprise.*` should be standard, but the API will error if a name is premium.

## Post-registration
- Route 53 auto-creates a **hosted zone** per domain with four name servers.
- **Canonical policy (per board record):** `aegiraenterprise.com` is canonical; point the others via **301 redirect** to `.com` (or a dedicated sub-path) — registrar/DNS-level, no app change.
- For **email**, verify the SES sender domain on `aegiraenterprise.com` (see `docs/AWS_TIER1_ACTIVATION.md`).

## Note on running this from the Cursor cloud agent
This environment has **no `aws` CLI and no AWS credentials**, and registration is a **paid action requiring your PII** — so run the script yourself in your AWS-authenticated shell. If you'd prefer I run it here, you'd need to install/authenticate the AWS CLI in the VM, provide the contact details, and give an explicit go — but self-serve is recommended for a paid purchase.
