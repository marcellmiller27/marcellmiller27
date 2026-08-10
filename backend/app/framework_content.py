# JHI-SIG: 69M2705M | Acquisition Intelligence Framework | JHI Research & Analytics Firm, Inc. (proprietary)
"""Fact-locked, derived-only content for the Acquisition Intelligence Framework.

This is educational reference material for search-fund / ETA / SMB acquirers. It is
research, not investment, legal, tax, or accounting advice. Nothing here is a
recommendation to buy or sell any specific business.
"""

from __future__ import annotations

from app.framework_models import (
    DDCategory,
    DDItem,
    DueDiligenceChecklist,
    ElementExplainer,
    ElementTool,
    FrameworkElement,
    FrameworkElementList,
    IndustryBenchmarks,
    MarketAnalysisTemplate,
    MarketSection,
    MarketWorksheetField,
    RatioCatalog,
    RatioDefinition,
    SectorBenchmark,
    ToolkitResource,
)

RESEARCH_DISCLAIMER = (
    "Educational framework — research, not investment, legal, tax, or accounting advice. "
    "Outputs are decision-support only. Every figure is derived from inputs you provide or "
    "from public aggregates; verify against source documents and consult licensed "
    "professionals before making an offer."
)

DERIVED_DISCLAIMER = (
    "Derived-only sector aggregates: median/typical values compiled from public company "
    "filings (SEC EDGAR) and Sharadar SF1 fundamentals. No licensed per-company data is "
    "surfaced. SMB and lower-middle-market targets vary widely from public-company medians — "
    "treat these as directional reference bands, not valuations."
)

# --- The ten framework elements ----------------------------------------------

