# Board Minutes — John Henry Investments / JHI Research & Analytics Firm

**Meeting date:** 2026-07-04 · **Type:** Founder working session (pre-formation) · **Recorder:** Cy (VP, Software Engineering — AI teammate)
**Present:** Marcellus Miller (Founder). **Note:** entity not yet formed; these are decisions of record to be ratified by the board upon incorporation.

> NOT legal/tax/accounting/investment advice. Formal actions (formation, IP assignment,
> contracts) require counsel/CPA. Prior session: `docs/board/BOARD_MINUTES_2026-07-03.md`.

---

## 1. Deal X-Ray — real-CIM validation & engine hardening (RESOLVED / DELIVERED)
- **Tested the CIM analyzer on a real deal:** *Carrollton Design Build* (Benjamin Ross Group listing) — a 40-yr-old Philadelphia-area B2B construction-management firm, asking **$6.2M**, SBA pari-passu structure.
- **Finding:** the first-pass engine was **too optimistic** on this deal (scored 69 / Watch, ethic **100 "looks credible"**, "undervalued"), because it priced off the **peak** 2025 year and ran an uncapped DCF.
- **Four hardening fixes shipped** (PR **#36**, branch `cursor/deal-xray-normalize-hardening-0d47`):
  1. **Blended-earnings basis** — new `earnings_history` input; valuation uses the 2-yr average (never a peak year) and reports the basis + earnings volatility.
  2. **Concentration + volatility → ethic rating** — heavy customer concentration, volatile earnings, and owner-driven turnarounds now dock the honest ethic rating (killed the false 100).
  3. **Curbed DCF** — growth capped/faded, WACC risk-adjusted, EV bounded to the multiple range; fair value weights market multiples 75% / DCF 25%.
  4. **Asset-light capex + construction industries** — capex resolves `explicit → depreciation proxy → industry estimate`; added `construction` and `construction_management` profiles.
- **Corrected read on CDB:** **Score 51 / Watch · Ethic 54 · "fairly priced"** (~3.1× the blended **$1.997M** basis) · DSCR ~2.0–2.3 (still SBA-fit). Killers to diligence: **64% customer concentration** and **owner-succession** (owner personally drove the 2024–25 profit recovery and is retiring).
- **Verification:** backend `pytest` 110 passed (5 new Deal X-Ray tests), `ruff` clean, `npm run lint` + `npm run build` clean, and a **recorded UI walkthrough** of the live analysis (video artifact).
- Refs: `backend/app/deal_xray.py`, `backend/app/deal_xray_models.py`, `src/components/deal-xray.tsx`.

## 2. Product copy — segment-section title rename (OPEN — founder to decide)
- **Context:** the Deal X-Ray results include a six-segment scorecard (Financial quality, Growth trajectory, People & execution, Assets, Market & durability, Risk profile). Its current H2 headline is **"Cradle-to-current breakdown"** (eyebrow: *"Segment scorecard"*).
- **Decision needed:** replace the H2 with a more professional, buyer-facing title. Founder proposed **"Business Health Status"** and will bring additional candidates; Cy to bring the slate below. **We will compare and conclude.**
- **Cy's brainstormed options (for the record):**
  - *Diagnostic / health family:* Business Health Assessment · Business Health Scorecard · Operational Health Diagnostic · Enterprise Health Index
  - *Institutional / diligence family:* Segment Diligence Scorecard · **Business Quality Assessment** · Acquisition Readiness Scorecard · **Six-Pillar Business Assessment** · Business Fundamentals Breakdown
  - *Value / underwriting family:* Value Driver Analysis · Underwriting Scorecard · Deal Quality Breakdown
  - *Punchy / brand-forward family:* The X-Ray Breakdown · Full-Spectrum Business Review · 360° Business Assessment
- **Cy's top 3 (with rationale):**
  1. **Business Quality Assessment** — the phrase acquirers, lenders, and QoE analysts actually use; rigor without jargon.
  2. **Six-Pillar Business Assessment** — concrete and proprietary-feeling; names the six weighted segments.
  3. **Business Health Scorecard** — founder's instinct; pairs naturally with the on-screen score bars.
- **Structural note:** avoid repeating "scorecard" in both the eyebrow and the H2 — e.g., pair eyebrow *"Weighted across six segments"* with the chosen H2.
- **Status:** awaiting founder's additional candidates → compare → lock a name → Cy ships the one-line copy change in `deal-xray.tsx`.

## 3. Financial Diligence Suite — new product line (RESOLVED / BUILD STARTED)
- **Approved** a QoE-support product for the search-fund/SMB niche, built and wired across the platform (web + mobile) this session.
- **CPA function is OUTSOURCED to a vetted partner network — NOT an owned CPA firm** (founder decision): capital-light, no attest E&O/peer-review/ownership burden, instant multi-state coverage. JHI is the software + deal-flow layer; partner CPAs sign and carry liability.
- **Three tiers:** (A) **Financial Integrity Screening** — included, automated, non-attest; (B) **Quality of Earnings (buy-side FDD)** — flagship add-on, partner-CPA-signed advisory; (C) **Formal attest (AUP/review/audit)** — partner firm engages the target; the four opinions live here only.
- **Hard compliance guardrails:** structure economics as SaaS/software + workpaper fee (avoid prohibited attest commissions, AICPA 1.520); **never label the SaaS output an "audit opinion";** raise the data-security bar for ingesting bank statements/financials; counsel to draft partner agreements + engagement letters.
- **Illustrative add-on pricing (to validate):** SBA/search-fund **$3,900–$6,500**; $1–3M EBITDA **$8–16K**; $3–10M **$18–35K**; $10–20M **$40–70K** — all well under the manual market. Marketing anchor: *"Deal QoE Report — from $4,900, CPA-signed, ~2 weeks."*
- **Delivered code:** backend `financial_diligence` engine/models/router (`/api/v1/financial-diligence/{analyze,tiers,pricing,engagement}`), web `/diligence-suite` page + nav, mobile "Run Financial Diligence" screen, and unit tests. Full system audit (pytest/ruff/lint/build) run and green.
- Ref: `docs/FINANCIAL_DILIGENCE_SUITE_CONCEPT.md`.

---

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | Decide final segment-section title; Cy ships copy change in `deal-xray.tsx` | Founder → Cy | 🟡 |
| 2 | Financial Diligence Suite: engage counsel (fee structure, partner agreements, engagement letters); recruit/vet partner-CPA network; validate pricing table | Founder + counsel | 🔴 |
| 3 | Extend Integrations module to feed QoE workpapers (accounting connectors / uploads / bank statements) | Cy | 🟡 |
| 4 | Consider CIM PDF upload → auto-extract (Deal X-Ray v2) and a printable one-page PDF report | Cy | 🟢 |
| 3 | Carry forward 2026-07-03 action items (code consolidation, WY formation + IP, NASDAQ Order Form, CI/CD, Terms/Privacy, RBAC, Stripe, CPA/banking, GTM wedge, backups/DR) | Founder + Cy | 🔴 |

**Next review:** next working session (finalize segment title) or upon WY incorporation.
**Recorded by:** Cy · signature of record `69M2705M`.
