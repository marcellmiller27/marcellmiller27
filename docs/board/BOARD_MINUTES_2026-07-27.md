# Board Minutes — JHI Research & Analytics Firm, Inc.

**Meeting date:** 2026-07-27 · **Type:** Founder working session (platform brand + UX) · **Recorder:** Cy Henry (VP, Software Engineering — AI teammate)
**Present:** Founder (Galen Marcellus Miller).

> NOT legal/tax/accounting advice. Prior session: `docs/board/BOARD_MINUTES_2026-07-26.md`.
> Signature of record: `69M2705M`. Ethos: *How we do anything is how we do everything.*

---

## 1. 🔴 PRIORITY — File a DBA for "Aegira" (RECORDED — new Founder task)
- **Founder directive:** legally register a **DBA / assumed name "Aegira"** under **JHI Research & Analytics Firm, Inc.** so the platform brand is used lawfully while the corporate entity remains the entity of record.
- **Why:** we now present the product publicly as **Aegira** (storefront, app, newsletters, deliverables). A DBA/"doing business as" filing lets JHI Research & Analytics Firm, Inc. legally trade and publish under the Aegira name; it complements the separate **trademark** clearance/filing already in flight.
- **Suggested essentials (Founder + counsel to execute):** file the assumed-name/DBA certificate in the state/county of formation (and any state where we transact); update bank account signer docs, Stripe, and invoices to reflect "Aegira, a DBA of JHI Research & Analytics Firm, Inc." where appropriate. *(Not legal advice — confirm with counsel.)*

## 2. Brand architecture — LOCKED rule (RECORDED)
The Founder confirmed the two-layer model and the precise split between **display** and **legal/provenance**:
- **Product / display = Aegira** — everything the reader/subscriber sees as the *product*: storefront, app shell + wordmark, newsletter masthead & byline, the "Ask Aegira" assistant, AI personas, editorial voice, marketing/about narrative, UI copy, entity "Opportunity Score," and **deliverable file names**.
- **Legal & provenance = JHI Research & Analytics Firm, Inc. + `JHI-SIG: 69M2705M`** — copyright ©, publisher-of-record ("Prepared by … Firm, Inc." / "Published by … Firm, Inc."), the workbook **Legal & Provenance** tab, `JHI_STAFF_EMAILS` infrastructure, internal field names, and code headers.
- **Financial work-product internals** (Excel workbook cell content, deal-memo document title) currently remain **JHI** for legality — see Open Item §5(a) for the refinement under discussion.
- Primary domain **`aegiraenterprise.com`** (+ `.ai/.io/.dev/.app`) purchased via **AWS Route 53** (registration in progress); `.com` canonical, others 301-redirect. (Ref: `docs/board/BRAND_NAMING_AEGIRA.md`.)

