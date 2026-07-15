"""No-key public macro sources: US Treasury, World Bank, IMF, OECD.

All free and (US Treasury) public domain / (WB, OECD) mostly CC-BY / (IMF)
free with attribution — broadly displayable and redistributable. Pure stdlib
HTTP; module-level fetchers are monkeypatchable in tests.
"""

from __future__ import annotations

import json
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

from app.public_macro_models import MacroPoint, MacroSeriesResponse

USER_AGENT = "John Henry Investments Research (research@johnhenrycapital.com)"
HTTP_TIMEOUT = 20.0
CACHE_TTL_SECONDS = 6 * 3600

# World Bank curated indicators (id, label, unit)
_WB: list[tuple[str, str, str]] = [
    ("NY.GDP.MKTP.CD", "GDP (current US$)", "USD"),
    ("NY.GDP.MKTP.KD.ZG", "GDP growth", "%"),
    ("FP.CPI.TOTL.ZG", "Inflation (CPI)", "%"),
    ("SL.UEM.TOTL.ZS", "Unemployment", "%"),
    ("SP.POP.TOTL", "Population", "count"),
]

# IMF WEO datamapper indicators (code, label, unit)
_IMF: list[tuple[str, str, str]] = [
    ("NGDP_RPCH", "Real GDP growth", "%"),
    ("PCPIPCH", "Inflation (avg CPI)", "%"),
    ("LUR", "Unemployment rate", "%"),
    ("GGXWDG_NGDP", "Govt gross debt (% GDP)", "%"),
]


class ProviderError(RuntimeError):
    """A public-macro fetch failed."""


# --------------------------------------------------------------------------- #
# Cache + HTTP
# --------------------------------------------------------------------------- #
_CACHE: dict[str, tuple[float, Any]] = {}
_CACHE_LOCK = threading.Lock()


def reset_cache() -> None:
    with _CACHE_LOCK:
        _CACHE.clear()


def _cached(key: str, producer):
    now = time.time()
    with _CACHE_LOCK:
        hit = _CACHE.get(key)
        if hit and hit[0] > now:
            return hit[1]
    value = producer()
    with _CACHE_LOCK:
        _CACHE[key] = (now + CACHE_TTL_SECONDS, value)
    return value


def _http_get_json(url: str, headers: dict[str, str] | None = None) -> Any:
    hdrs = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    request = urllib.request.Request(url, headers=hdrs)
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        raise ProviderError(str(exc)) from exc


# --------------------------------------------------------------------------- #
# Module-level fetchers (monkeypatchable)
# --------------------------------------------------------------------------- #
def fetch_treasury_debt() -> dict[str, Any]:
    url = (
        "https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v2/"
        "accounting/od/debt_to_penny?sort=-record_date&page%5Bsize%5D=1"
    )
    data = _http_get_json(url).get("data") or []
    if not data:
        raise ProviderError("No Treasury debt data.")
    return data[0]


def fetch_world_bank(country: str, indicator: str) -> Any:
    url = (
        f"https://api.worldbank.org/v2/country/{urllib.parse.quote(country)}"
        f"/indicator/{indicator}?format=json&mrv=1"
    )
    return _http_get_json(url)


def fetch_imf(indicator: str, country: str) -> dict[str, Any]:
    url = f"https://www.imf.org/external/datamapper/api/v1/{indicator}/{country}"
    return _http_get_json(url)


def fetch_oecd_cli(country: str) -> dict[str, Any]:
    url = (
        "https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_STES@DF_CLI,4.0/"
        f"{country}.M.LI...AA...H?lastNObservations=1&dimensionAtObservation=AllDimensions"
    )
    return _http_get_json(url, headers={"Accept": "application/vnd.sdmx.data+json"})


