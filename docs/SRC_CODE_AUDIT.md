# Source Code Audit

## Scope

This audit covers all current front-end source files in:

```text
src/
```

Files reviewed:

| File | Purpose |
| --- | --- |
| `src/app/layout.tsx` | Root layout and metadata |
| `src/components/platform-shell.tsx` | Shared shell and navigation |
| `src/app/page.tsx` | Public landing page |
| `src/app/dashboard/page.tsx` | Dashboard prototype |
| `src/app/opportunities/page.tsx` | Opportunity engine prototype |
| `src/app/due-diligence/page.tsx` | Due diligence center prototype |
| `src/app/portfolio/page.tsx` | Portfolio page prototype |
| `src/app/reports/page.tsx` | Reports page prototype |
| `src/app/assistant/page.tsx` | AI assistant page prototype |
| `src/app/register/page.tsx` | Registration foundation page |
| `src/app/login/page.tsx` | Login foundation page |
| `src/app/pricing/page.tsx` | Pricing/billing foundation page |
| `src/app/account/page.tsx` | Account foundation page |
| `src/app/globals.css` | Global styling |
| `src/lib/platform-data.ts` | Shared typed mock data |

## Automated verification result

The current `src` code passes the full front-end verification suite:

```bash
npm run typecheck
npm run lint
npm run build
npm audit --audit-level=moderate
```

Verification result:

```text
TypeScript: passed
ESLint: passed
Next.js production build: passed
npm audit: found 0 vulnerabilities
Generated static routes: 13
```

Routes generated successfully:

```text
/
/_not-found
/account
/assistant
/dashboard
/due-diligence
/login
/opportunities
/portfolio
/pricing
/register
/reports
```

## Executive summary

No syntax, TypeScript, ESLint, or production-build failures were found in `src`.

However, the code is currently a static prototype. The main issues are product-implementation gaps rather than compiler errors:

- Pages describe backend capabilities but do not call backend APIs.
- Registration and login pages are informational, not functional forms.
- Dashboard and account pages are not protected by front-end session logic.
- Data is hard-coded mock data in `src/lib/platform-data.ts`.
- Report generation button has no action handler.
- No loading, error, empty, unauthorized, or plan-restricted UI states exist.
- No front-end tests exist.
- No legal or investment disclaimer components are rendered in user-facing financial pages.

## Severity definitions

| Severity | Meaning |
| --- | --- |
| Critical | Blocks build, breaks route rendering, causes security exposure, or corrupts data |
| High | Major product/security gap before real users |
| Medium | Important maintainability, UX, or integration gap |
| Low | Cleanup, polish, or future improvement |

## Findings

### Finding 1 - No critical compile/build errors

Severity: informational

Evidence:

- `npm run typecheck` passed.
- `npm run lint` passed.
- `npm run build` passed.
- `npm audit --audit-level=moderate` passed.

Conclusion:

```text
There are no current reproducible TypeScript, lint, build, or dependency-audit failures in src.
```

### Finding 2 - Front-end authentication pages are not functional forms

Severity: high

Files:

- `src/app/register/page.tsx`
- `src/app/login/page.tsx`

Issue:

The registration and login pages describe API endpoints but do not render form inputs, submit handlers, validation, token storage, or backend API calls.

Current behavior:

- `/register` displays required fields as cards.
- `/login` displays endpoint descriptions.
- No user can actually register or log in through the UI.

Recommended fix:

- Add client components for registration and login forms.
- Add input validation.
- Call `/api/v1/auth/register` and `/api/v1/auth/login`.
- Store session token with a secure strategy.
- Add error, loading, and success states.
- Redirect authenticated users to `/dashboard`.

### Finding 3 - Protected pages are not protected in the front end

Severity: high

Files:

- `src/app/dashboard/page.tsx`
- `src/app/account/page.tsx`
- `src/app/portfolio/page.tsx`
- `src/app/reports/page.tsx`
- `src/components/platform-shell.tsx`

Issue:

The application has backend protected endpoint contracts, but front-end routes are static and publicly accessible.

Risk:

Users can view all prototype pages without a session. This is acceptable for a demo, but not for production financial workflows.

Recommended fix:

- Add a session-aware route group.
- Add middleware or server-side auth checks.
- Redirect unauthenticated users to `/login`.
- Add role and plan entitlement checks.
- Render unauthorized and upgrade-required states.

### Finding 4 - Static mock data drives the entire UI

Severity: high

File:

- `src/lib/platform-data.ts`

Issue:

All dashboard metrics, opportunities, diligence records, market signals, portfolio holdings, reports, and AI workflows are hard-coded.

Risk:

The UI can appear operational while not reflecting real backend data.

Recommended fix:

- Create a typed API client layer.
- Add backend calls for dashboard, opportunities, due diligence, portfolio, reports, account, and billing.
- Move mock data to fixtures or demo mode.
- Clearly label demo data when backend is not connected.

### Finding 5 - Report generation button has no behavior

Severity: medium

File:

- `src/app/reports/page.tsx`

Issue:

The `Generate report preview` button has no `onClick`, no form action, no disabled state, and no navigation target.

Recommended fix:

- Connect the button to a report-generation endpoint or preview route.
- Add loading state.
- Add success/failure messages.
- Add plan entitlement checks.

### Finding 6 - Landing page uses standard anchor links instead of Next.js Link

