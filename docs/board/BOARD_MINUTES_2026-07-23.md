# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-07-23 · **Type:** Founder working session (platform build) · **Recorder:** Cy Henry (VP, Software Engineering — AI teammate)
**Present:** Founder (Galen Marcellus Miller).

> NOT legal/tax/accounting advice. Prior session: `docs/board/BOARD_MINUTES_2026-07-22.md`.
> Signature of record: `69M2705M`. Ethos: *How we do anything is how we do everything.*

---

## 1. Access & admin (RECORDED)
- **God-Eye (super-admin) account** delivered: a **staff** account (email in `JHI_STAFF_EMAILS`) that sees the full menu incl. `Firm Operations → Accounting`. Verified `is_staff: true` end-to-end; fixed a reliability papercut so staff items appear immediately after login (role re-derives on navigation, no reload). PR **#108**.
- **Tier 1/2/3 test logins** created (Enterprise/Professional/Consumer). **Clarification recorded:** per-plan **feature/seat gating is not enforced yet** — today all paid tiers share the "subscriber" experience; the difference is pricing/positioning. Enforcement is scheduled: mechanism at **Gatekeeper P0**, per-plan entitlements + seat self-management at **P1**, full seat/billing + premium-route enforcement at **Phase 6 (Launch Gates)**. (`src/lib/roles.ts`, `docs/PRICING_BILLING_SCHEMA.md`.)

## 2. Institutional type-scale (RECORDED)
- Storefront headings were oversized ("kindergarten"); tightened `--fs-hero` (60px → 40px max) and lead/hero copy to an institutional scale. In-app compact scale unchanged. PR **#108**.

## 3. Subscription cancellation (RECORDED)
- Two-step cancel at `/account/cancel`: intent → a **required, full-sentence reason** that turns **red → green** (invalid → valid) before "Complete cancellation", then a confirmation with the deactivation date. Backend `POST /billing/cancel` validates the sentence, sets `canceled`, keeps access to period end, and logs the reason to the audit trail. PR **#108**.

## 4. Newsletter Print/PDF crash — FIXED (RECORDED)
- **Root cause:** all three editions called `window.print()`, which crashed the forwarded/desktop viewer.
- **Fix:** server-side PDF — `GET /api/v1/newsletters/{edition}/pdf` (reportlab, reusing the branded memo layer); editions ported to Python so the PDF matches on-screen and is **reusable for the Step-B email attachment**. Front-end "Print / Save as PDF" → "Download PDF" (fetch → save, no print dialog). PR **#109**.

