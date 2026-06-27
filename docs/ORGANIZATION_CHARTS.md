# John Henry Investments — Organization Charts (Company + Platform)

> Two complementary views, both rendered as Mermaid diagrams (GitHub/Cursor compatible):
>
> - **Part A — Company organization chart:** departments, roles, reporting lines, the
>   **five AI customer-service agents**, and how the org grows by staffing stage. Grounded
>   in `docs/JOB_DESCRIPTIONS_AND_STAFFING_REQUIREMENTS.md`.
> - **Part B — Platform organization chart (as-built):** the complete system, every
>   interface, and command→action flows for the features actually implemented in this
>   codebase. Complements the full-vision `docs/SYSTEM_FLOWCHARTS_AND_PROCESS_MAPS.md`.
>
> **Legend for build status (Part B):** ✅ built & tested · 🟡 partial/prototype · ⬜ planned.

---

# Part A — Company Organization Chart

## A1. Company-wide org chart (full build-out)

Solid lines = direct reports. Dashed lines = fractional / outside advisors.

```mermaid
flowchart TD
  CEO["Founder / CEO<br/>(strategy, capital, governance)"]

  COO["COO / Operations Lead"]
  CTO["CTO / Technical Lead"]
  HoP["Head of Product"]
  AIDL["AI / Data / Research Lead"]
  HoS["Head of Sales & Partnerships"]
  FIN["Controller / Finance Lead"]
  CS["Customer Success Lead"]

  GC["Outside General Counsel"]
  COMP["Compliance Officer / Advisor"]
  CPA["CPA / Bookkeeper"]

  CEO --> COO
  CEO --> CTO
  CEO --> HoP
  CEO --> AIDL
  CEO --> HoS
  CEO --> FIN
  CEO -.-> GC
  CEO -.-> COMP

  %% Engineering
  CTO --> FSE["Full-Stack Engineer"]
  CTO --> BE["Backend Engineer"]
  CTO --> FE["Frontend Engineer"]
  CTO --> INT["Integration Engineer"]
  CTO --> DEVOPS["DevOps / Cloud Engineer"]
  CTO --> SEC["Security Engineer"]
  CTO --> QA["QA Engineer / Test Analyst"]

  %% Product
  HoP --> UX["UX / UI Designer"]

  %% AI / Data / Research
  AIDL --> AIE["AI Engineer"]
  AIDL --> DS["Data Scientist / Quant Analyst"]
  AIDL --> FRA["Financial Research Analyst"]

  %% Sales
  HoS --> AE["Account Executive(s)"]

  %% Finance
  FIN --> CPA
  FIN --> FPA["FP&A Lead"]

  %% Customer success + AI agent team (see A3)
  COO --> CS
  CS --> CSM["Customer Success Manager"]
  CS --> SUP["Support Specialist"]
  CS --> AITEAM["AI Customer-Service Team<br/>(5 agents — see A3)"]

  %% Operations & admin
  COO --> OPS["Operations Manager"]
  COO --> HR["HR / People Ops"]

  %% Legal specialists under outside counsel
  GC -.-> SECC["Securities / Investment Adviser Counsel"]
  GC -.-> PRIV["Privacy / Data Protection Counsel"]
  GC -.-> EMP["Employment Counsel"]
  GC -.-> IP["IP / Trademark Counsel"]
```

## A2. Departments at a glance

| Department | Leader | Core purpose |
| --- | --- | --- |
| Executive leadership | Founder / CEO, COO | Strategy, capital, partnerships, governance |
| Product & design | Head of Product | Roadmap, UX, requirements, research |
| Engineering | CTO / Technical Lead | Frontend, backend, integrations, DB, reliability |
| AI, data & research | AI/Data/Research Lead | AI assistant, Opportunity Score, data models, research |
| Security & DevOps | (under CTO) | Infra, access control, cloud ops, incident response |
| Legal & compliance | Outside General Counsel | Terms, privacy, securities review, vendor contracts |
| Finance & accounting | Controller / Finance Lead | Bookkeeping, reporting, billing controls, FP&A |
| Sales & partnerships | Head of Sales | Revenue, enterprise pipeline, referral relationships |
| Customer success & support | Customer Success Lead | Onboarding, retention, support, training |
| Operations & administration | Operations Manager | Vendors, HR, procurement, internal process |
| Quality assurance | (under CTO) | Testing, release quality, regression, acceptance |

