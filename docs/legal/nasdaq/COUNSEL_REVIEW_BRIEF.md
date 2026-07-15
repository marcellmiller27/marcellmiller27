# NASDAQ SF1 Service Order — Counsel Review Brief

**For:** outside counsel reviewing the NASDAQ Data Link Service Order **00151172**
(Sharadar SF1) before execution.
**From:** JHI Research & Analytics Firm, Inc. (Wyoming C-corp).
**Status (2026-07-15):** founder forwarded to legal; **do not sign until counsel
clears the items below.** Monday 09:00 EDT call scheduled with NASDAQ.

**Background docs in this folder:** `ORDER_FORM_REVIEW.md` (signed-version review +
signature-timing gap), `DATA_LICENSE_TERMS_REVIEW.md` (base T&Cs), `NASDAQ_DATA_LICENSE_TERMS.md`
(verbatim T&Cs), `EMAIL_TO_NASDAQ_ORDER_FORM_ADDITIONAL_TERMS.md` (the agreed path).

**What JHI is buying / needs the contract to permit:** a client-facing **SaaS** that
serves subscribers **Derived Data** (analytics/scores computed from SF1). The base
T&Cs default to internal-use-only, so the grant must be explicit and enforceable.

---

## Priority review items (please confirm each in the signed document)

### 1. 🔴 Execution integrity — both parties must sign the SAME final version
NASDAQ's signatory (Garrick Stavrovich) signed **7/8/26**, *before* the Additional
Terms existed. The founder signed **7/14/26** *with* the Additional Terms. The DocuSign
envelope shows **Status "Delivered," Signatures: 1** (not "Completed"). ⇒ NASDAQ has
**not** executed the version containing the Additional Terms. **Confirm NASDAQ
re-executes/counter-signs the final Service Order that contains the Additional Terms**,
producing a completed envelope with both signatures on the same text.

### 2. 🔴 Enforceability of the Additional Terms vs. the base T&Cs
The Additional Terms grant (i) hosted/cloud **SaaS** use and (ii) creation +
distribution of **Derived Data** to external end users. The base **Terms & Conditions
bar SaaS use (§1.4(e)) and external distribution (§1.2)**. Confirm the Additional Terms
**override** those sections and **control in conflict** — the T&Cs set an order of
preference of **"Order Form, then Agreement" (§22 merger clause)**, so terms placed in
the Order Form's Service Description should prevail. Consider adding explicit
"**Notwithstanding §§1.2 and 1.4(e) … these Additional Terms control per §22**" wording.

### 3. 🟠 Definition of the counted unit ("1,000 external end users")
Confirm whether "user" is counted **per paying subscriber/seat** or **per client
account**. JHI's billing schema is **per seat**, so per-user counting is acceptable —
provided the term is unambiguous and the overage (below) is bounded.

### 4. 🟠 Overage is open-ended — bound it
Current language: *"Overage beyond 1,000 users, Nasdaq reserves the right to charge a
higher rate."* This is an uncapped unilateral right. Recommend fixing a **defined
overage rate / next-tier price**, or at minimum: the **first 1,000 stay at current
pricing through the term**, and any increase requires **advance written notice + good-faith
negotiation.**

### 5. 🟠 Third-party (Sharadar) consent
SF1 is **Sharadar Pty Ltd** data; **§1.3** makes third-party terms controlling. Confirm
the SaaS + Derived-Data grant **includes any required Sharadar consent**, so Sharadar's
own terms cannot undercut what NASDAQ granted.

### 6. 🟡 Merger/entire-agreement (§22) — nothing survives in email
Ensure **every** commercial promise (SaaS, Derived-Data distribution, 1,000-user scope,
overage, pricing) is **in the signed Order Form / Agreement** — side emails will not
supplement it.

### 7. 🟡 Standard risk clauses to assess
- **§11.1 indemnity** (scope/exposure), **liability cap**, data provided **"AS IS."**
- **Unilateral amendment** right over the online T&Cs.
- **Delete-on-termination** obligations (and effect on cached/derived data).
- **Audit rights**, **auto-renewal**, **annual price-escalation**, **30-day signing-window
  reprice.**

### 8. 🟡 Contracting party / signatory
Client/Distributor named as **JHI Research & Analytics Firm, Inc. (a Wyoming
corporation)** — the separate research entity, **not** "John Henry Investments, LLC dba
…". Signed by **Marcellus Miller, CEO** (authorized officer). Confirm consistent.

---

## Bottom line for counsel
The commercial substance is agreed. The review should focus on (1) getting the
Additional Terms **into a fully counter-signed final version**, (2) their
**enforceability** over the base T&Cs, and (3) **bounding the overage** — then the deal
is clean for a client-facing SaaS. **Not legal advice; internal issue list.**