_ELEMENTS: list[FrameworkElement] = [
    FrameworkElement(
        id="research-target",
        name="How to research a target",
        summary="Build a sourcing thesis and a first-pass screen before you spend real diligence time.",
        explainer=ElementExplainer(
            how_to=(
                "Start from your own criteria (industry, size, geography, owner situation). "
                "Assemble a target list from brokers, proprietary outreach, and screens, then "
                "run a fast qualify/disqualify pass on each before deep work."
            ),
            what_to_look_for=[
                "Recurring or repeat revenue and a durable reason customers stay",
                "Owner willing to transition, with a business that is not the owner",
                "Fragmented industry with tailwinds, not structural decline",
                "Clean-enough books and a plausible reason the business is for sale",
            ],
            why_it_matters=(
                "Most deals die in diligence; a disciplined screen keeps you from burning "
                "months on a target that was never a fit."
            ),
        ),
        tool=ElementTool(
            label="Open the Screener",
            href="/opportunities",
            description="Score and rank candidate targets against your acquisition criteria.",
        ),
        checklist=[
            "Written acquisition criteria (industry, revenue/SDE range, geography)",
            "Target list with source and owner situation noted",
            "One-line thesis for why each target could be a fit",
            "Quick disqualifiers checked (decline, single-customer, regulatory)",
            "Outreach / broker contact logged",
        ],
    ),
    FrameworkElement(
        id="financial-analysis",
        name="Financial analysis",
        summary="Normalize earnings and tie the numbers to cash before you trust a multiple.",
        explainer=ElementExplainer(
            how_to=(
                "Rebuild three years of P&L, normalize EBITDA/SDE for add-backs and one-time "
                "items, tie revenue to bank deposits (proof-of-cash), and trace margin trends "
                "and working-capital needs."
            ),
            what_to_look_for=[
                "Add-backs that are documented and truly non-recurring",
                "Deposits that reconcile to reported revenue within materiality",
                "Stable or improving gross margin; no unexplained spikes",
                "Working capital the buyer must fund at close",
            ],
            why_it_matters=(
                "The purchase price is a multiple of normalized earnings — if the earnings are "
                "overstated, you overpay on every dollar of the multiple."
            ),
        ),
        tool=ElementTool(
            label="Run Earnings / QoE",
            href="/diligence-suite",
            description="Software-accelerated Quality-of-Earnings: proof-of-cash, add-back scrutiny, NWC peg.",
        ),
        checklist=[
            "3 years financials + trailing-twelve-month interim",
            "EBITDA/SDE normalization schedule with support for each add-back",
            "Proof-of-cash: revenue tied to bank deposits",
            "Gross / operating / net margin trend",
            "Net working-capital peg quantified",
        ],
    ),
    FrameworkElement(
        id="industry-analysis",
        name="Industry analysis",
        summary="Benchmark the target against derived sector margins, growth, and multiples.",
        explainer=ElementExplainer(
            how_to=(
                "Place the target in its sector: compare its margins and growth to derived "
                "benchmarks, understand the value chain, and map structural tailwinds or "
                "headwinds and typical valuation multiples."
            ),
            what_to_look_for=[
                "Target margins in line with (or above) sector medians",
                "Sector growing, not in secular decline",
                "Fragmentation that supports a buy-and-build",
                "Multiple paid vs. typical sector EV/EBITDA range",
            ],
            why_it_matters=(
                "A great operator in a dying sector is still a hard hold; the industry sets the "
                "ceiling on realistic outcomes."
            ),
        ),
        tool=ElementTool(
            label="Open Industry Benchmarks",
            href="/framework/industry-analysis",
            description="Derived sector benchmarks: margins, growth, and EV/EBITDA multiples.",
        ),
        checklist=[
            "Target's sector identified and defined",
            "Margins vs. sector benchmark compared",
            "Growth vs. sector benchmark compared",
            "Value-chain position and supplier/customer power mapped",
            "Multiple paid sanity-checked against sector range",
        ],
    ),
    FrameworkElement(
        id="market-analysis",
        name="Market analysis",
        summary="Size the market (TAM/SAM/SOM) and map the competitive landscape.",
        explainer=ElementExplainer(
            how_to=(
                "Define the served market, size it top-down and bottom-up (TAM/SAM/SOM), "
                "segment demand, and map competitors and the target's positioning and moat."
            ),
            what_to_look_for=[
                "A market large enough to support your growth plan",
                "Demand drivers you can articulate and that are durable",
                "A defensible position (switching costs, brand, locality, scale)",
                "Rational competition, not a race to the bottom on price",
            ],
            why_it_matters=(
                "Financials are history; the market determines whether the growth in your model "
                "is achievable at all."
            ),
        ),
        tool=ElementTool(
            label="Open Market Analysis Template",
            href="/framework/market-analysis",
            description="TAM/SAM/SOM worksheet, five-forces prompts, and a competitive-landscape template.",
        ),
        checklist=[
            "TAM / SAM / SOM estimated (top-down and bottom-up)",
            "Demand drivers and durability documented",
            "Competitor set and relative positioning mapped",
            "Source of the target's moat identified",
            "Five-forces pressures assessed",
        ],
    ),
    FrameworkElement(
        id="company-analysis",
        name="Company analysis",
        summary="Understand how the business actually runs and where value concentrates.",
        explainer=ElementExplainer(
            how_to=(
                "Run a limited-scope review of the operating model: revenue quality, customer "
                "concentration, owner dependence, org structure, and the handful of things that "
                "make this specific company work."
            ),
            what_to_look_for=[
                "Low customer concentration (no single customer > ~15-20%)",
                "Documented processes; the business is not the owner",
                "A management layer that survives the transition",
                "Diversified suppliers and no single point of failure",
            ],
            why_it_matters=(
                "You are buying a going concern, not a spreadsheet; concentration and key-person "
                "risk are the most common post-close surprises."
            ),
        ),
        tool=ElementTool(
            label="Run a Limited Scope Review",
            href="/deal-xray",
            description="LSR / Scope: a fast structured read on the business and its key risks.",
        ),
        checklist=[
            "Revenue by customer (concentration measured)",
            "Owner-dependence and key-person risk assessed",
            "Org chart and management retention plan",
            "Core processes / SOPs documented or noted as missing",
            "Supplier concentration and terms reviewed",
        ],
    ),
    FrameworkElement(
        id="valuation-considerations",
        name="Valuation considerations",
        summary="Anchor price to normalized earnings, deal structure, and financeability.",
        explainer=ElementExplainer(
            how_to=(
                "Value the business on normalized earnings and a defensible multiple, then "
                "pressure-test the structure (debt, seller note, earnout) and confirm the deal "
                "can service its debt (DSCR) and clear working capital at close."
            ),
            what_to_look_for=[
                "Multiple justified by growth, margins, and risk — not the ask",
                "DSCR that comfortably clears lender minimums (SBA ~1.25x+)",
                "Structure that shares risk (seller note / earnout) where warranted",
                "Working-capital peg and net debt reflected in equity value",
            ],
            why_it_matters=(
                "Price is what protects (or destroys) your return; a fair business at the wrong "
                "price is a bad deal."
            ),
        ),
        tool=ElementTool(
            label="Open Cross-Asset Valuation",
            href="/valuation",
            description="Model value across methods and stress the multiple and structure.",
        ),
        checklist=[
            "Normalized EBITDA/SDE agreed",
            "Multiple benchmarked to sector and risk",
            "Debt service and DSCR modeled",
            "Working-capital peg and net-debt bridge to equity value",
            "Structure (seller note / earnout / escrow) drafted",
        ],
    ),
    FrameworkElement(
        id="risk-analysis",
        name="Risk analysis",
        summary="Enumerate what could go wrong and how the deal terms protect you.",
        explainer=ElementExplainer(
            how_to=(
                "Catalog risks by category (financial, customer, operational, legal, key-person, "
                "market), score likelihood and impact, and map each material risk to a mitigation "
                "in price, structure, or the purchase agreement."
            ),
            what_to_look_for=[
                "Red flags surfaced in earnings quality and proof-of-cash",
                "Concentration and key-person risks with no mitigation",
                "Contingent liabilities (litigation, tax, environmental)",
                "Reps, warranties, indemnities, and escrow sized to the risk",
            ],
            why_it_matters=(
                "You cannot eliminate risk, but unpriced, unmitigated risk is how acquirers lose "
                "their equity."
            ),
        ),
        tool=ElementTool(
            label="Surface risks in Earnings / QoE",
            href="/diligence-suite",
            description="Red-flag detection across add-backs, cash, concentration, and debt-like items.",
        ),
        checklist=[
            "Risk register by category with likelihood × impact",
            "Customer & supplier concentration quantified",
            "Contingent liabilities identified (legal / tax / environmental)",
            "Each material risk mapped to a mitigation",
            "Reps/warranties/indemnity/escrow sized",
        ],
    ),
    FrameworkElement(
        id="due-diligence",
        name="Due diligence",
        summary="Run a comprehensive, categorized checklist and track it to close.",
        explainer=ElementExplainer(
            how_to=(
                "Work a structured checklist across financial, legal, operational, commercial, "
                "HR, and IT workstreams; request documents early, track open items, and confirm "
                "or kill your thesis before removing contingencies."
            ),
            what_to_look_for=[
                "Confirmation (or contradiction) of every underwriting assumption",
                "Documents that reconcile to what the seller represented",
                "Open items resolved before contingencies are waived",
                "A clean data room versus persistent gaps",
            ],
            why_it_matters=(
                "Diligence is your last, best chance to find the deal-killer before your money is "
                "at risk."
            ),
        ),
        tool=ElementTool(
            label="Open the Due-Diligence Framework",
            href="/framework/due-diligence",
            description="Exportable, categorized DD checklist — start a diligence deal in the Pipeline.",
        ),
        checklist=[
            "Document request list issued to the seller",
            "Financial, legal, operational, commercial, HR, IT workstreams opened",
            "Open-items tracker maintained with owners and dates",
            "Findings tied back to price / structure / agreement",
            "Diligence deal tracked in the Pipeline",
        ],
    ),
    FrameworkElement(
        id="economic-environment",
        name="Economic environment",
        summary="Read rates, inflation, and the cycle — they drive financing and demand.",
        explainer=ElementExplainer(
            how_to=(
                "Track the macro backdrop that moves your deal: interest rates and credit "
                "availability (cost of acquisition debt), inflation and labor (margins), and the "
                "cycle position of the target's end markets."
            ),
            what_to_look_for=[
                "Rate path and its effect on DSCR and financeability",
                "Input-cost and wage inflation pressuring margins",
                "End-market demand tied to the cycle vs. non-discretionary",
                "Credit conditions for SBA / acquisition lending",
            ],
            why_it_matters=(
                "The same business is a different deal at 6% money versus 11% money; macro sets "
                "the cost and availability of your leverage."
            ),
        ),
        tool=ElementTool(
            label="Open Economics",
            href="/macro",
            description="Live economic tracking: rates, inflation, growth, and labor.",
        ),
        checklist=[
            "Current rate environment and acquisition-debt cost noted",
            "Inflation / wage pressure on the target's margins assessed",
            "End-market cyclicality classified (discretionary vs. staple)",
            "Credit availability for the deal confirmed",
            "Macro sensitivities reflected in the model",
        ],
    ),
    FrameworkElement(
        id="key-financial-ratios",
        name="Key financial ratios",
        summary="Compute the ratios that decide value, safety, and financeability.",
        explainer=ElementExplainer(
            how_to=(
                "Compute the deal's core ratios from normalized figures — the valuation multiple, "
                "leverage and coverage (Debt/EBITDA, DSCR), profitability margins, liquidity "
                "(current/quick), returns (ROE), and the working-capital peg — and read each "
                "against benchmark bands."
            ),
            what_to_look_for=[
                "DSCR comfortably above the lender minimum",
                "Debt/EBITDA that leaves headroom, not a knife's edge",
                "Margins consistent with the sector",
                "Liquidity (current/quick) that funds operations post-close",
            ],
            why_it_matters=(
                "Ratios translate raw statements into the few numbers that actually decide whether "
                "a deal is safe, financeable, and fairly priced."
            ),
        ),
        tool=ElementTool(
            label="Open Key Financial Ratios",
            href="/framework/ratios",
            description="Compute + interpret each ratio with plain-English meaning and benchmark bands.",
        ),
        checklist=[
            "Valuation multiple (price ÷ SDE or EBITDA) computed",
            "Leverage & coverage (Debt/EBITDA, DSCR) computed",
            "Gross / operating / net margins computed",
            "Liquidity (current & quick ratios) computed",
            "Working-capital peg and ROE computed",
        ],
    ),
]

