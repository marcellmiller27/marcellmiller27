# Marketing Strategy & Campaign — Research Phase Two

> **Think-tank session.** A high-level "GodMode" view of how John Henry Investments
> (JHI) creates **targeted demand with high-probability conversion** into paid
> subscriptions, plus the detailed demographics, segments, channels, funnels, and
> measurement that make it repeatable.
>
> **Companion docs:** `docs/GTM_FUNNELS_NEXTJS.md` (funnels + lean stack),
> `docs/SERVICES_PRICING_FIT_ANALYSIS.md` (tiers + willingness-to-pay),
> `docs/RESEARCH_THESIS_PROBLEM_SOLUTION_FIT.md` (problems P1–P4),
> `docs/CASHFLOW_PROJECTION_12MO.md` (ARPU/economics),
> `docs/OPERATING_COST_LEAN_VS_STAFFED.md` (budget envelope).
>
> **Status / honesty rule (carried from the thesis):** the John Henry Opportunity
> Score's *predictive validity is unproven* (H5 still **FAIL**). Marketing must sell
> **decision-support, organization, and access** — not "alpha" or guaranteed returns.
> Overclaiming is both a conversion risk (sophisticated buyers churn) and a
> regulatory risk (advice/RIA positioning). This is a hard constraint, not a footnote.

---

## 0. Phase Two framing — why this is a research segment, not just a plan

Phase One (the thesis, §1–§8) asked *"is the problem real and does the product address
it?"* — answer: **the problems P1–P4 are real; the solution is design-confirmed but not
yet market-confirmed.** Phase Two asks the next falsifiable question:

> **PT-H1 — Demand:** Can JHI acquire qualified subscribers at a **CAC that yields
> LTV:CAC ≥ 3 and payback ≤ 12 months** through repeatable, mostly-organic channels?
>
> **PT-H2 — Conversion:** Does **content/score-led, segment-specific** messaging convert
> at materially higher rates than generic finance-app messaging (target: visitor→lead
> ≥ 25% on intent pages; lead→trial ≥ 30%; trial→paid ≥ 20% for Consumer, ≥ 30% for
> Professional)?
>
> **PT-H3 — Segment fit:** Is the **Professional/SMB-acquisition** segment the
> highest-probability beachhead (clearest willingness-to-pay per
> `SERVICES_PRICING_FIT_ANALYSIS.md`), versus broad retail?

Everything below is structured so each tactic produces a measurable result that
confirms or rejects these hypotheses. **Treat the first 90 days as an experiment, not a
launch.**

---

## 1. GodMode view (the one-paragraph strategy)

**Win a narrow, high-intent beachhead first — SMB/search-fund acquirers and the
advisors around them (Professional $299) — using authority content + a free
"Acquisition/Opportunity analyzer" lead magnet, captured on our own Next.js funnel,
nurtured by email, and converted via a guided trial.** Use the cheaper, higher-volume
**Consumer ($50)** retail audience as a *content flywheel and freemium top-of-funnel*,
not the primary revenue bet. Layer **Enterprise/Family-Office ($1,500+)** as
founder-led, relationship/referral sales — never paid ads. Keep paid advertising
**minimal and retargeting-only** until organic conversion math is proven. Measure
everything; double down on the two channels with the best payback and kill the rest.

```
                        ┌─────────────────────────────────────────────┐
   AUTHORITY (organic)  │  SEO/MDX + LinkedIn + niche communities      │  cheap, compounding
                        └───────────────┬─────────────────────────────┘
                                        ▼
   LEAD MAGNET                ┌───────────────────────┐
   (free value)               │  Analyzer / report /  │  ← squeeze + waitlist (built)
                              │  checklist + email    │
                              └──────────┬────────────┘
                                         ▼
   NURTURE (email)            ┌───────────────────────┐
                              │  5–7 email sequence,   │  segment-specific
                              │  segment-routed        │
                              └──────────┬────────────┘
                                         ▼
   ACTIVATE (trial)           ┌───────────────────────┐
                              │  Guided trial →        │  Stripe checkout (built)
                              │  first "aha" moment    │
                              └──────────┬────────────┘
                                         ▼
   CONVERT / EXPAND           ┌───────────────────────┐
                              │  Paid → upsell tier →  │  referral loop
                              │  referral             │
                              └───────────────────────┘
```

