"""SEC EDGAR public data integration (data.sec.gov) — free, no API key.

Reads public company filings/XBRL to power fundamentals, Deal X-Ray/QoE, and
comps. SEC data is US public domain (display + redistribution permitted). The SEC
requires a declared ``User-Agent`` with contact info and fair-access (<=10 req/s);
we throttle and cache to comply.

Phase 1: ticker -> CIK resolver + companyfacts fetch -> normalized headline
annual financials. (Phase 2/3: Deal X-Ray/QoE wiring + frames-based comps.)

Pure standard library HTTP so tests can monkeypatch the module-level fetchers.
"""

from __future__ import annotations

import json
import os
import threading
import time
import urllib.request
from datetime import datetime, timezone
from typing import Any

from app.edgar_models import EdgarFinancials, EdgarHistory, EdgarYear

# SEC requires a descriptive User-Agent with contact info (else 403).
USER_AGENT = os.getenv(
    "EDGAR_USER_AGENT",
    "John Henry Investments Research (research@johnhenrycapital.com)",
)
HTTP_TIMEOUT = 12.0
TICKERS_TTL_SECONDS = 24 * 3600  # ticker->CIK map changes slowly
FACTS_TTL_SECONDS = 3600  # fundamentals change at filing cadence
_MIN_REQUEST_INTERVAL = 0.15  # ~<=7 req/s, safely under the SEC 10 req/s limit

ANNUAL_FORMS = {"10-K", "20-F", "40-F", "10-K/A", "20-F/A"}

# Candidate US-GAAP tags per concept (companies tag inconsistently; first hit wins).
_CONCEPT_TAGS: dict[str, list[str]] = {
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
        "SalesRevenueNet",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
    ],
    "cost_of_revenue": ["CostOfRevenue", "CostOfGoodsAndServicesSold", "CostOfGoodsSold"],
    "gross_profit": ["GrossProfit"],
    "operating_income": ["OperatingIncomeLoss"],
    "net_income": ["NetIncomeLoss", "ProfitLoss"],
    "total_assets": ["Assets"],
    "total_liabilities": ["Liabilities"],
    "stockholders_equity": [
        "StockholdersEquity",
        "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
    ],
    "cash_and_equivalents": [
        "CashAndCashEquivalentsAtCarryingValue",
        "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
    ],
}


class ProviderError(RuntimeError):
    """An EDGAR data fetch failed or returned no usable data."""


# --------------------------------------------------------------------------- #
# TTL cache + fair-access throttle
# --------------------------------------------------------------------------- #
_CACHE: dict[str, tuple[float, Any]] = {}
_CACHE_LOCK = threading.Lock()
_THROTTLE_LOCK = threading.Lock()
_last_request_at = 0.0


def reset_cache() -> None:
    with _CACHE_LOCK:
        _CACHE.clear()


def _cached(key: str, ttl: int, producer):
    now = time.time()
    with _CACHE_LOCK:
        hit = _CACHE.get(key)
        if hit and hit[0] > now:
            return hit[1]
    value = producer()
    with _CACHE_LOCK:
        _CACHE[key] = (now + ttl, value)
    return value


def _http_get_json(url: str) -> Any:
    global _last_request_at
    with _THROTTLE_LOCK:
        delta = time.time() - _last_request_at
        if delta < _MIN_REQUEST_INTERVAL:
            time.sleep(_MIN_REQUEST_INTERVAL - delta)
        _last_request_at = time.time()
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - normalize all network/parse failures
        raise ProviderError(f"EDGAR request failed: {exc}") from exc


# --------------------------------------------------------------------------- #
# Module-level fetchers (monkeypatchable in tests)
# --------------------------------------------------------------------------- #
def company_tickers() -> dict[str, Any]:
    """Raw SEC ticker->CIK map (https://www.sec.gov/files/company_tickers.json)."""
    return _http_get_json("https://www.sec.gov/files/company_tickers.json")


def company_facts(cik10: str) -> dict[str, Any]:
    """companyfacts JSON for a zero-padded 10-digit CIK."""
    return _http_get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json")


# --------------------------------------------------------------------------- #
# Resolution + normalization
# --------------------------------------------------------------------------- #
def _ticker_index() -> dict[str, tuple[str, str]]:
    """Map UPPER ticker -> (cik10, title)."""
    raw = _cached("edgar:tickers", TICKERS_TTL_SECONDS, company_tickers)
    index: dict[str, tuple[str, str]] = {}
    # The map is {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}, ...}
    for row in raw.values():
        try:
            ticker = str(row["ticker"]).upper()
            cik10 = str(int(row["cik_str"])).zfill(10)
            index[ticker] = (cik10, str(row.get("title", "")))
        except (KeyError, ValueError, TypeError):
            continue
    return index


def ticker_to_cik(ticker: str) -> tuple[str, str]:
    """Resolve a ticker to (cik10, entity_name). Raises ProviderError if unknown."""
    key = ticker.strip().upper()
    if not key:
        raise ProviderError("Empty ticker.")
    index = _ticker_index()
    if key not in index:
        raise ProviderError(f"Ticker '{ticker}' not found in SEC EDGAR.")
    return index[key]