Severity: low

File:

- `src/app/page.tsx`

Issue:

The landing page uses:

```tsx
<a className="button button--primary" href="/dashboard">
```

This works, but internal app navigation should generally use Next.js `Link` for client-side transitions.

Recommended fix:

- Import `Link` from `next/link`.
- Replace internal route anchors with `Link`.

### Finding 7 - No front-end API client exists

Severity: high

Files:

- Missing from `src/`

Issue:

There is no centralized front-end API client for backend routes.

Recommended fix:

Add:

```text
src/lib/api-client.ts
src/lib/session.ts
src/lib/types.ts
```

Minimum API client responsibilities:

- Base URL configuration.
- Bearer token attachment.
- JSON parsing.
- Error normalization.
- Typed response contracts.
- Unauthorized handling.

### Finding 8 - No loading, error, empty, or permission states

Severity: medium

Files:

- All route pages under `src/app/`

Issue:

All pages assume successful static content rendering. Production pages need:

- Loading states
- Empty states
- Error states
- Unauthorized states
- Upgrade-required states
- Integration-disconnected states

Recommended fix:

- Add reusable UI state components.
- Add route-specific states as backend integration begins.

### Finding 9 - No visible financial/legal disclaimer component

Severity: high

Files:

- `src/app/page.tsx`
- `src/app/opportunities/page.tsx`
- `src/app/assistant/page.tsx`
- `src/app/reports/page.tsx`
- `src/app/dashboard/page.tsx`

Issue:

The product displays investment-oriented scores, recommendations, report concepts, and AI research workflows, but does not render a clear user-facing disclaimer.

Recommended fix:

Add a reusable disclaimer component:

```text
src/components/financial-disclaimer.tsx
```

Suggested disclaimer coverage:

- Not financial advice.
- Not legal, tax, or accounting advice.
- AI outputs may be inaccurate.
- User should consult qualified professionals.
- Data may be delayed or estimated.

### Finding 10 - No accessibility focus styles are defined

Severity: medium

File:

- `src/app/globals.css`

Issue:

Interactive elements have visual styling, but no explicit focus-visible styles were found.

Risk:

Keyboard users may have difficulty navigating the application.

Recommended fix:

Add global focus-visible styles:

```css
:focus-visible {
  outline: 3px solid var(--gold);
  outline-offset: 4px;
}
```

### Finding 11 - Global list styling may affect future rich content

Severity: low

File:

- `src/app/globals.css`

Issue:

The global `ul` and `li` rules remove default list styling for every list across the app.

Risk:

Future rich text, legal pages, markdown-rendered content, or article content may inherit non-standard list behavior.

Recommended fix:

- Scope decorative list styles to card/list classes.
- Restore default list styles for prose/legal content.

### Finding 12 - Navigation does not expose login/register links

Severity: medium

File:

- `src/components/platform-shell.tsx`

Issue:

The shared navigation includes dashboard, opportunities, reports, pricing, and account, but does not include `/login` or `/register`.

Recommended fix:

- Add login/register links for unauthenticated state.
- Add account/logout links for authenticated state.
- Make navigation session-aware after auth integration.

### Finding 13 - No front-end tests exist

Severity: medium

Files:

- Missing from `src/`

Issue:

No front-end unit, component, route, or end-to-end tests were found.

Recommended test additions:

- Component tests for shell, pricing cards, report cards, opportunity cards.
- Route smoke tests for all app routes.
- Form tests after login/register forms are added.
- E2E tests for registration, login, checkout, dashboard access, and report generation.

### Finding 14 - Financial figures are hard-coded and unlabeled as assumptions

Severity: medium

Files:

- `src/app/page.tsx`
- `src/app/dashboard/page.tsx`
- `src/lib/platform-data.ts`

Issue:

Financial, portfolio, market, and valuation figures are hard-coded in the UI.

Risk:

Users may interpret demo figures as live or verified.

Recommended fix:

- Add "Demo data" labels.
- Add data-source timestamps.
- Replace mock values with API-driven values when backend integrations are ready.

## Recommended remediation order

### Phase 1 - Production safety

1. Add financial/legal disclaimer component.
2. Add session-aware auth flow.
3. Protect dashboard/account/report routes.
4. Add API client and backend integration.
5. Add demo-data labels.

### Phase 2 - Functional workflows

1. Implement registration form.
2. Implement login form.
3. Implement account session page.
4. Connect pricing page to billing plans.
5. Connect report generation button to report endpoint.

### Phase 3 - UX and reliability

1. Add loading/error/empty states.
2. Add focus-visible styles.
3. Add front-end tests.
4. Scope global list styles.
5. Add backend data timestamps.

## Suggested source additions

```text
src/components/financial-disclaimer.tsx
src/components/ui-state.tsx
src/lib/api-client.ts
src/lib/session.ts
src/lib/demo-data-label.tsx
src/app/(auth)/login/
src/app/(auth)/register/
src/app/(platform)/
src/middleware.ts
```

## Audit conclusion

The `src` codebase is valid and currently passes automated checks, but it should be treated as a static front-end prototype. The highest-priority issues are missing functional auth forms, missing front-end route protection, missing backend API integration, missing disclaimers, and static mock data.

No critical source-code errors remain from the perspective of TypeScript, ESLint, Next.js production build, or npm audit.
