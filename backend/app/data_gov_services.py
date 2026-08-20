# JHI-SIG: 69M2705M | US government economic data adapter (api.data.gov) | JHI Research & Analytics Firm, Inc. (proprietary)
"""US government ECONOMIC / financial data integration.

High-value public feeds for the Economics + acquisition/financials work:

  - **US Treasury Fiscal Data** (``api.fiscaldata.treasury.gov``) — KEYLESS/public.
    Debt-to-penny + average interest rates on marketable Treasury securities.
  - **FDIC BankFind Suite** (``api.fdic.gov/banks``) — KEYLESS/public. Number of
    FDIC-insured institutions + per-institution financial health (ROA/ROE/assets).
  - **EIA** energy/commodities (``api.eia.gov/v2``) — REQUIRES a key. EIA accepts the
    founder's shared **api.data.gov** key (``DATA_GOV_API_KEY``) as its ``api_key``, and
    a dedicated ``EIA_API_KEY`` overrides it when set. WTI crude, Henry Hub natural gas,
    and US retail electricity price.

Design (mirrors ``market_services`` / ``bea_services`` exactly):
  - Pure standard library (``urllib``) — no new runtime dependency.
  - Whitespace-stripped key accessors (dashboard-pasted secrets can carry a stray
    newline; a padded key must not be silently rejected).
  - Short/long TTL in-memory cache + transient-failure retry with exponential backoff.
  - Graceful degradation: a missing key returns ``requires_credentials`` and a fetch
    failure returns ``unavailable`` — NEVER a fabricated value.
  - As-of dating: every value carries its actual data date/period and a cadence-aware
    as-of label (Data Foundation doctrine, via ``data_registry``).

The api.data.gov key works via the ``X-Api-Key`` header (or ``api_key`` query param) but
ONLY on api.data.gov-fronted / participating APIs; Treasury and FDIC are keyless-but-
valuable and are integrated without any key.
"""

from __future__ import annotations

import json
import os
import threading
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any, Callable

from app import data_registry as dr
from app.data_gov_models import GovIndicator, GovSeriesResponse

USER_AGENT = "John Henry Investments Research (research@johnhenrycapital.com)"
HTTP_TIMEOUT = 20.0
CACHE_TTL_SECONDS = 6 * 3600  # government macro/fiscal data refreshes slowly
RETRY_ATTEMPTS = 3
RETRY_BASE_DELAY = 0.4  # seconds; exponential backoff (0.4s, 0.8s, ...)

_TREASURY_BASE = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"
_FDIC_BASE = "https://api.fdic.gov/banks"
_EIA_BASE = "https://api.eia.gov/v2"


def _env_key(*names: str) -> str | None:
    """First non-empty environment value among ``names``, whitespace-stripped.

    Secrets pasted through a dashboard often pick up a stray leading/trailing newline
    or space (see PR #175). We defensively strip so a present-but-padded key is not
    silently rejected by the upstream API.
    """
    for name in names:
        raw = os.getenv(name)
        if raw is not None:
            cleaned = raw.strip()
            if cleaned:
                return cleaned
    return None


def data_gov_api_key() -> str | None:
    """The founder's shared api.data.gov key (whitespace-stripped)."""
    return _env_key("DATA_GOV_API_KEY")


def eia_api_key() -> str | None:
    """EIA key: a dedicated ``EIA_API_KEY`` if set, else the shared api.data.gov key.

    EIA runs its own key registry but accepts api.data.gov keys, so the founder's
    ``DATA_GOV_API_KEY`` activates EIA out of the box; a separate ``EIA_API_KEY`` can
    override it (e.g. for rate-limit isolation) without a code change.
    """
    return _env_key("EIA_API_KEY", "DATA_GOV_API_KEY")


class ProviderError(RuntimeError):
    """A government-data fetch failed or returned no usable data."""


# --------------------------------------------------------------------------- #
# Cache + retry
# --------------------------------------------------------------------------- #
_CACHE: dict[str, tuple[float, Any]] = {}
_CACHE_LOCK = threading.Lock()


def reset_cache() -> None:
    with _CACHE_LOCK:
        _CACHE.clear()


