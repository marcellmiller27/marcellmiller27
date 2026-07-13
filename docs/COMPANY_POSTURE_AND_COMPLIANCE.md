# Company Posture & Compliance — Authoritative

> **This is the controlling statement of what John Henry Investments (JHI) is and is not.**
> Where any other document conflicts, **this document governs.**
>
> NOT legal/tax advice — confirm entity structure and regulated-activity questions with counsel.

---

## Founder directives (definitive — decided 2026-06-30)

1. **JHI is a research & analytics firm** — deep-dive, cross-asset market research and
   analysis sold to clients as **research, insight, education, and decision-support** (SaaS).
2. **JHI will NEVER manage outside funds or other people's money.** No client AUM, custody,
   discretionary management, pooled vehicles, or investment-manager/RIA role.
3. **JHI stays 100% private and bootstrapped.** **No VC, no seed rounds, no outside
   investors, no outside raised capital — ever.** The venture is **self-funded from
   revenue**, scaling resources in phases as paying users grow.

> Decision history: earlier drafts explored VC/seed; the founder has **decided against
> outside capital entirely**. JHI is bootstrapped and private. This supersedes any prior
> fundraising framing.

---

## What JHI IS
- A **private, founder-owned research & analytics firm / SaaS** selling cross-asset
  research, the John Henry Opportunity Score, and decision-support tools by subscription.
  Clients make **their own** decisions.
- **Self-funded** — growth paced by revenue, not investors.

## What JHI is NOT
- **Not** an investment manager, adviser-of-funds, broker-dealer, custodian, or fund.
- **Not** a manager of client/third-party money (never takes custody or discretion).
- **Not** raising or accepting outside investment of any kind.

---

## Why fully-private + bootstrapped is the clean path
Taking **no outside capital** removes a whole class of complexity and risk:
- **No securities offering** → no Reg D, no Form D, no accredited-investor/solicitation rules.
- **No investor fiduciary duties**, board seats, dilution, or growth-at-all-costs pressure.
- **No need for a separate entity to "sell equity in a segment"** — that problem only exists
  if you raise. Since JHI never sells equity, the structure can stay simple.
- **Full founder control.**

The one line that still matters: selling software/research isn't money management, but
**personalized investment advice for compensation** can implicate adviser rules even
without managing money. Keep the platform on the **research / education / analysis /
decision-support** side (score = one input, with disclaimers; no promised returns;
confirm with counsel).

---

## Structure — TWO separate entities (decided 2026-07-02)
Founder decision: the research platform is its **own separate company**, not a DBA:

```
  John Henry Investments, LLC          JHI Research & Analytics Firm, Inc.
  (family office — own funds,          (separate WYOMING CORPORATION — the research/SaaS
   private, no outside money)           business; holds the data license, client
                                        contracts, platform IP & liability)
  ───────── kept separate; intercompany only via documented, arm's-length terms ─────────
```

> **Entity type (decided 2026-07-03):** the research entity is **JHI Research & Analytics
> Firm, Inc.** (a **Wyoming corporation**). Confirm **C-corp vs. S-corp** election with the
> CPA (a corporation has more formalities and, as a C-corp, double taxation on distributed
> profits; S-corp election is restricted if another entity is a shareholder). The entity must
> be **formed before it signs** the NASDAQ data license.

- **Two distinct legal entities** (not a "dba" of one). This gives a real **liability
  firewall** — a platform dispute / data-license / breach issue stays in the research LLC and
  can't reach the family office's investment assets, and vice versa.
- **The research entity is the contracting party** for third-party deals — importantly the
  **NASDAQ SF1 data license must be held by JHI Research & Analytics Firm, Inc.**, not the
  family office (see `docs/legal/nasdaq/ORDER_FORM_REVIEW.md` — the founder has asked Nasdaq
  to **remove the "dba" and name the separate entity** before signing).
- **Separate bank accounts + clean books per entity**; no commingling; any value moving
  between them goes through **documented, arm's-length** channels (service agreements /
  intercompany loans / distributions).
- The family office may **own** the research corporation (parent/subsidiary) or hold it as a
  **sibling** — either preserves separation; confirm ownership + tax election with counsel/CPA.

### Registration & multi-state footprint (as of 2026-06-30; updated 2026-07-03)
- **Formation status (2026-07-03):** ✅ **EIN obtained** for JHI Research & Analytics Firm,
  Inc.; 🔄 **Wyoming C-corp formation in progress.** Next: bylaws + founder stock →
  **IP assignment (founder → corp)** → business bank account/Stripe → sign NASDAQ as the corp.
- **Domicile:** **JHI Research & Analytics Firm, Inc.** — a **Wyoming corporation** (no state
  corporate income tax, privacy, low cost, asset protection — good fit for a private firm).
- **Operating states:** **Georgia** (current) and **Florida** (to add) → **foreign-qualify**
  the WY corporation in each, with a **registered agent in all three states** (WY, GA, FL).
- **Income tax follows nexus:** WY's no-income-tax benefit does **not** erase tax owed where
  you operate (GA corporate income tax; FL corporate income tax for C-corps). File where you
  have nexus.