---

## 2. Detailed demographics & target audience (who we convert)

We market to **three primary segments** that already exist in the product as
`userTypes` and pricing tiers. Below: who they are, what they feel, where they are, and
the conversion trigger.

### Segment A — "The Operator-Acquirer" (PRIMARY beachhead → Professional $299)

| Attribute | Detail |
| --- | --- |
| **Who** | Search funds, self-funded searchers, SMB buyers, ETA (Entrepreneurship-Through-Acquisition) operators, M&A advisors, brokers, deal-focused CPAs/attorneys |
| **Age / stage** | 30–55; MBA or operator background; mid-career, capital-access, high agency |
| **Income / budget** | Personal $150k–$500k+; deal budgets $0.5M–$10M; expenses are tax-deductible business costs |
| **Psychographics** | Analytical, time-poor, ROI-driven, allergic to fluff; trust peers and data over ads |
| **Jobs-to-be-done** | Screen/compare targets fast; sanity-check EBITDA/DSCR/SBA serviceability; produce a credible diligence/report artifact |
| **Pain (maps to P4)** | SMB acquisition is *under-tooled* vs public markets; analysis lives in messy spreadsheets |
| **Where they are** | LinkedIn, Twitter/X "#ETA" + "SMB Twitter", search-fund newsletters/podcasts, BizBuySell, SBA-lender networks, Reddit r/search_fund, Slack/Circle ETA communities, university ETA programs |
| **Conversion trigger** | A free **deal analyzer** that turns a P&L into a Buy/Watch/Pass + DSCR view in minutes |
| **Why first** | Clearest willingness-to-pay; $299 is well-positioned for the niche; smallest, reachable audience = cheapest CAC |

### Segment B — "The Self-Directed Wealth-Builder" (VOLUME flywheel → Consumer $50)

| Attribute | Detail |
| --- | --- |
| **Who** | Retail/DIY investors, FIRE-minded professionals, accredited-but-self-directed individuals diversifying across stocks/crypto/real estate |
| **Age / stage** | 28–50; tech-comfortable; multiple accounts/brokerages |
| **Income / budget** | $80k–$250k; price-sensitive; compares to Seeking Alpha/Morningstar/Koyfin ($10–50/mo) |
| **Psychographics** | Curious, identity = "smart with money," wants an edge but skeptical of hype |
| **Jobs-to-be-done** | One place to compare opportunities across asset classes (P3); macro context (P1); track scattered holdings |
| **Pain (maps to P1/P3)** | Tool fragmentation; no standardized cross-asset comparison |
| **Where they are** | Google search (high-intent "compare X vs Y", "is X a good investment"), YouTube finance, Reddit (r/investing, r/financialindependence), X finance, newsletters |
| **Conversion trigger** | Free Opportunity Score lookup / cross-asset comparison + a great macro dashboard |
| **Why second** | Big TAM but low ARPU + higher churn; use for **SEO content flywheel and freemium**, not paid CAC |

### Segment C — "The Professional Allocator / Family Office" (EXPANSION → Enterprise $1,500+)

| Attribute | Detail |
| --- | --- |
| **Who** | RIAs, wealth advisors, small family offices, boutique investment firms, bankers/attorneys serving HNW clients |
| **Age / stage** | 35–65; fiduciary; team-based; brand/trust-sensitive |
| **Income / budget** | Firm budgets; replaces or complements $2k+ terminals (Bloomberg/FactSet) |
| **Psychographics** | Risk-averse on vendors, relationship-driven, references matter |
| **Jobs-to-be-done** | Team accounts, oversight, branded client reports, standardized scoring across a book |
| **Pain (maps to P2)** | Access asymmetry; expensive incumbents; need defensible, client-ready outputs |
| **Where they are** | LinkedIn, industry events/associations, referrals, warm intros — **not** ad networks |
| **Conversion trigger** | Founder-led demo + a pilot; references; branded report output |
| **Why last** | Long sales cycle, high ACV, low volume — pursue **founder/referral sales**, zero paid ads |