FRAMEWORK_ELEMENTS = FrameworkElementList(
    elements=_ELEMENTS,
    disclaimer=RESEARCH_DISCLAIMER,
)

# --- Key financial ratio definitions -----------------------------------------

RATIO_DEFINITIONS: list[RatioDefinition] = [
    RatioDefinition(
        key="sde_multiple",
        name="SDE multiple",
        category="Valuation",
        formula="Purchase price ÷ Seller's Discretionary Earnings",
        unit="x",
        plain_english="How many years of owner earnings you are paying for the business.",
        benchmark="Main-street SMBs commonly trade ~2–4× SDE; higher for size, growth, and recurring revenue.",
        higher_is_better=None,
    ),
    RatioDefinition(
        key="ebitda_multiple",
        name="EBITDA multiple",
        category="Valuation",
        formula="Purchase price (enterprise value) ÷ EBITDA",
        unit="x",
        plain_english="Enterprise value expressed as a multiple of normalized operating earnings.",
        benchmark="Lower-middle-market deals commonly ~3–6× EBITDA; varies widely by sector and size.",
        higher_is_better=None,
    ),
    RatioDefinition(
        key="dscr",
        name="Debt-service coverage (DSCR)",
        category="Leverage & coverage",
        formula="EBITDA (or cash flow) ÷ Annual debt service",
        unit="x",
        plain_english="How comfortably operating cash flow covers loan payments.",
        benchmark="Lenders typically require ≥ 1.25×; ≥ 1.5× is comfortable, < 1.0× cannot pay its debt.",
        higher_is_better=True,
    ),
    RatioDefinition(
        key="debt_to_ebitda",
        name="Debt / EBITDA",
        category="Leverage & coverage",
        formula="Total debt ÷ EBITDA",
        unit="x",
        plain_english="How many years of earnings the total debt represents — the leverage load.",
        benchmark="≤ 2× conservative, 2–3× moderate, 3–4× aggressive, > 4× stretched for SMBs.",
        higher_is_better=False,
    ),
    RatioDefinition(
        key="gross_margin",
        name="Gross margin",
        category="Profitability",
        formula="(Revenue − COGS) ÷ Revenue",
        unit="%",
        plain_english="What's left after the direct cost of delivering the product or service.",
        benchmark="Highly sector-dependent: services 40–60%+, distribution/retail often 20–35%.",
        higher_is_better=True,
    ),
    RatioDefinition(
        key="operating_margin",
        name="Operating margin",
        category="Profitability",
        formula="Operating income ÷ Revenue",
        unit="%",
        plain_english="Profitability from core operations before interest and tax.",
        benchmark="≥ 20% strong, 10–20% healthy, 3–10% thin, < 3% fragile for most SMBs.",
        higher_is_better=True,
    ),
    RatioDefinition(
        key="net_margin",
        name="Net margin",
        category="Profitability",
        formula="Net income ÷ Revenue",
        unit="%",
        plain_english="Bottom-line profit per dollar of revenue after all costs.",
        benchmark="≥ 15% strong, 7–15% healthy, 2–7% thin, < 2% fragile for most SMBs.",
        higher_is_better=True,
    ),
    RatioDefinition(
        key="current_ratio",
        name="Current ratio",
        category="Liquidity",
        formula="Current assets ÷ Current liabilities",
        unit="ratio",
        plain_english="Ability to cover near-term obligations with near-term assets.",
        benchmark="≥ 2.0 strong, 1.5–2.0 adequate, 1.0–1.5 watch, < 1.0 liquidity risk.",
        higher_is_better=True,
    ),
    RatioDefinition(
        key="quick_ratio",
        name="Quick ratio",
        category="Liquidity",
        formula="(Current assets − Inventory) ÷ Current liabilities",
        unit="ratio",
        plain_english="Liquidity excluding inventory — the acid test.",
        benchmark="≥ 1.5 strong, 1.0–1.5 adequate, 0.7–1.0 watch, < 0.7 tight.",
        higher_is_better=True,
    ),
    RatioDefinition(
        key="roe",
        name="Return on equity (ROE)",
        category="Returns",
        formula="Net income ÷ Total equity",
        unit="%",
        plain_english="Profit generated on the equity invested in the business.",
        benchmark="≥ 20% strong, 10–20% healthy, 3–10% modest, < 3% weak (context-dependent).",
        higher_is_better=True,
    ),
    RatioDefinition(
        key="working_capital",
        name="Working-capital peg",
        category="Liquidity",
        formula="Current assets − Current liabilities",
        unit="$",
        plain_english="The net working capital the buyer must fund to keep operations running at close.",
        benchmark="No universal band — negotiate a target (peg) in the LOI; deficits reduce equity value.",
        higher_is_better=None,
    ),
]