## A3. The five AI customer-service agents (operational layer)

These are **AI agents implemented in the platform** (`backend/app/agents_services.py`,
`/api/v1/agents`), accounted for as operating-cost centers (not payroll) per
`docs/AI_AGENT_OPERATING_COST.md`. They form the front line of customer service and sit
within Customer Success, with the **founder as the escalation owner**.

```mermaid
flowchart TD
  Member["Member / User message"] --> Router{"Auto-routing<br/>by category / intent"}

  Router -->|"Getting started"| Ava["🟢 Ava Bennett<br/>Onboarding Concierge"]
  Router -->|"Billing / plans / Stripe"| Max["🟢 Max Carter<br/>Subscriptions & Billing"]
  Router -->|"Login / 2FA / biometric / privacy"| Sage["🟢 Sage Okafor<br/>Account & Security"]
  Router -->|"Features / market data / Opportunity Score"| Quinn["🟢 Quinn Alvarez<br/>Product & Markets Guide"]
  Router -->|"Bug / incident / problem"| Tess["🟢 Tess Nakamura<br/>Technical Support & Triage"]

  Ava --> Resolve["Resolved with answer + suggestions"]
  Max --> Resolve
  Sage --> Resolve
  Quinn --> Resolve

  Tess -->|"Needs action"| Ticket["Open tracked ticket"]
  Resolve -->|"Low confidence / issue"| Tess
  Ticket --> Founder["👤 Founder<br/>(escalation owner / action)"]

  CSL["Customer Success Lead"] -.-> Ava
  CSL -.-> Max
  CSL -.-> Sage
  CSL -.-> Quinn
  CSL -.-> Tess
```

**Agent roster & responsibilities:**

| Agent | Role | Handles (categories) | Escalates? |
| --- | --- | --- | --- |
| **Ava Bennett** | Onboarding Concierge | Getting started, account setup, walkthroughs, activation | No |
| **Max Carter** | Subscriptions & Billing Specialist | Plans, pricing/upgrades, billing/invoices, Stripe | No |
| **Sage Okafor** | Account & Security Agent | Authentication, 2FA/biometric, data protection, privacy | No |
| **Quinn Alvarez** | Product & Markets Guide | Opportunity Score, live market data, modules, how-to (no advice) | No |
| **Tess Nakamura** | Technical Support & Triage | Incident triage, troubleshooting, bug intake → **founder** | **Yes** |

Routing logic: messages are matched to a category → mapped to the owning agent;
issue-like messages (or any low-confidence answer) route to **Tess**, who triages and
forwards anything needing action to the **founder** as a tracked ticket.

## A4. Org by staffing stage (grows with revenue/risk)

Staffing follows revenue and risk — not all roles are hired at once.

```mermaid
flowchart LR
  subgraph S1["1) Prototype / Controlled Beta"]
    F1["Founder"] --> C1["Dev contractor"]
    F1 --> L1["Outside legal (review)"]
    F1 --> K1["CPA / bookkeeper"]
    F1 --> A1["AI agents (5) — tier-1 support"]
  end

  subgraph S2["2) Paid MVP"]
    F2["Founder"] --> FS2["Full-stack engineer"]
    F2 --> BE2["Backend / data engineer"]
    F2 --> CS2["Customer success / support"]
    F2 --> L2["Outside legal / compliance"]
    F2 --> K2["CPA / fractional controller"]
    F2 --> D2["DevOps / security contractor"]
    F2 --> A2["AI agents (5) — tier-1 support"]
  end

  S1 --> S2
```

```mermaid
flowchart LR
  subgraph S3["3) Growth"]
    CEO3["CEO"] --> CTO3["CTO + eng team"]
    CEO3 --> PM3["Product manager"]
    CEO3 --> AI3["AI / data lead"]
    CEO3 --> DO3["DevOps / security"]
    CEO3 --> CS3["Customer success + AI agents (5)"]
    CEO3 --> SA3["Sales / partnerships"]
    CEO3 --> FN3["Finance / controller"]
    CEO3 --> CO3["Compliance advisor / lead"]
    CEO3 --> LG3["Legal counsel"]
  end

  subgraph S4["4) Scale / Enterprise"]
    CEO4["CEO + COO"] --> DEP4["Formal departments:<br/>Eng · Product · AI/Data · Security ·<br/>Legal · Compliance · Finance · Sales ·<br/>Support (human + AI agents) · Ops · QA"]
  end

  S3 --> S4
```