def _latest_annual(facts: dict[str, Any], tags: list[str]) -> tuple[float, int, str] | None:
    """Latest annual (10-K/20-F/40-F) USD value across candidate tags -> (val, fy, end)."""
    us_gaap = (facts.get("facts") or {}).get("us-gaap") or {}
    for tag in tags:
        node = us_gaap.get(tag)
        if not node:
            continue
        units = (node.get("units") or {}).get("USD") or []
        annual = [d for d in units if d.get("form") in ANNUAL_FORMS and d.get("end")]
        if not annual:
            continue
        best = max(annual, key=lambda d: d["end"])
        try:
            return float(best["val"]), int(best.get("fy") or 0), str(best["end"])
        except (KeyError, ValueError, TypeError):
            continue
    return None


def _safe_ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or not denominator:
        return None
    return round(numerator / denominator, 4)


def normalize(ticker: str) -> EdgarFinancials:
    cik10, entity_name = ticker_to_cik(ticker)
    facts = _cached(f"edgar:facts:{cik10}", FACTS_TTL_SECONDS, lambda: company_facts(cik10))
    if not entity_name:
        entity_name = str(facts.get("entityName") or ticker.upper())

    values: dict[str, float | None] = {}
    fy: int | None = None
    period_end: str | None = None
    for concept, tags in _CONCEPT_TAGS.items():
        hit = _latest_annual(facts, tags)
        if hit is None:
            values[concept] = None
            continue
        val, hit_fy, hit_end = hit
        values[concept] = val
        # Use revenue (else net income) as the headline statement period.
        if concept in ("revenue", "net_income") and period_end is None:
            fy, period_end = (hit_fy or None), hit_end

    # Derive gross profit if not directly disclosed.
    if values.get("gross_profit") is None and values.get("revenue") is not None and values.get(
        "cost_of_revenue"
    ) is not None:
        values["gross_profit"] = values["revenue"] - values["cost_of_revenue"]

    revenue = values.get("revenue")
    return EdgarFinancials(
        ticker=ticker.strip().upper(),
        cik=cik10,
        entity_name=entity_name,
        fiscal_year=fy,
        period_end=period_end,
        revenue=revenue,
        cost_of_revenue=values.get("cost_of_revenue"),
        gross_profit=values.get("gross_profit"),
        operating_income=values.get("operating_income"),
        net_income=values.get("net_income"),
        total_assets=values.get("total_assets"),
        total_liabilities=values.get("total_liabilities"),
        stockholders_equity=values.get("stockholders_equity"),
        cash_and_equivalents=values.get("cash_and_equivalents"),
        gross_margin=_safe_ratio(values.get("gross_profit"), revenue),
        operating_margin=_safe_ratio(values.get("operating_income"), revenue),
        net_margin=_safe_ratio(values.get("net_income"), revenue),
        as_of=datetime.now(timezone.utc),
    )


def _annual_series(facts: dict[str, Any], tags: list[str]) -> dict[int, float]:
    """Fiscal-year -> value across candidate tags (latest annual filing per year)."""
    us_gaap = (facts.get("facts") or {}).get("us-gaap") or {}
    for tag in tags:
        node = us_gaap.get(tag)
        if not node:
            continue
        units = (node.get("units") or {}).get("USD") or []
        by_year: dict[int, dict[str, Any]] = {}
        for d in units:
            if d.get("form") not in ANNUAL_FORMS or not d.get("end") or d.get("fy") is None:
                continue
            try:
                fy = int(d["fy"])
            except (ValueError, TypeError):
                continue
            if fy not in by_year or str(d["end"]) > str(by_year[fy]["end"]):
                by_year[fy] = d
        result: dict[int, float] = {}
        for fy, d in by_year.items():
            try:
                result[fy] = float(d["val"])
            except (ValueError, KeyError, TypeError):
                continue
        if result:
            return result
    return {}


def history(ticker: str, max_years: int = 5) -> EdgarHistory:
    cik10, entity_name = ticker_to_cik(ticker)
    facts = _cached(f"edgar:facts:{cik10}", FACTS_TTL_SECONDS, lambda: company_facts(cik10))
    if not entity_name:
        entity_name = str(facts.get("entityName") or ticker.upper())

    series = {concept: _annual_series(facts, tags) for concept, tags in _CONCEPT_TAGS.items()}
    all_years = set(series.get("revenue", {})) | set(series.get("net_income", {}))
    years = sorted(all_years)[-max_years:]

    rows: list[EdgarYear] = []
    for y in years:
        rev = series["revenue"].get(y)
        gp = series["gross_profit"].get(y)
        if gp is None and rev is not None and series["cost_of_revenue"].get(y) is not None:
            gp = rev - series["cost_of_revenue"][y]
        oi = series["operating_income"].get(y)
        ni = series["net_income"].get(y)
        rows.append(EdgarYear(
            fiscal_year=y,
            revenue=rev,
            cost_of_revenue=series["cost_of_revenue"].get(y),
            gross_profit=gp,
            operating_income=oi,
            net_income=ni,
            total_assets=series["total_assets"].get(y),
            total_liabilities=series["total_liabilities"].get(y),
            stockholders_equity=series["stockholders_equity"].get(y),
            cash_and_equivalents=series["cash_and_equivalents"].get(y),
            gross_margin=_safe_ratio(gp, rev),
            operating_margin=_safe_ratio(oi, rev),
            net_margin=_safe_ratio(ni, rev),
        ))
    return EdgarHistory(
        ticker=ticker.strip().upper(), cik=cik10, entity_name=entity_name,
        years=rows, as_of=datetime.now(timezone.utc),
    )


class EdgarService:
    """Thin service wrapper (parity with other JHI services)."""

    def financials(self, ticker: str) -> EdgarFinancials:
        return normalize(ticker)

    def history(self, ticker: str, max_years: int = 5) -> EdgarHistory:
        return history(ticker, max_years)
