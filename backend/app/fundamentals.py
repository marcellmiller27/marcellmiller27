# JHI-SIG: 69M2705M | Point-in-time fundamentals provider (Sharadar SF1 primary, SEC EDGAR fallback) | JHI Research & Analytics Firm, Inc. (proprietary)
"""Unified point-in-time equity-fundamentals provider.

Sourcing policy — **Sharadar SF1 first, SEC EDGAR fallback**:

  1. If a Nasdaq Data Link key is configured, pull Sharadar SF1 (As-Reported
     *annual* — ``ARY`` — so figures are point-in-time, no look-ahead) and map the
     SF1 indicator columns to the normalized fields the valuation/scoring engines
     need. A multi-year series is pulled so revenue CAGR can be derived.
  2. If SF1 is unavailable (no key, empty response, missing an essential field, or
     any network/parse error) we fall back to the existing SEC EDGAR readers.

The provider is resilient by contract: it never raises for an SF1 problem — it
degrades to EDGAR. It only raises ``edgar_services.ProviderError`` when EDGAR (the
fallback) also cannot supply data, preserving the existing exception contract that
callers/routers already handle.

────────────────────────────────────────────────────────────────────────────────
DATA GOVERNANCE — Founder mandate ("no spillage / derived-only") — CRITICAL:
  Raw Sharadar SF1 datatable rows/fields are LICENSED data and MUST stay INTERNAL.
  This module returns only the normalized inputs our engines consume to compute
  DERIVED outputs (valuations, opportunity scores, ratios, margins). Only those
  DERIVED outputs may be surfaced to users, newsletters, or workbooks. Never expose
  or redistribute raw SF1 rows/fields in any API response, newsletter, or export.

  Consequently, consumers that surface RAW fundamental line-items to users — the
  SEC EDGAR financials endpoint/workbook (``routers/edgar.py``,
  ``edgar_workbook.py``) and the Deal X-Ray public-comp benchmark
  (``routers/deal_xray.py``, which surfaces raw peer ``revenue``) — deliberately
  remain on public-domain SEC EDGAR and do NOT use this SF1-primary provider.
────────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app import edgar_services
from app.market_services import (
    nasdaq_data_link_api_key,
    sharadar_sf1_annual,
)

logger = logging.getLogger(__name__)

SOURCE_SF1 = "sharadar_sf1"
SOURCE_EDGAR = "sec_edgar"

# Human-readable provenance strings (safe to surface — they name the SOURCE, never
# raw licensed rows). Used to populate the disclosed ``sources`` of derived outputs.
SOURCE_LABELS: dict[str, str] = {
    SOURCE_SF1: "Sharadar SF1 (Nasdaq Data Link — point-in-time fundamentals; derived output only)",
    SOURCE_EDGAR: "SEC EDGAR (fundamentals — public domain)",
}

# SF1 indicator columns -> normalized fields (Founder-specified mapping).
#   netinc   -> net_income
#   revenue  -> revenue
#   equity   -> stockholders_equity
#   opinc    -> operating_income (operating_margin = opinc / revenue)
#   gp       -> gross_profit    (gross_margin = gp / revenue)
#   sharesbas / shwa -> shares outstanding (prefer period-end basic shares)
#   rnd      -> research_and_development expense (Valuation 2.0: R&D-as-investment)
#   fcf      -> free_cash_flow  (cash-flow-statement based)
#   capex    -> capital expenditure
#   ebitda   -> ebitda
#   roic     -> return on invested capital (reinvestment-driven growth trigger)
#   roe      -> return on equity (roic proxy when roic is absent)


@dataclass
class FundamentalsYear:
    """One fiscal year of the fields used for trend/CAGR + ratio derivation (internal)."""

    fiscal_year: int
    revenue: float | None = None
    net_income: float | None = None
    operating_income: float | None = None
    stockholders_equity: float | None = None
    rnd: float | None = None  # research & development expense (for R&D-growth trend)
    gross_margin: float | None = None
    # Ratio-trend inputs (SF1-rich; None when the source lacks them).
    eps: float | None = None                 # diluted EPS preferred, else basic
    ebitda: float | None = None
    free_cash_flow: float | None = None
    operating_margin: float | None = None
    net_margin: float | None = None
    period_end: str | None = None


@dataclass
class EquityFundamentals:
    """Normalized, source-agnostic fundamentals bundle for the derived engines.

    Shapes the subset of fields the Cross-Asset Valuation DCF and the equity
    Opportunity Scan need, plus a multi-year ``years`` series for revenue CAGR.
    ``.years`` is duck-compatible with the existing ``_revenue_cagr(hist)`` helpers
    (each element exposes ``fiscal_year`` and ``revenue``).
    """

    ticker: str
    entity_name: str
    source: str
    fiscal_year: int | None = None
    period_end: str | None = None
    revenue: float | None = None
    operating_income: float | None = None
    net_income: float | None = None
    stockholders_equity: float | None = None
    gross_margin: float | None = None
    operating_margin: float | None = None
    net_margin: float | None = None
    shares_outstanding: float | None = None
    # Valuation Framework 2.0 inputs (SF1-rich; None when the source lacks them).
    rnd: float | None = None                # research & development expense
    free_cash_flow: float | None = None     # SF1 fcf (cash-flow-statement based)
    capex: float | None = None              # capital expenditure (SF1 sign preserved)
    ebitda: float | None = None
    roic: float | None = None               # return on invested capital
    roe: float | None = None                # return on equity
    # Balance-sheet / ratio inputs (SF1-rich; EDGAR fills a subset; None otherwise).
    cost_of_revenue: float | None = None
    gross_profit: float | None = None
    ebit: float | None = None
    interest_expense: float | None = None
    total_assets: float | None = None
    total_liabilities: float | None = None
    total_debt: float | None = None
    current_assets: float | None = None
    current_liabilities: float | None = None
    inventory: float | None = None
    cash_and_equivalents: float | None = None
    eps: float | None = None                # diluted EPS preferred, else basic
    eps_basic: float | None = None
    dividends_per_share: float | None = None
    years: list[FundamentalsYear] = field(default_factory=list)
    as_of: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


def _to_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def _pick(row: dict, *keys: str) -> float | None:
    for key in keys:
        val = _to_float(row.get(key))
        if val is not None:
            return val
    return None


def _row_year(row: dict) -> int | None:
    """Fiscal year integer from an SF1 row (parsed from the period-end date)."""
    for key in ("reportperiod", "calendardate", "datekey"):
        raw = row.get(key)
        if isinstance(raw, str) and len(raw) >= 4 and raw[:4].isdigit():
            return int(raw[:4])
    return None


def _safe_ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or not denominator:
        return None
    return round(numerator / denominator, 4)


def _from_sf1(ticker: str, max_years: int) -> EquityFundamentals | None:
    """Build the bundle from Sharadar SF1 (annual, as-reported). Returns None to
    signal 'fall back to EDGAR' when SF1 lacks the essential fields."""
    rows = sharadar_sf1_annual(ticker, limit=max(max_years, 2))
    if not rows:
        return None
    # Newest fiscal year first (defensive: don't rely on API row ordering).
    rows = sorted(rows, key=lambda r: str(r.get("datekey") or r.get("reportperiod") or ""), reverse=True)
    latest = rows[0]

    revenue = _pick(latest, "revenue")
    net_income = _pick(latest, "netinc")
    equity = _pick(latest, "equity")
    operating_income = _pick(latest, "opinc")
    gross_profit = _pick(latest, "gp")
    shares = _pick(latest, "sharesbas", "shwa")
    # Valuation 2.0 inputs (leave None when SF1 omits them — engine degrades safely).
    rnd = _pick(latest, "rnd")
    fcf = _pick(latest, "fcf")
    capex = _pick(latest, "capex")
    ebitda = _pick(latest, "ebitda")
    roic = _pick(latest, "roic")
    roe = _pick(latest, "roe")
    # Balance-sheet / ratio inputs.
    cost_of_revenue = _pick(latest, "cor")
    ebit = _pick(latest, "ebit")
    interest_expense = _pick(latest, "intexp")
    total_assets = _pick(latest, "assets")
    total_liabilities = _pick(latest, "liabilities")
    total_debt = _pick(latest, "debt")
    current_assets = _pick(latest, "assetsc")
    current_liabilities = _pick(latest, "liabilitiesc")
    inventory = _pick(latest, "inventory")
    cash = _pick(latest, "cashneq")
    eps_dil = _pick(latest, "epsdil")
    eps_basic = _pick(latest, "eps")
    dps = _pick(latest, "dps")

    # SF1 must supply the core income-statement fields to be considered usable;
    # otherwise fall back to EDGAR rather than emit a half-populated bundle.
    if net_income is None or revenue is None:
        return None

    years: list[FundamentalsYear] = []
    for row in rows:
        fy = _row_year(row)
        if fy is None:
            continue
        row_rev = _pick(row, "revenue")
        row_ni = _pick(row, "netinc")
        row_oi = _pick(row, "opinc")
        years.append(
            FundamentalsYear(
                fiscal_year=fy,
                revenue=row_rev,
                net_income=row_ni,
                operating_income=row_oi,
                stockholders_equity=_pick(row, "equity"),
                rnd=_pick(row, "rnd"),
                gross_margin=_safe_ratio(_pick(row, "gp"), row_rev),
                eps=_pick(row, "epsdil", "eps"),
                ebitda=_pick(row, "ebitda"),
                free_cash_flow=_pick(row, "fcf"),
                operating_margin=_safe_ratio(row_oi, row_rev),
                net_margin=_safe_ratio(row_ni, row_rev),
                period_end=str(row.get("reportperiod") or row.get("calendardate") or "") or None,
            )
        )

    entity_name = str(latest.get("name") or ticker).strip() or ticker
    return EquityFundamentals(
        ticker=ticker,
        entity_name=entity_name,
        source=SOURCE_SF1,
        fiscal_year=_row_year(latest),
        period_end=str(latest.get("reportperiod") or latest.get("calendardate") or "") or None,
        revenue=revenue,
        operating_income=operating_income,
        net_income=net_income,
        stockholders_equity=equity,
        gross_margin=_safe_ratio(gross_profit, revenue),
        operating_margin=_safe_ratio(operating_income, revenue),
        net_margin=_safe_ratio(net_income, revenue),
        shares_outstanding=shares if (shares and shares > 0) else None,
        rnd=rnd,
        free_cash_flow=fcf,
        capex=capex,
        ebitda=ebitda,
        roic=roic,
        roe=roe if roe is not None else _safe_ratio(net_income, equity),
        cost_of_revenue=cost_of_revenue,
        gross_profit=gross_profit,
        ebit=ebit,
        interest_expense=interest_expense,
        total_assets=total_assets,
        total_liabilities=total_liabilities,
        total_debt=total_debt,
        current_assets=current_assets,
        current_liabilities=current_liabilities,
        inventory=inventory,
        cash_and_equivalents=cash,
        eps=eps_dil if eps_dil is not None else eps_basic,
        eps_basic=eps_basic,
        dividends_per_share=dps,
        years=years,
    )


def _from_edgar(ticker: str, max_years: int) -> EquityFundamentals:
    """Build the bundle from SEC EDGAR (public domain) — the resilient fallback."""
    fin = edgar_services.normalize(ticker)
    hist = edgar_services.history(ticker, max_years=max_years)
    shares = edgar_services.latest_shares_outstanding(ticker)

    years = [
        FundamentalsYear(
            fiscal_year=getattr(row, "fiscal_year", None),
            revenue=getattr(row, "revenue", None),
            net_income=getattr(row, "net_income", None),
            operating_income=getattr(row, "operating_income", None),
            stockholders_equity=getattr(row, "stockholders_equity", None),
            gross_margin=getattr(row, "gross_margin", None),
            operating_margin=getattr(row, "operating_margin", None),
            net_margin=getattr(row, "net_margin", None),
            eps=(
                _safe_ratio(getattr(row, "net_income", None), shares)
                if (shares and shares > 0)
                else None
            ),
        )
        for row in getattr(hist, "years", [])
    ]
    return EquityFundamentals(
        ticker=ticker,
        entity_name=fin.entity_name,
        source=SOURCE_EDGAR,
        fiscal_year=fin.fiscal_year,
        period_end=fin.period_end,
        revenue=fin.revenue,
        operating_income=fin.operating_income,
        net_income=fin.net_income,
        stockholders_equity=fin.stockholders_equity,
        gross_margin=fin.gross_margin,
        operating_margin=fin.operating_margin,
        net_margin=fin.net_margin,
        shares_outstanding=shares if (shares and shares > 0) else None,
        # EDGAR does not expose SF1-rich fields; derive ROE where the inputs allow.
        roe=_safe_ratio(fin.net_income, fin.stockholders_equity),
        cost_of_revenue=getattr(fin, "cost_of_revenue", None),
        gross_profit=getattr(fin, "gross_profit", None),
        total_assets=getattr(fin, "total_assets", None),
        total_liabilities=getattr(fin, "total_liabilities", None),
        cash_and_equivalents=getattr(fin, "cash_and_equivalents", None),
        eps=(
            _safe_ratio(fin.net_income, shares) if (shares and shares > 0) else None
        ),
        years=years,
    )


def equity_fundamentals(ticker: str, max_years: int = 5) -> EquityFundamentals:
    """Normalized point-in-time fundamentals for one ticker.

    SF1 primary, EDGAR fallback. Raises ``edgar_services.ProviderError`` only when
    the EDGAR fallback also fails (preserves the callers' existing contract). Never
    raises because of an SF1 problem — it silently degrades to EDGAR.
    """
    ticker = ticker.strip().upper()
    if nasdaq_data_link_api_key():
        try:
            bundle = _from_sf1(ticker, max_years)
        except Exception as exc:  # noqa: BLE001 - resilient by contract: any SF1 issue -> EDGAR
            logger.info("fundamentals: SF1 unavailable for %s (%s); falling back to EDGAR", ticker, exc)
            bundle = None
        if bundle is not None:
            logger.info("fundamentals: %s sourced from Sharadar SF1", ticker)
            return bundle
    result = _from_edgar(ticker, max_years)
    logger.info("fundamentals: %s sourced from SEC EDGAR", ticker)
    return result


def source_label(source: str) -> str:
    """Human-readable provenance for a source key (safe to surface)."""
    return SOURCE_LABELS.get(source, source)