RATIO_CATALOG = RatioCatalog(ratios=RATIO_DEFINITIONS, disclaimer=RESEARCH_DISCLAIMER)

# --- Due-diligence checklist --------------------------------------------------


def _item(i: str, text: str, priority: str = "standard") -> DDItem:
    return DDItem(id=i, text=text, priority=priority)


_DD_CATEGORIES: list[DDCategory] = [
    DDCategory(
        id="financial",
        name="Financial",
        purpose="Confirm the earnings you are paying a multiple of are real and sustainable.",
        items=[
            _item("fin-1", "3 years of financial statements + trailing-twelve-month interim", "critical"),
            _item("fin-2", "Quality-of-Earnings / EBITDA normalization with add-back support", "critical"),
            _item("fin-3", "Proof-of-cash: revenue reconciled to bank deposits", "critical"),
            _item("fin-4", "Federal and state tax returns reconciled to the financials", "critical"),
            _item("fin-5", "AR aging, bad-debt history, and collection terms"),
            _item("fin-6", "AP aging and supplier payment terms"),
            _item("fin-7", "Debt schedule and off-balance-sheet / debt-like items", "critical"),
            _item("fin-8", "Capex history and maintenance vs. growth split"),
            _item("fin-9", "Net working-capital trend and proposed peg", "critical"),
            _item("fin-10", "Revenue recognition policy and any changes"),
        ],
    ),
    DDCategory(
        id="legal",
        name="Legal",
        purpose="Verify ownership, obligations, and that nothing transfers a hidden liability.",
        items=[
            _item("leg-1", "Entity good standing, formation docs, and cap table", "critical"),
            _item("leg-2", "Material contracts and change-of-control provisions", "critical"),
            _item("leg-3", "Litigation history and pending claims", "critical"),
            _item("leg-4", "IP ownership, registrations, and assignments"),
            _item("leg-5", "Licenses, permits, and regulatory compliance", "critical"),
            _item("leg-6", "Real-property and equipment leases (assignability)"),
            _item("leg-7", "Insurance policies, limits, and claims history"),
            _item("leg-8", "Employment, non-compete, and confidentiality agreements"),
        ],
    ),
    DDCategory(
        id="operational",
        name="Operational",
        purpose="Understand how the business actually delivers and where it could break.",
        items=[
            _item("ops-1", "Org chart, key roles, and decision rights", "critical"),
            _item("ops-2", "Core processes / SOPs (or documented gaps)"),
            _item("ops-3", "Supplier concentration, terms, and single points of failure", "critical"),
            _item("ops-4", "Facilities, equipment condition, and capacity"),
            _item("ops-5", "Backlog, lead times, and quality / warranty history"),
            _item("ops-6", "Environmental, health, and safety posture"),
        ],
    ),
    DDCategory(
        id="commercial",
        name="Commercial",
        purpose="Test whether demand and the competitive position support your growth plan.",
        items=[
            _item("com-1", "Customer concentration and revenue by customer", "critical"),
            _item("com-2", "Retention / churn and repeat-revenue mix", "critical"),
            _item("com-3", "Sales pipeline, backlog, and win rates"),
            _item("com-4", "Pricing power and discounting behavior"),
            _item("com-5", "Competitive landscape and relative positioning"),
            _item("com-6", "Market size, growth, and demand drivers"),
        ],
    ),
    DDCategory(
        id="hr",
        name="HR / People",
        purpose="Assess key-person risk and the true cost and stability of the team.",
        items=[
            _item("hr-1", "Key-person dependence and retention plan", "critical"),
            _item("hr-2", "Compensation vs. market and owner comp normalization"),
            _item("hr-3", "Benefits, PTO, and accrued liabilities"),
            _item("hr-4", "Turnover, culture, and open roles"),
            _item("hr-5", "Contractor vs. employee classification compliance"),
        ],
    ),
    DDCategory(
        id="it",
        name="IT / Technology",
        purpose="Confirm systems, security, and data will survive the transition.",
        items=[
            _item("it-1", "Systems inventory and software licenses"),
            _item("it-2", "Cybersecurity posture and incident history", "critical"),
            _item("it-3", "Data ownership, backups, and recovery"),
            _item("it-4", "Technical debt and single-vendor dependencies"),
            _item("it-5", "Business continuity / disaster-recovery plan"),
        ],
    ),
]

