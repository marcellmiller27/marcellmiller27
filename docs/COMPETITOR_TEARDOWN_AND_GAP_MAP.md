# Competitor Teardown, Moat & Gap Map — Reverse-Engineering the Institutional Research Platforms

> JHI-SIG: 69M2705M · Strategy / analysis document. No UI code. Prepared to align on
> direction **before** we rebuild the platform + mobile app. Companion to
> `docs/BRAND_AND_COLOR_SYSTEM.md`, `docs/MARKETING_STRATEGY_CAMPAIGN.md`, and
> `docs/FINANCIAL_DILIGENCE_SUITE_CONCEPT.md`.

## 0. Why reverse-engineer
As a new-to-market challenger, we let incumbents spend hundreds of millions proving what
works, then we **copy the revenue mechanics** and **attack the pain points they leave open.**
Two rules throughout this doc:

1. **Separate mechanics from aesthetics.** Their *funnel, workflow lock-in, and validated
   outputs* drive revenue — not the color palette. Copy mechanics; let design serve them.
2. **Compete where we can win.** We cannot out-data PitchBook. We win on **integration
   (end-to-end), price, the underserved SMB/search-fund niche, and radical transparency.**

---

## 1. The reverse-engineering method (repeatable, not vibes)
For each competitor we score on a 1–5 rubric across seven lenses, then build the gap map.

| Lens | What we extract |
|---|---|
| 1. Positioning / ICP | Who they serve; the one-line promise |
| 2. Information architecture | Nav model, # of top-level areas, screen→screen flow |
| 3. Visual system | Canvas, dominant color, accent, typography, density |
| 4. **Plumbing** (data + formulas + tools + outputs) | Where data comes from, what models compute, what deliverables ship |
| 5. Moat | Why it's defensible (data, workflow, brand, switching cost) |
| 6. Validation / "stress-test" strategy | How they earn trust in their numbers + how they optimize conversion |
| 7. Pricing & packaging | Tiers, transparency, per-seat vs. flat |

**How to gather it (execution):** trial/demo each product; screen-record the first-run funnel + pricing gate; mine G2 / Reddit / search-fund forums for churn reasons; read published methodology PDFs. This doc is v1 from public research; a live-trial pass will deepen it.

---

## 2. Scorecard (1 = weak, 5 = strong)

| Platform | ICP fit (searcher/SMB) | IA | Visual | Plumbing | Moat | Validation | Price accessibility |
|---|---|---|---|---|---|---|---|
| PitchBook | 3 | 4 | 4 | 5 | 5 | 4 | 1 |
| S&P Capital IQ | 2 | 4 | 3 | 5 | 5 | 4 | 1 |
| Preqin | 2 | 4 | 4 | 4 | 4 | 3 | 2 |
| Grata / SourceScrub | 4 | 4 | 4 | 3 | 3 | 2 | 2 |
| Seeking Alpha | 2 | 3 | 3 | 3 | 3 | 3 | 5 |
| Morningstar | 3 | 4 | 4 | 5 | 4 | 5 | 4 |
| AlphaSense | 3 | 4 | 4 | 4 | 4 | 3 | 1 |
| **JHI (today)** | **5** | **2** | **2** | **2** | **2** | **3** | **5** |

**Read:** JHI already wins on **ICP fit** (end-to-end for searchers) and **price**, and is honest on **validation** (we disclose H5 FAIL — most competitors never publish a t-stat). We are behind on **IA, visual polish, plumbing depth, and moat.** The plan in §8 attacks exactly those.

---

## 3. Per-competitor teardown

### PitchBook (Morningstar) — the data king
- **ICP:** VC/PE/IB/corp-dev; $5M+ EBITDA buyers. **Promise:** the comprehensive private-market database.
- **Plumbing:** 25 discrete datasets; **VC Exit Predictor** — an ML classification model trained on ~46,000 known-outcome startups, tested on ~11,000 out-of-sample, ~**75% accuracy**, outputs an "opportunity score" percentile + exit-path probabilities (requires ≥2 VC rounds). Excel/PowerPoint/Chrome plugins; desktop + mobile.
- **Moat:** a genuine **data network effect** — 1M+ web crawlers + NLP/ML + **1,800+ human researchers** + 100+ proprietary QA processes + primary-source calls (10M+ research hours in 5 yrs). Morningstar itself frames this as an intangible-asset moat with high barriers to entry.
- **Validation/stress strategy:** publishes out-of-sample accuracy; human-in-the-loop QA (preventative + corrective validation); explicitly says the model **is not a substitute for diligence** and **omits financials/business model** — a documented gap.
- **Pricing:** opaque, $12–30k/seat, +$7k/extra seat, enterprise $70–125k+. Annual lock-in.
- **Pain points we exploit:** price, per-seat gouging, opaque pricing, steep learning curve, thin sub-$5M SMB coverage, exit predictor ignores financials/QoE.

