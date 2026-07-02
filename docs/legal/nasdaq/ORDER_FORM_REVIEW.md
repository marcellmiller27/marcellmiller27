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
| **NDL Platform Fee (QNDL)** | **$4,200.00** (Item 1011428) |
| **All-in annual total** | **$18,000.00** ✅ (matches the quote) |
| T&Cs referenced | https://data.nasdaq.com/terms |
| Signature status | **Nasdaq signed** (Garrick Stavrovich, VP Head of Data Product, 7/2/26 11:18 EDT); **Marcellus Miller viewed 7/2/26 4:58 PM — NOT yet signed** |
| Effective Date | later of Service Order Date or last signature |
| Signing window | Nasdaq may revise pricing if not signed within **30 days** of Service Order date |

## Page 2 — additional terms confirmed
- ✅ **Total = $18,000/yr** ($13,800 SF1 + $4,200 NDL Platform Fee). Matches the quote.
- ✅ **Trial cancellation right (explicit):** *"Client shall have the right to terminate the
  NDL Products at any point during the Trial Period upon advance written notice."* → **$0
  walk-away IF you send written notice within the 5-day trial.** If you do **not** cancel in
  the trial, you're committed through the **full 12-month Initial Term** ($18k), then
  auto-renew. **The 5-day window is firm — validate fast and send written notice before it
  ends if POC fails.**
- ⚠️ **Renewal fee** = last month of prior term (subject to the T&C annual price-increase clause).
- ⚠️ **30-day signing window** — price may change if not signed within 30 days.

## ✅ Good — the grants we needed are appearing
1. **"System Details: Internal & External"** — this is the override of the T&C §1.1/§1.2
   *internal-only* default. **External use/distribution appears granted** — exactly what a
   client-serving model needs.
2. **"Client/Distributor"** framing throughout — consistent with **distribution rights**.
3. **5-day Trial** is explicitly on the Order Form (your no-cost validation window).

## ⚠️ Confirm / fix BEFORE signing (still open after page 2)
1. **Explicit SaaS + Derived-Data distribution language.** The only grant language is
   **"System Details: Internal & External"** — there is **no explicit clause** saying you may
   (a) **use SF1 within a SaaS** (T&C **§1.4(e) bans SaaS use**) or (b) **distribute your
   Derived Data/scores to external clients** (T&C **§1.2** default bans it). **Get the account
   manager (Michael Cornacchia) to confirm in writing** — ideally as an added line under
   "Additional Terms" — that "Internal & External" covers your **SaaS delivery of derived
   scores to end clients.** This is the single most important item.
2. **The "up to 1,000 clients" cap is NOT written anywhere in the 2-page Service Order.** It
   was verbal. **Get it in writing** — the permitted **distribution scope / client cap** and
   the **overage/next-tier price** — so there's no surprise true-up later. (Verbal ≠ contract.)
3. ✅ **Total confirmed: $18,000/yr** ($13,800 + $4,200). No longer open.
4. ✅ **Trial cancellation confirmed** ($0 if written notice within the 5-day trial). Note:
   **5 days is firm and requires advance written notice**; miss it → locked for 12 months,
   then 90-day non-renewal notice. **Be ready to validate H5 and send notice fast.**
5. **Entity / dba is malformed — fix it.** "John Henry Investments, LLC **dba JHI Research &
   Analytics Firm, LLC**" is inconsistent: a **dba (fictitious name) should NOT include
   "LLC."** Confirm the **exact contracting legal entity**, correct the dba, and reconcile the
   **Florida** entity/address with the **Wyoming** registration plan (counsel).
6. **Confirm the online T&Cs** at https://data.nasdaq.com/terms **match** the version reviewed
   in `DATA_LICENSE_TERMS_REVIEW.md`. **Third-party Sharadar terms** (T&C §1.3) still apply.
7. **30-day signing window** — price may be revised if not signed within 30 days of the
   Service Order date (06-Jul-26).

## Verdict
Commercially the deal is **solid and correctly shaped**: **$18,000/yr all-in**, **Internal &
External** (distributor) use, and an explicit **5-day $0-cancellation trial**. **Two items
should be nailed in writing before you DocuSign:** (1) explicit **SaaS + external
Derived-Data distribution** rights, and (2) the **client cap/distribution scope** (the
"1,000 clients" was verbal and isn't in the document). Also **fix the dba** and have
**counsel** do a quick pass. Then the 5-day trial is your zero-risk window — the H5 PIT
engine is already built (PR #30), so I can validate immediately on day 1 and you can cancel
in-window at $0 if it fails.
