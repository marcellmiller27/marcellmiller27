# NASDAQ Data License T&Cs — Review & JHI Impact (authoritative text)

> JHI-SIG: 69M2705M · Analysis of the **verbatim** terms in `NASDAQ_DATA_LICENSE_TERMS.md`
> (provided by founder 2026-07-13), focused on what makes or breaks JHI's SaaS research model.
> **Not legal advice** — confirm with counsel before signing. Companion: `ORDER_FORM_REVIEW.md`,
> `SERVICE_ORDER_00151172_REVIEW.md`.

## Bottom line up front (read this first)
The **base T&Cs do NOT permit JHI's product as designed.** Three clauses gate everything, and all three are overcome **only by explicit language in the Order Form** (§22: the Order Form overrides the T&Cs on conflict):

1. **§1.1 — "internal business purposes only unless otherwise detailed in the Order Form."** A client-facing SaaS is *not* internal use. → The **Order Form must grant external/client-facing use.**
2. **§1.4(e) — prohibits using the Data "in any … software-as-a-service, cloud or other technology service."** JHI *is* SaaS/cloud. → The **Order Form must expressly authorize SaaS/cloud use of the Data.**
3. **§1.2 — Derived Data "cannot be distributed outside of Client except as … detailed in the Order Form or without Licensor's prior written approval."** JHI's business = distributing derived analytics (scores/research) to clients. → The **Order Form must expressly grant external distribution of Derived Data.**

**Without these three express Order-Form grants, running JHI on this data would breach the license.** This is exactly the addendum under negotiation — now confirmed from the actual text as non-negotiable to secure in writing.

## What is safe vs. prohibited under the base terms
- ✅ **Allowed:** receive/use/process/**store** the Data for **internal** work; **create Derived Data** you own — *if* (a) it can't be reverse-engineered back to the raw Data, **and** (b) it isn't a substitute for a NASDAQ/Sharadar service (§1.2).
- ❌ **Prohibited (unless Order Form says otherwise):** SaaS/cloud use (§1.4e); redistributing the **raw Data** or incorporating it into a database/report/marketing list (§1.4b); **distributing Derived Data outside JHI** (§1.2); anything that **competes with or substitutes for** a Licensor data service (§1.4f).

**Design implication:** JHI must ship **derived analytics** (the Opportunity/Deal Score, normalized metrics, research narratives) — *never* the raw SF1 fields, and never in a form a client could reconstruct the raw Data from. Keep raw Data server-side and internal; expose only transformed outputs, and only if the Order Form grants external Derived-Data distribution.

## Clause-by-clause — what it means for JHI
| § | Clause | Impact on JHI |
|---|---|---|
| 1.1 | Internal-use-only default | Client SaaS needs explicit Order-Form grant. |
| 1.2 | Derived Data ownership + no external distribution by default | JHI owns its scores/analytics, but **can't serve them to clients** without Order-Form grant/approval; must be non-reversible + non-substitutive. |
| 1.3 | Third-party provider terms (Sharadar) bind too | **Must also comply with Sharadar's terms** (nasdaqtrader third-party PDF); Sharadar can enforce directly as a third-party beneficiary. Read Sharadar's derived-data rules specifically. |
| 1.4(e) | No SaaS/cloud use of Data | The core blocker — Order Form must authorize SaaS/cloud. |
| 1.4(f) | No competing/substitute distribution | Product must be analytics, not a data-resale substitute. |
| 2.3 | Reasonable security safeguards + breach notice | JHI must secure the Data and notify NASDAQ on breach (ties to security posture + entitlements). |
| 3 | Data may change/stop, minimal notice | No guarantee of continuity — don't hard-depend the product on any single field; degrade gracefully. |
| 4.1 | Annual price increases (notice only if > greater of 3% or CPI) | Budget for annual rises; calendar the notice window. |
| 4.2 | Net-30; 1.5%/mo late fee | Pay on time; automate. |
| 5 | Data stays NASDAQ's; JHI can't touch their marks | No NASDAQ logo/marks in marketing without written consent (§5.2). |
| 6.1 | 1-yr term, auto-renew, **90-day** non-renewal notice | **Calendar the non-renewal deadline** or you're locked another year. |
| 6.3 | On termination: **cease use + delete/purge all Data**, certify | **Must architect a data-purge capability** + deletion certification. Retain only if legally compelled/for audit. |
| 8 | Annual audit right (30-day notice, on-site) | Keep usage records; be auditable → reinforces the admin/audit + entitlement controls. |
| 9 | Data is **"AS IS"**, no warranties | JHI must **not** warrant data accuracy to clients; pass through "AS IS"/no-advice disclaimers. |
| 10.3 | Licensor liability capped at **6 months' fees** | If the data is wrong and it hurts JHI/clients, recovery is tiny — JHI carries the downstream risk; disclaim hard to clients. |
| 11.1 | **Client (JHI) indemnifies NASDAQ + third-party providers** for misuse | Misusing/over-distributing the Data exposes JHI to uncapped indemnity to NASDAQ *and* Sharadar. High-stakes reason to stay strictly in-bounds. |
| 14 | NASDAQ may name/logo JHI as a customer | Minor; expect it. |
| 18.1 | Licensor may **unilaterally amend** on 90-day notice; continued use = acceptance | Monitor NASDAQ notices; changing terms is a standing risk. |
| 22 | **Order Form overrides T&Cs on conflict** | The lever: put every JHI-specific grant/carve-out in the **Order Form**. |

## JHI compliance & engineering checklist (build these in)
- [ ] **Order Form must expressly grant:** (1) external/client-facing use (vs. §1.1), (2) SaaS/cloud use of the Data (vs. §1.4e), (3) external distribution of Derived Data (§1.2), and (4) the client-count/scope you plan to serve.
- [ ] **Serve derived analytics only** — never raw SF1; ensure outputs are **non-reverse-engineerable** to the raw Data and **not a substitute** for a NASDAQ/Sharadar service (§1.2/1.4f).
- [ ] **Read & comply with Sharadar's third-party terms** (§1.3) — confirm they permit derived-data distribution; they can enforce directly.
- [ ] **Data-purge capability** (§6.3) — be able to delete/purge licensed Data on termination and **certify** it. Design storage so licensed Data is isolated/purgeable.
- [ ] **Entitlement enforcement** (ties to System Admin) — only authorized users/plans access licensed-data-derived output; supports the §8 audit.
- [ ] **Security safeguards + breach-notify** process (§2.3).
- [ ] **Client-facing disclaimers** — "AS IS", no warranty, research-not-advice — flow the §9 disclaimer downstream (feeds JHI's ToS).
- [ ] **Indemnity awareness** (§11.1) — internal control so no one over-distributes; this is the biggest financial risk.
- [ ] **Calendar:** 90-day **non-renewal** deadline (§6.1) and the annual **price-increase** notice window (§4.1).
- [ ] **Monitor NASDAQ notices** (§18.1 unilateral amendment; §3 data changes).

## Verdict
The economics and workflow can work, but **only** with an Order Form that expressly authorizes **SaaS use + external Derived-Data distribution**. Treat the Order Form as the real contract; the T&Cs alone forbid the business. Secure those grants (and confirm Sharadar's derived-data rules) **before** serving any client-facing output built on this data — consistent with the launch gate in the audit and the pending addendum.
