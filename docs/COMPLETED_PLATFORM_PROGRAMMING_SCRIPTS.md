# Completed Platform Programming Scripts

Project: John Henry Investments, LLC Investment Intelligence Platform

Purpose: Save the completed platform programming setup, commands, file map, and source-script locations in one organized reference file.

## 1. Completed platform build status

- Platform type: Subscription investment intelligence SaaS prototype
- Framework: Next.js
- Language: TypeScript
- UI library: React
- Current build: Routed front-end platform application
- Branch used for platform work: `cursor/compose-ai-agent-work-239d`

## 2. Package programming scripts

The runnable programming scripts are saved in `package.json`.

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint .",
    "typecheck": "next typegen && tsc --noEmit"
  }
}
```

### Script purpose

| Script | Command | Purpose |
| --- | --- | --- |
| Development server | `npm run dev` | Runs the local Next.js development server |
| Production build | `npm run build` | Builds the platform for production |
| Production server | `npm run start` | Starts the built production application |
| Lint check | `npm run lint` | Checks code quality with ESLint |
| Type check | `npm run typecheck` | Generates Next.js route types and checks TypeScript |

## 3. Setup script commands

Use these commands to install and run the saved platform application.

```bash
npm install
npm run dev
```

Then open the local development URL shown in the terminal.

## 4. Verification script commands

Use these commands to verify that the completed platform build is healthy.

```bash
npm run typecheck
npm run lint
npm run build
npm audit --audit-level=moderate
```

Expected result:

- TypeScript passes
- ESLint passes
- Next.js production build passes
- npm audit reports no moderate-or-higher vulnerabilities

## 5. Completed route programming files

| Route | Source file | Purpose |
| --- | --- | --- |
| `/` | `src/app/page.tsx` | Public platform overview, subscription plans, modules, scoring model, technology stack, and long-term vision |
| `/dashboard` | `src/app/dashboard/page.tsx` | Investor command center with portfolio metrics, market widgets, market signals, and AI recommendations |
| `/opportunities` | `src/app/opportunities/page.tsx` | Investment and acquisition opportunity engine with scores, recommendations, theses, and metrics |
| `/due-diligence` | `src/app/due-diligence/page.tsx` | AI due diligence center with document intake and sample risk-review queue |
| `/portfolio` | `src/app/portfolio/page.tsx` | Portfolio allocation, cash flow, asset tracking, and wealth projection scenarios |
| `/reports` | `src/app/reports/page.tsx` | John Henry Intelligence Center report generation workflow |
| `/assistant` | `src/app/assistant/page.tsx` | Private AI research assistant workflow examples |

## 6. Shared application programming files

| File | Purpose |
| --- | --- |
| `src/app/layout.tsx` | Root application layout and metadata |
| `src/app/globals.css` | Global platform styling, responsive layouts, app shell styles, cards, dashboards, and route-specific UI classes |
| `src/components/platform-shell.tsx` | Shared platform navigation and page shell component |
| `src/lib/platform-data.ts` | Typed product data for pricing, users, dashboard metrics, market signals, opportunities, diligence, portfolio, reports, assistant workflows, score categories, and technology stack |

## 7. Configuration programming files

| File | Purpose |
| --- | --- |
| `package.json` | Project metadata, dependencies, npm scripts, and PostCSS override |
| `package-lock.json` | Locked dependency versions |
| `next.config.mjs` | Next.js configuration |
| `tsconfig.json` | TypeScript configuration |
| `eslint.config.mjs` | ESLint configuration for Next.js and TypeScript |
| `next-env.d.ts` | Next.js generated type references |
| `.gitignore` | Ignores build output, dependencies, environment files, logs, and TypeScript cache files |

## 8. Documentation files saved with the programme

| File | Purpose |
| --- | --- |
| `README.md` | Project overview, route map, setup commands, and documentation links |
| `docs/PRODUCT_BLUEPRINT.md` | Full SaaS platform product blueprint and route map |
| `docs/PROJECT_MANAGEMENT_CHECKLIST.md` | Completed work checklist, remaining launch tasks, MVP checklist, and Marcellus Miller action items |
| `docs/COMPLETED_PLATFORM_PROGRAMMING_SCRIPTS.md` | This saved programming-script reference file |
| `AI_AGENT_WORK_SUMMARY.md` | Summary of AI-agent-created application work in the repository |

## 9. Dependency setup

The platform currently uses these main dependencies:

```json
{
  "dependencies": {
    "next": "^16.2.9",
    "react": "^19.2.7",
    "react-dom": "^19.2.7"
  },
  "devDependencies": {
    "@types/node": "^26.0.0",
    "@types/react": "^19.2.17",
    "@types/react-dom": "^19.2.3",
    "eslint": "^9.39.4",
    "eslint-config-next": "^16.2.9",
    "typescript": "^6.0.3"
  }
}
```

The project also includes this override to keep the dependency audit clean:

```json
{
  "overrides": {
    "postcss": "^8.5.15"
  }
}
```

## 10. One-command local verification bundle

Run this full command when checking the saved platform:

```bash
npm install && npm run typecheck && npm run lint && npm run build && npm audit --audit-level=moderate
```

## 11. Deployment preparation commands

After choosing the hosting provider, use the production build script as the required deployment check:

```bash
npm install
npm run build
```

Recommended production environment variables to define in the future:

```bash
NEXT_PUBLIC_APP_URL=
DATABASE_URL=
SUPABASE_URL=
SUPABASE_ANON_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
MARKET_DATA_API_KEY=
```

These variables are placeholders for the next backend, billing, database, and AI integration phases. Do not commit real secret values to the repository.

## 12. Next programming milestones

- Add authentication and protected routes
- Add Supabase/PostgreSQL database schema
- Add Stripe subscription billing
- Add AI assistant backend endpoint
- Add market and macro data integrations
- Add document upload and secure storage
- Add report PDF generation
- Add role-based permissions and team accounts
- Add automated tests for critical workflows
