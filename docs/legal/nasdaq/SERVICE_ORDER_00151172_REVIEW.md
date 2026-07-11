# NASDAQ SF1 Service Order 00151172 — Review, Additional Terms & Side Letter

> JHI-SIG: 69M2705M · Commercial review — NOT legal advice. Counsel to bless the
> incorporated T&Cs (`data.nasdaq.com/terms`) before signature.

## Snapshot
- **Service Order:** 00151172.0 · **Licensor:** Nasdaq, Inc. · **Account Manager:** Michael Cornacchia.
- **Client (binding):** **JHI Research & Analytics Firm, Inc.** (WY), 5830 E 2nd St. Ste. 7000 #37182, Casper, WY 82609.
- **Products:** Sharadar Core US Fundamentals (SF1) **$13,800/yr** + NDL Platform Fee (QNDL) **$4,200/yr** = **$18,000/yr**.
- **System Details:** Internal **& External** · Delivery: Nasdaq Data Link (Tables).
- **Term:** Initial 12 mo (11-Jul-26 → 10-Jul-27); Renewal 12 mo; **Trial 5 days**; **Notice 90 days**.
- **Payment terms:** **Net 30** (invoiced; due 30 days — not on signature).
- **Signature status:** Nasdaq countersigned 7/8/2026 (Garrick Stavrovich, VP Head of Data Product); Client to sign this month.

## Confirmed good
- Correct **entity** as the binding Client (the envelope subject line "John Henry Investments, LLC dba…" is **non-binding metadata** — the Service Order body + signature block govern; **no action**).
- **External** rights present (needed for client-facing use).
- **5-day cancellable trial** — lets us validate H5 and walk if it fails.
- **$18k/yr** as expected; **Net-30** eases cash flow.

## Open items to secure before / at signature
1. **External distribution scope ("up to 1,000") is not in the Order** — get it in writing (Additional Terms / side letter).
2. **Derived-Data + SaaS delivery** not expressly granted in the Order — confirm in writing.
3. **Termination**: confirm previously-distributed Derived Data survives (only raw SF1 must be deleted).
4. **Attribution** language (Nasdaq typically requires source attribution).

## Proposed Additional Terms (add to the Service Order, or side letter)
> **1. External Distribution & Permitted Users.** Client is licensed to distribute Derived Data to up to one thousand (1,000) external end-user subscribers via Client's subscription service during the Term at no additional per-end-user fee. Client will notify Licensor before exceeding this threshold, whereupon the parties will negotiate commercially reasonable overage pricing in good faith.
>
> **2. Derived Data & SaaS Delivery.** Client may use the SF1 data to create analytics, scores, models, and reports ("Derived Data") and deliver such Derived Data to its external subscribers through Client's software-as-a-service platform and downloadable reports. Client shall not distribute the raw SF1 datasets, or any substantial or reconstructable extract thereof, to external parties.
>
> **3. Effect of Termination.** Upon termination or expiration, Client shall cease use of and delete the raw SF1 datasets. Derived Data created and distributed to end-users in the ordinary course prior to termination shall survive, provided it does not permit reconstruction of the SF1 datasets.
>
> **4. Attribution.** Client will attribute the source as "Data provided by Nasdaq Data Link / Sharadar" where reasonably practicable in client-facing outputs.

## Side-letter email to Michael (ready to send)
> **Subject:** Service Order 00151172 — two additions before I countersign
>
> Hi Michael,
>
> Thanks — the Service Order looks good and I'm ready to sign this month. Before I countersign, please confirm two points in writing (either added to the Service Order's Additional Terms and re-issued, or via your reply to this email as a side letter):
>
> 1. **External distribution scope:** JHI Research & Analytics Firm, Inc. may distribute Derived Data to up to 1,000 external end-user subscribers via our subscription service during the Term at no additional per-end-user fee (with good-faith overage pricing above that).
> 2. **Derived Data & SaaS:** We may create analytics/scores/reports ("Derived Data") from SF1 and deliver them to our subscribers via our SaaS platform and downloadable reports; we will not redistribute the raw SF1 datasets or any reconstructable extract. Derived Data already delivered to subscribers survives termination; we will delete the raw SF1 data on termination.
>
> Also: (a) please confirm you can accept my signature as an emailed, signed PDF (Adobe) so we end with one fully-executed copy; and (b) given this is a single line item, could we extend the trial to ~10–14 days so we can complete our data validation without rushing?
>
> Once these are confirmed I'll sign and return promptly (well within the 30-day window). Payment terms noted as Net 30.
>
> Best,
> Founder — JHI Research & Analytics Firm, Inc.

