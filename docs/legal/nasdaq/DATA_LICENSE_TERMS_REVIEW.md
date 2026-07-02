# NASDAQ Data License Terms & Conditions — Review

> Cy's plain-English review of the Nasdaq Data Link Data License T&Cs (full text:
> `NASDAQ_DATA_LICENSE_TERMS.md`) for JHI's use case: a **research SaaS that serves
> SF1-derived scores/rankings to B2C/B2B clients**, bootstrapped/private.
>
> **NOT legal advice.** Have securities/commercial counsel review the **Order Form** and
> the **third-party (Sharadar) terms** (§1.3 link) before signing.

---

## 🔴 TL;DR — the Order Form is the whole ballgame
These T&Cs are **standard and Licensor-favorable**, and **by themselves they do NOT permit
JHI's business model.** The base grant is **internal use only** and it **explicitly
prohibits** the exact things we need. Our entire client-serving model depends on the
**Order Form** granting broader commercial rights.

**What the base T&Cs restrict (critical):**
- **§1.1** — license is for **"internal business purposes only unless otherwise detailed in
  the Order Form."**
- **§1.2 (Derived Data)** — you may create Derived Data (our Opportunity Score/rankings) and
  you **own** it, BUT it **"cannot be distributed outside of Client except as otherwise
  detailed in the Order Form or without Licensor's prior written approval."** → **Serving
  scores to your clients = distributing Derived Data outside your company → needs Order Form
  permission.** Also: Derived Data can't be reverse-engineerable back to the raw Data (a
  0–100 score is fine) and can't be a **substitute for a Licensor service**.
- **§1.4(e)** — you may **not** "use the Data in any ... **software-as-a-service, cloud or
  other technology service.**" → **JHI is a SaaS. This clause prohibits our core use unless
  the Order Form carves it out.**
- **§1.4(b)** — no redistributing Data or incorporating it into a **database/report** beyond
  §1.1/1.2.

### ✅ Therefore the Order Form MUST explicitly grant:
1. **SaaS use** of the Data (override §1.4(e)).
2. **External distribution of Derived Data** (scores/rankings) to your B2C/B2B clients (override §1.2 default).
3. The **$18k/yr, up to 1,000 clients** scope.
4. The **5-day evaluation + $0 cancellation** right (NOT in these T&Cs — must be in the Order Form).

> **If the Order Form says only "internal use," STOP — you cannot serve clients under it.**
> For **R&D/validation (internal backtesting), internal use is enough** — so you can validate
> H5 during the eval even under a limited grant; the commercial rights are needed at **client
> launch**.

---

## 🟡 Other material terms to weigh

| Clause | What it means for JHI |
| --- | --- |
| **§6.1 Term/renewal** | 1-year term, **auto-renews** yearly; must give **90-day notice** to not renew. Calendar this. The 5-day cancel is the Order Form eval — after that you're annual. |
| **§6.3 Effect of termination** | On exit you must **cease use and delete/purge ALL Data** and certify it. **Continuity risk:** if you ever leave Sharadar, fundamentals-based scores can't be refreshed. Pro-rata refund only if *Licensor* terminates without cause. |
| **§9 Disclaimer** | Data is **"AS IS," no warranty** (accuracy/completeness/timeliness). You must **disclaim data quality to your own clients** too. |
| **§10.3 Liability cap** | Licensor's max liability = **~6 months of fees (~$9k)**; no liability for trading/consequential losses. **You bear data-quality risk.** |
| **§11.1 Indemnity (you → Nasdaq)** | **Broad**: you indemnify Nasdaq (incl. attorneys' fees, consequential) for any use contrary to the Agreement. → Staying **within the Order Form's granted rights is critical**; over-distributing = big exposure. |
| **§4.1 Fees** | **Annual price increases** allowed; >greater of 3%/CPI gets 30-day notice. **Not price-locked** — budget ~3%/yr creep. |
| **§8 Audit** | Licensor may **audit your use once/year** (30-day notice, access to systems/personnel). Keep usage records that match the Order Form grants. |
| **§14 Publicity** | Nasdaq may **use your name/logo as a customer** (you can't use theirs without consent, §5.2). Asymmetric — note if you want a low profile. |
| **§18.1 Amendment** | Licensor may **unilaterally change the T&Cs on 90-day notice**; continued use = acceptance. Watch notices. |
| **§1.3 Third-party terms** | Sharadar (the actual SF1 provider) has its **own T&Cs** you must also follow; they can enforce against you. Review that PDF too. |
| **§19 Governing law** | New York. |

---

## Recommendations
1. **Get the Order Form and confirm the four grants above** (SaaS use, external Derived-Data
   distribution, $18k/1,000-client scope, 5-day eval/cancel). This is non-negotiable for the
   client-serving model.
2. **Counsel reviews** the Order Form + **third-party Sharadar terms** (§1.3), focusing on the
   distribution grant, indemnity (§11.1), liability cap (§10.3), and auto-renewal (§6.1).
3. **Validate H5 first** — internal use is sufficient for the eval; only sign the commercial
   distribution rights when you're launching to clients (ties to the bootstrap/timing plan).
4. **Operational safeguards:** calendar the 90-day non-renewal; plan for delete-on-termination
   (continuity); add **data-quality disclaimers** to your client-facing product (§9/§10);
   keep usage within granted rights (audit + indemnity).
5. **Positioning:** keep the product as **research/insight** (Derived Data), never a re-sale or
   **substitute** for SF1 data (§1.2(b)/§1.4(f)); never expose raw fields (§1.2(a)).

> Bottom line: the T&Cs are acceptable/standard — **but they only work for JHI if the Order
> Form explicitly authorizes SaaS use + client distribution of Derived Data.** That single
> document determines whether this contract fits the business.
