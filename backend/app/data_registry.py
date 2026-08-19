# JHI-SIG: 69M2705M | Data Foundation series registry + as-of/cadence/freshness | JHI Research & Analytics Firm, Inc. (proprietary)
"""Data Foundation — Phase 1: the central *series registry* and the as-of / cadence /
freshness primitives every data service threads through its values.

Design goals ("Always-Deliver · Cadence-Aware · As-Of-Disclosed"):

  - **Registry**: one lookup table describing every macro/market/fundamentals series —
    its id, source, release *cadence* (daily/weekly/monthly/quarterly/annual/irregular),
    unit, and license class. Services use this to reason about a value's expected refresh
    interval and to label it honestly.
  - **As-of everywhere**: a small typed wrapper (:class:`ObservedValue`) carries a value's
    actual data date (the observation/period it belongs to), the fetched-at timestamp, the
    source, and the cadence — so a reader always sees *when* a number is from.
  - **Freshness states**: :func:`classify_freshness` maps (cadence, observation date, now)
    to ``current`` / ``overdue`` / ``fetch-failed``. A monthly series *between releases* is
    CURRENT, not missing — this is the crux of "never omit / never fabricate".

Governance: this module is metadata + labeling only. It never fetches, never stores raw
licensed rows, and never fabricates a value. It only describes and classifies.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class Cadence(str, Enum):
    """How often a series is expected to publish a new observation."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"
    IRREGULAR = "irregular"


class Source(str, Enum):
    """Upstream provider / authority for a series."""

    FRED = "fred"
    BLS = "bls"
    BEA = "bea"
    EDGAR = "edgar"
    SF1 = "sf1"          # Sharadar SF1 (Nasdaq Data Link) — licensed, derived-only
    PRICES = "prices"    # market price feeds (Yahoo / Twelve Data / CoinGecko)
    TREASURY = "treasury"  # US Treasury Fiscal Data (keyless / public)
    FDIC = "fdic"          # FDIC BankFind Suite (keyless / public)
    EIA = "eia"            # US Energy Information Administration (api.data.gov key)


class LicenseClass(str, Enum):
    """Redistribution posture for a series' underlying data."""

    PUBLIC = "public"                        # public-domain gov data (FRED/BLS/BEA/EDGAR)
    PUBLIC_FEED = "public_feed"              # public market feeds (attribution, no raw resale)
    LICENSED_DERIVED_ONLY = "licensed_derived_only"  # SF1: only DERIVED metrics may surface


# Freshness state labels (stable strings surfaced in payloads / UI).
FRESH_CURRENT = "current"        # on cadence — a released value that is up to date
FRESH_OVERDUE = "overdue"        # a new observation was expected by now but isn't present
FRESH_FAILED = "fetch-failed"    # live fetch failed; serving the last-good value

# How stale (in days) an observation may be before it is "overdue" for its cadence.
# These grace windows fold in the real-world reporting lag (e.g. CPI for month M is
# released in month M+1), so a monthly series between releases stays CURRENT.
_CADENCE_MAX_AGE_DAYS: dict[Cadence, int] = {
    Cadence.DAILY: 5,        # markets: weekends + holidays
    Cadence.WEEKLY: 14,
    Cadence.MONTHLY: 75,     # ~1 period + reporting lag
    Cadence.QUARTERLY: 200,  # ~1 quarter + reporting lag
    Cadence.ANNUAL: 500,
    Cadence.IRREGULAR: 0,    # no schedule → never classified overdue on age alone
}


@dataclass(frozen=True)
class SeriesSpec:
    """Registry metadata for one series. Description-only (never carries a value)."""

    series_id: str
    name: str
    source: Source
    cadence: Cadence
    unit: str
    license_class: LicenseClass
    # Optional, where known. Free-form (ISO date or period label) for last release, and
    # a human hint for the next expected release.
    last_release: str | None = None
    next_release: str | None = None


@dataclass
class ObservedValue:
    """A fetched value threaded with its provenance — the small typed wrapper the data
    services return so as-of / cadence / freshness ride with every number.

    ``observation_date`` is the *actual data date* (the observation or period the value
    belongs to), which is NOT the same as ``fetched_at`` (wall-clock time of the fetch).
    """

    series_id: str
    value: float | None
    observation_date: str | None          # actual data date/period (e.g. "2026-06-01")
    fetched_at: datetime
    source: str
    cadence: Cadence
    unit: str
    freshness: str = FRESH_CURRENT
    note: str | None = None

    @property
    def as_of_label(self) -> str:
        """A compact "Monthly · as of Jun 2026" style label for UI/payloads."""
        return as_of_label(self.cadence, self.observation_date)