---

# Part B — Platform Organization Chart (as-built)

This reflects **what exists in this repository today**: a Next.js frontend, a FastAPI
backend with 14 router groups, durable SQL persistence, and live/external data adapters.

## B1. Complete system map (layered)

```mermaid
flowchart TB
  subgraph Clients["Clients"]
    Web["Next.js Web App ✅<br/>(marketing + app pages)"]
    Mobile["Mobile App /mobile ✅<br/>(live: password, 2FA, biometric)"]
  end

  subgraph Edge["Cross-cutting middleware ✅"]
    CORS["CORS (allowed origins)"]
    RL["Rate-limit middleware (env-gated)"]
    AUTHZ["Token auth + scoped tokens"]
  end

  subgraph API["FastAPI backend — router groups (/api/v1)"]
    direction TB
    R_auth["/auth ✅ register/login/me"]
    R_mobile["/auth (mobile) ✅ 2FA, biometric, security"]
    R_billing["/billing ✅ plans, checkout, webhook(verified)"]
    R_acct["/accounting ✅ COA, journal, trial balance"]
    R_reports["/reports ✅ financial, audit"]
    R_dash["/dashboards ✅ executive"]
    R_crm["/crm ✅ contacts, deals, activities"]
    R_market["/market ✅ quotes, providers, inflation"]
    R_research["/research 🟡 scores, backtests, coverage"]
    R_val["/valuations 🟡 illiquid estimates"]
    R_support["/support ✅ faq, ask"]
    R_agents["/agents ✅ roster, message, tickets"]
    R_leads["/leads ✅ capture, count"]
    R_intg["/integrations 🟡 connectors, sync, exports"]
  end

  subgraph Services["Service layer"]
    S_found["Foundation (auth/billing/audit) ✅"]
    S_mob["Mobile auth (TOTP+WebAuthn) ✅"]
    S_sec["Security (JWT, Fernet, TOTP) ✅"]
    S_acct["Accounting ✅"]
    S_crm["CRM ✅"]
    S_report["Reporting/Dashboards ✅"]
    S_market["Market data adapters ✅"]
    S_score["Opportunity Score 🟡"]
    S_research["Research studies 🟡"]
    S_val["Valuation engine 🟡"]
    S_agents["Agent routing + tickets ✅"]
    S_support["Support FAQ retrieval ✅"]
  end

  subgraph Data["Persistence ✅"]
    DB["SQLAlchemy ORM<br/>SQLite (dev) / Postgres (prod)"]
    Audit["Audit logs"]
  end

  subgraph Ext["External interfaces"]
    Stripe["Stripe 🟡 (webhook sig verified ✅)"]
    CoinGecko["CoinGecko ✅"]
    Yahoo["Yahoo Finance ✅"]
    BLS["US BLS ✅"]
    FRED["FRED ⬜ key-gated"]
    TwelveData["Twelve Data ⬜ key-gated"]
    Sharadar["Sharadar SF1 ⬜ key-gated"]
  end

  Web --> Edge
  Mobile --> Edge
  Edge --> API
  API --> Services
  Services --> Data
  S_found --> Audit
  S_agents --> DB
  R_billing --> Stripe
  S_market --> CoinGecko
  S_market --> Yahoo
  S_market --> BLS
  S_market --> FRED
  S_market --> TwelveData
  S_research --> Sharadar
```

## B2. Interface inventory (every interface required)

### Frontend routes (Next.js)

| Route | Purpose | Talks to backend? |
| --- | --- | --- |
| `/` | Marketing landing + mission + waitlist | 🟡 docs routes; waitlist ✅ |
| `/login`, `/register` | Auth entry | 🟡 prototype |
| `/mobile` | Live mobile app (sign-in, 2FA, biometric, status) | ✅ yes |
| `/dashboard` | Executive + live market widgets | ✅ live market |
| `/opportunities`, `/portfolio`, `/reports`, `/due-diligence`, `/assistant`, `/account` | Module pages | 🟡 mostly static |
| `/pricing` | Plans/tiers | 🟡 documents plans |
| `/support` | AI assistant chat (agent-routed) | ✅ yes |
| `/team` | AI agent roster profiles | ✅ yes |
| `/join` | Waitlist funnel | ✅ yes |

