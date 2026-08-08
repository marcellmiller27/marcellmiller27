# JHI-SIG: 69M2705M | H5 SF1 fundamental-factor validation back-test | JHI Research & Analytics Firm, Inc. (proprietary)
"""Point-in-time SF1 fundamental-factor Opportunity Score — H5 validation harness.

PURPOSE (thesis H5): test whether a FUNDAMENTAL-factor cross-sectional Opportunity
Score has genuine predictive validity against the PRE-REGISTERED bar
(``mean IC >= 0.03 AND |t-stat| >= 2.0 AND hit rate >= 0.55``), out-of-sample, on a
large/mid-cap US equity universe. This is the fundamentals follow-up to the prior
price-only H5 run (which FAILED: mean IC 0.0074, t 0.25) — see
``docs/H5_GAP_CLOSURE_RESULTS.md``.

PRE-REGISTERED FACTOR SET + WEIGHTS (fixed BEFORE reading any results — no fishing):

    Value   (0.40)  earnings_yield (E/P), book_yield (B/P), fcf_yield (FCF/P)  -> 0.40/3 each
    Quality (0.35)  roe, operating_margin, net_margin                          -> 0.35/3 each
    Growth  (0.25)  revenue_cagr (trailing, up to 5 PIT fiscal years)          -> 0.25

Every factor is oriented "higher = more attractive" (cheaper / higher quality /
faster growth). At each rebalance date the raw factors are cross-sectionally
z-scored, winsorized to +/-3 SD, weighted, and summed into a composite. The period
information coefficient (IC) is the Spearman rank correlation of that composite with
the NEXT-period return. This reuses the existing IC / long-short / cost machinery in
``app.research_services`` so the method matches the price-only harness.

LOOK-AHEAD CONTROL (critical): at rebalance date ``d`` a ticker may only use SF1 rows
whose ``datekey`` (the SEC filing date — when the annual figures first became public)
is ``<= d``. Market cap uses the *rebalance-date* price (Yahoo) times point-in-time
basic shares, never SF1's stale as-of-filing price. Forward returns are realized from
Yahoo monthly closes. This yields a genuine point-in-time panel with no restatement
or look-ahead bias (SF1 ``ARY`` is as-first-reported).

DATA GOVERNANCE — Founder mandate ("no spillage / derived-only"):
    Raw Sharadar SF1 rows are LICENSED and INTERNAL ONLY. This module keeps raw pulls
    in a gitignored on-disk cache (``backend/.sf1_cache/``) and surfaces ONLY derived
    metrics (ICs, hit rate, long-short spread, verdict). No raw SF1 field is returned
    from the public back-test result or written to any doc/export.
"""

from __future__ import annotations

import json
import logging
import os
import statistics
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.market_services import sharadar_sf1_annual, yahoo_chart_history
from app.research_services import COST_BPS_PER_SIDE, ResearchService, _spearman
from app.opportunity_score import _zscore

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# PRE-REGISTERED score definition (fixed before reading results).             #
# --------------------------------------------------------------------------- #
VALUE_WEIGHT = 0.40
QUALITY_WEIGHT = 0.35
GROWTH_WEIGHT = 0.25

FACTOR_WEIGHTS: dict[str, float] = {
    # Value 0.40
    "earnings_yield": VALUE_WEIGHT / 3.0,
    "book_yield": VALUE_WEIGHT / 3.0,
    "fcf_yield": VALUE_WEIGHT / 3.0,
    # Quality 0.35
    "roe": QUALITY_WEIGHT / 3.0,
    "operating_margin": QUALITY_WEIGHT / 3.0,
    "net_margin": QUALITY_WEIGHT / 3.0,
    # Growth 0.25
    "revenue_cagr": GROWTH_WEIGHT,
}
FACTORS: list[str] = list(FACTOR_WEIGHTS)

WINSOR_SD = 3.0            # clip cross-sectional z-scores to +/- this many SD
CAGR_MAX_YEARS = 5         # trailing PIT fiscal years used for revenue CAGR
MIN_NAMES_PER_PERIOD = 10  # need a real cross-section to compute a meaningful IC
PRICE_RANGE = "20y"        # Yahoo monthly window (SF1 availability gates the start)

