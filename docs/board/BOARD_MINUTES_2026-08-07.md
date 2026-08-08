# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-08-07 · **Type:** Founder working session (milestones + build) · **Recorder:** Cy Henry (VP, Software Engineering — Cloud Agent)
**Product:** Aegira · **Publisher:** JHI Research & Analytics Firm, Inc.
**Present:** Founder (Galen Marcellus Miller).

> NOT legal/tax/accounting advice. Prior session: `docs/board/BOARD_MINUTES_2026-07-31.md`.
> Signature of record — `JHI-SIG: 69M2705M`. Ethos: *How we do anything is how we do everything.*

---

## 1. Founder milestone — business banking (MILESTONE ✅)
- **The JHI business bank account is OPENED with Chase Bank.** This is a foundational corporate milestone.
- **Why it matters:** it unblocks **Stripe / live billing** setup (a real business bank account is required to receive payouts) and enables **vendor payments** (Nasdaq/AWS/Google invoices). Directly de-risks **Purchase Flow Phase B** (live Stripe).
- **Action items:**
  - Connect the Chase account to Stripe for payouts; obtain live Stripe keys/price IDs — **Owner: Founder.**
  - On receipt of Stripe keys, flip Purchase Flow to live and run a test charge/refund — **Owner: Cloud Agent.**

