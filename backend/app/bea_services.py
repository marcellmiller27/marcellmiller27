"""US Bureau of Economic Analysis (BEA) macro integration.

Public data; requires a free BEA API key (``BEA_API_KEY``). Exposes headline
national accounts (NIPA) indicators — GDP, PCE, real GDP growth, personal income.
BEA data is US public domain (display + redistribution permitted with attribution).

Pure standard-library HTTP so tests can monkeypatch the module-level fetcher.
"""

from __future__ import annotations

import json
import os
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

from app.bea_models import BeaIndicator, BeaMacroResponse

USER_AGENT = "John Henry Investments Research (research@johnhenrycapital.com)"
HTTP_TIMEOUT = 15.0
CACHE_TTL_SECONDS = 6 * 3600  # NIPA annual data changes rarely
_BASE = "https://apps.bea.gov/api/data"

# Curated headline indicators: (key, label, NIPA table, line number, unit).
_INDICATORS: list[tuple[str, str, str, str, str]] = [
    ("gdp", "US GDP (level)", "T10105", "1", "USD mn"),
    ("pce", "Personal Consumption Expenditures", "T10105", "2", "USD mn"),
    ("real_gdp_growth", "Real GDP (annual % change)", "T10101", "1", "%"),
    ("personal_income", "Personal Income", "T20100", "1", "USD mn"),
]


class ProviderError(RuntimeError):
    """A BEA fetch failed or returned no usable data."""


def bea_api_key() -> str | None:
    return os.getenv("BEA_API_KEY") or os.getenv("BEA_USER_ID")


# --------------------------------------------------------------------------- #
# Cache
# --------------------------------------------------------------------------- #
_CACHE: dict[str, tuple[float, Any]] = {}
_CACHE_LOCK = threading.Lock()


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
    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - normalize all network/parse failures
        raise ProviderError(f"BEA request failed: {exc}") from exc


def _recent_years(n: int = 6) -> str:
    year = datetime.now(timezone.utc).year
    return ",".join(str(y) for y in range(year - n, year + 1))


def bea_nipa(table: str, frequency: str = "A", years: str | None = None) -> list[dict[str, Any]]:
    """Fetch NIPA table rows (module-level so tests can monkeypatch it)."""
    key = bea_api_key()
    if not key:
        raise ProviderError("BEA_API_KEY is not configured.")
    url = (
        f"{_BASE}?UserID={urllib.parse.quote(key)}&method=GetData&datasetname=NIPA"
        f"&TableName={table}&Frequency={frequency}&Year={years or _recent_years()}"
        "&ResultFormat=json"
    )
    payload = _http_get_json(url)
    api = payload.get("BEAAPI") or {}
    if "Error" in api:
        raise ProviderError(str(api["Error"]))
    results = api.get("Results") or {}
    if isinstance(results, list):  # some errors return Results as a list
        results = results[0] if results else {}
    if results.get("Error"):
        raise ProviderError(str(results["Error"]))
    return results.get("Data") or []


def _latest(data: list[dict[str, Any]], line_number: str) -> tuple[float, str] | None:
    rows = [d for d in data if str(d.get("LineNumber")) == line_number and d.get("TimePeriod")]
    if not rows:
        return None
    best = max(rows, key=lambda d: str(d["TimePeriod"]))
    raw = str(best.get("DataValue", "")).replace(",", "").strip()
    try:
        return float(raw), str(best["TimePeriod"])
    except ValueError:
        return None


class BeaService:
    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def macro(self) -> BeaMacroResponse:
        if not bea_api_key():
            return BeaMacroResponse(
                as_of=self._now(),
                indicators=[
                    BeaIndicator(
                        key=k, label=label, unit=unit,
                        status="requires_credentials",
                        note="Set BEA_API_KEY to activate.",
                    )
                    for k, label, _table, _line, unit in _INDICATORS
                ],
            )

        # Group by table to minimize API calls (GDP + PCE share T10105).
        tables = {spec[2] for spec in _INDICATORS}
        table_data: dict[str, list[dict[str, Any]] | None] = {}
        for table in tables:
            try:
                table_data[table] = _cached(
                    f"bea:{table}", CACHE_TTL_SECONDS, lambda t=table: bea_nipa(t)
                )
            except ProviderError:
                table_data[table] = None

        indicators: list[BeaIndicator] = []
        for key, label, table, line, unit in _INDICATORS:
            data = table_data.get(table)
            if not data:
                indicators.append(
                    BeaIndicator(key=key, label=label, unit=unit, status="unavailable",
                                 note="BEA fetch failed.")
                )
                continue
            hit = _latest(data, line)
            if hit is None:
                indicators.append(
                    BeaIndicator(key=key, label=label, unit=unit, status="unavailable")
                )
            else:
                value, period = hit
                indicators.append(
                    BeaIndicator(key=key, label=label, value=value, unit=unit,
                                 period=period, status="ok",
                                 note=f"BEA NIPA {table} line {line}, {period}.")
                )
        return BeaMacroResponse(as_of=self._now(), indicators=indicators)
