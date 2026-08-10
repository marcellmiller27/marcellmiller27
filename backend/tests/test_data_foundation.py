# JHI-SIG: 69M2705M | Data Foundation Phase 1 — network-free tests | JHI Research & Analytics Firm, Inc. (proprietary)
"""Network-free coverage for the Data Foundation (Phase 1):

  - series registry lookups + cadence/license metadata
  - as-of / cadence labeling ("Monthly · as of Jun 2026")
  - freshness-state classification (current on-cadence / overdue / fetch-failed)
  - last-good fallback (serve last-known value with its as-of, never a hole)
  - chart partial-render (never [] when only one series is present)
  - no-fabrication (a missing series is disclosed as pending, never invented)

Every test is deterministic and hits no network (providers are monkeypatched / values
are hand-built), so this file must stay green in CI.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from app import data_registry as dr
from app import market_services
from app.data_registry import (
    FRESH_CURRENT,
    FRESH_FAILED,
    FRESH_OVERDUE,
    Cadence,
    LicenseClass,
    Source,
)
from app.market_models import Quote
from app.market_services import MarketDataService, ProviderError
from app.newsletter_content import build_edition


@pytest.fixture(autouse=True)
def _isolate_caches():
    market_services.reset_cache()
    market_services.reset_last_good()
    yield
    market_services.reset_cache()
    market_services.reset_last_good()


# ── Registry ─────────────────────────────────────────────────────────────────
def test_registry_covers_core_series_with_cadence_and_license() -> None:
    fed = dr.get_series("FED_FUNDS")
    assert fed is not None
    assert fed.source == Source.FRED
    assert fed.cadence == Cadence.MONTHLY
    assert fed.unit == "%"
    assert fed.license_class == LicenseClass.PUBLIC

    gdp = dr.get_series("GDP")
    assert gdp.cadence == Cadence.QUARTERLY  # GDP is quarterly, not monthly

    spx = dr.get_series("SPX")
    assert spx.source == Source.PRICES and spx.cadence == Cadence.DAILY

    cpi = dr.get_series("INFLATION")
    assert cpi.source == Source.BLS and cpi.cadence == Cadence.MONTHLY


def test_registry_marks_sf1_licensed_derived_only() -> None:
    sf1 = dr.get_series("SF1_FUNDAMENTALS")
    assert sf1 is not None
    assert sf1.source == Source.SF1
    assert sf1.license_class == LicenseClass.LICENSED_DERIVED_ONLY


def test_registry_lookup_is_case_insensitive_and_defaults() -> None:
    assert dr.get_series("fed_funds") is dr.get_series("FED_FUNDS")
    assert dr.get_series("NOT_A_SERIES") is None
    # Unregistered symbol defaults to a daily-quoted equity ticker cadence.
    assert dr.cadence_for("ZZZZ") == Cadence.DAILY


# ── As-of / cadence labeling ────────────────────────────────────────────────
def test_as_of_label_formats_by_cadence() -> None:
    assert dr.as_of_label(Cadence.MONTHLY, "2026-06-01") == "Monthly · as of Jun 2026"
    assert dr.as_of_label(Cadence.QUARTERLY, "2026-04-01") == "Quarterly · as of Q2 2026"
    assert dr.as_of_label(Cadence.ANNUAL, "2026-01-01") == "Annual · as of 2026"
    assert dr.as_of_label(Cadence.DAILY, "2026-06-09") == "Daily · as of Jun 9, 2026"


def test_as_of_label_parses_bls_period_and_pending() -> None:
    # BLS-style "May 2026" period label round-trips through the monthly formatter.
    assert dr.as_of_label(Cadence.MONTHLY, "May 2026") == "Monthly · as of May 2026"
    # A genuinely unknown date discloses "pending" — never a fabricated stamp.
    assert dr.as_of_label(Cadence.MONTHLY, None).endswith("pending")


# ── Freshness classification ────────────────────────────────────────────────
def test_monthly_series_between_releases_is_current_not_missing() -> None:
    now = datetime(2026, 8, 1, tzinfo=timezone.utc)
    # A June monthly print, viewed in August (a few weeks later) → CURRENT.
    assert dr.classify_freshness(Cadence.MONTHLY, "2026-06-01", now) == FRESH_CURRENT


def test_overdue_when_observation_exceeds_cadence_window() -> None:
    now = datetime(2026, 8, 1, tzinfo=timezone.utc)
    # A monthly series last printed in early 2026 is well past its grace window.
    assert dr.classify_freshness(Cadence.MONTHLY, "2026-01-01", now) == FRESH_OVERDUE
    # Daily series stale by two weeks is overdue.
    assert dr.classify_freshness(Cadence.DAILY, "2026-07-15", now) == FRESH_OVERDUE


def test_daily_series_over_a_weekend_is_still_current() -> None:
    now = datetime(2026, 8, 3, tzinfo=timezone.utc)  # Monday
    assert dr.classify_freshness(Cadence.DAILY, "2026-07-31", now) == FRESH_CURRENT


def test_fetch_failed_overrides_age() -> None:
    now = datetime(2026, 8, 1, tzinfo=timezone.utc)
    state = dr.classify_freshness(Cadence.MONTHLY, "2026-06-01", now, fetch_failed=True)
    assert state == FRESH_FAILED


def test_irregular_series_present_is_current() -> None:
    assert dr.classify_freshness(Cadence.IRREGULAR, "2020-01-01") == FRESH_CURRENT


# ── Threaded onto quotes ────────────────────────────────────────────────────
def _fred_fixture(monkeypatch, series_value: tuple[float, str]) -> None:
    monkeypatch.setattr(market_services, "fred_series_latest", lambda sid: series_value)
    monkeypatch.setenv("FRED_API_KEY", "test-key")


def test_quote_carries_cadence_asof_and_freshness(monkeypatch) -> None:
    # FED_FUNDS observed today → current, monthly, with an as-of label.
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    _fred_fixture(monkeypatch, (4.5, today))
    q = MarketDataService(cache_ttl=0).quotes(["FED_FUNDS"]).quotes[0]
    assert q.status == "ok"
    assert q.price == 4.5
    assert q.cadence == "monthly"
    assert q.observation_date == today
    assert q.freshness == FRESH_CURRENT
    assert q.as_of_label.startswith("Monthly · as of")


# ── Last-good fallback ──────────────────────────────────────────────────────
def test_last_good_served_on_transient_failure(monkeypatch) -> None:
    calls = {"n": 0}

    def _flaky(_sid):
        calls["n"] += 1
        if calls["n"] == 1:
            return (4.5, "2026-06-01")
        raise ProviderError("network down")

    monkeypatch.setattr(market_services, "fred_series_latest", _flaky)
    monkeypatch.setenv("FRED_API_KEY", "test-key")
    svc = MarketDataService(cache_ttl=0, retry_delay=0)

    first = svc.quotes(["FED_FUNDS"]).quotes[0]
    assert first.status == "ok" and first.freshness == FRESH_CURRENT

    # Second call: upstream fails on every retry → serve last-good, flagged fetch-failed,
    # keeping the ORIGINAL observation date (never a hole, never a fabricated new value).
    second = svc.quotes(["FED_FUNDS"]).quotes[0]
    assert second.status == "ok"
    assert second.price == 4.5
    assert second.freshness == FRESH_FAILED
    assert second.observation_date == "2026-06-01"
    assert "last-good" in (second.note or "")


def test_retries_before_giving_up(monkeypatch) -> None:
    calls = {"n": 0}

    def _always_down(_sid):
        calls["n"] += 1
        raise ProviderError("boom")

    monkeypatch.setattr(market_services, "fred_series_latest", _always_down)
    monkeypatch.setenv("FRED_API_KEY", "test-key")
    svc = MarketDataService(cache_ttl=0, retry_attempts=3, retry_delay=0)

    q = svc.quotes(["FED_FUNDS"]).quotes[0]
    # No prior last-good → honest unavailable placeholder (never fabricated).
    assert q.status == "unavailable"
    assert q.price is None
    assert q.freshness == FRESH_FAILED
    assert calls["n"] == 3  # retried the configured number of attempts


# ── Chart partial-render + no-fabrication in the edition ────────────────────
def _quotes(*pairs: tuple[str, float | None]) -> list[Quote]:
    out: list[Quote] = []
    for sym, price in pairs:
        spec = dr.get_series(sym)
        out.append(Quote(
            symbol=sym, name=spec.name if spec else sym, asset_class="macro",
            price=price, unit=spec.unit if spec else "%", source="fred",
            cadence=(spec.cadence.value if spec else "monthly"),
            observation_date="2026-06-01" if price is not None else None,
            as_of_label=dr.as_of_label(spec.cadence if spec else Cadence.MONTHLY,
                                       "2026-06-01" if price is not None else None),
        ))
    return out


def test_macro_chart_renders_with_a_single_available_series() -> None:
    # Only CPI is present (Fed Funds + 10Y missing). The chart must still render, not [].
    now = datetime.now(timezone.utc)
    quotes = _quotes(("INFLATION", 3.1))
    ed = build_edition("economic-brief", quotes, now, full=True)
    assert len(ed.charts) >= 1
    assert ed.charts[0].image.startswith("data:image/png;base64,")


def test_edition_never_omits_missing_indicator_labels_pending() -> None:
    # Fed Funds missing (price None): the section still lists it, disclosed as pending.
    now = datetime.now(timezone.utc)
    quotes = _quotes(("FED_FUNDS", None), ("UST10Y", 4.2))
    ed = build_edition("economic-brief", quotes, now, full=True)
    monetary = next(g for g in ed.groups if g.heading == "Monetary Policy & Rates")
    labels = {it.label: it for it in monetary.items}
    assert "US Fed Funds Rate" in labels  # not omitted
    assert labels["US Fed Funds Rate"].value.startswith("pending")
    # The available series carries a real value + as-of disclosure.
    assert labels["US 10Y Treasury yield"].as_of_label.startswith("Daily · as of")


def test_no_fabrication_pending_value_has_no_number() -> None:
    now = datetime.now(timezone.utc)
    quotes = _quotes(("FED_FUNDS", None))
    ed = build_edition("economic-brief", quotes, now, full=True)
    monetary = next(g for g in ed.groups if g.heading == "Monetary Policy & Rates")
    ff = next(it for it in monetary.items if it.label == "US Fed Funds Rate")
    # Never invented: the pending placeholder contains no fabricated percentage.
    assert "%" not in ff.value
    assert "pending" in ff.value and "next release" in ff.value


# ── Refresh hook (network-free) ─────────────────────────────────────────────
def test_refresh_all_summarizes_freshness(monkeypatch) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    _fred_fixture(monkeypatch, (4.5, today))
    summary = MarketDataService(retry_delay=0).refresh_all(["FED_FUNDS", "GDP"])
    assert summary["requested"] == 2
    assert summary["current"] >= 1
    symbols = {s["symbol"] for s in summary["series"]}
    assert symbols == {"FED_FUNDS", "GDP"}
    assert all("as_of" in s for s in summary["series"])