## 3. Platform modifications executed this session (RECORDED — on PRs, pre-merge)
- **"Ask JHI" → "Ask Aegira"** (header, menu, dashboard, nav). *(PR #132)*
- **Newsletter / PDF / AI-persona → Aegira** — masthead, byline ("VP of Editorial, Aegira (AI)"), editorial voice, teaser, editorial-LLM persona; legal © + "Prepared by … Firm, Inc." retained. *(PR #133)*
- **Wider product sweep → Aegira** — upgrade gate, cancel/login/register, entity "Aegira Opportunity Score," QoE/BQA display, assistant sub-agents, company-record, **About narrative** ("We built Aegira"; "…published by JHI Research & Analytics Firm, Inc." retained). *(PR #133)*
- **Nomenclature:** the "Deal X-Ray" page → **"Limited Scope Review — CIM analysis in Excel,"** submit button → **"Run LSR."** *(PR #133)*
- **Deliverable filenames → Aegira** — generated `Aegira_QoE_*`, `Aegira_BQA_*`, `Aegira_<co>_Financials.xlsx`, `aegira-<edition>-*.pdf`, and the static Documents assets (`Aegira_Sales_Commission…`, `Aegira_Data_Sources…`, `Aegira_Competitor…`). **File internals kept JHI** for legality. *(PR #133)*
- **Institutional type scale** — tightened oversized product headings (app hero, newsletter masthead/subheads) on screen and in the PDF. *(PR #133)*
- **Bug fix:** the persistent **"1 Issue"** dev badge (present on every app page) was the global search `<input>` missing `id`/`name`; fixed. *(PR #133)*
- **Verification:** eslint clean; 35 affected backend tests pass; headless PDF re-rendered with Aegira masthead/byline + JHI legal lines; live `:3009` verified with screen-recording walkthroughs.

## 4. AI editorial (E2) — status carry-over (RECORDED)
E2 on **AWS Bedrock (Claude Sonnet 4.5)** is **ACTIVE and verified live** this session (`ENABLE_LLM_EDITORIAL` on; region + model pinned via Secrets); all three editions elevate on-screen, fact-lock clean, ~$0.003–0.01/edition, $250/mo cap. Secrets persisted by Founder.

## 5. 🟣 OPEN — decisions to make next session (paused for discussion)
- **(a) Excel workbook masthead.** Question raised: since the workbook already carries `JHI-SIG` on every sheet **and** a dedicated **Legal & Provenance** tab, may the blue masthead row (and section headers) read **Aegira**? Cy's recommendation: **Yes (Option B)** — full **Aegira** on presentation surfaces + a "Published by JHI Research & Analytics Firm, Inc." subline, with JHI confined to the Legal & Provenance tab + `JHI-SIG`. **Founder to choose A (masthead Aegira only) or B (full presentation Aegira).**
- **(b) Home vs. Dashboard.** Founder wants **both** as **separate modules** (today they are conflated; Cy's "Dashboard→Home" menu rename is to be **reverted**). Proposed split: **Home** = front-door launchpad (module tiles, quick actions, what's-new, shortcuts); **Dashboard** = the cockpit (Portfolio Value, Watch List, Acquisition Pipeline, Economic Risk, live market). **Aegira wordmark → Home** (recommended). Founder to confirm the split, contents, menu order, and wordmark target before build.

## Decisions locked
DBA "Aegira" filing = new Founder priority; brand split (product = Aegira / legal & provenance = JHI R&A Firm, Inc. + `JHI-SIG`) is the standing rule; deliverable filenames = Aegira, file internals = JHI (pending §5a refinement); Home and Dashboard are **separate** modules (build next session).

---

## Action items (owner · priority)
| # | Action | Owner | Priority |
| --- | --- | --- | --- |
| 1 | **File the DBA / assumed name "Aegira"** under JHI Research & Analytics Firm, Inc. (+ update bank/Stripe/invoice docs) | Founder (+ counsel) | 🔴 |
| 2 | **Open the JHI business bank account** (carry-over; underpins Stripe payouts + books) | Founder (+ accountant/attorney) | 🔴 |
| 3 | Merge **#132** (Ask Aegira) and **#133** (brand/nomenclature/LSR/type-scale/1-Issue fix) | Founder | 🔴 |
| 4 | Decide **§5(a)** workbook masthead **A/B** and **§5(b)** Home-vs-Dashboard split → then Cy builds | Founder → Cy | 🟡 |
| 5 | **Rebuild the Docker frontend + backend** off `main` so live `:3000` + served PDFs reflect Aegira (currently stale, pre-brand) | Cy | 🟡 |
| 6 | Carry-over: **Stripe** live keys + price IDs; **NASDAQ 5H** + Order Form; **DNS** point `aegiraenterprise.com` at deploy target + **SES** for newsletter email; **storefront copy** rewrite; fix 10 pre-existing accounting tests | Founder / Cy | 🟡 |

**Next review:** next working session.
**Recorded by:** Cy Henry · signature of record `69M2705M`.
