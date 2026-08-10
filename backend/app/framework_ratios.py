# JHI-SIG: 69M2705M | Acquisition Intelligence Framework | JHI Research & Analytics Firm, Inc. (proprietary)
"""Pure, deterministic key-financial-ratio engine (unit-testable, network-free).

Computes the ratios that decide a deal — valuation multiple, leverage/coverage,
profitability, liquidity, returns, and the working-capital peg — from user-supplied
figures, and reads each against benchmark bands. Decision-support only, not advice.
"""

from __future__ import annotations

from app.framework_content import RATIO_CATALOG, RESEARCH_DISCLAIMER
from app.framework_models import RatioInputs, RatioReport, RatioResult

_DEFS = {d.key: d for d in RATIO_CATALOG.ratios}


def _safe_div(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator in (None, 0):
        return None
    return numerator / denominator


def _fmt(value: float | None, unit: str) -> str:
    if value is None:
        return "—"
    if unit == "%":
        return f"{value * 100:.1f}%"
    if unit == "x":
        return f"{value:.2f}×"
    if unit == "ratio":
        return f"{value:.2f}"
    if unit == "$":
        return f"${round(value):,}"
    return f"{value:.2f}"


# Ascending threshold bands. Each entry: (upper_bound_exclusive, status).
# For "higher is better" ratios the last band (inf) is the strong one.
_HIGHER_BANDS: dict[str, list[tuple[float, str]]] = {
    "operating_margin": [(0.03, "weak"), (0.10, "caution"), (0.20, "adequate"), (float("inf"), "strong")],
    "net_margin": [(0.02, "weak"), (0.07, "caution"), (0.15, "adequate"), (float("inf"), "strong")],
    "gross_margin": [(0.15, "weak"), (0.30, "caution"), (0.50, "adequate"), (float("inf"), "strong")],
    "roe": [(0.03, "weak"), (0.10, "caution"), (0.20, "adequate"), (float("inf"), "strong")],
    "current_ratio": [(1.0, "weak"), (1.5, "caution"), (2.0, "adequate"), (float("inf"), "strong")],
    "quick_ratio": [(0.7, "weak"), (1.0, "caution"), (1.5, "adequate"), (float("inf"), "strong")],
    "dscr": [(1.0, "weak"), (1.25, "caution"), (1.5, "adequate"), (float("inf"), "strong")],
}

# For "lower is better" ratios (leverage): ascending bands where small is strong.
_LOWER_BANDS: dict[str, list[tuple[float, str]]] = {
    "debt_to_ebitda": [(2.0, "strong"), (3.0, "adequate"), (4.0, "caution"), (float("inf"), "weak")],
}


def _band_status(key: str, value: float | None) -> str:
    if value is None:
        return "n/a"
    if key in _HIGHER_BANDS:
        for upper, status in _HIGHER_BANDS[key]:
            if value < upper:
                return status
        return "strong"
    if key in _LOWER_BANDS:
        for upper, status in _LOWER_BANDS[key]:
            if value < upper:
                return status
        return "weak"
    return "reference"


_STATUS_PHRASE = {
    "strong": "Strong — comfortably above the benchmark.",
    "adequate": "Adequate — within a healthy range.",
    "caution": "Caution — below a comfortable level; investigate.",
    "weak": "Weak — outside the benchmark; a material concern.",
    "reference": "Reference figure — read in context, no good/bad band.",
    "n/a": "Not computed — provide the required inputs.",
}


def _interpret(key: str, value: float | None, status: str) -> str:
    if value is None:
        return "Not computed — provide the required inputs."
    if key == "dscr":
        base = _STATUS_PHRASE[status]
        return base + " Lenders typically require ≥ 1.25×."
    if key == "working_capital":
        if value < 0:
            return "Negative net working capital — the business runs on supplier/customer float; confirm it is sustainable."
        return "Positive net working capital the buyer must fund at close — negotiate a peg in the LOI."
    if key in ("sde_multiple", "ebitda_multiple"):
        return "Reference multiple — compare to sector ranges and the quality of earnings before concluding."
    return _STATUS_PHRASE[status]


def _result(key: str, value: float | None) -> RatioResult:
    d = _DEFS[key]
    status = _band_status(key, value)
    return RatioResult(
        key=key,
        name=d.name,
        category=d.category,
        unit=d.unit,
        value=(round(value, 4) if value is not None else None),
        display=_fmt(value, d.unit),
        status=status,
        interpretation=_interpret(key, value, status),
        benchmark=d.benchmark,
    )


def compute_ratios(inputs: RatioInputs) -> RatioReport:
    revenue = inputs.revenue
    ebitda = inputs.ebitda
    sde = inputs.sde

    # Derive operating income if not supplied but its components are.
    operating_income = inputs.operating_income
    if operating_income is None and revenue is not None and inputs.cogs is not None:
        opex = inputs.operating_expenses or 0.0
        operating_income = revenue - inputs.cogs - opex

    gross_profit = None
    if revenue is not None and inputs.cogs is not None:
        gross_profit = revenue - inputs.cogs

    working_capital = None
    if inputs.current_assets is not None and inputs.current_liabilities is not None:
        working_capital = inputs.current_assets - inputs.current_liabilities

    quick_assets = None
    if inputs.current_assets is not None:
        quick_assets = inputs.current_assets - (inputs.inventory or 0.0)

    values: dict[str, float | None] = {
        "sde_multiple": _safe_div(inputs.purchase_price, sde),
        "ebitda_multiple": _safe_div(inputs.purchase_price, ebitda),
        "dscr": _safe_div(ebitda, inputs.annual_debt_service),
        "debt_to_ebitda": _safe_div(inputs.total_debt, ebitda),
        "gross_margin": _safe_div(gross_profit, revenue),
        "operating_margin": _safe_div(operating_income, revenue),
        "net_margin": _safe_div(inputs.net_income, revenue),
        "current_ratio": _safe_div(inputs.current_assets, inputs.current_liabilities),
        "quick_ratio": _safe_div(quick_assets, inputs.current_liabilities),
        "roe": _safe_div(inputs.net_income, inputs.total_equity),
        "working_capital": working_capital,
    }

    results = [_result(d.key, values.get(d.key)) for d in RATIO_CATALOG.ratios]

    computed = [r for r in results if r.value is not None]
    flagged = [r.name for r in computed if r.status in ("caution", "weak")]
    if not computed:
        summary = "No ratios computed yet — enter figures to see results."
    elif flagged:
        summary = (
            f"{len(computed)} ratios computed; watch: " + ", ".join(flagged) + "."
        )
    else:
        summary = f"{len(computed)} ratios computed — all within benchmark ranges."

    return RatioReport(results=results, summary=summary, disclaimer=RESEARCH_DISCLAIMER)
