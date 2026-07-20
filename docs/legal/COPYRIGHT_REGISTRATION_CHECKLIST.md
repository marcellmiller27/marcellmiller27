# Copyright Registration Filing Checklist — JHI Platform Software

> **Purpose:** a practical, step-by-step checklist for the founder to register copyright
> in the John Henry Investments (JHI) platform software (source code + documentation),
> establishing the strongest provenance and legal standing.
>
> **NOT LEGAL ADVICE.** This is a planning aid. Copyright rules — especially around
> AI-assisted code, deposits, and trade secrets — are nuanced. **Engage IP/copyright
> counsel** (see `docs/JOB_DESCRIPTIONS_AND_STAFFING_REQUIREMENTS.md` → IP/Trademark
> Counsel) before filing. U.S.-centric (U.S. Copyright Office / eCO); other countries
> differ.

---

## 0. Context (what we already have)

- ✅ Proprietary `LICENSE` (© John Henry Investments, LLC; all rights reserved).
- ✅ Founder provenance signature `69M2705M` on every source/config file (`docs/CODE_SIGNATURE.md`).
- ✅ Authorship/disclosure record: `docs/disclosure/JHI_Coding_Disclosure.xlsx` (work by subsystem + skillset).
- ✅ Component inventory: `docs/PLATFORM_TABLE_OF_CONTENTS.md`.
- ✅ Git history (timestamps + authorship trail).

> Copyright exists automatically on creation (Berne Convention). **Registration** is what
> adds enforceable benefits — in the U.S., it's required before filing an infringement
> suit for a U.S. work, and timely registration can unlock statutory damages + attorneys' fees.

---

## 1. Decide WHAT you're registering

- [ ] **Scope:** the whole platform as one "computer program" work (recommended for a first filing) vs. per-module. Confirm with counsel.
- [ ] **Include documentation?** Decide whether to also register key written docs (e.g., research thesis, blueprints) — these are separate "literary work" claims.
- [ ] **Title & version:** e.g., "John Henry Investments Platform — v0.1.0" (tie to a tagged git commit).
- [ ] **Completion date** of this version (and of any prior published versions).
- [ ] **Published vs. unpublished:** A SaaS deployment may count as "publication" — this affects deposit rules and timing. **Confirm status with counsel** (it materially changes the filing).

## 2. Establish WHO owns it (authorship & chain of title)

- [ ] **Claimant:** John Henry Investments, LLC (the entity that owns the IP).
- [ ] **Author(s):** identify human author(s). If contractors/employees contributed, ensure **work-made-for-hire** clauses or **signed IP assignment agreements** transfer rights to the LLC.
- [ ] **Transfer statement:** if claimant ≠ author, state how ownership was obtained (e.g., written assignment / WMFH).
- [ ] **Gather signed agreements:** founder IP assignment to the LLC, any contractor assignments. Keep on file (align with `docs/IP_INTANGIBLES_AMORTIZATION.md`).

## 3. ⚠️ Handle AI-assisted authorship (critical, do not skip)

The platform was built **founder-led with AI assistance**. The U.S. Copyright Office
requires **human authorship**; purely AI-generated material is generally **not**
copyrightable and **must be disclaimed**.

- [ ] **Identify human-authored contributions** (selection, arrangement, architecture, edits, integration, and human-written code) — this is what you claim.
- [ ] **Disclaim AI-generated portions** in the application if material, per current Copyright Office guidance on works containing AI-generated content.
- [ ] **Document the human creative process** (your direction, review, modifications) — keep evidence (commit history, prompts/edits) in case of inquiry.
- [ ] **Confirm the disclosure approach with counsel** — this is the highest-risk area for software built with AI tools.

## 4. Prepare the DEPOSIT (source code)

Computer programs register as **literary works**; the deposit is "identifying portions,"
not the whole codebase.

- [ ] **Default deposit:** first 25 and last 25 pages of source code (single file), with the title/version on the first page.
- [ ] **Protect trade secrets:** if the code contains trade secrets (e.g., the Opportunity Score logic, security internals), use a **redacted deposit** option (block out trade-secret portions) or the "rule of doubt" deposit. **Decide with counsel what to redact** (e.g., `opportunity_score.py`, `security.py`, `webauthn.py`, `billing_webhook.py`).
- [ ] **Assemble the deposit file** from a tagged commit so it matches the registered version.
- [ ] Keep the `69M2705M` signature headers visible in the deposit (supports provenance).

## 5. Choose the application & FILE (U.S. eCO)

- [ ] Create/log in to the **eCO** (electronic Copyright Office) account.
- [ ] Select the correct application (computer program → typically the **Standard Application**; one work, one author/claimant). Group options exist for multiple versions/updates — ask counsel.
- [ ] Complete: title, author, claimant, transfer statement, year of completion, publication status, AI-authorship disclaimer.
- [ ] Pay the **filing fee** (per-application; small).
- [ ] Upload the prepared deposit.
- [ ] Submit and **save the case/confirmation number**.

## 6. Versions & ongoing maintenance

- [ ] Plan for **new registrations** (or derivative-work claims) when you ship material new versions — copyright registration covers a snapshot.
- [ ] Keep the `©` notice current in `LICENSE` and headers (already in place).
- [ ] Maintain the IP register/amortization records (`docs/IP_INTANGIBLES_AMORTIZATION.md`).
- [ ] Consider **trademark** registration for the JHI name/logo separately (different process).
- [ ] International: copyright is automatic in Berne countries; register locally where you need enforcement.

## 7. Records to retain (provenance file)

- [ ] Registration certificate + case number.
- [ ] Tagged commit hash used for the deposit.
- [ ] Signed IP assignments / WMFH agreements.
- [ ] `docs/CODE_SIGNATURE.md`, `docs/disclosure/JHI_Coding_Disclosure.xlsx`, and this checklist.
- [ ] Evidence of human authorship (commit history, change logs).

---

## Quick "gather from this repo" list

| Need | Source in repo |
| --- | --- |
| Component/authorship inventory | `docs/PLATFORM_TABLE_OF_CONTENTS.md`, `docs/disclosure/JHI_Coding_Disclosure.xlsx` |
| Provenance signature | `docs/CODE_SIGNATURE.md` (token `69M2705M`) |
| Copyright/ownership notice | `LICENSE` |
| IP accounting / asset basis | `docs/IP_INTANGIBLES_AMORTIZATION.md` |
| Version/commit | `git tag` + commit hash for the registered build |

> Founder signature: `69M2705M` · JHI Research & Analytics Firm, Inc. (proprietary). Confirm all
> steps — especially **publication status**, **AI-authorship disclaimer**, and
> **trade-secret deposit** — with qualified IP counsel before filing.