### Backend API (as-built endpoints, prefix `/api/v1`)

| Group | Endpoints | Status |
| --- | --- | --- |
| `/auth` | `POST /register`, `POST /login`, `GET /me` | ✅ |
| `/auth` (mobile) | `POST /login/initiate`, `/2fa/{verify,dev-code,enable,disable}`, `/biometric/{register,challenge,assert}`, `GET /security/status` | ✅ |
| `/billing` | `GET /plans`, `GET /subscription`, `POST /checkout-session`, `POST /webhook`, `GET /audit-logs` | ✅ (webhook signature-verified) |
| `/accounting` | `GET /chart-of-accounts`, `/journal-entries`, `/trial-balance` | ✅ |
| `/reports` | `GET /audit`, `/financial` | ✅ |
| `/dashboards` | `GET /executive` | ✅ |
| `/crm` | `GET/POST /contacts`, `/deals`, `/activities`, `GET /summary` | ✅ |
| `/market` | `GET /quotes`, `/providers`, `/symbols`, `/inflation` | ✅ |
| `/research` | `GET /score-backtest`, `/opportunity-scores`, `/equity-oos-backtest`, `/fundamentals-status`, `/acquisition-validation`, `/data-coverage`, `/adoption` | 🟡 |
| `/valuations` | `GET /estimate` | 🟡 |
| `/support` | `GET /faq`, `POST /ask` | ✅ |
| `/agents` | `GET /` (roster), `POST /message`, `GET /tickets` | ✅ |
| `/leads` | `POST /`, `GET /count` | ✅ |
| `/integrations` | `GET /connectors`, `/connections`, `POST/GET /sync-jobs`, `GET /banking/transactions`, `POST/GET /vendor/bills`, `POST /office/export-package` | 🟡 |
| ops | `GET /health`, `GET /ready` | ✅ |

### External interfaces

| Interface | Use | Status |
| --- | --- | --- |
| Stripe | Checkout + webhook (signature verified) | 🟡 (verification ✅) |
| CoinGecko / Yahoo Finance / US BLS | Live crypto, equities/FX, inflation | ✅ |
| FRED / Twelve Data / Sharadar SF1 | Macro / licensed quotes / PIT fundamentals | ⬜ key-gated |

## B3. Core request/response protocol (every protected call)

```mermaid
sequenceDiagram
  participant UI as Client (Web/Mobile)
  participant MW as Middleware (CORS, rate-limit)
  participant API as FastAPI router
  participant SEC as Security (PyJWT)
  participant SVC as Service layer
  participant DB as Database
  participant AUD as Audit log

  UI->>MW: HTTPS request + Bearer token
  MW->>API: forward (if under rate limit)
  API->>SEC: decode_access_token()
  SEC-->>API: principal (user, org, role)
  API->>SVC: invoke with principal
  SVC->>DB: tenant-scoped read/write
  SVC->>AUD: record sensitive action
  SVC-->>API: result
  API-->>UI: authorized JSON response
```

## B4. Command → action flows (as-built features)

### Sign-up & login

```mermaid
flowchart TD
  Cmd1["POST /auth/register"] --> Hash["Hash password (PBKDF2)"] --> Tenant["Create org + membership + trial subscription"] --> Tok["Issue JWT (PyJWT)"] --> Out1["Return auth + token"]
  Cmd2["POST /auth/login"] --> Verify["Verify password"] --> Tok2["Issue JWT"] --> Out2["Return auth"]
```

### Two-factor (TOTP) — secret encrypted at rest ✅

```mermaid
flowchart TD
  E["POST /auth/2fa/enable"] --> Gen["Generate TOTP secret"] --> Enc["Encrypt at rest (Fernet)"] --> URI["Return otpauth URI + (dev) code"]
  LI["POST /auth/login/initiate"] --> Need{"2FA enabled?"}
  Need -->|no| Auth1["Return access token"]
  Need -->|yes| Ch["Issue scoped 2FA challenge token"]
  Ch --> V["POST /auth/2fa/verify (code)"] --> Dec["Decrypt secret + verify TOTP (±window)"] --> Auth2["Return access token"]
```

