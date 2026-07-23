# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-07-23 · **Type:** Founder working session (platform build) · **Recorder:** Cy Henry (VP, Software Engineering — AI teammate)
**Present:** Founder (Galen Marcellus Miller).

> NOT legal/tax/accounting advice. Prior session: `docs/board/BOARD_MINUTES_2026-07-22.md`.
> Signature of record: `69M2705M`. Ethos: *How we do anything is how we do everything.*

---

## 1. Access & admin (RECORDED)
- **God-Eye (super-admin) account** delivered: a **staff** account (email in `JHI_STAFF_EMAILS`) that sees the full menu incl. `Firm Operations → Accounting`. Verified `is_staff: true` end-to-end; fixed a reliability papercut so staff items appear immediately after login (role re-derives on navigation, no reload). PR **#108**.
- **Tier 1/2/3 test logins** created (Enterprise/Professional/Consumer). **Clarification recorded:** per-plan **feature/seat gating is not enforced yet** — today all paid tiers share the "subscriber" experience; the difference is pricing/positioning. Enforcement is scheduled: mechanism at **Gatekeeper P0**, per-plan entitlements + seat self-management at **P1**, full seat/billing + premium-route enforcement at **Phase 6 (Launch Gates)**. (`src/lib/roles.ts`, `docs/PRICING_BILLING_SCHEMA.md`.)

## 2. Institutional type-scale (RECORDED)
- Storefront headings were oversized ("kindergarten"); tightened `--fs-hero` (60px → 40px max) and lead/hero copy to an institutional scale. In-app compact scale unchanged. PR **#108**.

## 3. Subscription cancellation (RECORDED)
- Two-step cancel at `/account/cancel`: intent → a **required, full-sentence reason** that turns **red → green** (invalid → valid) before "Complete cancellation", then a confirmation with the deactivation date. Backend `POST /billing/cancel` validates the sentence, sets `canceled`, keeps access to period end, and logs the reason to the audit trail. PR **#108**.

## 4. Newsletter Print/PDF crash — FIXED (RECORDED)
- **Root cause:** all three editions called `window.print()`, which crashed the forwarded/desktop viewer.
- **Fix:** server-side PDF — `GET /api/v1/newsletters/{edition}/pdf` (reportlab, reusing the branded memo layer); editions ported to Python so the PDF matches on-screen and is **reusable for the Step-B email attachment**. Front-end "Print / Save as PDF" → "Download PDF" (fetch → save, no print dialog). PR **#109**.

## 5. 🔴 Storefront copy is not institutional-grade (RECORDED — TO ADDRESS)
- **Founder direction:** the storefront/marketing descriptions (home hero, "What you get", "How it works", "Who it's for", pricing feature lines) are **not the institutional-grade professional writing** required for the brand **JHI Research & Analytics Firm, Inc.** They must be re-edited.
- **Also flagged (brand consistency):** the home hero still renders the legacy brand mark **"John Henry Investments"** alongside the "JHI Research & Analytics Firm, Inc." eyebrow — reconcile to the single institutional entity name.
- **Disposition:** *We will address this issue.* Added to the Work Group as a dedicated copy/brand-voice pass (no rewrite executed this session — awaiting the founder's voice/scope direction).

## 6. "Generate report preview" is inactive — DISCUSSED
- **Why it's not active:** on `src/app/reports/page.tsx` the control is a **static placeholder** — `<button type="button">Generate report preview</button>` with **no `onClick`, no route, and no backend call**. It is marketing scaffolding that was never wired to an output, so clicking it does nothing.
- **Proposed activation (for authorization):** wire each report card to the **server-side PDF engine** shipped in #109 (or link to the matching `/newsletters` edition). Mapping is not 1:1 today — we have three editions (Economic Brief · Red Alerts · Opportunity Scan) vs. four marketing report cards (Weekly Economics · Business Acquisition · Crypto Intelligence · Dividend Opportunities), so activation needs the founder's call on the report→output mapping (and whether the extra cards get new editions or are trimmed). Added to the Work Group.

## 7. Hash-marks — REMOVED (storefront)
- Removed the residual gold **"/" list markers ("hash-lines")** on the **storefront** (pricing feature lists, marketing lists). The in-app platform (`.app-main`) and newsletters were already clean from Rule B (#91); this completes the removal on the public marketing pages.

## Decisions locked
God-Eye = staff account + `JHI_STAFF_EMAILS`; per-plan gating deferred to Gatekeeper P0/P1 → Phase 6; cancellation requires a full-sentence reason (audit-logged); newsletter PDF is **server-side** (no `window.print()`); storefront copy needs an institutional-grade rewrite (pending founder voice/scope); hash-marks removed platform-wide incl. storefront.

---

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | Review & merge this session's PRs: **#108** (god-eye/type/cancel — stacked on #104), **#109** (newsletter PDF), and this minutes/polish PR | Founder | 🔴 |
| 2 | **Institutional-grade storefront copy rewrite** — provide voice/scope; reconcile the "John Henry Investments" brand mark to the single entity name | Founder → Cy | 🔴 |
| 3 | **Authorize the "Generate report preview" activation** — confirm the report→output mapping (wire to #109 PDF engine / newsletter editions) | Founder → Cy | 🟡 |
| 4 | Carry-over: upload NASDAQ Order Form (pin **5h**); add SES creds (Step B email); add `TWELVEDATA`/`NASDAQ_DATA_LINK`/`FUNDAMENTALS` keys | Founder | 🟡 |

**Next review:** next working session.
**Recorded by:** Cy Henry · signature of record `69M2705M`.
