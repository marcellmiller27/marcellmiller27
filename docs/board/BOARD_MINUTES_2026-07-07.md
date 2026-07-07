# Board Minutes — John Henry Investments / JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-07-07 · **Type:** Founder working session · **Recorder:** Cy (VP, Software Engineering — AI teammate)
**Present:** Marcellus Miller (Founder).

> NOT legal/tax/accounting/investment advice. Prior sessions: `docs/board/BOARD_MINUTES_2026-07-04.md`, `2026-07-03.md`.

---

## 1. Formation & data-licensing status (UPDATE)
- **JHI Research & Analytics Firm, Inc.** — **Wyoming C-corp formation submitted;** full C-corp documents expected end of week.
- **NASDAQ SF1 MSA** — NASDAQ is making the requested amendments; **awaiting revised contract for signature.**

## 2. Competitive strategy — reverse-engineering (RESOLVED)
- Adopted a **reverse-engineering approach**: copy competitors' proven **revenue mechanics** (funnel, workflow lock-in, validated outputs), not just aesthetics; attack the **pain points** they leave open.
- Teardown delivered: `docs/COMPETITOR_TEARDOWN_AND_GAP_MAP.md` (PitchBook, Capital IQ, Preqin, Grata/SourceScrub, Seeking Alpha, Morningstar, AlphaSense) covering plumbing (formulas/tools/outputs), moats, validation strategy, and a gap map.
- **JHI's defensible position:** end-to-end integration (source → research → QoE → close) for the underserved search-fund/SMB niche, at a fraction of incumbent price, with **radical validation transparency** (we publish IC/t-stats; most incumbents don't). We do **not** try to out-data PitchBook.
- **Honest gap acknowledged:** *sourcing* is thin today; launch posture is **"diligence-first — bring your own deals."**

## 3. Design & platform direction (DECISIONS LOCKED)
- **Light institutional theme** for the web product (match PitchBook/Preqin/Morningstar/Grata); **navy as the single anchor** color, emerald reserved for the primary CTA, bronze-gold for premium labels only.
- **Mobile app stays a sleek dark app** (scoped tokens) — light web / dark mobile split.
- **Sans typography** in-app (serif reserved only for exported PDF research notes).
- **Progressive density:** airy overviews → dense, filterable, **exportable** analysis screens.
- **Grouped IA:** Overview · Research · Acquisitions · Portfolio · Account. Consolidated the overlapping diligence items → **Deal X-Ray**, **Quality of Earnings**, **Document Review**.
- **Naming precision:** the Deal X-Ray SMB output renamed **"Opportunity Score" → "Deal Score"** to end the collision with the markets Opportunity Score.

## 4. Phase 1 executed this session (DELIVERED)
Branch `cursor/phase-1-institutional-redesign-0d47`:
- Light institutional theme (design tokens, body, header, panels) with the mobile device kept dark.
- Grouped/renamed navigation; professional eyebrows/titles (removed dev-scaffolding language like "Account foundation," "Subscription billing foundation").
- "Deal Score" rename across model, engine, router, frontend, and tests.
- Verification: backend `pytest` 121 passed, `ruff` clean, `npm run lint` + `npm run build` clean.

## 5. Phase 2 requirements (APPROVED — build next)
- **Interactive Excel dashboard export** (Deal X-Ray + QoE first): a **Dashboard tab** with key target areas + **editable input cells** (price, down payment, rate, growth, add-backs, multiple) that **recompute outputs live** via native formulas, conditional formatting for red flags, and base/bull/bear scenarios; **Detail tabs** with the full underlying data. Built with `openpyxl` (formulas + data-validation dropdowns + conditional formatting; no macros).
- **Founder requirement:** every Excel export **must include legal terms/disclaimer, the founder signature `JHI-SIG: 69M2705M`, and "JHI Research & Analytics Firm, Inc."** attribution.
- Table-first analysis screens + Excel/PDF exports as the retention lock-in.

## 6. Roadmap addition
- **Deal Pipeline layer** added to the roadmap — track multiple targets through stages (Screen → Deal X-Ray → QoE → Financing → Offer) to make JHI a true *workflow* platform (daily-use stickiness → retention).

---

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | Phase 2: interactive Excel dashboard (legal terms + `69M2705M` + entity attribution) | Cy | 🔴 |
| 2 | Countersign NASDAQ SF1 MSA once revised contract arrives | Founder | 🔴 |
| 3 | File WY C-corp docs on receipt; then assign platform IP to the corp | Founder + counsel | 🔴 |
| 4 | Live-trial competitor teardown pass + 40–50 company matrix | Cy | 🟡 |
| 5 | Build Deal Pipeline workflow layer | Cy | 🟡 |
| 6 | Finalize Deal X-Ray section title (Business Quality Assessment vs Six-Pillar) | Founder → Cy | 🟢 |

**Next review:** next working session or upon WY incorporation.
**Recorded by:** Cy · signature of record `69M2705M`.
