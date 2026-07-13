# Security Posture & Data Protection — Honest Assessment

> **The one truth every founder must hear first:** there is **no such thing as a
> "non-hackable" or "hack-proof" platform.** Any vendor, engineer, or tool that promises
> that is either naive or lying. Every system — banks, governments, Apple, Google — can
> be attacked. What a serious company *actually* commits to is **defense-in-depth**:
> make a breach *hard*, keep the *blast radius small* if one happens, protect the most
> sensitive data even in a worst case, and be able to *detect, respond, and recover*.
>
> This document grades John Henry Investments (JHI) honestly against that bar — what is
> already strong, what is **not yet protected**, and the exact roadmap to get to
> bank-grade. It is grounded in the real code, not aspiration.
>
> **Companions:** `docs/ROBUSTNESS_READINESS_GAP_ANALYSIS.md`,
> `docs/PLATFORM_AUDIT_ANOMALIES.md`, `docs/TODO_NEXT_SESSION.md`.

---

## 0. Executive verdict (plain English)

| Question the founder asked | Honest answer |
| --- | --- |
| Is our IP / code "iron-clad"? | **Partially.** Strong foundations (modern password hashing, scoped tokens, parameterized DB access, fail-fast prod config, non-root containers), but several **P0 gaps remain open** before we can claim bank-grade. |
| Is the platform "non-hackable"? | **No platform is.** The correct goal is *defense-in-depth* — and we are **mid-maturity**, not yet hardened for real money/PII at scale. |
| Is users' banking data protected? | **Yes — largely by design choice: we do NOT store raw banking/card data.** Payments run through **Stripe** (PCI-DSS Level 1). We never see card numbers. This is our single biggest data-protection win. |
| Are addresses / personal info protected? | **At rest in our DB, yes (access-controlled), but field-level encryption and full at-rest encryption are not yet implemented.** We also currently store very little PII (see §2). |
| Is the mobile app robust and secure? | **Foundations yes** (password + TOTP 2FA + scoped challenge tokens), **but the biometric assertion is not yet cryptographically verified** (WebAuthn signature/counter) — a known P0. |

**Bottom line:** we have an above-average *foundation* for an early platform, with a
**clear, prioritized path** to bank-grade. We are **not there yet**, and it would be
dishonest to tell users otherwise. The plan in §6 closes the gap.

---

## 1. Guiding principle — what "protected" really means

We protect users with **layers**, so no single failure exposes them:

1. **Data minimization** — the safest data is the data you never collect. (Our biggest lever; see §2.)
2. **Strong identity** — modern password hashing, MFA, short-lived scoped tokens.
3. **Least privilege** — role checks, scoped tokens, narrow CORS, non-root containers.
4. **Encryption** — in transit (TLS) and at rest (DB + sensitive fields).
5. **Boundary defense** — rate limiting, input validation, secrets management, WAF.
6. **Detect & respond** — audit logs, error/anomaly monitoring, alerting, backups/DR.
7. **Process** — dependency scanning, code review, pen testing, incident response.

The rest of this doc scores each layer **as actually implemented today**.

---

## 2. What data we actually hold (and what we deliberately do NOT)

**This is the most reassuring section — and it's true.** Per `backend/app/db_models.py`:

| Data we store | Where | Sensitivity | Protection today |
| --- | --- | --- | --- |
| Email, full name | `users`, `crm_contacts`, `leads` | PII (low/medium) | Access-controlled; DB-level |
| Password **hash** (never the password) | `users.password_hash` | Credential | **PBKDF2-SHA256, 210k iters, per-user salt** ✅ |
| TOTP 2FA secret | `user_security.totp_secret` | Sensitive | ⚠️ **plaintext at rest** — needs encryption (P0) |
| Biometric credential id + public key | `device_credentials` | Public key (low) | Public keys aren't secret; assertion check is the gap |
| Phone (CRM contacts) | `crm_contacts.phone` | PII (low) | Access-controlled |
| Stripe customer/subscription **IDs only** | `subscriptions` | Reference tokens | Not secret; map to Stripe |
| Audit events | `audit_logs` | Operational | Stored (good for forensics) |

