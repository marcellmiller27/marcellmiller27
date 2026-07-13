# Market-Data Vendor Comparison & Decision Memo

**Prepared for:** JHI Research & Analytics Firm, Inc. — Board / Founder
**Purpose:** Decide whether (and when) to fund a licensed market-data partnership,
and which vendor best serves JHI's objectives. Companion to
`docs/FUNDAMENTALS_DATA_VENDORS.md` (point-in-time fundamentals / SF1) and
`docs/STRATEGIC_ROADMAP.md` (data-sourcing life cycle).

> **Procurement status (updated 2026-07-13).** Founder submitted a request to the
> **Twelve Data sales team** re: **Enterprise base usage / external-distribution
> terms**. **AWAITING TWELVE DATA RESPONSE.** See §4a for the questions to nail down
> in writing before committing.

> **One-line takeaway.** For JHI's SaaS, the headline "retail" price of every vendor
> is a trap: those tiers are **personal / internal-use only**. The right of a SaaS
> to *show data to paying subscribers* (external display) or *feed it to them*
> (external distribution) lives on a **business / commercial / enterprise** tier
> every time. Budget for that tier, not the sticker price.

---

## 1. Why this matters to JHI (objectives, not features)

The platform today runs its live market surface on **free, unofficial** sources —
Yahoo (scraped via failover hosts in `backend/app/market_services.py`), CoinGecko
(crypto), and BLS + FRED (macro). That is correct for a prototype. A paid
partnership advances four specific JHI objectives:

1. **Legal right to serve data to subscribers.** Free/retail data is internal-use
   only; a redistribution/display license is what makes a paid SaaS *lawful*. Same
   lesson as the NASDAQ SF1 addendum.
2. **Reliability the tiers demand.** Enterprise ($1,500) and Professional ($299)
   subscribers expect real-time, broad, SLA-backed data — not a scraped endpoint
   that can break without notice.
3. **Research integrity.** Clean, adjusted, survivorship-bias-free, point-in-time
   data is what lets an H5 "PASS" survive a skeptical reviewer.
4. **Competitive parity.** PitchBook, Capital IQ, Preqin, Grata, and Seeking Alpha
   all run on licensed feeds; its absence is a disqualifier under the hood.

