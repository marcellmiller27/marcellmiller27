# NASDAQ / Sharadar SF1 — MSA Call Checklist (09:00 prep)

> Quote on the table: **SF1 commercial usage — "$1,500 per pd."** Bring this list to the
> call. NOT legal advice — have counsel review the MSA before signing.

## 🔴 Confirm FIRST (these change the deal materially)

1. **What is "per pd"? Per YEAR, per MONTH, or per QUARTER?**
   - $1,500 **/year** = trivial for bootstrapping (break-even ~2 subscribers at ~$70 ARPU).
   - $1,500 **/month** = ~$18k/yr (break-even ~21 subscribers just for the data line).
   - Get the **billing period + annual total** in writing.

2. **"1 user seat" ≠ "commercial rights." Don't conflate them.**
   - A single-user seat = **one internal person** accessing the data.
   - Serving SF1-**derived** analytics (your Opportunity Score / rankings) to **paying
     clients** is **commercial display/redistribution** — a *separate* right from seat count.
   - **Ask explicitly:** "Does this license permit **displaying SF1-derived outputs to our
     external B2C/B2B clients** in a paid product?" If the $1,500 is only a 1-seat *internal*
     license, it does **NOT** let you serve clients — you'd be under-licensed.

3. **Derived-data rights — in writing.**
   - Can you show **derived** values (scores/rankings) to clients? ✔ needed.
   - Can you ever show **raw** SF1 fields to clients? (needs redistribution rights.)
   - Any restriction on **"creating a data product"**? (You sell *research/insight*, not raw
     data — make sure that's how they classify you.)

## 🟡 Scope & delivery (confirm included)
4. **Full dataset:** As-Reported dimensions (**ARQ/ART/ARY**) — the point-in-time data (not
   just MRY). ~20-year history. ~16k tickers, **survivorship-free** (active + delisted).
5. **API limits:** calls/day, rate limits, bulk export/download rights.
6. **Storage/caching:** can you **store SF1 in your DB** and **cache computed factors**? For
   how long? (You need this for backtests + serving.)
7. **Update cadence + SLA:** how fresh is the data; support contact.
8. **Attribution:** any required "Powered by Sharadar/Nasdaq" credit.

## 🟡 Commercial terms (negotiate/verify)
9. **Pricing basis:** flat commercial fee vs. **scales with your subscriber count / AUM**.
   Push for **flat** (you don't want per-end-user data fees as you grow).
10. **Term & renewal:** 12-month MSA; **auto-renewal?**; **price-lock on renewal** (cap
    increases); cancellation/termination terms; **what happens to access + stored data on
    termination**.
11. **Seat expansion cost** later (if you ever add a person).
12. **R&D credit:** ask if the eval/first period can be credited (minor).
13. **Payment terms:** annual upfront vs monthly; refund on early cancellation.

## 🟢 Legal / posture (tie-ins)
14. **Counsel reviews the MSA** — focus on **derived-data/redistribution**, **liability/
    indemnification**, and **termination/data-retention** clauses.
15. **Scope reality:** SF1 = US-listed (+ ADRs/Canadian). If marketing says "global/all
    asset classes," know the coverage limit (not a blocker; just don't over-claim).
16. Consistent with `docs/COMPANY_POSTURE_AND_COMPLIANCE.md` (bootstrapped, private) and
    `docs/FUNDAMENTALS_DATA_VENDORS.md` (licensing guardrails).

## The one-line question that de-risks the whole call
> "For a **paid SaaS that shows SF1-derived scores/rankings to external clients**, what is
> the exact license tier, its **derived-data display + redistribution** rights, the **billing
> period/annual total**, and is pricing **flat** or **per-end-user**?"

## After the call
- If it's **~$1,500/yr, flat, commercial with derived-data display rights, As-Reported +
  full history** → strong deal; sign (after counsel) and add the key to Secrets.
- Then ping Cy: I'll run the point-in-time H5 validation (value/quality/growth vs |t| ≥ 2.0).

> Note: the current key on file is the **free sample** (MRY-only, 30 tickers, ~2yr) — the
> commercial subscription is what unlocks the real validation (`docs/SF1_KEY_ENTITLEMENT_FINDING.md`).