# Pre-registered H5 success criteria (identical to the price-only harness — do NOT
# change; imported values keep a single source of truth).
H5_MIN_MEAN_IC = 0.03
H5_MIN_T_STAT = 2.0
H5_MIN_HIT_RATE = 0.55
H5_PASS_CRITERIA = (
    f"mean IC >= {H5_MIN_MEAN_IC} AND |t-stat| >= {H5_MIN_T_STAT} "
    f"AND hit rate >= {H5_MIN_HIT_RATE} (evaluated out-of-sample)"
)

SCORE_DEFINITION = (
    "SF1 fundamental-factor Opportunity Score: cross-sectional z-blend (winsorized "
    "+/-3 SD) of Value 0.40 [earnings_yield, book_yield, fcf_yield], Quality 0.35 "
    "[roe, operating_margin, net_margin], Growth 0.25 [revenue_cagr]. Point-in-time "
    "(SF1 datekey <= rebalance date); market cap = rebalance-date price x PIT shares."
)

# SF1 numeric fields we retain in the internal cache (raw, gitignored).
_SF1_KEEP = (
    "datekey", "reportperiod", "revenue", "netinc", "equity",
    "opinc", "gp", "fcf", "sharesbas",
)

_CACHE_DIR = os.path.join(os.path.dirname(__file__), os.pardir, ".sf1_cache")


# --------------------------------------------------------------------------- #
# Derived result (governance-safe: NO raw SF1 fields).                        #
# --------------------------------------------------------------------------- #
@dataclass
class SegmentMetrics:
    label: str
    n_periods: int
    mean_ic: float | None
    ic_t_stat: float | None
    hit_rate: float | None
    gross_annualized_long_short: float | None
    net_annualized_long_short: float | None
    avg_monthly_turnover: float | None
    passes: bool


@dataclass
class SF1BacktestResult:
    score_definition: str
    universe: list[str]
    n_assets: int
    first_period: str | None
    last_period: str | None
    factor_weights: dict[str, float]
    cost_bps_per_side: float
    pass_criteria: str
    full_sample: SegmentMetrics
    in_sample: SegmentMetrics
    out_of_sample: SegmentMetrics
    recent_third_holdout: SegmentMetrics
    oos_verdict: str
    h5_pass: bool
    interpretation: str
    caveats: list[str]
    status: str = "ok"
    as_of: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# --------------------------------------------------------------------------- #
# Pure factor / metric math (network-free; unit-tested).                      #
# --------------------------------------------------------------------------- #
def _to_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def pit_rows(sf1: list[dict], as_of: str) -> list[dict]:
    """SF1 rows known by ``as_of`` (datekey <= as_of), sorted by datekey ascending.

    ``datekey`` is the SEC filing date, so this is the point-in-time gate that
    prevents look-ahead: only fundamentals already public at the rebalance date.
    """
    known = [r for r in sf1 if str(r.get("datekey") or "") and str(r["datekey"]) <= as_of]
    return sorted(known, key=lambda r: str(r.get("datekey")))


def revenue_cagr(rows: list[dict], max_years: int = CAGR_MAX_YEARS) -> float | None:
    """Trailing revenue CAGR over the most recent (up to ``max_years``) PIT rows.

    ``rows`` must already be point-in-time and sorted ascending by datekey.
    """
    revs = [
        (str(r.get("reportperiod") or ""), _to_float(r.get("revenue")))
        for r in rows
    ]
    revs = [(p, v) for p, v in revs if p and v is not None and v > 0]
    if len(revs) < 2:
        return None
    revs = revs[-max_years:]
    first_period, first_rev = revs[0]
    last_period, last_rev = revs[-1]
    try:
        span = int(last_period[:4]) - int(first_period[:4])
    except ValueError:
        span = len(revs) - 1
    if span <= 0:
        span = len(revs) - 1
    if span <= 0:
        return None
    try:
        return (last_rev / first_rev) ** (1.0 / span) - 1.0
    except (ZeroDivisionError, ValueError):
        return None