> **Anti-personas (do not spend on):** day-trading "get-rich-quick" crowd (high churn,
> regulatory bait, wrong expectations); pure crypto-degens; anyone expecting guaranteed
> returns. Our honesty constraint makes these a bad fit and a compliance hazard.

---

## 3. Positioning & message architecture (what we say)

**Core positioning:** *"Institutional-grade decision-support for every asset class —
and the only place built for the people actually buying businesses."*

**Message house:**

- **Roof (brand promise):** *Clarity and discipline for serious allocators.*
- **Pillar 1 — Unify (P1):** "Stop stitching together five tools." One shell:
  discovery, scoring, diligence, macro, portfolio.
- **Pillar 2 — Compare (P3):** "One standardized 0–100 lens across stocks, crypto,
  real estate, and private deals." *(Sell the standardization/discipline, not predicted
  returns.)*
- **Pillar 3 — Acquire (P4):** "The acquisition workflow public-market tools forgot —
  EBITDA/DSCR/SBA, diligence, and a credible report." *(Hero pillar for Segment A.)*
- **Pillar 4 — Access (P2):** "Pro-grade research and team workflows without the
  $2k/mo terminal."

**Proof, not hype:** live market data, transparent methodology, "what the score is /
isn't," founder credibility, and (as it accrues) testimonials + case studies. Every
claim must be defensible.

**Compliance-safe language:** "decision-support," "research and analysis,"
"educational," "not investment advice." Add disclaimers; decide RIA positioning before
scaling (see thesis risk section). This protects conversion *and* the company.

---

## 4. Channel strategy — ranked by probability of high-ROI outcome

Channels are sequenced. **Earn organic proof before paying for reach.** Each lists the
target segment, expected cost profile, and the leading indicator we watch.

### Tier 1 — Do first (highest probability, lowest cost)

| # | Channel | Segment | Why high-probability | Leading metric |
| --- | --- | --- | --- | --- |
| 1 | **Founder-led / community + LinkedIn organic** | A, C | Direct access to ETA/SMB + advisor niches; trust transfers; ~$0 | replies, demo requests, waitlist joins |
| 2 | **SEO + MDX content engine** (Next.js native) | B (then A) | Compounding, high-intent ("compare X vs Y", "SBA DSCR calculator"); we own it | organic clicks → leads |
| 3 | **Lead-magnet tools** (free analyzer/score lookup/checklist) | A, B | Product-led: the magnet *is* a product taste; best lead quality | tool use → email capture rate |
| 4 | **Email/lifecycle nurture** (Resend/SES) | all | Cheapest conversion lift; owns the relationship | lead→trial, trial→paid |

### Tier 2 — Add once Tier 1 shows signal

| # | Channel | Segment | Why | Leading metric |
| --- | --- | --- | --- | --- |
| 5 | **Niche newsletter / podcast sponsorships** (ETA, search-fund, FIRE) | A, B | Targeted, trusted, measurable with promo codes | code redemptions, CAC by placement |
| 6 | **Referral loop** (invite → reward) | all | Lowest-CAC growth once there's value to share | k-factor, referred conversions |
| 7 | **Retargeting ads only** (Meta/Google/LinkedIn pixel) | warm visitors | Cheap, converts existing intent; not cold prospecting | ROAS on warm audiences |
| 8 | **YouTube / short-form** (methodology, deal teardowns) | A, B | Authority + SEO; repurposes content engine | watch→site→lead |

### Tier 3 — Only after CAC/LTV is proven (scale capital)

| # | Channel | Segment | Why later | Risk |
| --- | --- | --- | --- | --- |
| 9 | **Cold paid search (Google) on high-intent terms** | A, B | Scales volume | only profitable if conversion proven |
| 10 | **Cold paid social prospecting** | B | Volume | high CAC, expectation mismatch risk |
| 11 | **Conferences/events** | A, C | High-ACV relationships | expensive; reserve for Enterprise |