# --------------------------------------------------------------------------- #
# Parsing helpers
# --------------------------------------------------------------------------- #
def _f(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _imf_latest(values: dict[str, Any], indicator: str, country: str) -> tuple[float, str] | None:
    series = (values.get("values") or {}).get(indicator, {}).get(country, {})
    if not series:
        return None
    current_year = _now().year
    # Prefer the most recent actual/estimate (year <= current), else latest projection.
    actual = {y: v for y, v in series.items() if y.isdigit() and int(y) <= current_year}
    pick = actual or series
    year = max(pick, key=lambda y: int(y) if y.isdigit() else -1)
    val = _f(pick[year])
    return (val, year) if val is not None else None


# --------------------------------------------------------------------------- #
# Service
# --------------------------------------------------------------------------- #
class PublicMacroService:
    def treasury(self) -> MacroSeriesResponse:
        indicators: list[MacroPoint] = []
        try:
            row = _cached("treasury:debt", fetch_treasury_debt)
            period = row.get("record_date")
            indicators.append(MacroPoint(
                key="total_public_debt", label="Total public debt outstanding",
                value=_f(row.get("tot_pub_debt_out_amt")), unit="USD", period=period,
                country="US", note="US Treasury Fiscal Data (debt to penny).",
            ))
            indicators.append(MacroPoint(
                key="debt_held_by_public", label="Debt held by the public",
                value=_f(row.get("debt_held_public_amt")), unit="USD", period=period,
                country="US",
            ))
        except ProviderError as exc:
            indicators.append(MacroPoint(key="total_public_debt", label="Total public debt outstanding",
                                         unit="USD", status="unavailable", note=str(exc)))
        return MacroSeriesResponse(source="US Treasury (Fiscal Data)", as_of=_now(),
                                   country="US", indicators=indicators)

    def world_bank(self, country: str = "US") -> MacroSeriesResponse:
        indicators: list[MacroPoint] = []
        for ind, label, unit in _WB:
            try:
                raw = _cached(f"wb:{country}:{ind}", lambda i=ind: fetch_world_bank(country, i))
                rows = raw[1] if isinstance(raw, list) and len(raw) > 1 else []
                row = rows[0] if rows else {}
                val = _f(row.get("value"))
                if val is None:
                    indicators.append(MacroPoint(key=ind, label=label, unit=unit,
                                                 country=country, status="unavailable"))
                else:
                    indicators.append(MacroPoint(key=ind, label=label, value=val, unit=unit,
                                                 period=str(row.get("date")), country=country))
            except ProviderError as exc:
                indicators.append(MacroPoint(key=ind, label=label, unit=unit, country=country,
                                             status="unavailable", note=str(exc)))
        return MacroSeriesResponse(source="World Bank (WDI)", as_of=_now(),
                                   country=country, indicators=indicators)

    def imf(self, country: str = "USA") -> MacroSeriesResponse:
        indicators: list[MacroPoint] = []
        for code, label, unit in _IMF:
            try:
                raw = _cached(f"imf:{code}:{country}", lambda c=code: fetch_imf(c, country))
                hit = _imf_latest(raw, code, country)
                if hit is None:
                    indicators.append(MacroPoint(key=code, label=label, unit=unit,
                                                 country=country, status="unavailable"))
                else:
                    val, year = hit
                    indicators.append(MacroPoint(key=code, label=label, value=val, unit=unit,
                                                 period=year, country=country,
                                                 note="IMF WEO (may include estimates/projections)."))
            except ProviderError as exc:
                indicators.append(MacroPoint(key=code, label=label, unit=unit, country=country,
                                             status="unavailable", note=str(exc)))
        return MacroSeriesResponse(source="IMF (WEO)", as_of=_now(),
                                   country=country, indicators=indicators)

    def oecd(self, country: str = "USA") -> MacroSeriesResponse:
        indicators: list[MacroPoint] = []
        try:
            raw = _cached(f"oecd:cli:{country}", lambda: fetch_oecd_cli(country))
            datasets = (raw.get("data") or {}).get("dataSets") or []
            obs = datasets[0].get("observations", {}) if datasets else {}
            value = None
            if obs:
                first = next(iter(obs.values()))
                value = _f(first[0]) if first else None
            if value is None:
                indicators.append(MacroPoint(key="cli", label="Composite Leading Indicator",
                                             unit="index", country=country, status="unavailable"))
            else:
                indicators.append(MacroPoint(key="cli", label="Composite Leading Indicator",
                                             value=round(value, 2), unit="index", country=country,
                                             note="OECD CLI, amplitude-adjusted (100 = trend)."))
        except ProviderError as exc:
            indicators.append(MacroPoint(key="cli", label="Composite Leading Indicator",
                                         unit="index", country=country, status="unavailable",
                                         note=str(exc)))
        return MacroSeriesResponse(source="OECD (MEI/CLI)", as_of=_now(),
                                   country=country, indicators=indicators)