## 2. Nasdaq / Sharadar SF1 — fundamentals data (SIGNED + LIVE ✅)
- **Agreement SIGNED 2026-08-03** — Sharadar SF1 (Core US Fundamentals) via **Nasdaq Data Link**. **Agreement 00151172.0**, **Proposal Q-00090839**.
- **`NASDAQ_DATA_LINK_API_KEY` added and verified working** — clean **HTTP 200**, entitled to Sharadar SF1. No **403/QEPx04** (entitlement) and no **400/QELx01** (bad key) errors.
- **Build action (this session's PR):** make **Sharadar SF1 the PRIMARY point-in-time fundamentals source**, with **SEC EDGAR as the automatic fallback**. Wired into the Cross-Asset Valuation DCF and the equity Opportunity Scan. See branch `cursor/sf1-primary-fundamentals-0d47`.
- **Data governance — Founder mandate ("no spillage / derived-only"):**
  - Sharadar SF1 **raw datatable rows/fields stay INTERNAL**. Only **DERIVED outputs** (valuations, opportunity scores, ratios, margins) may be surfaced to users, newsletters, or workbooks.
  - Consumers that surface RAW line-items (the SEC EDGAR financials endpoint/workbook and the Deal X-Ray / LSR public-comp benchmark, which shows raw peer revenue) **deliberately remain on public-domain SEC EDGAR** and do not use SF1.
- **Recurring obligations (as Distributor):**
  - **Monthly usage reporting** via the Nasdaq **Data-Client Portal**.
  - **Invoicing** via **Nasdaq EIPP**.
  - **Governance:** data-set isolation ("no spillage") + **derived-only** outputs.
  - **Owner:** Founder / ops for reporting and invoicing.

## 3. Google / domain / email (MAJOR UNBLOCK ✅)
- **`aegiraenterprise.com` DNS is live** and **Google email validated (2026-08-04)** — a major unblock (email + EDGAR/branding swap + SES path).
- **Email accounts:**
  - **Tier-1 set created** (**support@ live**); list also includes **newsletters@, research@, no-reply@, billing@, legal@, compliance@**.
  - **Tier-2:** hello@/info@, sales@, privacy@, security@.
  - **Guidance:** keep **1–2 paid mailboxes**; make the rest **free Google Groups / aliases** to control cost.
- **AI Support Inbox access — via OAuth refresh token (not a service-account key):** org policy `iam.managed.disableServiceAccountKeyCreation` blocked SA keys, so we created an **OAuth Web client** (redirect = OAuth Playground) and **minted a refresh token** with scopes **`gmail.modify` + `gmail.send`** as **support@aegiraenterprise.com**.
  - **Secrets added:** `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`, `SUPPORT_MAILBOX`.
- **Action items:**
  - **(a) SECURITY — rotate the OAuth client secret and re-mint the refresh token** (both were shown on-screen during setup) — **Owner: Founder** (then update Secrets) → **Cloud Agent** verifies.
  - **(b) Build the "AI Support Inbox" bridge:** Gmail API → **Tess** triage → specialist agent → **human approval** → send, fully **audit-logged** — **Owner: Cloud Agent.**
  - **(c) EDGAR User-Agent swap + newsletter byline swap** to **research@aegiraenterprise.com** (now that DNS/email are validated) — **Owner: Cloud Agent.**

## 4. AWS / SES — newsletter + transactional email (RUNBOOK)
- **Go-live runbook:**
  1. Verify domain **`aegiraenterprise.com`** in **SES — US East (Ohio) region** (**Easy DKIM → 3 CNAMEs**).
  2. In **Route 53**: publish the **DKIM CNAMEs**; **merge SES into the single root SPF** — `v=spf1 include:_spf.google.com include:amazonses.com ~all`; add **DMARC TXT** at `_dmarc` (start **`p=none`**).
  3. **Keep Google MX untouched** — **Google = receiving, SES = sending.**
  4. **Request SES production access** (exit the sandbox).
  5. Flip config: `ENABLE_EMAIL_SEND=1`, `SES_SENDER="Aegira <newsletters@aegiraenterprise.com>"`, IAM creds (`ses:SendEmail` / `ses:SendRawEmail`), and set the `AWS_REGION` env to the US East (Ohio) region.
  6. Run a **verified test send** — confirm **DKIM / SPF / DMARC = pass**.
  - **Owner:** Founder (AWS/DNS + creds) → Cloud Agent (flip + test).
- **Domain → live platform hosting** still needs a **deploy target + AWS deploy creds**, then **Route 53 A/ALIAS** for apex + www and an **ACM cert**. **Owner: Founder** (provision) → **Cloud Agent** (wire).

## 5. Platform / product (STATUS)
- **"Deal X-Ray" → "Limited Scope Review (LSR)" rename complete** (**#150 merged**, **#151 closed**; glossary updated).
- **Previously merged / live:** **Cross-Asset Valuation Phase 1** (equity DCF + IRR + Enter/Accumulate/Sideline + Excel); **Newsletter Depth Phase 1 + Insider Briefs**; **Purchase Flow Phase A + pricing toggle**.
- **Newsletter vision (Founder, 2026-08-06):** match the **Federal Reserve "Economic Research"** style — **analytical essays WITH CHARTS and cited historical context.**
  - Maps to **Newsletter Depth Phase 2**: charts/visual layer + **Bedrock Knowledge Base / RAG** + research-essay format, powered by the **Bedrock editorial (Ellery)** layer.
  - **Clarified:** the **5 support agents are customer support, NOT editorial**; **Ellery + Bedrock is the writer.**
  - **Owner:** Cloud Agent (build) — requires AWS (Bedrock KB/RAG + charts).

## 6. Infrastructure note (PROCESS)
- The Founder's **interactive chat-session VM has had a wedged command shell** for an extended period.
- **Standard operating model:** execute builds via **fresh Cloud Agents**; after merges, **rebuild off `main` + hard refresh** to view changes. (Confirmed again this session — see §7 verification caveat.)

## 7. Open queue / next
| # | Item | Owner | Priority |
| --- | --- | --- | --- |
| 1 | **SF1 → primary fundamentals** (this build) | Cloud Agent | 🔴 (in progress) |
| 2 | **AI Support Inbox** build + **OAuth secret rotation** | Founder (rotate) → Cloud Agent | 🔴 |
| 3 | **SES go-live** (verify domain, DKIM/SPF/DMARC, prod access, test send) | Founder → Cloud Agent | 🟡 |
| 4 | **EDGAR / branding email swap** → research@aegiraenterprise.com | Cloud Agent | 🟡 |
| 5 | **Newsletter Depth Phase 2** (charts + RAG) | Cloud Agent | 🟡 |
| 6 | **Purchase Flow Phase B** (live Stripe — unblocked by Chase account; needs Stripe keys) | Founder → Cloud Agent | 🟡 |
| 7 | **Green CI** (fix ~10 accounting staff-auth tests) + prod hardening | Cloud Agent | 🟡 |
| 8 | **Stale-PR cleanup** — #83, #82, #79, #35, #30, #25, #21, #20, #19 | Founder → Cloud Agent | 🟢 |
| 9 | **Domain hosting / deploy** (deploy target + AWS creds → Route 53 + ACM) | Founder → Cloud Agent | 🟡 |

---

## Decisions locked
Chase business bank account opened (billing/vendor-payments unblocked); **Sharadar SF1 = primary point-in-time fundamentals** (EDGAR fallback) under **derived-only / no-spillage** governance; SF1 distributor obligations (monthly usage reporting via Data-Client Portal, EIPP invoicing); OAuth-refresh-token pattern for Gmail (SA keys blocked by org policy) with **mandatory secret rotation**; SES go-live runbook (Google MX untouched, SES sending only); Newsletter Depth Phase 2 = Fed "Economic Research" essay+charts via Bedrock/Ellery (support agents ≠ editorial).

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | Rotate OAuth client secret + re-mint Gmail refresh token; update Secrets | Founder | 🔴 |
| 2 | Land SF1-primary fundamentals PR; verify AAPL/CAT source + green tests | Cloud Agent | 🔴 |
| 3 | Connect Chase → Stripe; provide live Stripe keys/price IDs | Founder | 🟡 |
| 4 | SES: verify domain in US East (Ohio), publish DKIM/SPF/DMARC, request prod access | Founder | 🟡 |
| 5 | Flip `ENABLE_EMAIL_SEND=1` + SES sender/creds; run verified test send | Cloud Agent | 🟡 |
| 6 | EDGAR User-Agent + newsletter byline → research@aegiraenterprise.com | Cloud Agent | 🟡 |
| 7 | File monthly Nasdaq usage report (Data-Client Portal); handle EIPP invoicing | Founder / ops | 🟡 |
| 8 | Build AI Support Inbox bridge (Gmail → Tess → specialist → approval → send, audited) | Cloud Agent | 🟡 |

**Next review:** next working session.
**Recorded by:** Cy Henry · signature of record `JHI-SIG: 69M2705M`.
