# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-08-10 · **Type:** Founder working session (milestones + build) · **Recorder:** Cy Henry (VP, Software Engineering — Cloud Agent)
**Product:** Aegira · **Publisher:** JHI Research & Analytics Firm, Inc.
**Present:** Founder (Galen Marcellus Miller).

> NOT legal/tax/accounting advice. Prior session: `docs/board/BOARD_MINUTES_2026-08-07.md`.
> Signature of record — `JHI-SIG: 69M2705M`. Ethos: *How we do anything is how we do everything.*

---

## 1. Merged this session (SHIPPED ✅)
- **#155 — Expanded H5 validation = PASS.** The expanded hypothesis-5 (H5) validation ran clean — **5h validated**.
  Fundamentals + valuation path confirmed end-to-end. See `docs/H5_GAP_CLOSURE_RESULTS.md` /
  `docs/H5_SF1_VALIDATION_RESULTS.md`.
- **#156 — RAG scaffolding.** Foundation for **Bedrock Knowledge Base / RAG** over the historical macro corpus —
  the grounding layer for editorial "keen insight from history."
- **#157 — Newsletter Depth Phase 2.** Server-rendered **charts** + **SF1 factor-decomposition** in opportunities +
  **essay voice** (Fed "Economic Research" style, fact-locked).

## 2. Stale drafts closed (HOUSEKEEPING ✅)
- **Closed:** **#83, #82, #79, #35, #30, #25, #21, #20, #19** — superseded/stale drafts cleared to keep the queue
  clean (extends the stale-PR cleanup tracked on 2026-08-07).

## 3. Sandbox rebuilt off `main` with Secrets (LIVE ✅)
- Sandbox **rebuilt off `main`** carrying Secrets → **SF1 live** (primary point-in-time fundamentals) and
  **valuation live** (Cross-Asset DCF running on SF1-derived inputs).
- Confirms the standard operating model: execute builds via fresh Cloud Agents; after merges, **rebuild off `main` +
  hard refresh** to view/verify changes (see 2026-08-07 §6).

## 4. Constructs produced (DOCS ✅)
Four constructs authored this session (this PR):
- **`docs/DATA_FOUNDATION_CONSTRUCT.md`** — *Always-Deliver · Cadence-Aware · As-Of-Disclosed* data doctrine
  (principles P1–P6; source/series registry; acquisition/refresh; caching/freshness/as-of; graceful degradation;
  cadence + next-release calendar; resilience; transparency/audit; governance; application matrix; testing; rollout).
- **`docs/CROSS_ASSET_DISTRIBUTION_CONSTRUCT.md`** — cross-asset opportunity engine (common signal schema; validated
  US now, directional elsewhere) + editorial **distribution** (cadence, channels, free double-opt-in / paid lists,
  CAN-SPAM, archive); global-by-design (P7–P9).
- **`docs/ACQUISITION_INTELLIGENCE_FRAMEWORK.md`** — educational + tool map for search-fund/ETA/SMB acquirers
  (explainer → linked tool → exportable template → data source → status/gap for all ten elements; gap-fill modules;
  lead-gen funnel).
- **`docs/MAIN_STREET_ACQUIRER_CONSTRUCT.md`** — *The Main Street Acquirer* newsletter, **legit public data only**
  (no marketplace scraping); section-by-section source mapping incl. **SBA 7(a)/504** lending intelligence.

## 5. Builds dispatched (QUEUE ▶)
- **Data Foundation — Phase 1** (registry + provenance cache + last-good fallback + freshness states + as-of
  disclosure).
- **Distribution + Main Street Acquirer + SBA engine** (cadence scheduler + free double-opt-in list; SBA 7(a)/504
  ingestion powering the newsletter's lending intelligence).
- **Acquisition Intelligence Framework** (educational IP + gap-fill modules: industry/market analysis, exportable
  deal-linked DD checklist, key-ratios dashboard).

## 6. Cross-asset — held pending Founder decision (BLOCKED 🟣)
- **Commodities / FX / crypto full valuation + global equities** are **held pending the Founder's global-vendor
  decision** (EODHD / FMP / Intrinio — needs a **commercial + redistribution + point-in-time** license). Phase 1
  (distribution + **validated US equities** on SF1) ships without it.

## 7. Founder-gated open items
| # | Item | Owner | Priority |
| --- | --- | --- | --- |
| 1 | **Global-vendor license** decision (EODHD/FMP/Intrinio — commercial + redistribution + PIT) | Founder | 🔴 (unblocks cross-asset global) |
| 2 | **Stripe keys / Purchase Flow Phase B** (live billing — unblocked by Chase account) | Founder → Cloud Agent | 🔴 |
| 3 | **AWS deploy creds + SES domain verification** (deploy target + DKIM/SPF/DMARC → prod send) | Founder → Cloud Agent | 🟡 |
| 4 | **OAuth secret rotation** (re-mint Gmail client secret + refresh token; update Secrets) | Founder | 🔴 |
| 5 | **DBA "Aegira" filing** | Founder | 🟡 |
| 6 | **Nasdaq usage reporting** (monthly, Data-Client Portal + EIPP invoicing) | Founder / ops | 🟡 |

---

## Decisions locked
- **Standing data doctrine (of record):** **always-deliver** (no task blocked for missing data) **+ as-of disclosure**
  (every figure shows actual data date + cadence + source) **+ cadence categorization** (daily/weekly/monthly/
  quarterly/annual/irregular). Never-fabricate: missing/stale inputs are labeled, never invented. Codified in
  `docs/DATA_FOUNDATION_CONSTRUCT.md` (P1–P6) and inherited by all four constructs.
- **Cross-asset rigor labeling:** signals are **validated** (US equities on SF1 now) or **directional** (other classes
  until data/method qualify); global held on the vendor decision.
- **Main Street Acquirer = legit-data-only:** no scraping of marketplaces; SBA/BLS/Census/BEA/FRED public data +
  Flippa API / manual curation with link-back.

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | Decide global-data vendor (commercial + redistribution + PIT) | Founder | 🔴 |
| 2 | Provide live Stripe keys/price IDs → flip Purchase Flow Phase B | Founder → Cloud Agent | 🔴 |
| 3 | Rotate OAuth client secret + re-mint Gmail refresh token; update Secrets | Founder | 🔴 |
| 4 | Provide AWS deploy creds + verify SES domain (DKIM/SPF/DMARC, prod access) | Founder → Cloud Agent | 🟡 |
| 5 | File DBA "Aegira" | Founder | 🟡 |
| 6 | File monthly Nasdaq usage report (Data-Client Portal) + handle EIPP invoicing | Founder / ops | 🟡 |
| 7 | Build Data Foundation Phase 1 (registry + provenance cache + freshness + as-of) | Cloud Agent | 🟡 |
| 8 | Build Distribution + Main Street Acquirer + SBA engine (Phase 1) | Cloud Agent | 🟡 |
| 9 | Build Acquisition Intelligence Framework gap-fill modules | Cloud Agent | 🟢 |

**Next review:** next working session.
**Recorded by:** Cy Henry · signature of record `JHI-SIG: 69M2705M`.