def factor_vector(sf1: list[dict], as_of: str, price: float) -> dict[str, float] | None:
    """Point-in-time raw factor vector for one name at ``as_of`` (or None).

    Returns None (name excluded from the period's cross-section) if the price is
    missing or any of the seven pre-registered factor inputs cannot be derived from
    point-in-time data. Only DERIVED factors leave this function (governance).
    """
    if not price or price <= 0:
        return None
    rows = pit_rows(sf1, as_of)
    if not rows:
        return None
    latest = rows[-1]  # most recently filed row known by as_of

    revenue = _to_float(latest.get("revenue"))
    netinc = _to_float(latest.get("netinc"))
    equity = _to_float(latest.get("equity"))
    opinc = _to_float(latest.get("opinc"))
    fcf = _to_float(latest.get("fcf"))
    shares = _to_float(latest.get("sharesbas"))
    cagr = revenue_cagr(rows)

    if None in (revenue, netinc, equity, opinc, fcf, shares, cagr):
        return None
    if not revenue or revenue <= 0 or not equity or not shares or shares <= 0:
        return None

    market_cap = price * shares
    if market_cap <= 0:
        return None

    return {
        "earnings_yield": netinc / market_cap,
        "book_yield": equity / market_cap,
        "fcf_yield": fcf / market_cap,
        "roe": netinc / equity,
        "operating_margin": opinc / revenue,
        "net_margin": netinc / revenue,
        "revenue_cagr": cagr,
    }


def _winsorize(values: list[float], limit: float = WINSOR_SD) -> list[float]:
    return [max(-limit, min(limit, v)) for v in values]


def composite_scores(vectors: dict[str, dict[str, float]]) -> dict[str, float]:
    """Cross-sectional composite score per ticker from raw factor vectors.

    Each factor is z-scored across the cross-section, winsorized to +/- WINSOR_SD,
    weighted by the pre-registered FACTOR_WEIGHTS, and summed. Higher = more
    attractive.
    """
    tickers = list(vectors.keys())
    if len(tickers) < 2:
        return {}
    composite = {t: 0.0 for t in tickers}
    for factor, weight in FACTOR_WEIGHTS.items():
        z = _winsorize(_zscore([vectors[t][factor] for t in tickers]))
        for t, zv in zip(tickers, z):
            composite[t] += weight * zv
    return composite


@dataclass
class _Period:
    date: str
    composite: dict[str, float]
    forward: dict[str, float]


def _segment_metrics(label: str, periods: list[_Period]) -> SegmentMetrics:
    """Derived IC / hit-rate / costed long-short metrics over a list of periods."""
    if not periods:
        return SegmentMetrics(label, 0, None, None, None, None, None, None, False)

    ics: list[float] = []
    gross: list[float] = []
    net: list[float] = []
    turnovers: list[float] = []
    prev_port: dict[str, float] = {}
    for period in periods:
        assets = list(period.composite.keys())
        comp = [period.composite[a] for a in assets]
        fwd = [period.forward[a] for a in assets]
        ic = _spearman(comp, fwd)
        if ic is not None:
            ics.append(ic)
        port, g = ResearchService._long_short_portfolio(period.composite, period.forward)
        gross.append(g)
        turnover = ResearchService._turnover(prev_port, port)
        turnovers.append(turnover)
        net.append(g - turnover * (2 * COST_BPS_PER_SIDE / 10_000.0))
        prev_port = port

    if not ics:
        return SegmentMetrics(label, 0, None, None, None, None, None, None, False)

    mean_ic = statistics.fmean(ics)
    ic_sd = statistics.pstdev(ics) if len(ics) > 1 else 0.0
    t_stat = (mean_ic / (ic_sd / (len(ics) ** 0.5))) if ic_sd > 0 else None
    hit_rate = sum(1 for ic in ics if ic > 0) / len(ics)
    gross_ann = statistics.fmean(gross) * 12 if gross else None
    net_ann = statistics.fmean(net) * 12 if net else None
    avg_turnover = statistics.fmean(turnovers) if turnovers else None

    passes = bool(
        mean_ic >= H5_MIN_MEAN_IC
        and t_stat is not None
        and abs(t_stat) >= H5_MIN_T_STAT
        and hit_rate >= H5_MIN_HIT_RATE
    )
    return SegmentMetrics(
        label=label,
        n_periods=len(ics),
        mean_ic=round(mean_ic, 4),
        ic_t_stat=round(t_stat, 2) if t_stat is not None else None,
        hit_rate=round(hit_rate, 3),
        gross_annualized_long_short=round(gross_ann, 4) if gross_ann is not None else None,
        net_annualized_long_short=round(net_ann, 4) if net_ann is not None else None,
        avg_monthly_turnover=round(avg_turnover, 4) if avg_turnover is not None else None,
        passes=passes,
    )