**What we do NOT store (by design — major risk reduction):**

- ❌ **No raw card numbers / CVV / bank account numbers.** Payments → **Stripe**
  (PCI-DSS Level 1). We hold only Stripe reference IDs. *We cannot leak card data we
  never possess.*
- ❌ **No SSNs / government IDs.**
- ❌ **No home addresses** in the current schema.
- ❌ **No plaintext passwords** anywhere.
- ❌ **No crypto private keys** (we explicitly rejected custody — `docs/CRYPTO_HOLDINGS_STORAGE.md`).

> **Founder takeaway:** the strongest claim we can *honestly* make to users is
> **"we don't store your banking credentials — Stripe does, under PCI-DSS Level 1, and
> we minimize the personal data we keep."** That is real, defensible, and rare for an
> early platform. **Keep it that way:** before adding any address/SSN/bank-detail field,
> implement field-level encryption first (§6).

---

## 3. Current posture — what's already STRONG (with code evidence)

| Control | Evidence | Why it matters |
| --- | --- | --- |
| **Modern password hashing** | `security.py` → PBKDF2-SHA256, **210,000** iterations, 16-byte random salt, constant-time compare | OWASP-aligned; resists offline cracking |
| **Constant-time comparisons** | `hmac.compare_digest` for tokens, TOTP, passwords | Prevents timing attacks |
| **Scoped, short-lived challenge tokens** | `create_scoped_token`/`decode_scoped_token` (2fa/biometric, 5-min TTL, scope-bound key) | A 2FA token can't be replayed as an access token |
| **RFC 6238 TOTP 2FA** | `generate_totp_secret`, `verify_totp` (drift window) | Real second factor on mobile |
| **Fail-fast production config** | `config.py` blocks default `AUTH_JWT_SECRET` / SQLite in prod | Stops the #1 deploy mistake |
| **Parameterized DB access (no raw SQL)** | SQLAlchemy ORM throughout | Structural defense vs SQL injection |
| **Pydantic input validation** | request models on every router | Rejects malformed/oversized input early |
| **Rate-limit middleware** | `rate_limit.py` (per-IP, env-gated) | Throttles brute force / abuse when enabled |
| **Audit log model** | `AuditLogDB` | Forensics + tamper-evidence foundation |
| **Container hardening** | non-root user, healthchecks, multi-worker (Dockerfiles) | Smaller blast radius |
| **Token expiry** | `decode_access_token` enforces `exp` | Limits stolen-token lifetime |

This is a **genuinely solid early foundation** — better than many seed-stage fintechs.

---

## 4. Current posture — what is NOT yet protected (the honest gap list)

Severity: **P0** = fix before real paying users/PII; **P1** = before scale; **P2** = polish.