_DD_TOTAL = sum(len(c.items) for c in _DD_CATEGORIES)

DUE_DILIGENCE_CHECKLIST = DueDiligenceChecklist(
    categories=_DD_CATEGORIES,
    total_items=_DD_TOTAL,
    disclaimer=RESEARCH_DISCLAIMER,
)

# --- Industry analysis: derived sector benchmarks ----------------------------
# Directional medians compiled from public EDGAR / SF1 aggregates. Derived-only.

_SECTORS: list[SectorBenchmark] = [
    SectorBenchmark(
        sector="Business & professional services",
        gross_margin_pct=52.0, operating_margin_pct=14.0, net_margin_pct=9.0,
        revenue_growth_pct=7.0, ev_ebitda_multiple=8.5,
        note="People-led; watch key-person and utilization risk.",
    ),
    SectorBenchmark(
        sector="Construction & specialty trades",
        gross_margin_pct=24.0, operating_margin_pct=8.0, net_margin_pct=5.0,
        revenue_growth_pct=6.0, ev_ebitda_multiple=5.0,
        note="Project-based; working capital and backlog are decisive.",
    ),
    SectorBenchmark(
        sector="Healthcare services",
        gross_margin_pct=45.0, operating_margin_pct=13.0, net_margin_pct=8.0,
        revenue_growth_pct=8.0, ev_ebitda_multiple=9.0,
        note="Reimbursement and licensing risk; often defensive demand.",
    ),
    SectorBenchmark(
        sector="Manufacturing",
        gross_margin_pct=32.0, operating_margin_pct=11.0, net_margin_pct=7.0,
        revenue_growth_pct=5.0, ev_ebitda_multiple=6.0,
        note="Capital-intensive; scrutinize maintenance capex and cyclicality.",
    ),
    SectorBenchmark(
        sector="Retail & e-commerce",
        gross_margin_pct=38.0, operating_margin_pct=6.0, net_margin_pct=4.0,
        revenue_growth_pct=6.0, ev_ebitda_multiple=6.0,
        note="Thin margins; inventory and channel concentration matter.",
    ),
    SectorBenchmark(
        sector="Software & SaaS",
        gross_margin_pct=75.0, operating_margin_pct=18.0, net_margin_pct=12.0,
        revenue_growth_pct=18.0, ev_ebitda_multiple=12.0,
        note="Recurring revenue commands premium multiples; check churn and NRR.",
    ),
    SectorBenchmark(
        sector="Restaurants & hospitality",
        gross_margin_pct=30.0, operating_margin_pct=9.0, net_margin_pct=5.0,
        revenue_growth_pct=5.0, ev_ebitda_multiple=5.5,
        note="Labor and location driven; discretionary and cyclical.",
    ),
    SectorBenchmark(
        sector="Logistics & transportation",
        gross_margin_pct=28.0, operating_margin_pct=9.0, net_margin_pct=5.0,
        revenue_growth_pct=6.0, ev_ebitda_multiple=6.0,
        note="Fuel and fleet cost exposure; contract vs. spot mix matters.",
    ),
    SectorBenchmark(
        sector="Home & facilities services",
        gross_margin_pct=42.0, operating_margin_pct=12.0, net_margin_pct=8.0,
        revenue_growth_pct=8.0, ev_ebitda_multiple=6.5,
        note="Fragmented, recurring, roll-up friendly; route density helps.",
    ),
    SectorBenchmark(
        sector="Distribution & wholesale",
        gross_margin_pct=26.0, operating_margin_pct=7.0, net_margin_pct=4.0,
        revenue_growth_pct=5.0, ev_ebitda_multiple=6.0,
        note="Volume game; supplier terms and inventory turns are key.",
    ),
]