- **SaaS sales tax (don't skip):** subscriptions can be taxable in many states via
  **economic nexus** (driven by sales volume, not just registration). Use **Stripe Tax**
  (billing already on Stripe) or Avalara/TaxJar to automate taxability + thresholds.
- **Entity tax election (confirm with CPA):** the research entity is a **corporation (Inc.)**
  — confirm **C-corp vs. S-corp** with the CPA. A C-corp faces double taxation on distributed
  profits; S-corp election is **restricted if another entity (e.g., the family office) is a
  shareholder**. (An LLC would have been pass-through; the founder chose Inc.)
- Keep a **registered-agent + annual-report calendar** for all three states to stay in good
  standing.

## Bootstrapping & phased scale-up (feasibility)
Self-funding is feasible because this is a high-margin, low-infra SaaS (see
`docs/OPERATING_COST_LEAN_VS_STAFFED.md`, `docs/AWS_COST_10K_USERS.md`,
`docs/CASHFLOW_PROJECTION_12MO.md`):

| Phase | Run cost | Notes |
| --- | --- | --- |
| Prototype | **~$50–$300/mo** | free/lean tiers + deterministic AI FAQ; founder handles support |
| Paid MVP (lean) | **~$600–$1,600/mo** | billing live, reliable hosting, AI-first support |
| Production (~10k users, multi-AZ) | **~$950/mo** | scale infra as users grow |

- **Blended ARPU ~$70/user/mo → break-even at ~a few dozen paying users** (lean MVP) — and
  ~1–5 users at prototype scale. Cash-flow positive early; **let revenue fund each phase.**
- **Lumpy expense to time:** the **NASDAQ commercial SF1 license** (single-user dev ≈
  $120/mo; commercial tier TBD/awaiting quote). Validate on the cheap dev license first;
  buy the **commercial** license only when paying-user revenue justifies serving SF1-derived
  data to clients.
- **Real constraint = distribution + founder bandwidth, not capital.** Lean on the AI
  agents and the GTM/waitlist funnel; grow at a revenue-paced clip.

### Non-dilutive financing (debt / line of credit) — permitted, with discipline
Debt is **not** outside investment — no dilution, no investors, no board seats — so a
business loan or **line of credit is fully consistent** with staying 100% private. Options
once there is real ARR: **revenue-based financing** (Pipe/Capchase/Arc — fast, non-dilutive,
but can be pricey), **bank LOC** (cheapest; needs history + usually a personal guarantee),
**SBA loan**, or **MRR/ARR lines**. Discipline:
- **Borrow against ARR you have, not hope for** — lenders want real revenue + low churn +
  history. This is a **growth accelerant after traction**, not startup capital.
- **The collateral that matters is the recurring-revenue stream**, not the code/IP (lenders
  rarely lend much against early-stage software IP).
- **Avoid pledging family assets** (personal guarantees) — keep the family-office firewall.
- **Service debt from cash flow**; use it only for **specific, ROI-positive** needs (e.g.,
  the NASDAQ commercial license, a marketing push) — **never to fund operating losses.**
- **Option unique to this structure:** the family office can lend to the platform via a
  **documented, arm's-length intercompany loan** (note + interest) — non-dilutive, in-house,
  no external PG — provided the books stay clean (no commingling).

---

## Legal surface as a research-only firm (honest scope)
Being research-only (never managing money, never trading for clients) **removes the heavy
regime** (no investment-manager, broker-dealer, or custody rules). It is **low-risk, not
zero-risk.** What remains:
1. **Adviser line (key):** general, non-personalized research is typically protected
   ("publisher's exclusion"); **personalized, for-a-fee recommendations can make you an
   investment adviser even without managing money.** Keep outputs general/educational, not
   tailored "buy this" advice. Confirm the publisher's-exclusion posture with counsel.
2. **Data licensing:** NASDAQ **commercial** SF1 license required to serve derived data to
   clients; honor free-feed terms (CoinGecko/Yahoo/BLS).
3. **Marketing/consumer protection:** no misleading performance claims; clear
   "not investment advice" disclaimers; testimonial rules.
4. **Normal business legal:** liability entity, Terms of Service, privacy/data protection
   (user PII), billing terms, IP.
5. **Founder/family own trading:** trading the family's own money is fine; avoid
   front-running subscribers and disclose conflicts.

> Market this as a **"low, well-understood legal surface,"** not "no legal issues."

## Implications for product, messaging & internal docs
- Client-facing copy stays in the **research / analysis / education / decision-support**
  register; never imply JHI manages money or guarantees outcomes.
- Subscriptions sell **access to research and tools**, not money management.
- **Internal financial models** (`docs/COMPANY_VALUATION_ANALYSIS.md`,
  `docs/investor_package/`, EBITDA/DCF) are for **internal planning, IP valuation,
  estate/insurance, and lending** only — **not** fundraising (no outside investors).
- The platform **"Capital Raising Center"** (Module 12) is a **client-facing feature** for
  *users'* own ventures — unrelated to JHI's own funding (JHI raises nothing).

> Founder signature: `69M2705M` · John Henry Investments — private, bootstrapped research firm.