## 5. 🔴 Storefront copy is not institutional-grade (RECORDED — TO ADDRESS)
- **Founder direction:** the storefront/marketing descriptions (home hero, "What you get", "How it works", "Who it's for", pricing feature lines) are **not the institutional-grade professional writing** required for the brand **JHI Research & Analytics Firm, Inc.** They must be re-edited.
- **Also flagged (brand consistency):** the home hero still renders the legacy brand mark **"John Henry Investments"** alongside the "JHI Research & Analytics Firm, Inc." eyebrow — reconcile to the single institutional entity name.
- **Disposition:** *We will address this issue.* Added to the Work Group as a dedicated copy/brand-voice pass (no rewrite executed this session — awaiting the founder's voice/scope direction).

## 6. "Generate report preview" is inactive — DISCUSSED
- **Why it's not active:** on `src/app/reports/page.tsx` the control is a **static placeholder** — `<button type="button">Generate report preview</button>` with **no `onClick`, no route, and no backend call**. It is marketing scaffolding that was never wired to an output, so clicking it does nothing.
- **Proposed activation (for authorization):** wire each report card to the **server-side PDF engine** shipped in #109 (or link to the matching `/newsletters` edition). Mapping is not 1:1 today — we have three editions (Economic Brief · Red Alerts · Opportunity Scan) vs. four marketing report cards (Weekly Economics · Business Acquisition · Crypto Intelligence · Dividend Opportunities), so activation needs the founder's call on the report→output mapping (and whether the extra cards get new editions or are trimmed). Added to the Work Group.

## 7. Hash-marks — REMOVED (storefront)
- Removed the residual gold **"/" list markers ("hash-lines")** on the **storefront** (pricing feature lists, marketing lists). The in-app platform (`.app-main`) and newsletters were already clean from Rule B (#91); this completes the removal on the public marketing pages.

## 8. AWS Bedrock — AI Editorial Newsletter program (RECORDED, in detail)

### 8.1 Editorial engine status (E-roadmap)
- **E1 — SHIPPED (#113):** house style guide (`docs/EDITORIAL_STYLE_GUIDE.md`) + a **methodology & sources disclosure** now renders verbatim on every edition (screen + PDF). The engine is **deterministic, rule-based, fact-locked, hallucination-free** — the standing guardrail for E2.
- **E2 — grounded-LLM drafting layer:** an LLM elevates the *voice* while the deterministic engine remains the **sole source of every number**. Roadmap continues E3 (editor-in-the-loop) → E4 (forever-learning) → E5 (governance). Ref: `docs/EDITORIAL_PROGRAM_ASSESSMENT.md`.

### 8.2 Platform decision — **AWS Bedrock** (Founder created an AWS account)
- The editorial LLM will run on **AWS Bedrock**, so all candidate models sit **under one account** with **data-in-account** isolation (aligns with the NASDAQ **no-spillage** posture; no training on our data).

### 8.3 Model evaluation — **OPEN (not closed)**; multi-model tiered by cadence
- **Candidates on Bedrock:** **Anthropic Claude Sonnet 5** (lead writer — nuanced institutional prose), **Amazon Nova Pro** (cost/perf workhorse), **Meta Llama 3.1 8B Instruct** (cheap utility/first-draft; note 8B is small — reserve for short-form; 70B is the safer floor for reader-facing prose).
- **Which Claude:** the **Sonnet** tier (Sonnet 5) balances quality/cost; Opus for the flagship annual; Haiku for cheap/high-volume.
- **Cadence → tier routing (the editorial calendar):**
  | Cadence | Role → model |
  |---|---|
  | **Daily** (high volume) | Nova Pro workhorse; Llama 8B for short blurbs/alerts |
  | **Monthly** | Nova Pro; escalate the marquee piece to Sonnet 5 |
  | **Quarterly** | Claude Sonnet 5 (lead) |
  | **Year-end / yearly** | Claude Sonnet 5 (consider Opus) |
- **Design:** roles, not a 3× run — **lead writer / workhorse / cheap utility**, plus an optional **second-model fact-checker** verifying every figure against the engine.
- **Decision method:** run a **Bedrock bake-off** across the candidates on the same editions (score voice, factual fidelity = zero invented figures, latency, cost/edition), then lock the model. **Fact-lock guardrail applies to all.**

### 8.4 AWS/Anthropic first-time use-case submission — **approved to proceed**
- Bedrock requires a **one-time responsible-use intake** for Anthropic models (shared with Anthropic). **Opinion of record: green-light.** It is a **use-case description, not data sharing** — it does **not** expose our datasets/prompts/subscriber data and does **not** affect the no-spillage commitment (Bedrock keeps inference in-account; no training on our data).
- **Action:** submit a **minimal, truthful blurb** (financial-research SaaS; model rephrases engine-computed public-data figures; not investment advice; low scheduled volume; no PII/no licensed-data redistribution). Do not paste secrets or licensed-data specifics.

### 8.5 Newsletter reliability (fixed)
- **Dev (`:3009`)** renders with live data and downloads PDFs correctly. **Docker prod (`:3000`)** was returning **404** on `/newsletters/*` — a **stale 3-day-old container** predating the routes; **rebuilt → now 200** (index + editions + PDF). Server-side PDF is role-aware (#109 merged).
- **Company domain — verified 2026-07-23:** **`johnhenrycapital.com`** is **registered** (Google-managed nameservers) with **Google Workspace email live** (MX + SPF `v=spf1 include:_spf.google.com ~all`). **However:** **no website A record** (apex serves nothing), it is **not wired into the app** (no `metadataBase`/site URL/Stripe/OG), and it is **not SES-verified**. Remaining for launch: deploy target + DNS, app wiring, and **SES domain verification** (DKIM/TXT; extend SPF to include `amazonses.com`) — or send Step-B via Google Workspace.

## 9. Monthly AI Editorial Budget (RECORDED) + Contribution-Margin treatment
- **Budget range to choose (a hard cap):** **$100 (Starter) / $250 (Recommended) / $500 (Growth)** — range **$100–$500/mo**. Enforced as a **hard cap with deterministic fallback** (when the cap is hit, publish the deterministic edition — spend cannot run away). Estimated **steady-state ≈ $25–$75/mo**; the cap is headroom for iteration/bake-off/growth. *(Founder to select the cap.)*
- **Contribution-Margin treatment (correct accounting):** the editorial LLM spend is a **shared production cost** (one edition serves all subscribers) → it belongs in **Fixed Costs (F)**, **not** per-seat variable cost. Cost-per-subscriber **falls with scale**; **CM impact is negligible** (at a $250 cap: $2.50/sub at 100 subs → $0.25 at 1,000 → $0.005 at 50,000; break-even rises by only ~2–3 Consumer subs). Detail + tables in `docs/CONTRIBUTION_MARGIN_CVP.md` §7 (PR #118). The chosen cap folds into **F** in the consolidated projections.

## Decisions locked
God-Eye = staff account + `JHI_STAFF_EMAILS`; per-plan gating deferred to Gatekeeper P0/P1 → Phase 6; cancellation requires a full-sentence reason (audit-logged); newsletter PDF is **server-side** (no `window.print()`); storefront copy needs an institutional-grade rewrite (pending founder voice/scope); hash-marks removed platform-wide incl. storefront.
**Added this session:** editorial LLM runs on **AWS Bedrock** (data-in-account); **model choice OPEN** — decided by a Bedrock bake-off across Claude Sonnet 5 / Nova Pro / Llama 3.1 (tiered by cadence); **fact-lock is non-negotiable** (models only rephrase engine figures); the AWS/Anthropic use-case intake is **approved** (not data sharing); the AI editorial budget is a **fixed production cost** (negligible CM impact).

---

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | Review & merge this session's PRs: **#108** (god-eye/type/cancel — stacked on #104), **#109** (newsletter PDF), and this minutes/polish PR | Founder | 🔴 |
| 2 | **Institutional-grade storefront copy rewrite** — provide voice/scope; reconcile the "John Henry Investments" brand mark to the single entity name | Founder → Cy | 🔴 |
| 3 | **Authorize the "Generate report preview" activation** — confirm the report→output mapping (wire to #109 PDF engine / newsletter editions) | Founder → Cy | 🟡 |
| 4 | Carry-over: upload NASDAQ Order Form (pin **5h**); add SES creds (Step B email); add `TWELVEDATA`/`NASDAQ_DATA_LINK`/`FUNDAMENTALS` keys | Founder | 🟡 |
| 5 | **Select the monthly AI Editorial budget cap** — $100 / $250 / $500 (recommended $250) → folds into F | Founder | 🟡 |
| 6 | **Close the E2 model discussion / authorize the Bedrock bake-off**; then enable Bedrock model access + add `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`/`AWS_REGION` | Founder | 🟡 |
| 7 | **Submit the AWS/Anthropic one-time use-case blurb** (minimal, truthful) to unlock Claude on Bedrock | Founder | 🟢 |
| 8 | **Company domain `johnhenrycapital.com` — verified registered (Google Workspace email live).** Remaining: pick a deploy target + point DNS, wire the app (metadataBase/`NEXT_PUBLIC_SITE_URL`/Stripe URLs/OG), and **SES domain verification** for newsletter send (or send via Workspace) | Founder → Cy | 🔴 |

**Next review:** next working session.
**Recorded by:** Cy Henry · signature of record `69M2705M`.