### S&P Capital IQ Pro — the financial-breadth king
- **ICP:** IB / public-markets / credit. **Plumbing:** ~60M private companies, deep financials, credit data, ChatIQ conversational analysis. **Moat:** data breadth + S&P brand + workflow lock-in. **Price:** $25–100k+/seat. **Pain:** cost, complexity, overkill for SMB buyers.

### Preqin (BlackRock) — the alternatives/fund-data specialist
- **ICP:** LPs/GPs, fund benchmarking. **Plumbing:** fund performance, LP/GP relationships, alt-asset benchmarks; being integrated with Aladdin/eFront. **Moat:** fund-return dataset + BlackRock distribution. **Price (published!):** $2.1k single-asset → $6.7k enterprise — the most **transparent** pricing of the group. **Visual (your screenshot):** light canvas, deep-indigo header, magenta accent link, "a part of BlackRock" trust endorsement, airy sections. **Pain:** not deal-level SMB; institutional-only.

### Grata / SourceScrub (Datasite) — the AI sourcing challengers
- **ICP:** independent sponsors, search funds, thematic PE. **Plumbing:** AI reads company websites like an analyst; thesis-to-target similarity search over ~19M private companies; verified founder/owner contacts; intent signals (hiring, growth). **Moat:** AI search maturity + contact data (weaker/newer than PitchBook's). **Validation:** thin/none published. **Price:** custom, ~$15–40k/seat. **Pain (our biggest opening):** **stops at sourcing** — no QoE, no financial diligence, no close workflow. Searchers still bolt on Excel + a CPA + a data room.

### Seeking Alpha — the accessible retail model
- **ICP:** self-directed retail equity investors. **Plumbing:** crowd + quant "Quant Ratings," factor grades (value/growth/momentum/profitability/revisions). **Moat:** community + content flywheel + SEO. **Validation:** publishes quant-rating performance. **Price:** ~$300/yr (the accessibility benchmark). **Pain:** public equities only; no private/SMB/diligence. **Lesson:** proves a **low-price, content-led** model can scale — our retail flywheel template.

### Morningstar — the transparency/methodology king
- **Plumbing:** **quantitative star rating** = gradient-boosted regression (300 trees, **61 input variables** across growth/liquidity/financial-health/profitability); quantitative fair value = 1/EXP(log PFV); star rating from valuation-vs-price + uncertainty + market cap + momentum; **±5% buffering** for rating stability; recomputed daily. **Moat:** brand trust + methodology transparency (published PDFs) + analyst+quant hybrid. **Lesson:** **published, buffered, out-of-sample methodology = trust.** This is the model to emulate for our scores.

### AlphaSense — the AI-search specialist
- **ICP:** analysts. **Plumbing:** AI/NLP search across filings, transcripts, broker research, expert-call library; sentiment. **Moat:** licensed content library + AI relevance. **Price:** enterprise, ~$10k+/seat. **Pain:** search/insight, not diligence/valuation.

---

## 4. The "plumbing" — what to learn (formulas → tools → outputs)
Reverse-engineered pattern across the leaders:

1. **A named, defensible score** (PitchBook "opportunity score", Morningstar "star rating", SA "quant grade"). Users anchor on it.
2. **A published methodology** with a real model (gradient boosting / classification), a defined **input-factor set**, and **out-of-sample accuracy**.
3. **Stability engineering** (Morningstar's ±5% buffering) so the score doesn't flicker — trust through consistency.
4. **Workflow outputs** that leave the platform: Excel/PPT/PDF exports, CRM sync, screeners, comps. This is the retention lock-in.

**Direct implications for JHI's plumbing (our scores):**
- We already have named scores (Opportunity Score, Deal Score, Financial Integrity Score) and a **validation harness with pre-registered bars** — more rigorous *disclosure* than most incumbents. Our gap is **depth of inputs** (price-only vs. their 61-factor fundamentals) and **coverage** (equities only in the live score).
- Emulate: (a) add fundamentals once SF1 is licensed; (b) add **score-stability buffering**; (c) ship **Excel/PDF exports** as a retention hook; (d) keep publishing IC/t-stats — **out-transparent** the incumbents (most never publish a t-stat; we do).

---

## 5. Their moats — copyable vs. not
| Moat | Who | Copyable by JHI? |
|---|---|---|
| Proprietary data network effect (crawlers + 1,800 researchers) | PitchBook, Capital IQ | **No** — don't try to out-data them |
| Fund-return / LP-GP dataset | Preqin | No |
| Brand + methodology trust | Morningstar | **Yes, partially** — via published, buffered, validated methodology + transparency |
| Workflow lock-in (Excel/CRM/exports, daily-tool habit) | All | **Yes** — build exports + a daily-use surface |
| Community/content flywheel + SEO | Seeking Alpha | **Yes** — our retail content engine (per marketing strategy) |
| **End-to-end integration (source→research→QoE→close)** | *Nobody* | **This is OUR moat to build** |
| Price accessibility for the underserved searcher | *Nobody at quality* | **Ours** |

**Conclusion:** our defensible position is **integration + niche + price + transparency**, reinforced over time by our own outcome data (labeled deals) — a *small* data network effect in the SMB/search-fund corner the giants ignore.

---

## 6. Their "stress-test" strategy (two meanings, both matter)
- **Model/data validation (trust):** out-of-sample accuracy claims (PitchBook 75%), published methodology (Morningstar), rating-stability buffering, human QA. **Our edge:** we already publish pre-registered IC/t-stat bars and disclose FAILs — we should make *radical validation transparency* a marketed feature.
- **Conversion/GTM testing (revenue):** free trials (PitchBook trial gating), demo funnels, published transparent pricing (Preqin), low-price content funnel (Seeking Alpha). **Our plan:** A/B-tested landing pages, a free/low Consumer trial, "Book a demo" for Enterprise, and a content flywheel (per `MARKETING_STRATEGY_CAMPAIGN.md`).

---

## 7. Gap map → JHI's wedge
| Pain point in the market | JHI answer |
|---|---|
| Fragmentation (5–8 tools stitched together) | **One platform:** source → research → QoE → close |
| Cost ($15–100k/seat) | Consumer $50 / Professional $299 / Enterprise $1,500+ |
| Sourcing tools stop before diligence | Deal X-Ray + CPA-signed QoE built in |
| Thin sub-$5M SMB coverage | SMB/search-fund is our beachhead, not an afterthought |
| Opaque scores, no t-stats | Published, validated, transparent methodology |
| Institutional-only, intimidating | Educational, approachable, compliance-safe framing |

---

## 8. Execution plan — the new platform + mobile (design decisions locked in this thread)
Analysis/design agreed: **light institutional web product**, **premium marketing surface**, **progressive density**, **sans typography (serif only for exported reports)**, **one anchor color (navy) with disciplined gold/emerald accents**. Phased so we ship value continuously and can react.

### Workstream A — Visual system (design tokens)
Institutional light theme (the reverted draft's exact plan, preserved here so nothing is lost):
- Canvas `#f5f7fb`; cards `#ffffff`; borders `rgba(15,39,68,0.12)`; ink `#0c1f33`; muted `#5a6b7d`.
- Anchor **navy** (from logo/trust); **trust-blue** `#1f5fe0` for links; **emerald** `#0f9d63` reserved for the single primary CTA; **bronze-gold** `#9a6b12` for labels/premium only.
- Keep the **mobile device mock dark** (scoped tokens) as a sleek phone app.
- Sans (Inter) across UI; optional serif reserved for exported PDF research notes only.

### Workstream B — Information architecture
Replace the flat 12-item nav with grouped areas: **Overview · Research · Acquisitions · Portfolio · Account** (resolves the Deal X-Ray / Diligence Suite / Due Diligence overlap → Deal X-Ray, Quality of Earnings, Document Review under Acquisitions). Rename SMB "Opportunity Score" → **"Deal Score"** to end the collision with the markets Opportunity Score.

### Workstream C — Density & workflow lock-in
Progressive density: airy overviews → dense, filterable, **exportable** analysis screens (Excel/PDF). Exports are the retention hook the incumbents all use.

### Workstream D — Marketing funnel (revenue mechanics, not just look)
Premium marketing surface with a real funnel: free/low Consumer trial, "Book a demo" for Enterprise, social proof (SF1/NASDAQ data, CPA-partner network, sample reports), transparent pricing (mirror Preqin's transparency as a differentiator).

### Workstream E — Plumbing / score credibility
Add fundamentals once SF1 licensed; add score-stability buffering; keep publishing IC/t-stats; surface a "methodology & validation" page (out-transparent the incumbents).

### Workstream F — Mobile parity
Bring the new IA + institutional (dark app) styling to `/mobile`; ensure every module (incl. Deal Score, QoE) is reachable and does real work, not just viewing.

### Phasing
- **Phase 1 (design foundation):** tokens + typography + grouped nav + rename Deal Score. Reversible, low-risk, high visual impact.
- **Phase 2 (density + exports):** table-first analysis screens + Excel/PDF export.
- **Phase 3 (marketing funnel):** landing pages, trial/demo, pricing transparency, proof.
- **Phase 4 (plumbing):** fundamentals + buffering + public methodology page.
- **Phase 5 (mobile):** parity pass.

Each phase ships behind review with before/after evidence; nothing goes irreversible without your sign-off.

---

## 9. What we should NOT do
- Don't try to match their **data breadth** — it's a 10M-research-hour moat.
- Don't cargo-cult the **look** without the **funnel** — pretty ≠ converting.
- Don't overclaim scores — our transparency is a feature; keep disclosing limits.

## 10. Open decisions for you
1. Confirm **navy as the single anchor** color (vs. keeping the trio).
2. Confirm **light web / dark mobile** split.
3. Approve the **phasing** (start with Phase 1 design foundation?).
4. Green-light a **live-trial teardown pass** (I sign up/demo each to deepen §3 and mine real churn reasons) and the 40–50 company matrix.