### Biometric (real WebAuthn ES256) ✅

```mermaid
flowchart TD
  Reg["POST /auth/biometric/register<br/>(public key)"] --> Store["Store credential + sign_count"]
  Cg["POST /auth/biometric/challenge"] --> Nonce["Issue nonce + scoped token"]
  Nonce --> As["POST /auth/biometric/assert<br/>(signature, authenticatorData, clientDataJSON)"]
  As --> Vf{"Verify: challenge bound +<br/>ES256 signature + counter↑"}
  Vf -->|valid| Ok["Issue access token"]
  Vf -->|invalid| Deny["401 (prod requires real assertion)"]
```

### Billing checkout + verified webhook ✅

```mermaid
flowchart TD
  Co["POST /billing/checkout-session"] --> Set["Set subscription incomplete + audit"] --> Url["Return checkout URL"]
  Wh["POST /billing/webhook (raw body)"] --> Sig{"STRIPE_WEBHOOK_SECRET set?"}
  Sig -->|yes| Verify["Verify Stripe signature"] --> Map["Map event → tenant/plan/status"]
  Sig -->|no| Mock["Dev JSON mock path"]
  Map --> Apply["Update subscription + audit"]
  Mock --> Apply
  Verify -->|invalid| R400["400 reject forged event"]
```

### AI customer service (agent routing + escalation) ✅

```mermaid
flowchart TD
  Msg["POST /agents/message"] --> FAQ["Support FAQ retrieval (confidence)"] --> Issue{"Issue or low confidence?"}
  Issue -->|no| Route["Route to owning agent (Ava/Max/Sage/Quinn)"] --> Reply["Reply + suggestions"]
  Issue -->|yes| Tess["Tess triages"] --> Tk["Open ticket → founder"] --> Reply2["Acknowledge + escalation notice"]
  Roster["GET /agents"] --> List["Return 5-agent roster"]
  Tickets["GET /tickets"] --> View["Founder views escalated tickets"]
```

### Other as-built commands

```mermaid
flowchart LR
  L["POST /leads"] --> Cap["Persist lead + dedupe"] --> Cnt["GET /leads/count"]
  Q["GET /market/quotes"] --> Adapt["Provider adapters + cache + failover"] --> Px["Live prices"]
  J["POST journal entry"] --> Bal{"Debits = credits?"} -->|yes| Post["Post + trial balance"]
  Bal -->|no| Rej["Reject (validation)"]
  Sc["GET /research/opportunity-scores"] --> Fac["Compute multi-factor 0–100 score"] --> Rank["Ranked cross-asset comparison"]
```

## B5. As-built module dependency map

```mermaid
flowchart TB
  Auth["Auth + scoped tokens ✅"] --> App["App pages / Mobile ✅"]
  Billing["Billing + entitlements ✅"] --> App
  DBL["Database + audit ✅"] --> App
  App --> Market["Live market data ✅"]
  App --> Support["Support + AI agents ✅"]
  App --> CRM["CRM ✅"]
  App --> Acct["Accounting ✅"]
  Acct --> Reports["Reports + dashboards ✅"]
  CRM --> Reports
  Market --> Score["Opportunity Score 🟡"]
  Score --> Research["Research studies 🟡"]
  Market --> Val["Valuations 🟡"]
  Integrations["External integrations 🟡"] --> Acct
  Integrations --> CRM
  Billing --> Stripe["Stripe (verified webhook) 🟡"]
```

---

## Notes & cross-references

- Company roles, levels, and credential requirements: `docs/JOB_DESCRIPTIONS_AND_STAFFING_REQUIREMENTS.md`.
- AI agent profiles & cost accounting: `docs/AI_AGENT_TEAM_PROFILES.md`, `docs/AI_AGENT_OPERATING_COST.md`.
- Full **vision** flowcharts (all planned modules): `docs/SYSTEM_FLOWCHARTS_AND_PROCESS_MAPS.md`.
- As-built code objectives & audit: `docs/CODE_OBJECTIVES.md`, `docs/SRC_CODE_AUDIT.md`.
- Security model behind the auth/2FA/biometric/webhook flows: `docs/SECURITY_POSTURE_AND_DATA_PROTECTION.md`.
