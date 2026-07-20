# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-07-20 · **Type:** Founder working session (platform build) · **Recorder:** Cy Henry (VP, Software Engineering — AI teammate)
**Present:** Founder (Galen Marcellus Miller).

> NOT legal/tax/accounting advice. Prior session: `docs/board/BOARD_MINUTES_2026-07-13.md`.
> Signature of record: `69M2705M`. Ethos: *How We Do Anything Is, How We Do Everything.*

---

## 1. Platform restructure — phased build executed (RECORDED)
Executed the institutional (Mergr-parallel) restructure as a stacked sequence of draft PRs. Each is foundation-first and awaits Founder review/merge.

| PR | Phase / scope | Base |
| --- | --- | --- |
| **#85** | **Phase 1 — Structural spine:** two-shell split, dark-chrome top bar, left TOC with line icons + tight spacing, Home icon for Dashboard, compact institutional type | `main` |
| **#86** | **Phase 2 — Dashboard workspace:** launchpad (grouped, disclosed definitions) + at-a-glance rail (Coverage · Watch List · Market snapshot) | #85 |
| **#87** | **Phase 3 — Entity graph + records:** Company/Firm/Advisor/Transaction graph, Company record with flat tabs, Firm/Advisor records, entity directory + working global search, cross-entity pivot (no dead ends) | #86 |
| **#88** | **Platform cleanup:** monochrome informational labels, removed gold "/" list markers ("hash-lines"), deleted the "Command center" hero | #87 |

Merge order = `main ← #85 ← #86 ← #87 ← #88`. All lint + build green; each verified with screenshots/video.

## 2. Design & nomenclature decisions (RECORDED)
- **Nomenclature:** function-first, institutional, one-word outliers where warranted (Economics, Screener, Scope [Limited Scope Review], Earnings [QoE], Document Review, Pipeline, Portfolio, Ask JHI, Documents). Mirror Principle + Core Rule (name + disclosed definition) upheld; no invented "kindergarten" terms.
- **Iconography:** adopted `lucide-react` as the platform icon system (TOC + launchpad). Icon color **kept** by Founder direction.
- **Monochrome pass (in progress):** inside the platform, informational word-labels drop the gold and read near-black; the storefront keeps its palette. **Deferred (Founder scope "for now, only the words"):** colored kind-badges, blue links/"View all", status dots — next pass.
- **"Every detail matters":** row density, leading icons, heading scale, and micro-labels are treated as credibility signals across Tiers 1–3.

## 3. Environment / access note (RECORDED)
- **Dev server** runs on **:3009** (Next dev, hot-reload, serves the working tree). Restarting it during rebuilds can drop the forwarded-port tunnel — refresh/reopen the forward if a tab looks dead.
- **Docker** frontend on **:3000** is a **baked production build** (`docker compose up -d --build frontend`); it must be **rebuilt to reflect new code/routes/dependencies**. Rebuilt this session so :3000 now carries today's work.

---

## Monday work group — action items (by order of tasks)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | Merge the stack in order: #85 → #86 → #87 → #88 (each retargets to `main` as the one below merges) | Founder | 🔴 |
| 2 | Finish the monochrome pass: decide rule (full grayscale vs. one restrained functional accent, e.g. muted red for High-risk only), then apply to badges/links/status dots | Founder → Cy | 🟡 |
| 3 | **Phase 3.1 — backend:** Postgres entity/relationship schema + router behind the record UI (underpins Phases 4–5) | Cy | 🔴 |
| 4 | **Phase 4 — Tools & Insights:** consolidate "Diligence a Target" on shared engines; stand up Buyer Match + the LSR ↔ Buyer Match loop | Cy | 🟡 |
| 5 | **Phase 5 — data depth:** EDGAR financials/valuation on public records; client-upload path for private-company depth (graduate "not yet mapped") | Cy | 🟡 |
| 6 | **Phase 6 — launch gates:** mobile parity decision, RBAC/seat enforcement, empty/error states | Cy | 🟢 |

## Meeting to explore (Ideas) — proposed agenda (Monday, session open)
1. Buyer Match design — the differentiator loop and Tier 1–2 monetization.
2. Data-sourcing depth — EDGAR vs. client-upload vs. modeled estimates; how "n/a" graduates to real depth.
3. Lock the design principle — monochrome vs. one functional accent (so it compounds).
4. 30-rep GTM alignment — record/pivot depth as the sales proof.
5. Mobile parity path — companion-plus vs. native.

---

**Next review:** Monday working session (Ideas meeting → execute action #1).
**Recorded by:** Cy Henry · signature of record `69M2705M`.
*Teamwork makes the dream work.*