## Signing plan
- **Adobe-sign + email is acceptable** IF (a) it is the **final** version incorporating the Additional Terms (ask Nasdaq to re-issue the Service Order or accept the side letter) and (b) Michael confirms he'll accept an emailed signed PDF in lieu of the DocuSign envelope; otherwise complete their DocuSign once re-issued. End state must be **one fully-executed document with both signatures**.

## Key dates
- **Sign-by (avoid reprice):** ~**05-Aug-26** (within 30 days of the 06-Jul-26 Service Order date).
- **Effective Date:** later of Service Order date or last signature.
- **Initial Term:** 11-Jul-26 → 10-Jul-27.
- **Non-renewal notice deadline (90 days):** ~**11-Apr-27** — calendar it to preserve the exit option.

## Trial / H5 plan (5-day, cancellable)
- **Pre-register the pass/fail bar before day 1:** mean IC ≥ 0.03, |t| ≥ 2.0, hit rate ≥ 0.55 (already defined).
- **Provision data on day 1**; our SF1 adapter + PIT fundamentals engine are pre-built to run immediately.
- **Decide by day 4 and send any cancellation notice early that day** (confirm recipient + that notice must be *received* within the trial window). Ask Michael for the ~10–14 day extension to remove timing risk.

## "Leave the Order as-is" debate & decision (2026-07-10)
**Question raised:** could we leave the Service Order un-amended and rely on the *absence* of stated restrictions to use/distribute the data however we choose?

**Decision: NO — pursue the express addendum** (email sent to Michael 2026-07-09). Reasoning, grounded in Nasdaq's own data-licensing language:
- Data/IP licenses grant **only what is expressly stated; all other rights are reserved.** Silence favors the **licensor**, not us.
- Nasdaq's standard terms: Derived Data **"is not distributed outside of Customer except to the extent expressly authorized in the applicable Order Form,"** and a customer **"may not … distribute, license, commercialize … any analytics product, valuation product … except to the extent expressly authorized."** **"All rights not granted hereunder are expressly reserved."** Our Opportunity/Deal Score + Deal X-Ray + QoE **are** derived analytics/valuation products distributed externally → require express authorization.
- The "1,000 clients" email is likely **unenforceable** if the incorporated T&Cs contain an **integration/merger clause** (only the signed document counts) — the strongest reason to get it in writing.
- Risk is **asymmetric**: cost to secure the grant ≈ $0; cost of exceeding scope = audit, breach, termination, delete-data, indemnity — an existential hit to the product's data layer.
- (Analysis cited Nasdaq's closely-analogous standard terms; the exact `data.nasdaq.com/terms` page is JS-gated — **counsel to confirm against the incorporated version.**)

## Movements (execution sequence)
1. ✅ Addendum email sent to Michael (2026-07-09) — 4 points + email-signature acceptance + trial extension.
2. ⏳ Await Michael: re-issued Order **or** written side letter granting the 4 points.
3. 🔎 Review the response (counsel checks incorporated T&Cs).
4. ✍️ Sign the **final amended** version by **~05-Aug-26** (do NOT sign the original as-is).
5. ▶️ Signature → trial clock starts.
6. 🧪 Trial: run SF1/H5 vs. pre-registered bar; **cancel by ~day 4 if fail.**
7. 💵 Proceed → Net-30 payment; committed to Initial Term.
8. 🗓️ Non-renewal notice deadline: **~11-Apr-27**.

**Guardrails:** don't sign the un-amended Order; don't distribute derived data to real subscribers until scope is expressly granted (trial validation is internal R&D); keep `NASDAQ_DATA_LINK_API_KEY` ready for Secrets on day 1.