> **Budget discipline:** the lean GTM stack (`GTM_FUNNELS_NEXTJS.md`) runs **$0–150/mo**
> in tools. Reserve any ad spend for **retargeting first**; cap early cold-ad tests at a
> small, explicitly-budgeted experiment with a kill-rule (see §7).

---

## 5. Funnel design & conversion mechanics (how we convert)

We already have the rails (`GTM_FUNNELS_NEXTJS.md`): landing, **waitlist (built)**,
auth/2FA trial, **Stripe checkout (built)**. Phase Two adds the *conversion machinery*.

**The high-conversion path (per segment):**

1. **Acquire** → authority content / community / lead-magnet tool.
2. **Capture** → email (offer a *specific* magnet, not "sign up"). Segment-route on a
   single qualifying question ("Are you buying a business, investing for yourself, or
   advising clients?").
3. **Nurture** → 5–7 email sequence tailored to the segment's pain (P4 for A, P1/P3 for
   B, P2 for C). Teach, then invite to trial.
4. **Activate** → guided trial engineered around **one "aha" in <10 minutes**
   (Segment A: analyze a sample deal → Buy/Watch/Pass; Segment B: run a cross-asset
   comparison; Segment C: generate a branded report).
5. **Convert** → in-trial paywall at the aha moment; annual discount; "founding member"
   pricing while features mature (honest about Partial/Prototype status).
6. **Expand** → upsell Consumer→Professional when usage signals deal/advisory intent;
   referral prompt after first value.

**Conversion-rate levers (highest impact first):**

- **Match magnet → segment → trial "aha"** (relevance beats cleverness).
- **Reduce time-to-value** in trial (pre-loaded sample data; no blank states).
- **Social proof** at the decision point (testimonials, usage counts, logos as earned).
- **Annual pricing + founding-member** offer to lift ARPU and cut churn.
- **A/B test** headline, magnet, pricing-page order (PostHog/flags — native to Next.js).
- **Honesty as conversion**: a "what the score is / isn't" section *raises* trust with
  sophisticated buyers and cuts bad-fit churn.

**Target funnel math (hypotheses to validate, not promises):**

| Stage | Consumer (B) | Professional (A) |
| --- | --- | --- |
| Visitor → Lead (intent page) | 20–30% | 25–35% |
| Lead → Trial | 25–35% | 30–40% |
| Trial → Paid | 15–25% | 25–35% |
| Implied Visitor → Paid | ~1–2.5% | ~2–5% |

**Unit-economics guardrails** (from `CASHFLOW_PROJECTION_12MO.md`: blended ARPU $70/mo,
Stripe 2.9%+$0.30): keep **CAC < ~$210** so a ~$70 ARPU user with ~12-mo retention
clears **LTV:CAC ≥ 3** and **payback ≤ 12 mo**; for Professional ($299), CAC can be
materially higher and still clear the bar — another reason A is the beachhead.

---

## 6. 90-day experiment plan (sequenced, falsifiable)

**Days 0–30 — Instrument & seed (prove the rails + first signal):**
- Stand up analytics + A/B (PostHog), CRM (HubSpot Free/Attio), email (Resend/SES) —
  the $0–150/mo stack.
