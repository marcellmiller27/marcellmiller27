# JHI Editorial House Style Guide (E1)

**Owner:** Ellery Vance, VP of Editorial (AI) · **Steward:** Cy Henry (VP Software Engineering — AI)
**Signature:** `69M2705M` · **Status:** E1 (deterministic, no ML). Precedes the E2 grounded-LLM layer.

> Purpose: codify the **Ivy-league, institutional-grade voice** and the **methodology-first
> discipline** for every JHI edition (The Economic Brief · Red Alerts · Cross-Asset Opportunity
> Scan) — so quality is consistent today (rule-based) and remains the guardrail when the LLM
> drafting layer (E2) is added.

## 1. Voice & tone
- **Institutional, not retail.** Write for allocators, acquirers, CPAs, and advisors. Assume literacy in rates, inflation, valuation, and cash flow.
- **Measured and evidence-led.** State the number, then its significance. No hype, no hot takes, no exclamation points.
- **Active, precise, plain.** Prefer "policy is restrictive" over "the Fed is super hawkish." Avoid jargon-for-jargon's-sake and never use elementary/"kindergarten" phrasing.
- **Perspective, not advice.** We publish JHI's independent professional read — never a recommendation to buy/sell.

## 2. Non-negotiable rules
1. **Every figure is sourced and dated.** No number appears without a provenance trail (source + vintage). Data comes only from our services — never invented.
2. **Methodology is disclosed on every edition.** State how it was produced (deterministic thresholds), the data window, and limitations.
3. **Compliance line on every edition:** "For research and educational purposes only. Not investment, legal, tax, or accounting advice."
4. **No licensed-data spillage** (NASDAQ posture): publish only derived outputs; never redistribute raw licensed datasets.
5. **Deterministic = reproducible.** Same inputs → same edition. (Under E2, the LLM may only rephrase facts the rules produce; it may never introduce or alter figures.)

## 3. Structure (every edition)
1. **Masthead** — brand · edition line · byline (Ellery Vance, VP of Editorial).
2. **Executive read** — 2–4 sentences framing the regime (policy stance × inflation × labor/risk).
3. **Body** — sections/alerts/ideas with **figure → significance → so-what for allocators/acquirers**.
4. **Methodology & sources** — how it was generated, data window, sources, limitations.
5. **Disclosure** — the compliance line.

## 4. House lexicon (display terms)
- "Policy rate / long end," "restrictive/neutral/accommodative," "disinflation," "cost of capital," "risk appetite," "safe-haven demand," "cyclical demand risk."
- Prefer **"Economics"** (not "Macro"), **"Scope"** (Deal X-Ray), **"Earnings/QoE"** — consistent with the platform nomenclature (two-layer: display vs. internal ids; Title Case for headings).

## 5. Numbers & formatting
- Percentages to two decimals (e.g., 3.10%); indices to one; large USD abbreviated (T/B/M).
- Always attach the unit and the "as of" date. Use "—" for an awaited release (never 0 or blank).
- Cite the issuing body (FRED · U.S. BLS · BEA · market feeds).

## 6. Methodology disclosure (standard block — used verbatim by the engine)
> *Methodology: This edition is generated deterministically from JHI's polled public-data feeds
> (Federal Reserve/FRED · U.S. Bureau of Labor Statistics · BEA · market feeds). Commentary is
> rule-based on disclosed thresholds; figures are shown as last released ("as of" above). It is an
> independent professional read, not a forecast or advice.*

## 7. Do / Don't
| Do | Don't |
|---|---|
| "Inflation at 3.10% keeps the last mile of disinflation sticky, constraining rate cuts." | "Inflation is still way too hot!!!" |
| "Long rates elevated; higher discount rates compress valuations." | "Rates are crushing everything." |
| Disclose thresholds + data window | Imply real-time precision we don't have |
| Attribute every figure | Present unsourced numbers |

## 8. Governance & evolution
- E1 (now): this guide + methodology disclosure + deterministic depth.
- E2+: an LLM may elevate phrasing **only within these rules** — fact-locked to engine figures, cited, and human/AI-editor approved. This guide is the standing guardrail.
