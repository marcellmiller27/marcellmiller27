# Homepage & Presentation Audit — Public Site vs. Institutional Competitors

> JHI-SIG: 69M2705M · Analysis for founder review (no code changes yet). Grounded in the
> current `src/app/page.tsx` + `src/lib/platform-data.ts` and live competitor sites
> (Mergr, CB Insights, PitchBook). Companion to `docs/COMPETITOR_TEARDOWN_AND_GAP_MAP.md`.

## Bottom line (the honest verdict you asked for)
**Not kindergarten — but the homepage is our *internal pitch deck wearing a customer costume*.** The underlying product is genuinely strong (interactive Excel, Deal X‑Ray/BQA, QoE, Pipeline, live multi‑asset data, published methodology). The problem is **presentation + leakage**, not substance:

- We are **in the ballpark on VALUE**, but **below the bar on page‑1 credibility** because the front page reads like a business plan (ARR targets, per‑tier revenue, module blueprint, enterprise valuation) instead of a product a subscriber buys.
- Fix is a **major front‑page make‑over + removal of internal‑only content** — *not* a product rebuild. The good news: we have more real value than the page currently communicates.

---

## A. Internal‑only content leaking to subscribers (remove from public site immediately)
These are "eyes‑only / investor‑deck" items currently visible to anyone:

| # | On the page now | Why it must go (public) | Source |
|---|---|---|---|
| 1 | **Legal name eyebrow: "John Henry Investments, LLC"** | Wrong entity for the platform; should be **JHI Research & Analytics Firm, Inc.** | `page.tsx:45` |
| 2 | **"Target ARR scenario — $90M"** | Internal financial target | `page.tsx:15` (keyMetrics) |
| 3 | **"Revenue model" section** + per‑tier **`target` / `revenue`**: "50,000 subscribers", "$2.5M monthly recurring revenue", "$1.495M MRR", "$750K+ MRR" | Subscribers must never see our revenue plan / subscriber targets | `page.tsx:147‑171`, `platform-data.ts:83‑110` |
| 4 | **"Application blueprint — Thirteen modules…"** | Internal build/roadmap plan | `page.tsx:174‑194` |
| 5 | **"Technology stack — selected for … future enterprise value"** | Internal architecture rationale | `page.tsx:250‑263` |
| 6 | **"Five‑year vision" + "$720M – $1.3B+ … at 8x‑15x ARR if … $90M ARR"** | **Worst offender** — internal valuation projection on the public page | `page.tsx:265‑277` |

**Rule going forward:** revenue targets, subscriber counts, valuation, roadmap phases, and tech‑stack rationale live in the **investor/internal deck**, never on the subscriber‑facing site.

## B. Copy / positioning problems
- **Mission title:** "Institutional intelligence in service of family legacy." → poetic but vague. Shorter, professional options:
  - "Institutional research for independent investors and acquirers."
  - "Research and diligence, at software speed."
  - "Know before you buy." (punchy)
  - "Institutional‑grade research, without the institutional price."
- **Hero H1** ("Investment intelligence for markets, acquisitions, and generational wealth") is decent but broad — tighten to the wedge (search‑fund/SMB diligence + multi‑asset research).
- **Grammar/lengthy blocks:** the mission "story" (steel‑driving man) is long for page 1 — move to a short **About** page (competitors keep the homepage tight and put narrative on About).
- **Font/layout:** define one type scale (H1/H2/body), consistent spacing, and a single accent — the page currently mixes many section styles.

## C. What the competitors do on page 1 (grounded)
- **Mergr** — *"Why Mergr exists: PE and M&A research should be clear, focused, and grounded in real data."* Then a crisp **"Who uses Mergr"**: Investment Bankers · Business Brokers · Accountants · Lawyers · Executive Recruiters · Corporate Development · Wealth Advisors · Business Owners · Investors · Consultants. **Lesson:** lead with clarity + an explicit audience list; no internal financials anywhere.
- **CB Insights** — one benefit line: *"Predictive intelligence on private companies — how strategy and deal teams see opportunity before the market does."* Then **proof** (12M companies, 1,600 markets), a **named score** (Mosaic), **trust** ("trusted by the world's smartest companies"), and a **10‑day free trial** CTA. **Lesson:** benefit → proof → named IP → trust → trial.
- **PitchBook** — comprehensive‑data promise, plugins, "request pricing / free trial." **Lesson:** value + frictionless CTA; pricing gated, never a revenue table.

**None of them show ARR targets, subscriber counts, module lists, or enterprise valuations.** That's the gap.

## D. Recommended public homepage structure (for the make‑over)
1. **Hero:** entity **JHI Research & Analytics Firm, Inc.**; benefit‑led H1 + one‑line subhead; single primary CTA (Start free trial / Join). Keep the **Opportunity/Deal Score** visual — it's our Mosaic equivalent.
2. **Who it's for** (Mergr‑style list): Search‑fund & SMB acquirers · Independent sponsors · Family offices · Investment advisors/RIAs · CPAs & attorneys · Self‑directed investors · Business brokers.
3. **What you get (product proof — showcase the real value):** Deal X‑Ray (BQA), Quality of Earnings, the Deal Pipeline, **interactive Excel + PDF deliverables**, live multi‑asset research, the Opportunity/Deal Score.
4. **Why trust us:** research/decision‑support (not advice) framing, published methodology & validation transparency, NASDAQ/Sharadar data, CPA‑partner network.
5. **Pricing:** clean 3‑tier cards (Consumer/Professional/Enterprise) — **features + price only, no `target`/`revenue`.**
6. **CTA + short About link** (move the founder story/mission narrative to About).

## E. Move internal content here (not on the public site)
Create an **investor/internal one‑pager** (or keep in the board/deck) for: ARR targets, per‑tier subscriber goals, the module blueprint, tech‑stack rationale, and the $720M–$1.3B valuation. These are fundraising/planning assets — powerful internally, damaging publicly.

## F. The value we should be *bragging* about (and currently bury)
You're right that we've created real value — the site under‑sells it. Front‑and‑center‑worthy: **interactive Excel models** (editable → live DSCR/valuation), **CPA‑signed QoE**, **Deal X‑Ray/BQA**, the **Deal Pipeline** workflow, **live multi‑asset data**, and **transparent, published methodology** (we out‑disclose incumbents). This is genuinely competitive for the search‑fund/SMB niche.

## Verdict, in one line
**We're in the ballpark with a strong product — the front page just needs a professional make‑over and a hard scrub of internal‑only content before subscribers see it.** On your approval, Phase‑A = remove leakage + fix entity/mission/copy; Phase‑B = the full institutional homepage rebuild per §D.