### What JHI actually needs from a market-data vendor
- **Redistribution / external-display rights** for a client-facing SaaS (non-negotiable).
- **Cross-asset breadth** — equities, ETFs, FX, crypto, indices (the Opportunity
  Score's differentiator is *cross-asset* comparison).
- **Reliability / SLA** and a real support relationship.
- **Fundamentals** (nice-to-have overlap with the SF1 track and Deal X-Ray).
- **Cost that scales from bootstrap → growth** and stays behind revenue.

---

## 2. Side-by-side comparison

Pricing verified from public pages **as of mid-2026**; treat as directional and
**re-confirm at contract** (all vendors revise tiers). The decisive row is
**Redistribution / commercial**, not price.

| Dimension | **Twelve Data** | **Polygon.io** (now "Massive") | **Finnhub** | **EODHD** |
|---|---|---|---|---|
| **Best at** | Broad multi-asset quotes + fundamentals, easy integration | Tick/quote data, options (OPRA), full tape, deep history | Global fundamentals, estimates, transcripts, news/sentiment | Cheapest all-in-one EOD + global fundamentals |
| **Asset coverage** | Stocks, ETFs, FX, crypto, indices, fixed income, mutual-fund NAV; 70–84 markets | US + global stocks, options, indices, FX, crypto, futures | US + global equities, FX, crypto, ETFs, fundamentals | Global EOD equities/ETFs/funds, intraday, FX, crypto, fundamentals |
| **Real-time** | Real-time US/EU on business tiers | Real-time on Advanced/business | Real-time quotes (segmented) | Intraday (delayed feel); EOD focus |
| **Retail / self-serve price** (personal/internal only) | Individual: Basic $0, Grow $79, Pro $229, Ultra $999 | Basic $0 (EOD), Starter $29 (delayed), Developer $79, Advanced $199 (real-time) | Free $0; data-type plans ~$50–$200/mo per market; All-In-One ~$3,500/mo | Free $0; EOD $19.99, EOD+Intraday $29.99, Fundamentals $59.99, All-In-One $99.99 |
| **Commercial / redistribution tier** | **Business** plans: Venture **$499/mo** (external *display*), Enterprise **$1,099/mo** (external *distribution*, 99.99% SLA), Enterprise+ custom (white-label, SOC 2/ISO). Redistribution needs a **Business plan + Redistribution Rights Add-On**. | **Business/Enterprise contract** (custom, contact sales). Retail ToS **explicitly prohibits** redistribution/display/derived works to third parties. | **Enterprise** only: "Commercial use. Redistribution right." Flexible/custom pricing, contact sales. Self-serve plans are **personal use**. | **Separate commercial license** (request quote; onboarding in ~3 business days). Self-serve plans are **personal use**. |
| **Redistribution clarity** | Clear tiered model; add-on + compliance team assist | Clear prohibition on retail; business is contract-gated | Docs less explicit; needs early sales clarification | Very clear personal-vs-commercial split |
| **SLA (business)** | 99.95% (Venture) → 99.99% (Enterprise) | Exchange-colocated infra; contract SLA | Enterprise-defined | Commercially reasonable |
| **Fundamentals depth** | Good | Limited (price/tape focus) | **Excellent** (30+ yrs, as-reported, estimates, transcripts, ownership) | **Very good** (global, 30+ yrs) |
| **JHI integration status** | **Already wired** (`TWELVEDATA_API_KEY`, primary-with-Yahoo-fallback) | Not wired (adapter needed) | Not wired | Not wired |
| **Effective cost to JHI (redistribution)** | **~$499–$1,099/mo** self-serve | **Custom** (typically $$$; sales-gated) | **Custom** (Enterprise) | **Custom** (commercial quote; likely lowest) |

### Key cross-cutting insight
Every vendor's advertised low price is **personal/internal use only**. For a SaaS
that shows data to subscribers, the *real* options are:
- **Twelve Data** — the only one with a **transparent, self-serve commercial price**
  ($499 display / $1,099 distribution), **and it's already integrated**.
- **Polygon/Finnhub/EODHD** — all require a **sales conversation and custom quote**
  for redistribution (no public self-serve commercial price).

---

## 3. Recommendation (tied to launch gates & bootstrapped posture)

**Do not buy market-data redistribution today.** The value only materializes at
paid launch or when a validated score is ready to publish. Sequence it:

- **Now (R&D / pre-launch):** keep free sources (Yahoo, CoinGecko, FRED, BLS) and
  focus data spend on **SF1 fundamentals for H5** (see `FUNDAMENTALS_DATA_VENDORS.md`).
  Market-data redistribution buys nothing until there are subscribers.
- **At paid launch (primary pick): Twelve Data Enterprise ($1,099/mo; ~$916/mo with 17% annual billing ≈ ~$11k/yr).**
  - Rationale: Enterprise is the tier that grants **external *distribution* market
    data** + **analysis data** (all markets, ETF metrics, **99.99% SLA**, integration
    support, Slack Connect). This is the right fit because **JHI's Opportunity Score
    is a *derived work*** served across subscribers — that is distribution, not mere
    display — and the 99.99% SLA matches the Enterprise ($1,500) client tier's
    expectations.
  - **Already wired:** drop `TWELVEDATA_API_KEY` into Secrets → live (compose
    pass-through in place, Yahoo as automatic fallback). Lowest time-to-value and,
    critically, a **single transparent commercial price** — no sales-gated quote.
  - **Possible cost saver — Venture ($499/mo):** covers **external *display*** only
    ("client-facing apps/websites"). This may suffice **if JHI renders raw quotes
    in-app only** and does not distribute a derived score/feed or expose its own
    data API to clients. **Get Twelve Data compliance to confirm in writing** which
    tier your exact usage (derived score to logged-in subscribers) requires before
    committing — err toward Enterprise when a derived work is involved.
- **Keep as documented alternates (adapter-ready, not bought):**
  - **Polygon/Massive** — if JHI ever needs **tick/quote data or options** (Deal
    X-Ray / advanced analytics). Best raw "data infrastructure."
  - **Finnhub Enterprise** — if the **fundamentals/estimates/transcripts** side
    (Deal X-Ray, Financial Diligence Suite) needs more than SF1 provides.
  - **EODHD** — likely the **lowest-cost commercial** path for global EOD +
    fundamentals if budget is the binding constraint.

**Bottom line:** the payoff of a market-data partnership is **legal redistribution
+ reliability + research integrity**, not "more numbers." It's a **launch-gate
investment**, and **Twelve Data is the lowest-friction first move** because JHI
already built the integration.

---

## 4. "Pull-the-trigger" checklist (apply to any vendor, every time)

- [ ] **Redistribution / external-display right is explicit and in writing** for a
      client-facing SaaS (the whole point — mirror the NASDAQ addendum discipline).
- [ ] Scope confirmed: **display vs distribution vs non-display / derived works**
      (indexes, scores). JHI's Opportunity Score is a **derived work** — confirm it's permitted.
- [ ] **Exchange fees / professional-vs-nonprofessional** subscriber reporting
      obligations understood (some vendors must report commercial users to exchanges).
- [ ] **Real-time vs delayed** matches the tier's promise to subscribers.
- [ ] **SLA, rate limits, and caching/storage rights** adequate (JHI caches ~60s).
- [ ] **Attribution** requirements known and satisfiable in the UI.
- [ ] **Term, renewal, price-escalation, and termination-delete** clauses reviewed.
- [ ] **Cost maps to revenue** — a data plan should be covered by a small number of
      retained Professional/Enterprise seats before committing.
- [ ] Counsel review for any custom/enterprise contract.

### 4a. Twelve Data Enterprise — questions for the sales/compliance team (in writing)

Nail these down before signing (mirror the NASDAQ addendum discipline):

1. **Distribution vs display.** Confirm that serving JHI's **Opportunity Score
   (a derived work) to logged-in subscribers** falls under Enterprise's **external
   distribution** grant — and whether Venture's external *display* would ever
   suffice for our exact usage. Get the classification in writing.
2. **Derived / non-display use.** Confirm we may **compute, store, and serve
   analytics/scores derived from** the data (indexes/scores can be treated as
   "non-display use" in some licenses). Enterprise lists "Analysis data" — confirm
   that covers a derived score product.
3. **End-user / subscriber cap.** Is Enterprise **unlimited end-users**, or capped?
   (NASDAQ's was "up to 1,000 clients" — get the number, if any.)
4. **Exchange fees & pro/non-pro reporting.** Any **per-subscriber exchange fees**
   on top of $1,099, and must JHI **report subscribers** as professional/
   non-professional to exchanges? Which markets trigger extra approval?
5. **Real-time entitlements.** Which markets are **real-time vs delayed** at
   Enterprise; is **real-time US equities** included at no add-on?
6. **Caching / storage rights.** JHI caches ~60s and stores history for scoring —
   confirm permitted, and any retention/redisplay limits.
7. **Attribution.** Exact attribution text/placement required in the UI.
8. **Credits / rate limits.** Confirm Enterprise credit allotment covers JHI's
   polling cadence (UI 15s → backend 60s cache) across the symbols we serve.
9. **Commercials.** Confirm **17% annual-billing discount** (~$916/mo), term,
   renewal, **price-escalation** cap, and **termination / delete-on-termination**
   obligations.
10. **Evaluation.** Ask for a short **paid trial or eval** to validate data quality
    end-to-end against the (already-built) integration before committing.

---

## 5. How activation works in the platform (no rebuild of logic needed)

- The backend already treats **Twelve Data** as the licensed primary source with
  Yahoo fallback (`market_services.py: twelvedata_quote`, gated on
  `TWELVEDATA_API_KEY`). `providers()` reports it `live` once the key is set.
- `docker-compose.yml` now **forwards** `TWELVEDATA_API_KEY` (and the other data
  keys) from the VM/Secrets into the backend container. So activation is literally:
  **add the key to Secrets → it flows to the backend**.
- Adopting Polygon/Finnhub/EODHD instead would require a **new adapter** (a
  `*_quote()` function + provider entry), not a rewrite.

---

## 6. Sources (public, mid-2026 — re-verify at contract)

- Twelve Data pricing & business/redistribution terms — twelvedata.com/pricing,
  /pricing-business, support.twelvedata.com (commercial & US-equities articles).
- Polygon.io / Massive pricing & Market Data ToS — polygon.io/pricing, massive.com
  (rebrand blog + market_data_terms).
- Finnhub pricing & enterprise redistribution — finnhub.io/pricing,
  /pricing-startups-and-enterprise.
- EODHD pricing, terms, and commercial-license process — eodhd.com/pricing,
  /financial-apis/terms-conditions, /financial-apis/commercial-vs-personal-license-use.

---

## 7. Proposed board resolution

> *Resolved,* that JHI will continue on free/licensed-R&D data through validation
> (H5) and, upon approaching paid launch, activate **Twelve Data Enterprise
> ($1,099/mo)** — which grants **external distribution** of market data plus
> analysis-data rights and a 99.99% SLA — as the primary licensed market-data
> vendor (stepping down to **Venture ($499/mo)** only if Twelve Data compliance
> confirms in writing that JHI's usage qualifies as external *display* only);
> retaining Polygon/Massive, Finnhub, and EODHD as pre-vetted alternates for
> tick/options, fundamentals depth, and low-cost EOD respectively; and that no
> market-data redistribution spend be committed until the redistribution right is
> secured in writing and the cost is covered by subscriber revenue.
