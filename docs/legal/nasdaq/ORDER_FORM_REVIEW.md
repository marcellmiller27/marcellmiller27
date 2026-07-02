# NASDAQ Service Order (Order Form) — Review

> Review of Service Order **00151172.0** (provided 2026-07-02, Page 1 of 2). The Order Form
> controls the commercial grants that the base T&Cs leave to it
> (`DATA_LICENSE_TERMS_REVIEW.md`). **NOT legal advice** — counsel should review before signing.

## Captured terms
| Field | Value |
| --- | --- |
| Client/**Distributor** | John Henry Investments, LLC **dba JHI Research & Analytics Firm, LLC** |
| Contact / signer | Marcellus Miller (marcellus.miller@johnhenrycapital.com) |
| Address | 7010 Lake Nona Blvd, Unit 548, Orlando, FL 32827 |
| Account Manager | Michael Cornacchia |
| Service Order Date | 06-Jul-26 |
| Product | **Sharadar (SF1)** — Sharadar Core US Fundamentals, Item 1002655 |
| **System Details** | **Internal & External** |
| Delivery | Nasdaq Data Link (Tables) |
| Line items | Sharadar SF1 + **NDL Platform Fee** |
| Term | Initial **12 mo**, Renewal **12 mo**, **Trial 5 days**, **Cancellation notice 90 days** |
| Initial term dates | **11-Jul-26 → 10-Jul-27** |
| **SF1 Annual Fee** | **$13,800.00** |
| NDL Platform Fee | **(amount not shown on page 1)** |

## ✅ Good — the grants we needed are appearing
1. **"System Details: Internal & External"** — this is the override of the T&C §1.1/§1.2
   *internal-only* default. **External use/distribution appears granted** — exactly what a
   client-serving model needs.
2. **"Client/Distributor"** framing throughout — consistent with **distribution rights**.
3. **5-day Trial** is explicitly on the Order Form (your no-cost validation window).

## ⚠️ Confirm / fix BEFORE signing
1. **Explicit SaaS + Derived-Data distribution language.** "Internal & External" is
   promising, but T&C **§1.4(e) specifically bans using the Data in a SaaS/cloud service**
   and **§1.2 bans distributing Derived Data outside the company** absent Order Form
   permission. Get the account manager to **confirm in writing** that "Internal & External"
   covers: (a) **using SF1 within your SaaS**, and (b) **distributing your Derived Data
   (Opportunity Score/rankings) to external end clients.** Don't rely on "External" being
   implied — make it explicit (Order Form or a Distributor schedule).
2. **The "up to 1,000 clients" cap is NOT on page 1.** This is "Page 1 of 2" — check **page
   2 / any distribution schedule** for the end-client cap and any per-client or
   redistribution terms. Get the **1,000-client cap in writing**, plus the **next-tier
   price** beyond 1,000.
3. **Total fee clarity.** SF1 = **$13,800/yr**; the **NDL Platform Fee amount is blank** on
   page 1 (likely ~$4,200 to reach the ~$18k you were quoted). **Confirm the all-in annual
   total.**
4. **5-day trial mechanics.** Confirm the trial = **$0 walk-away if POC fails**, and how it
   interacts with the term (billing starts 11-Jul-26?). After the trial, **90-day
   cancellation notice** applies (auto-renews 12 mo per T&C §6.1) — calendar it.
5. **Entity / dba is malformed — fix it.** "John Henry Investments, LLC **dba JHI Research &
   Analytics Firm, LLC**" is inconsistent: a **dba (fictitious name) should NOT include
   "LLC"** (that implies a separate entity). Confirm the **exact contracting legal entity**
   and correct the dba (e.g., "dba JHI Research & Analytics"). Also reconcile with the
   **Wyoming** registration plan — this shows a **Florida** entity/address; counsel should
   confirm which entity signs and that names are consistent. (See
   `docs/COMPANY_POSTURE_AND_COMPLIANCE.md`.)
6. **Third-party Sharadar terms** (T&C §1.3) still apply — review alongside.

## Verdict
The Order Form is **materially the right shape** — **Internal & External + Distributor +
5-day trial** are the grants we wanted, and **$13,800/yr** is reasonable. Before DocuSign,
**get explicit written confirmation of the SaaS + Derived-Data-distribution rights and the
1,000-client cap (page 2), confirm the all-in total, and fix the dba/entity name** — ideally
with counsel. Then the 5-day trial is your window to validate H5 at zero risk.