| # | Sev | Gap | Evidence | Risk if ignored |
| --- | --- | --- | --- | --- |
| 1 | **P0** | **Biometric assertion not cryptographically verified** (presence check, not WebAuthn signature/counter) | `mobile_services.biometric_assert`; `PLATFORM_AUDIT_ANOMALIES.md` #7 | Biometric login could be spoofed |
| 2 | **P0** | **TOTP secret stored in plaintext** at rest | `db_models.UserSecurityDB.totp_secret` | DB leak → attacker can mint valid 2FA codes |
| 3 | **P0** | **Hand-rolled JWT/HMAC** instead of a vetted library | `security.py` (custom encode/decode) | Subtle crypto bugs; prefer audited `PyJWT`/`authlib` |
| 4 | **P0** | **Stripe webhook signature not verified** (billing is mock) | `ROBUSTNESS_READINESS_GAP_ANALYSIS.md` P0 #3 | Forged billing events; payment fraud |
| 5 | **P0** | **Rate limiting off by default + per-instance only** | `rate_limit.py` (`RATE_LIMIT_PER_MINUTE=0`, in-memory) | Brute force / credential stuffing at scale |
| 6 | **P0** | **No enforced at-rest encryption / field-level encryption** | no KMS/pgcrypto integration | DB/backup theft exposes PII |
| 7 | **P1** | **CORS allows all methods/headers** | `main.py` (`allow_methods=["*"]`, `allow_headers=["*"]`) | Loosens browser boundary; tighten in prod |
| 8 | **P1** | **No security response headers** (HSTS, CSP, X-Frame-Options, X-Content-Type-Options) | none set | Clickjacking, MIME sniffing, downgrade |
| 9 | **P1** | **No secrets manager** (env vars only) | deploy config | Secret sprawl; rotation is manual |
| 10 | **P1** | **Limited RBAC** (only `require_admin`; not enforced on all sensitive routes) | `dependencies.py` | Privilege gaps as features grow |
| 11 | **P1** | **No MFA enforcement / account lockout / breached-password check** | auth flow | Weak/reused passwords slip through |
| 12 | **P1** | **No automated dependency/secret/SAST scanning in CI** | no CI yet | Known-vuln libs ship unnoticed |
| 13 | **P1** | **Error monitoring / anomaly alerting not wired** (Sentry planned) | `TODO_NEXT_SESSION.md` | Breaches go undetected |
| 14 | **P2** | **No documented backups + restore drill / DR** | infra TODO | Ransomware/data loss recovery unproven |
| 15 | **P2** | **No third-party penetration test / bug bounty** | — | Unknown unknowns remain |
| 16 | **P2** | **Unusual test dep `httpx2`** (a fork) | `PLATFORM_AUDIT_ANOMALIES.md` #13 | Supply-chain hygiene |

---

## 5. Threat model — how attackers actually get in (OWASP) & our standing

