# Competitor Audit — 42 Macro (42macro.com)

> JHI-SIG: 69M2705M · JHI Research & Analytics Firm, Inc. (proprietary)
> Deep-dive audit to inform the JHI **Editorial module** (VP of Editorial). Focus per
> Founder: writing methods, financial-market detail, visual aids, opportunities & pain
> points. Sources: 42macro.com (research, education, product, FAQ, investment-process,
> "The Playbook"), and a Founder-supplied "The Weekly" email sample. Not affiliated.

## 0. Executive summary
42 Macro (founder **Darius Dale**) is the benchmark for **process-driven macro research as a
subscription product**. Its edge is not "better predictions" — it's a **repeatable, named,
teachable system** (regimes + signals + model portfolio) delivered on a **cadence-tiered**
schedule, wrapped in **heavy data-visualization** and an **education moat**, and fed by a
**free weekly newsletter funnel** ("The Weekly"). That combination — *system + visuals +
education + free→paid funnel* — is exactly the blueprint our Editorial module should mirror
(institutional voice), then differentiate on **JHI's integrated company/deal depth**, which
42 Macro does not have.

**What to take:** the writing method (process-first, probabilistic, disclosed jargon),
the visual-aid catalog (regime quadrant, heat maps, scatter plots, dashboards), and the
free-newsletter → paid funnel mechanics. **Where we win:** 42 Macro is *top-down macro only*
— no bottom-up companies, transactions, or diligence. JHI fuses macro **with** the entity
graph (companies/deals) and diligence tools; nobody else pairs the two.

---

## 1. Positioning & business model
- **Tagline:** "Global Wall Street's leader in macro risk management." Sells **actionable risk-management signals + data-driven insight**, explicitly "hedge-fund-caliber… now accessible" (anchors against the ~$50k/yr institutional price to justify retail pricing).
- **Model:** pure **research subscription** (SaaS-like: reports + a client **Signals dashboard** + community + AI research library + education). No advice/management — same software-publisher posture as JHI.
- **Cadence-tiered products** (depth is *inversely* correlated with frequency):
  - **Leadoff Morning Note** — daily; high-touch read of the data/flows (1–3 month horizon).
  - **Around the Horn** — weekly (Sat); regime + KISS/Dr. Mo updates (1–3 quarter horizon).
  - **Macro Scouting Report** — monthly; deepest deep-dive (1–3 year horizon).
- **Pricing (2026):** Macro Risk Manager **$95/mo** (weekly), Macro Strategist Pro **$195/mo** (daily+weekly+monthly). Quarterly discount; "cancel anytime" emphasized.
- **Free funnel:** **"The Weekly"** email + public blog/"Explore Insights" + YouTube/podcast appearances → capture email → convert to paid.

**Takeaway for JHI:** our Tier 1–3 already mirrors the depth-tiering logic. 42 Macro proves the **free newsletter is the top of the funnel**, and that **cadence × depth** is a clean way to justify price tiers — directly reusable for the Editorial module funnel.

---

## 2. Writing methodology (the parts to integrate)
42 Macro's writing is distinctive and disciplined. The transferable methods:

1. **Process-first, not prediction-first.** Every piece is framed as the output of a **named, repeatable system**, not a pundit's opinion. Reader trusts the *machine*, not the mood.
2. **Probabilistic, full-distribution framing.** "Highest-probability scenario," "moderate risk of a RORO phase transition," conditional probabilities, ranges — never false certainty. They explicitly research the *full distribution of outcomes, bullish or bearish*.
3. **Consistent skeleton every edition.** The same six lenses recur: **Growth · Inflation · Monetary Policy · Fiscal Policy · Liquidity · Positioning.** Readers learn the structure once and navigate every issue instantly.
4. **Named, proprietary vocabulary — but disclosed.** GRID, VAMS, KISS, Dr. Mo, CACRI, "Four Horsemen," Probable Range. Jargon builds a moat *and* is fully defined in a public **Playbook/glossary** (education = trust + conversion). (This is JHI's **Core Rule** — name + disclosed definition — done at scale.)
5. **Provocative, question-led headlines.** The Weekly sample: *"Are Consensus Expectations Too Optimistic?"* → curiosity + a thesis. Then a warm "Welcome to The Weekly!" and an enumerated risk list ("The first is… The second is…").
6. **Always actionable + risk-managed.** Every view resolves to *what to do* (overweight/underweight, position sizing, when to book gains) — signals, not just narrative.
7. **Contrarian vs. consensus, explicitly.** They position their call *against* "consensus" and social-media noise, giving the reader a reason to pay for an edge.

---

## 3. Financial-market detail & analytical depth (their engine)
The depth that makes it credible — a layered system:

- **GRID regimes** — 2×2 of growth × inflation deltas → **GOLDILOCKS / REFLATION / INFLATION / DEFLATION** (risk-on vs risk-off). The backbone; tells you *where/how much* to allocate.
- **Bottom-Up Macro Regime** — computed from 3-mo deltas of the **OECD Composite Leading Index** (growth) and **Headline CPI YoY** (inflation), with **conditional probabilities** from two models (mean-reversion + agent-based nowcast).
- **Macro Weather Model** — nowcasts 6 principal components (Growth, Inflation, Monetary, Fiscal, Liquidity, Positioning) → **3-month asset outlook** (stocks/bonds/USD/commodities/BTC). Includes a proprietary **Net Liquidity** model (Fed balance sheet − TGA − RRP).
- **VAMS (Volatility-Adjusted Momentum Signal)** — the momentum engine (bearish/neutral/bullish scoring).
- **Global Macro Risk Matrix** — daily **Bayesian** intermarket process across **42 indicators / a dozen asset classes** → the **Top-Down Market Regime** (Share/Sum of Confirming Markets, Conviction Score).
- **CACRI + "Four Horsemen of Market Risk"** (VVIX/VIX, High/Low Beta, Small/Mega Cap, Value/Growth) — near-term correction-risk gauges.
- **GRID Asset Market Backtests + Risk/Reward Scatter Plots** — 25-yr regime-segmented return/vol/covariance rankings → visual reward-vs-risk maps.
- **KISS (Keep It Simple & Systematic)** model portfolio + **Dr. Mo** discretionary overlay — the outputs that turn all the above into positions (incl. crypto).

**Takeaway for JHI:** we don't need to clone this quant stack. We need the **pattern**: a *small set of named, repeatable frames* the reader sees every edition, each tied to a *signal* and a *so-what*. Our editions already have the raw material (FRED/BEA/BLS + markets); we should give it a **named JHI framing** and consistent skeleton.

---

## 4. Visual-aid catalog (what to integrate)
42 Macro is visual-first; charts *are* the product. The reusable visual types, roughly in build-difficulty order:

| Visual | What it does | JHI build difficulty |
|---|---|---|
| **Regime quadrant (2×2)** | Plot current growth×inflation state → risk-on/off at a glance | Low — high signal |
| **Signal heat map / table** | Rows = indicators, columns = state (bull/neutral/bear), color-coded | Low |
| **Indicator "cards" with trend** | Value + delta + a one-line read (we already do this) | Done |
| **Time-series charts** | The staple — indicator history with regime shading | Medium (charting lib) |
| **Risk/Reward scatter plot** | Expected return (y) vs risk (x) across assets | Medium |
| **Gauge / dial** | Single composite (e.g., "correction risk," "net liquidity") | Low–Medium |
| **Dashboard ("Signals")** | One screen of the live system state | Medium (we have a dashboard already) |
| **Hero image per edition** | A visual metaphor at the top of each newsletter (The Weekly uses one every issue) | Low — instant polish |
| **Video walkthrough (webcast)** | Darius narrates the deck; huge trust/retention driver | High (later) |

**Takeaway:** start with **regime quadrant + signal heat map + hero image** (low effort, high credibility), then add **time-series charts** and a **risk/reward scatter**. This is the single biggest visible gap between our current text editions and 42 Macro's look.

---

## 5. "The Weekly" (free newsletter) teardown — the funnel
From the Founder-supplied sample (*"Are Consensus Expectations Too Optimistic?"*):
- **Provocative question headline** (thesis + curiosity).
- **Branded hero image** ("THE WEEKLY" over a US/China chip — a visual metaphor for the issue's theme).
- **Warm open** ("Welcome to The Weekly!") then an **enumerated thesis** ("The first… the second…").
- **Teaser depth** — enough to be valuable, not the full system; the **full report is gated** (PDF/paid).
- **Reply-to a real address** (feels personal, not no-reply).

This is precisely the **free→paid conversion mechanic** the Founder envisioned for our Editorial module: free registrants get a **compelling teaser**; the **full detail + archive** sits behind Tier 1–3.

---

## 6. Opportunities to integrate (into the JHI Editorial module)
1. **Adopt the writing method:** process-first, probabilistic, consistent skeleton, disclosed vocabulary, question-led headlines, always end on a "so-what." Bake this into the VP of Editorial's templates.
2. **Name a JHI framing** (institutional, our own) so every edition reads as one system — e.g., a compact regime/climate read from the data we already poll, shown the same way each week.
3. **Ship the visual layer:** regime quadrant + signal heat map + per-edition hero image now; time-series + risk/reward scatter next. This is our biggest credibility upgrade.
4. **Cadence-tiered editions** mirror their model → maps cleanly to our tiers: a **free weekly teaser**, a **fuller weekly** (Tier 1–2), and a **deep monthly** (Tier 2–3).
5. **Build the education moat:** a public **glossary/playbook** that defines every JHI term (we already have `docs/GLOSSARY_AND_ACRONYMS.md` + the Core Rule) — doubles as SEO + conversion.
6. **Free→paid funnel mechanics:** teaser + gated full report + archive, reply-to a real inbox, provocative headlines — exactly the module the Founder specced.
7. **Video walkthroughs (later):** a narrated edition is their top retention driver; a JHI VP-of-Editorial video is a Phase-later differentiator.

---

## 7. Pain points (theirs) → where JHI wins
1. **Top-down macro ONLY.** No companies, no transactions, no diligence. **JHI's edge:** we pair macro **with** the entity graph (Companies/Firms/Advisors/Transactions) and diligence tools (Scope/Earnings/Document Review). We can write "here's the regime **and** here are the specific targets/deals it implies" — 42 Macro structurally cannot.
2. **Jargon wall / steep learning curve.** GRID/VAMS/CACRI/Dr. Mo is powerful but intimidating for Tier-3 (retail) users. **JHI:** disclosed-but-plain nomenclature (our anti-kindergarten *and* anti-jargon balance) widens the funnel.
3. **Price/among-the-highest for retail** ($95–$195/mo, macro-only). **JHI:** Tier 1 ($110 consumer) delivers macro **plus** company/deal tooling — more surface for a comparable price.
4. **No personalization / no portfolio-of-record.** It's one-to-many signals. **JHI:** records, watchlists, pipeline, portfolio — the reader's *own* context.
5. **Heavy on the founder (key-person risk).** The brand *is* Darius. **JHI:** the AI VP of Editorial (Ellery Vance) scales editorial without a single-human bottleneck (disclosed as AI, human-directed).
6. **Static PDFs/decks.** Reports are download-and-read. **JHI:** live, on-platform, data-refreshed editions with pivots into records — interactive, not a PDF.

---

## 8. Recommendations for the Editorial module (build order)
1. **Funnel first (the Founder's spec):** free email signup → **teaser** edition; gated **full** + **archive** for Tier 1–3; upgrade CTAs throughout.
2. **Writing templates:** encode the process-first / probabilistic / consistent-skeleton / question-headline method into the VP of Editorial's edition generators.
3. **Visual layer (phased):** hero image + **regime quadrant** + **signal heat map** now → time-series charts + risk/reward scatter next.
4. **JHI regime framing:** a named, disclosed "market climate" read from our polled data, shown identically each edition (mirror principle, our vocabulary).
5. **Differentiate hard:** every macro edition links to the **companies/deals** it implies (our moat) — the one thing 42 Macro can't do.
6. **Education moat:** publish the glossary/playbook; disclose every term (Core Rule).
7. **Later:** video walkthroughs; personalization from the user's records/watchlist.

**Bottom line:** 42 Macro is the model for *how to package and sell research* (system + visuals + education + funnel). We adopt the packaging discipline and the visual bar, keep our plain-but-institutional voice, and win on the **macro-×-microdepth integration** they don't have.