- Ship **one lead magnet for Segment A** (deal/score analyzer or "SMB acquisition
  checklist") + a segment-routing question on capture.
- Publish **3–5 cornerstone SEO/MDX articles** (e.g., "SBA DSCR explained," "How to
  read SMB add-backs," "Cross-asset comparison, honestly").
- Founder: 5–10 LinkedIn posts + active participation in 2–3 ETA/search-fund
  communities. **Goal: first 100–250 qualified leads, ≥1 nurture sequence live.**

**Days 31–60 — Convert & learn:**
- Turn on guided trial + paywall-at-aha; launch the 5–7 email nurture.
- A/B test headline + magnet + pricing order. Add 1–2 niche newsletter/podcast
  sponsorships **with promo codes** (measurable CAC).
- **Goal: validate lead→trial ≥ 30% and first paying cohort; compute first real CAC.**

**Days 61–90 — Double down / kill:**
- Keep the **two** best-performing channels by payback; cut the rest.
- Add **retargeting** on warm visitors; launch **referral** loop.
- Founder-led outreach to 5–10 Enterprise/family-office prospects for pilots.
- **Goal: LTV:CAC ≥ 3 on the lead channel; documented re-forecast.**

---

## 7. Measurement, KPIs & kill-rules (how we know it works)

**North-star:** *qualified-lead → paid* conversion at a **payback ≤ 12 months**.

| Funnel stage | KPI | Early target |
| --- | --- | --- |
| Awareness | organic clicks, post engagement, community mentions | growth WoW |
| Acquisition | visitor→lead %, lead quality by segment | ≥ 20–25% on intent pages |
| Activation | trial starts, time-to-first-value | aha < 10 min |
| Conversion | trial→paid %, by segment | B ≥ 15–20%, A ≥ 25–30% |
| Revenue | ARPU, MRR, annual mix | ARPU ≥ $70 blended |
| Retention | churn, NRR by segment | NRR ≥ 100% for A/C |
| Efficiency | **CAC, LTV:CAC, payback** by channel | LTV:CAC ≥ 3, payback ≤ 12 mo |
| Virality | referral k-factor | trending up |

**Kill-rules (pre-commit to discipline):**
- Any **cold paid** channel with CAC payback > 12 mo after a defined test budget → **stop**.
- Any magnet with visitor→lead < 10% after 1k visitors → **replace**.
- Any segment with trial→paid < half its target after 50 trials → **re-message or deprioritize**.
- Re-forecast **monthly** with real ARPU/churn/CAC (the projection script supports this).

---

## 8. Budget envelope (stays inside the lean plan)

| Item | Monthly (MVP) | Notes |
| --- | --- | --- |
| Analytics + A/B (PostHog) | $0 | generous free tier |
| CRM (HubSpot Free / Attio) | $0–low | |
| Email (Resend / SES) | $0–20 | transactional + nurture |
| Scheduling (Cal.com) | $0 | demos |
| **Organic tools subtotal** | **$0–150** | matches `GTM_FUNNELS_NEXTJS.md` |
| Niche sponsorship (test) | $200–1,000 | only with promo-code tracking |
| Retargeting ads (warm) | $100–500 | only after organic signal |
| Cold ads (Tier 3) | budgeted experiment | only after CAC/LTV proven |

The whole Phase-Two GTM can start for **effectively the cost of the existing lean stack
plus the founder's time**, with paid spend gated behind proof.

---

## 9. Risks, anomalies & honest caveats

- **Unproven score (H5 FAIL):** do **not** market performance/alpha. Sell discipline,
  unification, and the acquisition workflow. Re-message instantly if any copy implies
  returns.
- **Prototype features:** several modules are Partial/Prototype
  (`SERVICES_PRICING_FIT_ANALYSIS.md`). **Don't gate paid tiers on what isn't built;**
  market what's delivered, use "founding member" framing for the rest.
- **Regulatory:** advice/RIA line is real. Keep disclaimers; resolve positioning before
  scaling paid acquisition.
- **Single-founder bandwidth:** the plan leans on founder-led organic + AI agents
  (support) to stay lean; protect founder time for the two channels that work.
- **Expectation mismatch from cold ads:** highest churn + worst fit comes from broad
  paid social — another reason it's Tier 3.

---

## 10. Bottom line (the bet)

> **Beachhead on Segment A (acquirers/advisors, Professional $299) with authority
> content + a free analyzer + guided trial on our own Next.js funnel; use Segment B
> retail as an organic flywheel; pursue Segment C via founder/referral sales. Prove
> LTV:CAC ≥ 3 organically before spending on cold ads. Treat the first 90 days as a
> falsifiable experiment (PT-H1/H2/H3) and let the metrics — not enthusiasm — decide
> where capital goes.**

This is the **highest-probability path to high-conversion, targeted demand** given our
real product status, lean budget, and honesty constraints — and it doubles as the
Research Phase Two segment: every tactic returns a measurable result that confirms or
rejects the demand, conversion, and segment-fit hypotheses.
