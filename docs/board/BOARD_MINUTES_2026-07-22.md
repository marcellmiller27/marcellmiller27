# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-07-22 · **Type:** Founder working session (platform build) · **Recorder:** Cy Henry (VP, Software Engineering — AI teammate)
**Present:** Founder (Galen Marcellus Miller).

> NOT legal/tax/accounting advice. Prior session: `docs/board/BOARD_MINUTES_2026-07-20.md`.
> Signature of record: `69M2705M`. Ethos: *How we do anything is how we do everything.*

---

## 1. Editorial system launched — VP of Editorial (AI) + newsletters (RECORDED)
- Created the **AI VP of Editorial** ("Ellery Vance" — working label; nomenclature is living) who authors the firm's published intelligence. Team-page leadership card + `docs/EDITORIAL_CHARTER.md`.
- **Step A (live):** auto-generated, on-platform, PDF-ready editions from the **public data we poll** (FRED · BLS · market feeds), each bylined to the VP of Editorial:
  - **The Economic Brief** (recurring update), **Red Alerts** (threshold-triggered), **Cross-Asset Opportunity Scan** (idea generation across all asset classes). Desk at `/newsletters`.
- **Step B (foundation):** subscribe opt-in → durable leads store; SES send pipeline documented and **gated on email-provider credentials** (founder action). `docs/NEWSLETTER_DISTRIBUTION_STEP_B.md`.
- PR **#98**.

## 2. Platform UX & nomenclature (RECORDED)
- **Rule B** monochrome platform + one reserved red accent for negative/high-severity only; removed the gold "/" list markers ("hash-lines"). PR **#91**.
- **TOC → click-to-open left menu drawer** (CapIQ/PitchBook pattern; not Mergr's right/top menu); full-width content. PR **#96**.
- **Nomenclature:** retired the display word "Macro" → **Economics/Economic**; Economics heading set to **"Federal Policy & Global Economic Data"** (Title Case). PR **#92**.
- **Standing rule:** kindergarten/elementary naming is upgraded to institutional-grade; **two-layer** (institutional display names vs. stable internal ids); **Title Case** for dictated headings. **Nomenclature is living** and pinned to the top of the work group. PR **#97**.

## 3. Reliability & data (RECORDED)
- **Same-origin API fix:** frontend defaults to `/api/v1` (was absolute `localhost:8000`), fixing the FRED "Loading…" hang on forwarded ports. PR **#93**.
- **API keys confirmed live:** FRED, BEA, BLS return real data; **empty:** TwelveData, Nasdaq Data Link, Fundamentals (add to Secrets to enable those feeds).

## 4. NASDAQ / legal (RECORDED)
- **Agreement resolution — subject CLOSED:** proceeding into the MSA; new Order Form to be uploaded (without the previously stated terms). PR **#94**.
- **Seat basis:** Tiers 1–3 = 1 user-seat; additional at current rates (stated in the JHI subscriber MSA); revisit rate at **1,000 subscriptions/seats**.
- **Binding commitment — no data-set spillage:** licensed data isolated + server-side; derived-only outputs; provenance tagging.
- **Contingency:** if **line-item 5h** is not validated within the **5-day trial**, refute the MSA and execute the back-up (FMP → Tiingo → Intrinio → EODHD, + free EDGAR immediately). 5h's exact pass/fail to be pinned from the uploaded Order Form. PR **#95**.

## 5. Decisions locked
Monochrome **Rule B**; **left-nav** menu drawer; **nomenclature is living** (institutional-grade, two-layer, Title-Case headings); **VP of Editorial** persona (name is a working label); newsletter content is **public-data sourced** (no vendor footprint); newsletter **email send is gated** on SES/provider credentials.

---

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | Review & merge open platform PRs: **#89, #91, #92, #93, #94, #95, #96, #97, #98** | Founder | 🔴 |
| 2 | **Lock nomenclature** — approve the Macro-scrub + elementary lists so Cy runs the sweep | Founder → Cy | 🟡 |
| 3 | **Upload the new NASDAQ Order Form** so Cy pins the line-item **5h** pass/fail test | Founder | 🔴 |
| 4 | **Add email-provider (SES) credentials** to Secrets to enable newsletter sending (Step B) | Founder | 🟡 |
| 5 | Add `TWELVEDATA` / `NASDAQ_DATA_LINK` / `FUNDAMENTALS` keys to Secrets when ready | Founder | 🟢 |
| 6 | Then Cy proceeds: **Phase 3.1** (entity schema) → Phase 4 → Phase 5 → Phase 6 | Cy | 🟡 |

**Next review:** next working session.
**Recorded by:** Cy Henry · signature of record `69M2705M`.