INDUSTRY_BENCHMARKS = IndustryBenchmarks(
    sectors=_SECTORS,
    basis=(
        "Directional medians compiled from public-company filings (SEC EDGAR) and Sharadar "
        "SF1 fundamentals, grouped to SMB-relevant sectors. Aggregates only — no licensed "
        "per-company data is surfaced."
    ),
    disclaimer=DERIVED_DISCLAIMER,
)

# --- Market analysis template -------------------------------------------------

MARKET_ANALYSIS_TEMPLATE = MarketAnalysisTemplate(
    sections=[
        MarketSection(
            id="define",
            name="Define the market",
            guidance="State precisely what market the target serves — product, buyer, and geography.",
            prompts=[
                "What problem does the target solve, for whom?",
                "What is the served geography and channel?",
                "Which adjacent markets are in or out of scope?",
            ],
        ),
        MarketSection(
            id="size",
            name="Size the market (TAM/SAM/SOM)",
            guidance="Estimate the market both top-down (industry reports) and bottom-up (units × price).",
            prompts=[
                "TAM: total demand if you served everyone",
                "SAM: the segment you can realistically serve",
                "SOM: the share you can win in your plan horizon",
            ],
        ),
        MarketSection(
            id="segment",
            name="Segment demand",
            guidance="Break demand into segments with distinct needs, willingness to pay, and dynamics.",
            prompts=[
                "Which segments are growing vs. flat?",
                "Where does the target over- or under-index?",
                "Which segment funds the growth plan?",
            ],
        ),
        MarketSection(
            id="competition",
            name="Competitive landscape",
            guidance="Map competitors, their positioning, and where the target wins or loses.",
            prompts=[
                "Who are the direct and indirect competitors?",
                "On what basis do customers choose (price, service, locality)?",
                "Where is the target advantaged or exposed?",
            ],
        ),
        MarketSection(
            id="moat",
            name="Positioning & moat",
            guidance="Identify the durable source of advantage that protects margins over time.",
            prompts=[
                "Switching costs, brand, scale, locality, or network effects?",
                "How defensible is pricing?",
                "What would a well-funded entrant need to displace the target?",
            ],
        ),
        MarketSection(
            id="drivers",
            name="Demand drivers & risks",
            guidance="Tie the model's growth to concrete, durable drivers — and name the risks.",
            prompts=[
                "What structural drivers grow this market?",
                "What could shrink it (substitution, regulation, cycle)?",
                "How sensitive is demand to the economy?",
            ],
        ),
    ],
    tam_worksheet=[
        MarketWorksheetField(key="total_customers", label="Total potential customers",
                             hint="Universe of buyers in the served market"),
        MarketWorksheetField(key="avg_annual_spend", label="Average annual spend per customer ($)",
                             hint="Typical annual revenue per buyer"),
        MarketWorksheetField(key="serviceable_pct", label="Serviceable share (%)",
                             hint="Portion you can realistically reach (SAM)"),
        MarketWorksheetField(key="obtainable_pct", label="Obtainable share (%)",
                             hint="Portion you can win in the plan horizon (SOM)"),
    ],
    five_forces=[
        "Competitive rivalry — intensity and basis of competition",
        "Supplier power — concentration and switching cost of inputs",
        "Buyer power — customer concentration and price sensitivity",
        "Threat of substitutes — alternatives to the target's offering",
        "Threat of new entrants — barriers protecting the market",
    ],
    disclaimer=RESEARCH_DISCLAIMER,
)

