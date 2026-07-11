# Board Minutes — John Henry Investments / JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-07-08 · **Type:** Founder working session · **Recorder:** Cy (VP, Software Engineering — AI teammate)
**Present:** Founder.

> NOT legal/tax/accounting/investment advice. Prior sessions: `docs/board/BOARD_MINUTES_2026-07-07.md` and earlier.

---

## 1. Delivered this session
- **Phase 2.1 — provenance watermark:** every Excel export now carries a footer on every printed page — `© JHI Research & Analytics Firm, Inc. · JHI-SIG: 69M2705M · Confidential — not for redistribution · Prepared for {subscriber} · Page N`. Branding + IP + free marketing when shared.
- **Branded PDF deal memos:** one-page client-ready leave-behinds for **Deal X-Ray (Business Quality Assessment)** and **Quality of Earnings** (serif headline for gravitas; provenance footer with legal + `69M2705M` + entity on every page). Endpoints `POST /deal-xray/export.pdf`, `/financial-diligence/export.pdf`; "Export to PDF" buttons in both UIs.
- **Deal Pipeline (Save & revisit) — the workflow layer:** analyses are no longer stateless. "Save to Pipeline" on Deal X-Ray and QoE persists the run; a `/pipeline` page tracks each target through stages **Screen → Analysis → QoE → Financing → Offer → Closed / Passed** with stage moves and removal. Durable Postgres/SQLite model `pipeline_deals`; endpoints under `/api/v1/pipeline`.
- **Deps:** `openpyxl` + `reportlab` declared in `backend/pyproject.toml`.
- **Verification:** backend `pytest` 136 passed, `ruff` clean, `npm run lint` + `npm run build` clean.

## 2. Decisions of record
- **White-label / client-ready export** confirmed as a **paid Professional/Enterprise add-on** (subscriber's own branding), NOT a "pay to remove an annoying watermark" gate. Legal disclaimer + a provenance line remain on **every** export regardless of tier.
- Deal Pipeline endpoints are **single-tenant for now**; scope by organization once auth is wired into the module endpoints.

## 3. Forward roadmap (agreed order)
1. **Go-live basics (gate revenue):** real **Stripe checkout + trial/paywall**; publish **Terms / Privacy / disclaimers** + a marketing-claims compliance pass; an onboarding "aha" first-run flow.
2. **Repo consolidation + reliability:** merge the stacked PR chain down to a clean `main`; add **CI (tests on push), error monitoring, backups** (top operational risk — ~40 stacked PRs, nothing merged to main yet).
3. **Differentiators:** public **methodology & validation page** (publish IC/t-stats; out-transparent incumbents); **CIM PDF upload → auto-extract** (Deal X-Ray v2).
4. **White-label export** add-on (from §2).
5. **Plumbing:** SF1 fundamentals once the MSA is countersigned.

---

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | Stripe checkout + trial/paywall + Stripe Tax | Cy | 🔴 |
| 2 | Publish Terms/Privacy/disclaimers + marketing compliance pass | Founder + counsel | 🔴 |
| 3 | Repo consolidation → clean `main`; add CI + monitoring + backups | Cy | 🔴 |
| 4 | Countersign NASDAQ SF1 MSA; file WY C-corp docs on receipt + assign IP | Founder | 🔴 |
| 5 | Methodology & validation page; CIM auto-extract (v2) | Cy | 🟡 |
| 6 | White-label export add-on (tiered) | Cy | 🟡 |

**Next review:** next working session.
**Recorded by:** Cy · signature of record `69M2705M`.