| Attack vector (OWASP Top 10) | Our exposure | Standing |
| --- | --- | --- |
| **A01 Broken Access Control** | RBAC partial | ⚠️ tighten (gaps #10) |
| **A02 Cryptographic Failures** | hand-rolled JWT, plaintext TOTP, no at-rest enc | ⚠️ **P0** (#2,#3,#6) |
| **A03 Injection** | ORM parameterizes; Pydantic validates | ✅ structurally strong |
| **A04 Insecure Design** | data minimization + scoped tokens | ✅ good foundation |
| **A05 Security Misconfiguration** | wildcard CORS, no headers, fail-fast prod ✅ | ⚠️ partial (#7,#8) |
| **A06 Vulnerable Components** | no dependency scanning; `httpx2` | ⚠️ add CI scan (#12,#16) |
| **A07 Auth/Identity Failures** | strong hashing + TOTP; weak biometric verify; no lockout | ⚠️ **P0** (#1,#11) |
| **A08 Software/Data Integrity** | no webhook verify; no SBOM | ⚠️ **P0** (#4) |
| **A09 Logging/Monitoring Failures** | audit model exists; no alerting | ⚠️ wire monitoring (#13) |
| **A10 SSRF** | outbound calls to fixed market APIs only | ✅ low exposure |

**Mobile-app-specific:** strongest path today = **password → TOTP 2FA** (solid).
Biometric path needs full **WebAuthn** verification (#1). Also recommended: certificate
pinning, jailbreak/root detection, secure local storage (Keychain/Keystore), and no
secrets in the bundle when the native/PWA shell hardens.

---

## 6. The hardening roadmap to "bank-grade" (prioritized, concrete)

### P0 — before any real paying user or real PII (the gate)
1. **Real WebAuthn biometric verification** — validate challenge + signature + signature
   counter; reject on counter regression. *(closes #1)*
2. **Encrypt secrets at rest** — encrypt `totp_secret` (and any future PII fields) with a
   KMS-backed key (AWS KMS / libsodium sealed box). Turn on **DB at-rest encryption**
   (RDS encryption). *(closes #2, #6)*
3. **Swap to a vetted JWT library** (`PyJWT`/`authlib`); keep scoped-token semantics.
   *(closes #3)*
4. **Live Stripe + webhook signature verification** (`stripe.Webhook.construct_event`).
   *(closes #4)*
5. **Turn rate limiting on in prod**, move to a **shared store (Redis)** so limits hold
   across instances; add **account lockout / backoff** on failed logins. *(closes #5, part of #11)*
6. **Enforce a strong `AUTH_JWT_SECRET`** everywhere; rotate the dev default. (config
   already fails fast — verify in deploy).

### P1 — before scaling
7. **Tighten CORS** to explicit prod origins, methods, headers. *(closes #7)*
8. **Add security headers** middleware: HSTS, CSP, X-Frame-Options, X-Content-Type-Options,
   Referrer-Policy. Enforce **HTTPS/TLS** end-to-end + WAF (CloudFront/ALB). *(closes #8)*
9. **Secrets manager** (AWS Secrets Manager / SSM) + rotation. *(closes #9)*
10. **Full RBAC** on every sensitive route; default-deny. *(closes #10)*
11. **Auth hygiene:** enforce/encourage MFA, breached-password check (HaveIBeenPwned k-anon),
    password policy, session revocation. *(closes #11)*
12. **CI security gates:** dependency scanning (Dependabot/`pip-audit`/`npm audit`),
    secret scanning, SAST (CodeQL); replace `httpx2` with standard `httpx`. *(closes #12, #16)*
13. **Observability:** Sentry + structured logs + alerting on auth anomalies / 4xx-5xx spikes.
    *(closes #13)*

### P2 — top-tier / trust signals
14. **Backups + tested restore drill; DR runbook.** *(closes #14)*
15. **Third-party penetration test + bug-bounty;** publish a `security.txt` and responsible-disclosure policy. *(closes #15)*
16. **SOC 2 Type II path** + data-retention/deletion (GDPR/CCPA) automation; DPA with subprocessors.

---

## 7. Compliance posture (what users/regulators expect)

| Framework | Status | Note |
| --- | --- | --- |
| **PCI-DSS** | ✅ **Outsourced to Stripe** (Level 1) | We don't touch card data — keep it that way |
| **GDPR / CCPA** | ⚠️ partial | Need privacy policy, consent, data export/delete; minimal PII helps |
| **SOC 2** | ❌ not started | Buyers (esp. B2B/family offices) will ask; start the path post-revenue |
| **Encryption in transit** | ⚠️ enforce TLS/HSTS in prod | Standard via CloudFront/ALB |
| **Encryption at rest** | ⚠️ enable RDS + field-level | P0 #2/#6 |
| **Breach response** | ❌ no IR plan yet | Write an incident-response runbook |

---

## 8. What we can honestly tell users TODAY

✅ **True now:**
- "We never store your card or bank-account numbers — payments are processed by Stripe
  under PCI-DSS Level 1."
- "Passwords are stored only as salted, heavily-iterated PBKDF2 hashes — we can't see them."
- "We support two-factor authentication (TOTP) and minimize the personal data we collect."
- "Database access is parameterized and input is validated, defending against common
  injection attacks."

🚫 **Do NOT say (yet) — it would be false:**
- "Hack-proof" / "non-hackable" / "unbreakable" / "100% secure." (No one can.)
- "Bank-grade security" — *until* the P0 list is closed.
- "Biometric login is cryptographically secured" — *until* WebAuthn verification ships.

**Recommended public phrasing:** *"We take a defense-in-depth approach and minimize the
sensitive data we hold; payment data is handled by Stripe (PCI-DSS Level 1)."* Honest,
strong, and defensible.

---

## 9. Bottom line

We have built a **above-average early-stage foundation** with one standout strength —
**data minimization (no card/bank data, no private keys)** — plus modern hashing, scoped
MFA tokens, parameterized data access, fail-fast prod config, and hardened containers.

But **"iron-clad / non-hackable" is not a state any real platform reaches** — and we
still have **six P0 items** open (WebAuthn verification, encrypt-at-rest for secrets,
vetted JWT lib, live Stripe webhook verification, enforced/shared rate limiting +
lockout, strong secret enforcement). Closing the P0/P1 roadmap in §6 takes us to a
**defensible, bank-grade, defense-in-depth posture** — and lets us make strong, *honest*
security promises to the clients whose trust we prize.

> Security is not a feature you finish — it's a discipline you maintain. The plan above
> is how JHI earns and keeps that trust.