def _cached(key: str, ttl: int, producer: Callable[[], Any]) -> Any:
    if ttl <= 0:
        return producer()
    now = time.time()
    with _CACHE_LOCK:
        hit = _CACHE.get(key)
        if hit and hit[0] > now:
            return hit[1]
    value = producer()
    with _CACHE_LOCK:
        _CACHE[key] = (now + ttl, value)
    return value


def _retry(
    producer: Callable[[], Any],
    attempts: int = RETRY_ATTEMPTS,
    base_delay: float = RETRY_BASE_DELAY,
) -> Any:
    """Call ``producer``, retrying transient :class:`ProviderError`s with exponential
    backoff. Re-raises the last error if every attempt fails. ``base_delay <= 0``
    disables sleeping (used in tests)."""
    last_error: Exception | None = None
    for attempt in range(max(1, attempts)):
        try:
            return producer()
        except ProviderError as exc:
            last_error = exc
            if attempt < attempts - 1 and base_delay > 0:
                time.sleep(base_delay * (2 ** attempt))
    assert last_error is not None
    raise last_error


def _cached_retry(key: str, producer: Callable[[], Any]) -> Any:
    return _cached(key, CACHE_TTL_SECONDS, lambda: _retry(producer))


# --------------------------------------------------------------------------- #
# Low-level HTTP + module-level fetchers (monkeypatchable in tests)
# --------------------------------------------------------------------------- #
def _http_get_json(url: str, headers: dict[str, str] | None = None) -> Any:
    hdrs = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    request = urllib.request.Request(url, headers=hdrs)
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - normalize all network/parse failures
        raise ProviderError(str(exc)) from exc


def fetch_treasury(path: str, params: dict[str, str]) -> list[dict[str, Any]]:
    """GET a US Treasury Fiscal Data v1/v2 endpoint (keyless). Returns the ``data`` list."""
    url = f"{_TREASURY_BASE}/{path}?{urllib.parse.urlencode(params)}"
    payload = _http_get_json(url)
    data = payload.get("data") if isinstance(payload, dict) else None
    if not data:
        raise ProviderError(f"No Treasury data for {path}.")
    return data


def fetch_fdic(path: str, params: dict[str, str]) -> dict[str, Any]:
    """GET an FDIC BankFind Suite endpoint (keyless). Returns the raw payload
    (``meta`` + ``data``) so callers can read aggregate counts as well as rows."""
    url = f"{_FDIC_BASE}/{path}?{urllib.parse.urlencode(params)}"
    payload = _http_get_json(url)
    if not isinstance(payload, dict):
        raise ProviderError(f"Bad FDIC payload for {path}.")
    return payload


def fetch_eia(route: str, params: list[tuple[str, str]]) -> dict[str, Any]:
    """GET an EIA v2 data route. Sends the key as ``api_key`` (EIA accepts api.data.gov
    keys). Raises :class:`ProviderError` when no key is configured or EIA errors."""
    key = eia_api_key()
    if not key:
        raise ProviderError("No EIA key (set EIA_API_KEY or DATA_GOV_API_KEY).")
    query = [("api_key", key), *params]
    url = f"{_EIA_BASE}/{route}?{urllib.parse.urlencode(query)}"
    payload = _http_get_json(url)
    if not isinstance(payload, dict) or payload.get("error"):
        message = payload.get("error") if isinstance(payload, dict) else "bad response"
        raise ProviderError(f"EIA error for {route}: {message}")
    response = payload.get("response") or {}
    rows = response.get("data") or []
    if not rows:
        raise ProviderError(f"No EIA data for {route}.")
    return response


# --------------------------------------------------------------------------- #
# Parsing / labeling helpers
# --------------------------------------------------------------------------- #
def _f(value: Any) -> float | None:
    if value in (None, "", "null"):
        return None
    try:
        return float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _ok_indicator(
    series_id: str,
    key: str,
    label: str,
    value: float | None,
    unit: str,
    period: str | None,
    cadence: dr.Cadence,
    note: str | None = None,
) -> GovIndicator:
    """Build an ``ok`` indicator, threading the as-of / cadence / freshness labeling.

    A parsed-but-null value degrades to ``unavailable`` (never a fabricated number)."""
    if value is None:
        return _unavailable(key, label, unit, cadence, "No value in upstream response.")
    return GovIndicator(
        key=key,
        label=label,
        value=value,
        unit=unit,
        period=period,
        status="ok",
        cadence=cadence.value,
        as_of_label=dr.as_of_label(cadence, period),
        freshness=dr.classify_freshness(cadence, period, _now()),
        note=note,
    )