def build_periods(
    sf1_by_ticker: dict[str, list[dict]],
    prices_by_ticker: dict[str, list[tuple[str, float]]],
    min_names: int = MIN_NAMES_PER_PERIOD,
) -> list[_Period]:
    """Assemble the point-in-time monthly rebalance panel (pure; no network).

    ``prices_by_ticker`` maps ticker -> [(iso_date, close), ...] monthly ascending.
    At each rebalance date only tickers with (a) a price that date, (b) a next-month
    price (for the forward return), and (c) a full PIT factor vector are included.
    """
    price_maps = {t: dict(rows) for t, rows in prices_by_ticker.items()}
    all_dates = sorted({d for rows in prices_by_ticker.values() for d, _ in rows})

    periods: list[_Period] = []
    for i in range(len(all_dates) - 1):
        d, d_next = all_dates[i], all_dates[i + 1]
        vectors: dict[str, dict[str, float]] = {}
        forward: dict[str, float] = {}
        for ticker, pmap in price_maps.items():
            price = pmap.get(d)
            price_next = pmap.get(d_next)
            if price is None or price_next is None or price <= 0:
                continue
            vec = factor_vector(sf1_by_ticker.get(ticker, []), d, price)
            if vec is None:
                continue
            vectors[ticker] = vec
            forward[ticker] = price_next / price - 1.0
        if len(vectors) < min_names:
            continue
        composite = composite_scores(vectors)
        if not composite:
            continue
        periods.append(_Period(date=d, composite=composite, forward=forward))
    return periods


def summarize(universe: list[str], periods: list[_Period]) -> SF1BacktestResult:
    """Turn the assembled panel into the derived, governance-safe result."""
    caveats = [
        "Point-in-time SF1 fundamentals (datekey<=rebalance) + Yahoo monthly closes.",
        f"Costs modeled at {COST_BPS_PER_SIDE} bps/side via long-short turnover.",
        "Universe is a curated large/mid-cap list (survivorship-aware but not fully "
        "survivorship-bias-free); single price vendor (Yahoo).",
        "Factor set + weights were PRE-REGISTERED before reading results (see "
        "score_definition); no configuration was tuned to the outcome.",
    ]
    n_assets = len({t for p in periods for t in p.composite})
    if not periods:
        empty = SegmentMetrics("empty", 0, None, None, None, None, None, None, False)
        return SF1BacktestResult(
            score_definition=SCORE_DEFINITION, universe=universe, n_assets=0,
            first_period=None, last_period=None, factor_weights=FACTOR_WEIGHTS,
            cost_bps_per_side=COST_BPS_PER_SIDE, pass_criteria=H5_PASS_CRITERIA,
            full_sample=empty, in_sample=empty, out_of_sample=empty,
            recent_third_holdout=empty, oos_verdict="FAIL", h5_pass=False,
            interpretation="Insufficient point-in-time data to assemble a panel.",
            caveats=caveats, status="unavailable",
        )

    split = len(periods) // 2
    third = (len(periods) * 2) // 3
    full = _segment_metrics("full_sample", periods)
    in_sample = _segment_metrics("in_sample (first half)", periods[:split])
    oos = _segment_metrics("out_of_sample (second half)", periods[split:])
    recent = _segment_metrics("recent_third_holdout", periods[third:])

    h5_pass = oos.passes
    verdict = "PASS" if h5_pass else "FAIL"
    interpretation = (
        f"H5 (fundamental factors) = {verdict} out-of-sample. OOS mean IC "
        f"{oos.mean_ic}, t-stat {oos.ic_t_stat}, hit rate "
        f"{(f'{oos.hit_rate:.1%}' if oos.hit_rate is not None else 'n/a')} over "
        f"{oos.n_periods} months / {n_assets} equities. "
        + (
            "The SF1 fundamental Opportunity Score clears the pre-registered bar "
            "out-of-sample."
            if h5_pass
            else "Below the pre-registered bar out-of-sample; H5 remains unconfirmed "
            "for this factor set."
        )
    )
    return SF1BacktestResult(
        score_definition=SCORE_DEFINITION,
        universe=universe,
        n_assets=n_assets,
        first_period=periods[0].date,
        last_period=periods[-1].date,
        factor_weights={k: round(v, 4) for k, v in FACTOR_WEIGHTS.items()},
        cost_bps_per_side=COST_BPS_PER_SIDE,
        pass_criteria=H5_PASS_CRITERIA,
        full_sample=full,
        in_sample=in_sample,
        out_of_sample=oos,
        recent_third_holdout=recent,
        oos_verdict=verdict,
        h5_pass=h5_pass,
        interpretation=interpretation,
        caveats=caveats,
    )