# --- Lead-gen toolkit resources ----------------------------------------------

TOOLKIT_RESOURCES: list[ToolkitResource] = [
    ToolkitResource(
        title="The 10-element acquisition framework",
        body=(
            "A concise walkthrough of how to research a target, analyze the financials, industry, "
            "market, and company, weigh valuation and risk, run diligence, read the economy, and "
            "compute the ratios that decide the deal."
        ),
        href="/framework",
    ),
    ToolkitResource(
        title="Key financial ratios calculator",
        body=(
            "Compute the valuation multiple, DSCR, Debt/EBITDA, margins, liquidity, ROE, and the "
            "working-capital peg from your own figures — with plain-English meaning and benchmark bands."
        ),
        href="/framework/ratios",
    ),
    ToolkitResource(
        title="Comprehensive due-diligence checklist",
        body=(
            "A categorized, exportable checklist across financial, legal, operational, commercial, "
            "HR, and IT workstreams that you can track to close in the Pipeline."
        ),
        href="/framework/due-diligence",
    ),
    ToolkitResource(
        title="Industry benchmarks & market template",
        body=(
            "Derived sector margins, growth, and multiples to benchmark a target, plus a TAM/SAM/SOM "
            "and competitive-landscape template."
        ),
        href="/framework/industry-analysis",
    ),
]

TOOLKIT_CTA_LABEL = "Upgrade to Professional (Tier 2)"
TOOLKIT_CTA_HREF = "/pricing"