def _unavailable(
    key: str, label: str, unit: str, cadence: dr.Cadence, note: str
) -> GovIndicator:
    return GovIndicator(
        key=key, label=label, unit=unit, status="unavailable",
        cadence=cadence.value, as_of_label=dr.as_of_label(cadence, None),
        freshness=dr.FRESH_FAILED, note=note,
    )


def _requires_credentials(
    key: str, label: str, unit: str, cadence: dr.Cadence, note: str
) -> GovIndicator:
    return GovIndicator(
        key=key, label=label, unit=unit, status="requires_credentials",
        cadence=cadence.value, as_of_label=dr.as_of_label(cadence, None), note=note,
    )


# --------------------------------------------------------------------------- #
# Provider status (surfaced in /market/providers)
# --------------------------------------------------------------------------- #
def eia_provider_status() -> str:
    return "live" if eia_api_key() else "requires_credentials"


# --------------------------------------------------------------------------- #
# Service
# --------------------------------------------------------------------------- #
class DataGovService:
    # -- US Treasury Fiscal Data (keyless) --------------------------------- #
    def treasury_fiscal(self) -> GovSeriesResponse:
        indicators: list[GovIndicator] = []
        indicators.extend(self._treasury_debt())
        indicators.extend(self._treasury_avg_rates())
        return GovSeriesResponse(
            source="US Treasury (Fiscal Data)",
            provider="us_treasury_fiscal",
            as_of=_now(),
            requires_key=False,
            key_status="live",
            indicators=indicators,
        )

    def _treasury_debt(self) -> list[GovIndicator]:
        cadence = dr.Cadence.DAILY
        try:
            rows = _cached_retry(
                "treasury:debt",
                lambda: fetch_treasury(
                    "v2/accounting/od/debt_to_penny",
                    {"sort": "-record_date", "page[size]": "1"},
                ),
            )
        except ProviderError as exc:
            return [
                _unavailable("total_public_debt", "Total public debt outstanding",
                             "USD", cadence, str(exc)),
                _unavailable("debt_held_by_public", "Debt held by the public",
                             "USD", cadence, str(exc)),
            ]
        row = rows[0]
        period = row.get("record_date")
        return [
            _ok_indicator("TREASURY_TOTAL_DEBT", "total_public_debt",
                          "Total public debt outstanding", _f(row.get("tot_pub_debt_out_amt")),
                          "USD", period, cadence, "US Treasury debt to the penny."),
            _ok_indicator("TREASURY_DEBT_HELD_PUBLIC", "debt_held_by_public",
                          "Debt held by the public", _f(row.get("debt_held_public_amt")),
                          "USD", period, cadence),
        ]

    # Map security_desc -> (series_id, key, label).
    _AVG_RATE_SECURITIES = [
        ("Total Marketable", "TREASURY_AVG_RATE_MARKETABLE", "avg_rate_marketable",
         "Avg interest rate · total marketable"),
        ("Treasury Bills", "TREASURY_AVG_RATE_TBILLS", "avg_rate_tbills",
         "Avg interest rate · Treasury Bills"),
        ("Treasury Notes", "TREASURY_AVG_RATE_TNOTES", "avg_rate_tnotes",
         "Avg interest rate · Treasury Notes"),
        ("Treasury Bonds", "TREASURY_AVG_RATE_TBONDS", "avg_rate_tbonds",
         "Avg interest rate · Treasury Bonds"),
    ]

    def _treasury_avg_rates(self) -> list[GovIndicator]:
        cadence = dr.Cadence.MONTHLY
        try:
            rows = _cached_retry(
                "treasury:avg_rates",
                lambda: fetch_treasury(
                    "v2/accounting/od/avg_interest_rates",
                    {"sort": "-record_date", "page[size]": "30"},
                ),
            )
        except ProviderError as exc:
            return [
                _unavailable(key, label, "%", cadence, str(exc))
                for _desc, _sid, key, label in self._AVG_RATE_SECURITIES
            ]
        # Keep only the most recent record_date (the API returns each security once/month).
        latest_date = max((r.get("record_date") or "" for r in rows), default="")
        by_desc = {
            r.get("security_desc"): r for r in rows if r.get("record_date") == latest_date
        }
        out: list[GovIndicator] = []
        for desc, series_id, key, label in self._AVG_RATE_SECURITIES:
            row = by_desc.get(desc)
            if not row:
                out.append(_unavailable(key, label, "%", cadence,
                                        f"No '{desc}' row in latest release."))
                continue
            out.append(_ok_indicator(
                series_id, key, label, _f(row.get("avg_interest_rate_amt")),
                "%", row.get("record_date"), cadence,
                f"US Treasury average interest rate ({desc}).",
            ))
        return out

    # -- FDIC BankFind Suite (keyless) ------------------------------------- #
    def banking(self) -> GovSeriesResponse:
        cadence = dr.Cadence.QUARTERLY
        indicators: list[GovIndicator] = []
        try:
            inst = _cached_retry(
                "fdic:active_count",
                lambda: fetch_fdic(
                    "institutions",
                    {"filters": "ACTIVE:1", "fields": "CERT", "limit": "1",
                     "format": "json"},
                ),
            )
            count = ((inst.get("meta") or {}).get("total"))
            period = self._fdic_latest_repdte()
            indicators.append(_ok_indicator(
                "FDIC_INSURED_INSTITUTIONS", "insured_institutions",
                "FDIC-insured institutions (active)", _f(count), "count", period, cadence,
                "Count of active FDIC-insured institutions.",
            ))
        except ProviderError as exc:
            indicators.append(_unavailable(
                "insured_institutions", "FDIC-insured institutions (active)",
                "count", cadence, str(exc)))
        return GovSeriesResponse(
            source="FDIC BankFind Suite",
            provider="fdic_bankfind",
            as_of=_now(),
            requires_key=False,
            key_status="live",
            indicators=indicators,
        )

    def _fdic_latest_repdte(self) -> str | None:
        """Most recent call-report date (REPDTE), formatted as an ISO date for as-of."""
        try:
            fin = _cached_retry(
                "fdic:latest_repdte",
                lambda: fetch_fdic(
                    "financials",
                    {"fields": "REPDTE", "sort_by": "REPDTE", "sort_order": "DESC",
                     "limit": "1", "format": "json"},
                ),
            )
        except ProviderError:
            return None
        rows = fin.get("data") or []
        if not rows:
            return None
        repdte = str((rows[0].get("data") or {}).get("REPDTE") or "")
        if len(repdte) == 8 and repdte.isdigit():  # YYYYMMDD -> YYYY-MM-DD
            return f"{repdte[:4]}-{repdte[4:6]}-{repdte[6:]}"
        return repdte or None

    def institution_financials(self, cert: str) -> GovSeriesResponse:
        """Per-institution financial health for one FDIC cert (acquisition/financials
        support): assets, deposits, net income, ROA, ROE — as-of the latest call report."""
        cadence = dr.Cadence.QUARTERLY
        fields = "CERT,NAME,ASSET,DEP,NETINC,ROA,ROE,REPDTE"
        specs = [
            ("ASSET", "asset", "Total assets", "USD th"),
            ("DEP", "deposits", "Total deposits", "USD th"),
            ("NETINC", "net_income", "Net income", "USD th"),
            ("ROA", "roa", "Return on assets", "%"),
            ("ROE", "roe", "Return on equity", "%"),
        ]
        try:
            payload = _cached_retry(
                f"fdic:inst:{cert}",
                lambda: fetch_fdic(
                    "financials",
                    {"filters": f"CERT:{cert}", "fields": fields, "sort_by": "REPDTE",
                     "sort_order": "DESC", "limit": "1", "format": "json"},
                ),
            )
            rows = payload.get("data") or []
            if not rows:
                raise ProviderError(f"No FDIC financials for CERT {cert}.")
            row = rows[0].get("data") or {}
        except ProviderError as exc:
            return GovSeriesResponse(
                source="FDIC BankFind Suite", provider="fdic_bankfind", as_of=_now(),
                requires_key=False, key_status="live",
                indicators=[_unavailable(k, label, unit, cadence, str(exc))
                            for _col, k, label, unit in specs],
            )
        repdte = str(row.get("REPDTE") or "")
        period = f"{repdte[:4]}-{repdte[4:6]}-{repdte[6:]}" if len(repdte) == 8 else repdte
        name = row.get("NAME") or f"CERT {cert}"
        indicators = [
            _ok_indicator(f"FDIC_{col}", key, f"{name} · {label}", _f(row.get(col)),
                          unit, period, cadence)
            for col, key, label, unit in specs
        ]
        return GovSeriesResponse(
            source="FDIC BankFind Suite", provider="fdic_bankfind", as_of=_now(),
            requires_key=False, key_status="live", indicators=indicators,
        )

    # -- EIA energy / commodities (requires a key) ------------------------- #
    _EIA_FEEDS = [
        # (series_id, key, label, unit, cadence, route, series_code, value_col)
        ("EIA_WTI", "wti_crude", "WTI crude oil spot", "USD/bbl", dr.Cadence.DAILY,
         "petroleum/pri/spt", "RWTC", "value"),
        ("EIA_HENRY_HUB", "henry_hub_natgas", "Henry Hub natural gas spot",
         "USD/MMBtu", dr.Cadence.DAILY, "natural-gas/pri/fut", "RNGWHHD", "value"),
        ("EIA_ELECTRICITY_PRICE", "electricity_price",
         "US retail electricity price (all sectors)", "cents/kWh", dr.Cadence.MONTHLY,
         None, None, "price"),
    ]

    def energy(self) -> GovSeriesResponse:
        keyed = eia_api_key()
        indicators: list[GovIndicator] = []
        for series_id, key, label, unit, cadence, route, series_code, col in self._EIA_FEEDS:
            if not keyed:
                indicators.append(_requires_credentials(
                    key, label, unit, cadence,
                    "Set EIA_API_KEY or DATA_GOV_API_KEY to activate EIA.",
                ))
                continue
            indicators.append(
                self._eia_indicator(series_id, key, label, unit, cadence, route,
                                    series_code, col)
            )
        return GovSeriesResponse(
            source="US Energy Information Administration (EIA)",
            provider="eia",
            as_of=_now(),
            requires_key=True,
            key_status=eia_provider_status(),
            indicators=indicators,
        )

    def _eia_indicator(
        self, series_id: str, key: str, label: str, unit: str, cadence: dr.Cadence,
        route: str | None, series_code: str | None, col: str,
    ) -> GovIndicator:
        try:
            if series_code:  # spot-price routes filtered by series id
                response = _cached_retry(
                    f"eia:{series_id}",
                    lambda: fetch_eia(
                        f"{route}/data/",
                        [("frequency", "daily"), ("data[]", col),
                         ("facets[series][]", series_code),
                         ("sort[0][column]", "period"), ("sort[0][direction]", "desc"),
                         ("length", "1")],
                    ),
                )
            else:  # retail electricity price (US total, all sectors, monthly)
                response = _cached_retry(
                    f"eia:{series_id}",
                    lambda: fetch_eia(
                        "electricity/retail-sales/data/",
                        [("frequency", "monthly"), ("data[]", col),
                         ("facets[stateid][]", "US"), ("facets[sectorid][]", "ALL"),
                         ("sort[0][column]", "period"), ("sort[0][direction]", "desc"),
                         ("length", "1")],
                    ),
                )
        except ProviderError as exc:
            return _unavailable(key, label, unit, cadence, str(exc))
        rows = response.get("data") or []
        row = rows[0] if rows else {}
        return _ok_indicator(series_id, key, label, _f(row.get(col)), unit,
                             row.get("period"), cadence, "US EIA open data.")
