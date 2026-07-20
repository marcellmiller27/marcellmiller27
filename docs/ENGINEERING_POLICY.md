# JHI Engineering Policy & Procedures

**Status:** Authoritative. Effective 2026-07-16. No exceptions.
**Owner:** Founder/CEO (Marcellus Miller). **Steward:** Cy Henry (VP, Software Engineering).

> Everything starts with a solid foundation. We do not build features on top of an
> unstable base. Process discipline is how the firm's systems stay robust as we scale.

---

## 1. Pull Request review & merge authority

1. **All PRs are opened as drafts.** The engineering agent (Cy) never merges.
2. **The Founder/CEO reviews and approves every PR** before it is merged.
3. **The Founder/CEO performs the merge.** No auto-merge, no force-merge, no
   ready-for-review flips without explicit instruction.
4. Each PR must carry **evidence** (tests run, before/after artifacts where UI is
   affected) so review is fact-based, not assumed.

## 2. How we add on top of existing work

1. **Branch from the correct base.** New work branches off the current base branch;
   naming: `cursor/<descriptive-name>-0d47`.
2. **One logical change per PR.** Keep scope tight and reviewable. A refactor and a
   feature do not share a PR.
3. **Foundation before features.** Shared systems (design tokens, auth, data layer)
   are stabilized before feature work stacks on them.
4. **No unrelated drift.** Do not fold opportunistic edits into an unrelated PR; log
   them in the roadmap instead.

## 3. Definition of Done (every PR)

- [ ] Backend: `pytest` green (from `backend/`).
- [ ] Frontend: `npm run lint` clean **and** `npm run build` succeeds.
- [ ] UI changes: before/after screenshots and/or a walkthrough video attached.
- [ ] No temporary/debug code committed.
- [ ] Opened as a **draft** PR with a clear description and evidence.

## 4. Design system rule (foundation)

- Typography, spacing, and radii **must** reference the design tokens defined in
  `src/app/globals.css` `:root` (`--fs-*`, `--space-*`, `--radius-*`, `--lh-*`,
  `--fw-*`). See also `docs/BRAND_AND_COLOR_SYSTEM.md` for color tokens.
- Raw font-size/spacing literals are only allowed for intentional, documented
  one-off decorative elements (e.g. oversized display numerals).
- New components inherit the base type scale by default; do not reintroduce ad-hoc
  `fontSize` inline styles with raw values.

## 5. Testing discipline

- Prefer end-to-end evidence over "it compiles." A change to a page is proven by
  loading that page, not by a successful build alone.
- Reuse proven patterns (e.g. authenticated file-download flow in
  `src/components/deal-xray.tsx`) rather than reinventing them per feature.
