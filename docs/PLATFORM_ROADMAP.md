# JHI Platform Roadmap (living document)

**Last updated:** 2026-07-16. Maintained by Cy. Reviewed by the Founder/CEO.
Governed by `docs/ENGINEERING_POLICY.md` (foundation first; every PR reviewed &
merged by the Founder/CEO).

---

## ✅ Done this pass — Design-token / typography foundation
- Added the platform design-token system to `src/app/globals.css` `:root`:
  a full type scale (`--fs-*`), line-heights (`--lh-*`), weights (`--fw-*`),
  spacing scale (`--space-*`), and radii (`--radius-*`).
- Migrated **61** ad-hoc CSS `font-size` declarations and **50** inline `fontSize`
  overrides across pages/components onto the scale (was ~35 distinct CSS sizes +
  51 inline literals with no system — the root cause of the inconsistent look).
- Unified 7 divergent hero/lead `clamp()` sizes into `--fs-hero` / `--fs-lead`.
- Verified: `npm run lint` clean, `npm run build` green; before/after screenshots
  + walkthrough video attached to the PR.

---

## Priority backlog (each = its own draft PR)

### P0 — Foundation & correctness
- [ ] **Mobile welcome headline contrast bug (pre-existing).** On `/mobile`, the
  headline "Your platform, now in your pocket." renders dark-on-dark and is nearly
  invisible (confirmed present *before* the typography pass, so not a regression).
  Fix the gradient/text color on the dark phone frame.
- [ ] **Component polish on top of tokens.** Now that tokens exist, tighten tables,
  cards, and chart labels to a consistent institutional density.

### P1 — Close audited functionality gaps
- [ ] **Recover the Macro Dashboard UI.** Backend macro data is live (FRED/BEA/
  Treasury/World Bank/IMF/OECD routers registered) but the front-end page +
  component were never merged — they exist only in orphan commit `383dd96`
  (`src/app/macro/page.tsx`, `src/components/live-macro.tsx`) plus a nav link.
  Rebuild/cherry-pick so the data has a front door.
- [ ] **Ticker → detail page.** Ticker click → charts + company data (SEC EDGAR) +
  authenticated Excel workbook download (reuse the `deal-xray.tsx` download pattern).

### P2 — Premium deliverables
- [ ] **Institutional Research & Analytics Workbook** (multi-sheet, gated T1/T2),
  built in phased passes on `backend/app/edgar_workbook.py`:
  - Pass 1: Exec dashboard + financial statements + nav/index.
  - Pass 2: Ratio sheets + distress/credit models (Altman Z, Piotroski F, Beneish M, Ohlson O).
  - Pass 3: Macro dashboard sheet + charts + sources/disclaimers + provenance watermark.
- [ ] **Newsletter engine.** Data-driven market outlook / concerns / rebalancing
  from polled macro + market data.

### P3 — Mobile strategy (decision required)
- [ ] Decide mobile direction and log the decision in board minutes:
  - **Option A (recommended):** keep `/mobile` as a responsive web companion and
    expand its screens toward parity (dashboard, opportunities, deal x-ray, macro),
    reusing existing API wiring.
  - **Option B:** stand up a real native app (React Native/Expo) as a separate
    track — larger lift (toolchain, builds, store submission).

### Ongoing — Launch gates
- [ ] Seat/billing enforcement end-to-end; RBAC on every premium route.
- [ ] Empty/error states so no page shows dead panels.
- [ ] NASDAQ Order Form countersignature; Twelve Data license decision at gate.