# --------------------------------------------------------------------------- #
# Registry
# --------------------------------------------------------------------------- #
# Cadence assignments follow each series' real publication schedule. Market prices are
# DAILY (trading days); CPI/labor/most FRED activity series are MONTHLY; GDP and the
# credit-delinquency series are QUARTERLY; a few structural ratios are ANNUAL; SF1
# fundamentals are QUARTERLY (as-reported) and are licensed/derived-only.
_SPECS: list[SeriesSpec] = [
    # ── Crypto (CoinGecko, public feed) — daily/continuous ────────────────────
    SeriesSpec("BTC", "Bitcoin", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    SeriesSpec("ETH", "Ethereum", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    SeriesSpec("XRP", "XRP", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    SeriesSpec("XLM", "Stellar", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    SeriesSpec("SOL", "Solana", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    # ── Equity indices / commodities / rates / proxies (prices) — daily ───────
    SeriesSpec("SPX", "S&P 500", Source.PRICES, Cadence.DAILY, "index", LicenseClass.PUBLIC_FEED),
    SeriesSpec("DJIA", "Dow Jones", Source.PRICES, Cadence.DAILY, "index", LicenseClass.PUBLIC_FEED),
    SeriesSpec("NASDAQ", "Nasdaq Composite", Source.PRICES, Cadence.DAILY, "index", LicenseClass.PUBLIC_FEED),
    SeriesSpec("GOLD", "Gold (front future)", Source.PRICES, Cadence.DAILY, "USD/oz", LicenseClass.PUBLIC_FEED),
    SeriesSpec("OIL", "WTI Crude (front future)", Source.PRICES, Cadence.DAILY, "USD/bbl", LicenseClass.PUBLIC_FEED),
    SeriesSpec("UST3M", "US 13-week T-bill yield", Source.PRICES, Cadence.DAILY, "%", LicenseClass.PUBLIC_FEED),
    SeriesSpec("UST5Y", "US 5Y Treasury yield", Source.PRICES, Cadence.DAILY, "%", LicenseClass.PUBLIC_FEED),
    SeriesSpec("UST10Y", "US 10Y Treasury yield", Source.PRICES, Cadence.DAILY, "%", LicenseClass.PUBLIC_FEED),
    SeriesSpec("UST30Y", "US 30Y Treasury yield", Source.PRICES, Cadence.DAILY, "%", LicenseClass.PUBLIC_FEED),
    SeriesSpec("REIT", "US Real Estate (VNQ)", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    SeriesSpec("EURUSD", "Euro / US Dollar", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    SeriesSpec("GBPUSD", "British Pound / US Dollar", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    SeriesSpec("USDJPY", "US Dollar / Japanese Yen", Source.PRICES, Cadence.DAILY, "JPY", LicenseClass.PUBLIC_FEED),
    SeriesSpec("DXY", "US Dollar Index", Source.PRICES, Cadence.DAILY, "index", LicenseClass.PUBLIC_FEED),
    SeriesSpec("BOND_AGG", "US Aggregate Bond (AGG)", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    SeriesSpec("BOND_IG", "IG Corporate Bond (LQD)", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    SeriesSpec("BOND_HY", "High-Yield Bond (HYG)", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    SeriesSpec("BOND_MUNI", "Municipal Bond (MUB)", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    SeriesSpec("BOND_TIPS", "TIPS (TIP)", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    SeriesSpec("PE_PROXY", "Listed Private Equity (PSP)", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    SeriesSpec("SMB_PROXY", "US Small Caps (IWM)", Source.PRICES, Cadence.DAILY, "USD", LicenseClass.PUBLIC_FEED),
    # ── Inflation (BLS CPI) — monthly ─────────────────────────────────────────
    SeriesSpec("INFLATION", "US CPI (YoY)", Source.BLS, Cadence.MONTHLY, "%", LicenseClass.PUBLIC),
    # ── Macro (FRED) — cadence per series ─────────────────────────────────────
    SeriesSpec("M2", "US M2 Money Supply", Source.FRED, Cadence.MONTHLY, "USD bn", LicenseClass.PUBLIC),
    SeriesSpec("GDP", "US GDP", Source.FRED, Cadence.QUARTERLY, "USD bn", LicenseClass.PUBLIC),
    SeriesSpec("UNEMPLOYMENT", "US Unemployment Rate", Source.FRED, Cadence.MONTHLY, "%", LicenseClass.PUBLIC),
    SeriesSpec("FED_FUNDS", "US Fed Funds Rate", Source.FRED, Cadence.MONTHLY, "%", LicenseClass.PUBLIC),
    SeriesSpec("CONSUMER_CREDIT", "US Consumer Credit (total)", Source.FRED, Cadence.MONTHLY, "USD mn", LicenseClass.PUBLIC),
    SeriesSpec("REVOLVING_CREDIT", "US Revolving Consumer Credit", Source.FRED, Cadence.MONTHLY, "USD mn", LicenseClass.PUBLIC),
    SeriesSpec("HOUSEHOLD_DEBT_GDP", "US Household Debt to GDP", Source.FRED, Cadence.QUARTERLY, "%", LicenseClass.PUBLIC),
    SeriesSpec("CC_DELINQUENCY", "Credit Card Delinquency Rate", Source.FRED, Cadence.QUARTERLY, "%", LicenseClass.PUBLIC),
    SeriesSpec("LOAN_DELINQUENCY", "All Bank Loans Delinquency Rate", Source.FRED, Cadence.QUARTERLY, "%", LicenseClass.PUBLIC),
    SeriesSpec("MORTGAGE_DELINQUENCY", "Mortgage Delinquency Rate", Source.FRED, Cadence.QUARTERLY, "%", LicenseClass.PUBLIC),
    SeriesSpec("RETAIL_SALES", "US Retail Sales", Source.FRED, Cadence.MONTHLY, "USD mn", LicenseClass.PUBLIC),
    SeriesSpec("CONSUMER_SENTIMENT", "US Consumer Sentiment (UMich)", Source.FRED, Cadence.MONTHLY, "index", LicenseClass.PUBLIC),
    SeriesSpec("INDUSTRIAL_PRODUCTION", "US Industrial Production", Source.FRED, Cadence.MONTHLY, "index", LicenseClass.PUBLIC),
    # ── US Treasury Fiscal Data (keyless / public) ────────────────────────────
    SeriesSpec("TREASURY_TOTAL_DEBT", "Total public debt outstanding", Source.TREASURY,
               Cadence.DAILY, "USD", LicenseClass.PUBLIC),
    SeriesSpec("TREASURY_DEBT_HELD_PUBLIC", "Debt held by the public", Source.TREASURY,
               Cadence.DAILY, "USD", LicenseClass.PUBLIC),
    SeriesSpec("TREASURY_AVG_RATE_MARKETABLE", "Avg interest rate · total marketable",
               Source.TREASURY, Cadence.MONTHLY, "%", LicenseClass.PUBLIC),
    SeriesSpec("TREASURY_AVG_RATE_TBILLS", "Avg interest rate · Treasury Bills",
               Source.TREASURY, Cadence.MONTHLY, "%", LicenseClass.PUBLIC),
    SeriesSpec("TREASURY_AVG_RATE_TNOTES", "Avg interest rate · Treasury Notes",
               Source.TREASURY, Cadence.MONTHLY, "%", LicenseClass.PUBLIC),
    SeriesSpec("TREASURY_AVG_RATE_TBONDS", "Avg interest rate · Treasury Bonds",
               Source.TREASURY, Cadence.MONTHLY, "%", LicenseClass.PUBLIC),
    # ── FDIC BankFind Suite (keyless / public) ────────────────────────────────
    SeriesSpec("FDIC_INSURED_INSTITUTIONS", "FDIC-insured institutions (active)",
               Source.FDIC, Cadence.QUARTERLY, "count", LicenseClass.PUBLIC),
    # ── EIA energy / commodities (api.data.gov key) ───────────────────────────
    SeriesSpec("EIA_WTI", "WTI crude oil spot", Source.EIA, Cadence.DAILY, "USD/bbl",
               LicenseClass.PUBLIC),
    SeriesSpec("EIA_HENRY_HUB", "Henry Hub natural gas spot", Source.EIA, Cadence.DAILY,
               "USD/MMBtu", LicenseClass.PUBLIC),
    SeriesSpec("EIA_ELECTRICITY_PRICE", "US retail electricity price (all sectors)",
               Source.EIA, Cadence.MONTHLY, "cents/kWh", LicenseClass.PUBLIC),
    # ── Fundamentals (Sharadar SF1) — quarterly, licensed / derived-only ──────
    SeriesSpec("SF1_FUNDAMENTALS", "Point-in-time fundamentals (Sharadar SF1)", Source.SF1,
               Cadence.QUARTERLY, "derived", LicenseClass.LICENSED_DERIVED_ONLY),
    # ── Filings (SEC EDGAR) — irregular (event-driven) ────────────────────────
    SeriesSpec("EDGAR_FUNDAMENTALS", "SEC EDGAR company facts", Source.EDGAR,
               Cadence.IRREGULAR, "derived", LicenseClass.PUBLIC),
]

REGISTRY: dict[str, SeriesSpec] = {spec.series_id: spec for spec in _SPECS}


def get_series(series_id: str) -> SeriesSpec | None:
    """Registry lookup by series id (case-insensitive). ``None`` if unregistered."""
    return REGISTRY.get(series_id.strip().upper())


def all_series() -> list[SeriesSpec]:
    """All registered series specs (stable order)."""
    return list(_SPECS)


def cadence_for(series_id: str, default: Cadence = Cadence.DAILY) -> Cadence:
    """Cadence for a series id, falling back to ``default`` for unregistered ids
    (an unknown symbol is treated as a daily-quoted equity ticker)."""
    spec = get_series(series_id)
    return spec.cadence if spec else default


# --------------------------------------------------------------------------- #
# As-of / cadence labeling + freshness classification
# --------------------------------------------------------------------------- #
def _coerce_cadence(cadence: Cadence | str) -> Cadence:
    if isinstance(cadence, Cadence):
        return cadence
    try:
        return Cadence(str(cadence).lower())
    except ValueError:
        return Cadence.IRREGULAR


def parse_observation_date(observation_date: str | None) -> datetime | None:
    """Best-effort parse of an observation date/period into a datetime.

    Handles ISO dates ("2026-06-01"), year-month ("2026-06"), plain year ("2026"),
    and BLS-style period labels ("May 2026", "Q2 2026"). Returns ``None`` if it can't
    parse (freshness then can't be aged and defaults to current-if-present).
    """
    if not observation_date:
        return None
    text = observation_date.strip()
    # ISO-ish first.
    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    # "Mon YYYY" / "Month YYYY".
    for fmt in ("%b %Y", "%B %Y"):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    # "Q2 2026".
    if text[:1].upper() == "Q" and len(text) >= 6:
        try:
            q = int(text[1])
            year = int(text.split()[-1])
            month = (q - 1) * 3 + 1
            return datetime(year, month, 1, tzinfo=timezone.utc)
        except (ValueError, IndexError):
            pass
    # Plain year.
    try:
        return datetime(int(text), 1, 1, tzinfo=timezone.utc)
    except ValueError:
        return None


def cadence_label(cadence: Cadence | str) -> str:
    """Human title-case cadence word, e.g. ``Monthly``."""
    return _coerce_cadence(cadence).value.capitalize()


def as_of_label(cadence: Cadence | str, observation_date: str | None) -> str:
    """A compact "Monthly · as of Jun 2026" label.

    The date granularity follows the cadence: daily → "Jun 10, 2026"; monthly →
    "Jun 2026"; quarterly → "Q2 2026"; annual → "2026". Falls back to the raw string
    (or "pending" when unknown) so nothing is ever fabricated.
    """
    cad = _coerce_cadence(cadence)
    label = cadence_label(cad)
    if not observation_date:
        return f"{label} · as of pending"
    dt = parse_observation_date(observation_date)
    if dt is None:
        return f"{label} · as of {observation_date}"
    if cad == Cadence.ANNUAL:
        stamp = dt.strftime("%Y")
    elif cad == Cadence.QUARTERLY:
        stamp = f"Q{(dt.month - 1) // 3 + 1} {dt.year}"
    elif cad in (Cadence.MONTHLY,):
        stamp = dt.strftime("%b %Y").replace(" 0", " ")
    else:  # daily / weekly / irregular → precise day
        stamp = dt.strftime("%b %d, %Y").replace(" 0", " ")
    return f"{label} · as of {stamp}"


def classify_freshness(
    cadence: Cadence | str,
    observation_date: str | None,
    now: datetime | None = None,
    *,
    fetch_failed: bool = False,
) -> str:
    """Classify a value's freshness state.

    - ``fetch-failed`` when the live fetch failed (serving last-good), regardless of age.
    - ``overdue`` when the observation is older than the cadence's grace window (a new
      release was expected by now but isn't present).
    - ``current`` otherwise — INCLUDING a series that is simply *between releases*
      (a monthly series a few weeks after its last print is CURRENT, not missing).
    """
    if fetch_failed:
        return FRESH_FAILED
    cad = _coerce_cadence(cadence)
    max_age = _CADENCE_MAX_AGE_DAYS.get(cad, 0)
    if max_age <= 0:
        return FRESH_CURRENT  # irregular / unscheduled: present == current
    dt = parse_observation_date(observation_date)
    if dt is None:
        return FRESH_CURRENT  # can't age it → don't cry wolf; treat as current
    ref = now or datetime.now(timezone.utc)
    if ref.tzinfo is None:
        ref = ref.replace(tzinfo=timezone.utc)
    age_days = (ref - dt).total_seconds() / 86400.0
    return FRESH_OVERDUE if age_days > max_age else FRESH_CURRENT
