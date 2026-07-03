# Board Minutes — John Henry Investments / JHI Research & Analytics Firm

**Meeting date:** 2026-07-03 · **Type:** Founder working session (pre-formation) · **Recorder:** Cy (VP, Software Engineering — AI teammate)
**Present:** Marcellus Miller (Founder). **Note:** entity not yet formed; these are decisions of record to be ratified by the board upon incorporation.

> NOT legal/tax/accounting/investment advice. Formal actions (formation, IP assignment,
> contracts) require counsel/CPA. Companion: `docs/OPERATIONAL_DUE_DILIGENCE_AUDIT.md`.

---

## Formation status update (2026-07-03, later)
- ✅ **JHI Research & Analytics Firm, Inc. has obtained its EIN from the IRS.**
- 🔄 **Wyoming C-corp formation in progress** (Articles of Incorporation + registered agent).
- **EIN letter review (per founder clarification):**
  - **Name:** the EIN filing establishes the entity as a **C-corporation**; both
    **"JHI Research & Analytics Firm"** and **"JHI Research & Analytics Firm, Inc."** are
    legally valid forms. No correction required — just **use the name consistently** on
    signatures/contracts (match the WY Articles). ✅
  - **Responsible Party** name kept consistent across EIN, Articles, NASDAQ, and bank.
  - **~2-week IRS lag:** EIN works now for bank-account opening; e-file/e-pay/TIN-matching
    (e.g., Stripe verification) may take up to two weeks.
  - **Privacy:** the **EIN number and SSN are REDACTED — never committed to the repo**
    (verified 2026-07-03); the confirmation letter is stored securely, outside the codebase.
- **Remaining formation sequence (order matters):** complete WY incorporation → adopt **bylaws** + issue **founder stock** (83(b) election if applicable) → **assign platform IP** (founder → corp, written IP-assignment agreement) → open **business bank account** (EIN enables this) + Stripe under the entity → **then** sign the NASDAQ Order Form as the corp → foreign-qualify in GA/FL as needed.

## 1. Corporate structure & posture (RESOLVED)
- **Two separate entities:** **John Henry Investments, LLC** (family office — invests own funds, private) and **JHI Research & Analytics Firm, Inc.** (a **Wyoming corporation** — the research/analytics SaaS holding the platform, IP, client contracts, and data licenses).
- **Bootstrapped & private — no outside investors / no VC, ever.** Growth is revenue-paced; self-funded.
- **Never manages outside funds / other people's money** (no AUM/custody/RIA-as-manager).
- **Non-dilutive financing (business loan / line of credit) is permitted** once ARR supports it; family office may lend via a documented arm's-length intercompany loan.
- Keep **separate bank accounts + clean books per entity**; no commingling.
- Ref: `docs/COMPANY_POSTURE_AND_COMPLIANCE.md`.

## 2. Market positioning & product (RESOLVED)
- JHI is a **research & analytics firm** selling **research, insight, education, and decision-support** — **not investment advice, not a business broker.**
- **Beachhead niche:** **search-fund / ETA / SMB-acquisition buyers** (targeting retiring baby-boomer "silverback" business owners).
- **Tiers:** Consumer $50 / **Professional $299 (primary)** / Enterprise $1,500+.
- Professional package wedge: **CIM analyzer + deal screener + SBA/DSCR toolkit + branded memo** (to build on the existing engine). Ref: product spec (planned).

## 3. Data licensing — NASDAQ Sharadar SF1 (IN PROGRESS)
- Approved to pursue **SF1 commercial license — $18,000/yr, up to 1,000 subscribers, 5-day $0-cancel trial.**
- **Conditions before signing:** Order Form must (a) name **JHI Research & Analytics Firm, Inc.** (remove "dba"); (b) grant **SaaS use + external distribution of Derived Data**; (c) state the **1,000-subscriber cap + overage pricing in the Order Form** (not email); (d) counsel review (indemnity, liability cap, auto-renewal, Sharadar third-party terms).
- Refs: `docs/legal/nasdaq/*`.

## 4. Research validation — H5 (IN PROGRESS)
- Adopted the **pre-registered validation protocol**: out-of-sample, costed, **|t| ≥ 2.0** bar. Ref: `docs/RND_VALIDATION_PROTOCOL.md`.
- **Baseline (price factors only): H5 FAILED (t = 0.98).** SF1 point-in-time fundamentals engine **built and tested; awaiting full-data access** to run the real validation during the 5-day trial.
- If H5 fails: reposition the score as transparent decision-support (not alpha) — business does not depend on H5.

## 5. IP & provenance (IN PROGRESS)
- Founder provenance signature **`69M2705M`** stamped on source code (entity-agnostic).
- Proprietary **`LICENSE`** adopted; **formal copyright registration** to be filed (`docs/legal/COPYRIGHT_REGISTRATION_CHECKLIST.md`).
- **Copyright/entity attribution rename to "JHI Research & Analytics Firm, Inc."** deferred until the corp is **formed** and **IP assigned** to it.

## 6. Valuation (RESOLVED — internal use only)
- **Private valuation floor ≈ $360K** (asset/cost basis). Hockey-stick ($720M–$1.3B) is a **long-horizon target earned via ARR/retention/moat**, not a current value. For internal/estate/lending only (no equity raise).

## 7. Financial plan — Phase 1 (RESOLVED)
- **Pre-revenue burn ≈ $250/mo** (SF1 commercial deferred until ~20–25 subs). **Break-even ≈ 25–30 subs.** Total cash to sustainability ≈ **$5–15K** — bootstrappable.
- **Phase-1 target reframed to ≈ $70K MRR** (≈ **235 Professional subs**, not 1,000). Ref: `docs/PHASE1_ZERO_TO_1000_PLAYBOOK.md` (planned).

## 8. Platform status (RESOLVED / DELIVERED)
- Durable persistence complete (CRM, Accounting, Reports, **Integrations** all on Postgres).
- Security P0s delivered (TOTP encrypted at rest, PyJWT, Stripe webhook verification, real WebAuthn).
- All six module pages wired to **live backend data** (verified via UI + video review).
- **Operational gap:** 33 open PRs, 1 merged — consolidation required (see audit §1).

---

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | Consolidate code: merge `unified-platform` → main, then feature PRs | Cy | 🔴 |
| 2 | Form **JHI Research & Analytics Firm, Inc.** (WY) + assign IP — **EIN obtained ✅; WY formation in progress 🔄; IP assignment pending** | Founder + counsel | 🔴 |
| 3 | Amend + sign NASDAQ Order Form (correct entity, rights, cap); validate H5 in trial | Founder + Cy | 🔴 |
| 4 | CI/CD + Alembic migrations + observability (Sentry/logs) | Cy | 🔴 |
| 5 | Publish Terms/Privacy/disclaimers; confirm advice/broker positioning | Founder + counsel | 🔴 |
| 6 | Enforce RBAC + prod security env (secrets, TLS/headers, Redis rate-limit) | Cy | 🔴 |
| 7 | Live Stripe checkout + Stripe Tax | Cy | 🔴 |
| 8 | Engage CPA; open per-entity bank accounts; clean intercompany books | Founder + CPA | 🟡 |
| 9 | Stand up GTM stack; ship search-fund wedge (CIM analyzer/screener) | Cy + Founder | 🟡 |
| 10 | Backups/DR, support SLA, incident runbook, SES notifications | Cy | 🟡 |

**Next review:** upon WY incorporation (ratify these resolutions) or next working session.
**Recorded by:** Cy · signature of record `69M2705M`.