# --------------------------------------------------------------------------- #
# Data loading (network) — cached to keep SF1 raw rows internal + rate-safe.  #
# --------------------------------------------------------------------------- #
def _cache_path(ticker: str) -> str:
    return os.path.join(_CACHE_DIR, f"{ticker.upper()}.json")


def load_ticker(
    ticker: str, use_cache: bool = True, sf1_limit: int = 30
) -> tuple[list[dict], list[tuple[str, float]]] | None:
    """Load (trimmed) SF1 annual rows + Yahoo monthly closes for one ticker.

    Results are cached in the gitignored internal cache. Only the numeric SF1 fields
    in ``_SF1_KEEP`` are retained (still raw/internal — never surfaced). Returns None
    if either source is unavailable.
    """
    ticker = ticker.strip().upper()
    path = _cache_path(ticker)
    if use_cache and os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                blob = json.load(fh)
            return blob["sf1"], [(d, float(c)) for d, c in blob["prices"]]
        except (OSError, ValueError, KeyError):
            pass

    try:
        raw = sharadar_sf1_annual(ticker, limit=sf1_limit)
    except Exception as exc:  # noqa: BLE001 - resilient: skip names SF1 can't supply
        logger.info("sf1_backtest: SF1 unavailable for %s (%s)", ticker, exc)
        return None
    sf1 = [{k: r.get(k) for k in _SF1_KEEP} for r in raw]

    try:
        hist = yahoo_chart_history(ticker, range_=PRICE_RANGE, interval="1mo")
    except Exception as exc:  # noqa: BLE001 - resilient: skip names Yahoo can't supply
        logger.info("sf1_backtest: Yahoo unavailable for %s (%s)", ticker, exc)
        return None
    prices = [
        (datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat(), float(close))
        for ts, close in hist
    ]

    os.makedirs(_CACHE_DIR, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"sf1": sf1, "prices": prices}, fh)
    except OSError:
        pass
    return sf1, prices


def run_backtest(
    universe: list[str] | None = None, use_cache: bool = True
) -> SF1BacktestResult:
    """Full point-in-time SF1 fundamental-factor H5 back-test (loads data + summarizes)."""
    from app.equity_opportunity_scan import LARGE_MID_CAP_UNIVERSE

    uni = universe or LARGE_MID_CAP_UNIVERSE
    sf1_by_ticker: dict[str, list[dict]] = {}
    prices_by_ticker: dict[str, list[tuple[str, float]]] = {}
    for ticker in uni:
        loaded = load_ticker(ticker, use_cache=use_cache)
        if loaded is None:
            continue
        sf1, prices = loaded
        sf1_by_ticker[ticker] = sf1
        prices_by_ticker[ticker] = prices

    periods = build_periods(sf1_by_ticker, prices_by_ticker)
    return summarize(uni, periods)
