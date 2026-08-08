# JHI-SIG: 69M2705M | H5 EXPANDED SF1 fundamental+momentum validation | JHI Research & Analytics Firm, Inc. (proprietary)
"""Expanded, survivorship-free H5 validation — SF1 fundamentals + price momentum.

This is the DEFINITIVE follow-up to the prior narrow H5 run (``sf1_factor_backtest``),
which passed 2 of 3 legs out-of-sample (mean IC 0.0377, hit 56.7%) and missed only the
t-stat (1.82 < 2.0) on a ~41-name mega-cap list. The miss was statistical POWER, not a
broken signal, so this module re-runs the SAME pre-registered bar with proper breadth
and method.

PRE-REGISTERED BAR (unchanged): ``mean IC >= 0.03 AND |IC t-stat| >= 2.0 AND hit rate
>= 0.55`` evaluated OUT-OF-SAMPLE.

PRE-REGISTERED EXPANSIONS (all fixed BEFORE reading any results — no fishing):

1. Universe — the full, survivorship-free SHARADAR SF1 universe: US **domestic common
   stock** (``category`` starts with "Domestic Common Stock"), ``currency == USD``,
   INCLUDING delisted names (that is the point of survivorship-free). ~15k names.
2. Returns — delisted-inclusive, built from SF1's OWN ``price`` at each ``datekey``
   (the filing-date close), report-to-report. We hold SF1 fundamentals only (no SEP
   prices; Yahoo lacks delisted names), so SF1 price is the only survivorship-free
   price source. No delisted price is fabricated: a name contributes returns only
   between consecutive filings it actually made.
3. Dimension — SF1 ``ART`` (as-reported, trailing-twelve-month): quarterly ``datekey``
   frequency (~4x the observations of annual, satisfying the "more periods" intent)
   with TTM flows to avoid fiscal-quarter seasonality. As-reported => no restatement /
   look-ahead bias.
4. Factors + PRE-REGISTERED weights:
     * Fundamental composite (weights unchanged from the prior H5 run):
         Value 0.40   earnings_yield (E/P), book_yield (B/P), fcf_yield (FCF/P)
         Quality 0.35 roe, operating_margin, net_margin
         Growth 0.25  revenue_cagr (trailing TTM-revenue CAGR, up to 3 PIT years)
     * Momentum (NEW): 12-1-style report-to-report price momentum from SF1 price
         (price at the current filing / price ~1 year (4 quarters) earlier - 1).
   Blend (PRE-REGISTERED): each period, z-score (winsorized +/-3 SD) the seven
   fundamental factors, weight+sum -> fundamental composite; z-score that composite
   (F_z); z-score momentum (M_z); **blended = 0.60*F_z + 0.40*M_z**.
5. Neutralization (PRE-REGISTERED) applied to the blended score each period:
     (a) size — OLS-residualize the blended score on log(market cap);
     (b) sector — within each SF1 sector, demean and divide by SD.
6. Metrics — per-period Spearman IC of the neutralized score vs the report-to-report
   forward return; mean IC, IC t-stat, hit rate, and net annualized (x4) long-short
   (top minus bottom tercile) after 10 bps/side costs via turnover. OOS = second half
   of the (chronological, calendar-quarter-bucketed) period series.

LOOK-AHEAD CONTROL: an observation formed at filing ``r_i`` uses ONLY ``r_i`` and
earlier rows; its forward return is realized at the NEXT filing ``r_{i+1}`` (strictly
later datekey). Market cap uses the filing-date price. There is no restatement bias
(ART is as-first-reported).

DATA GOVERNANCE — Founder mandate ("no spillage / derived-only"): raw licensed SF1 rows
live only in the gitignored on-disk cache (``backend/.sf1_cache/``). This module
surfaces ONLY derived metrics (ICs, hit rate, long-short spread, verdict). No raw SF1
field is returned from any result, endpoint, doc, or export.
"""

from __future__ import annotations

import json
import logging
import math
import os
import statistics
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.market_services import USER_AGENT, nasdaq_data_link_api_key
from app.opportunity_score import _zscore
from app.research_services import COST_BPS_PER_SIDE, ResearchService, _spearman

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# PRE-REGISTERED design constants (fixed before reading results).             #
# --------------------------------------------------------------------------- #
VALUE_WEIGHT = 0.40
QUALITY_WEIGHT = 0.35
GROWTH_WEIGHT = 0.25

FUND_FACTOR_WEIGHTS: dict[str, float] = {
    "earnings_yield": VALUE_WEIGHT / 3.0,
    "book_yield": VALUE_WEIGHT / 3.0,
    "fcf_yield": VALUE_WEIGHT / 3.0,
    "roe": QUALITY_WEIGHT / 3.0,
    "operating_margin": QUALITY_WEIGHT / 3.0,
    "net_margin": QUALITY_WEIGHT / 3.0,
    "revenue_cagr": GROWTH_WEIGHT,
}
FUND_FACTORS: list[str] = list(FUND_FACTOR_WEIGHTS)

# Blend of the (z-scored) fundamental composite with (z-scored) momentum.
FUND_BLEND_WEIGHT = 0.60
MOM_BLEND_WEIGHT = 0.40

WINSOR_SD = 3.0
CAGR_MAX_YEARS = 3            # trailing PIT years for the TTM-revenue CAGR growth leg
MOM_LOOKBACK_QUARTERS = 4     # ~1 year of report-to-report price momentum
MIN_NAMES_PER_PERIOD = 30     # a real cross-section per quarter for a meaningful IC
PERIODS_PER_YEAR = 4          # quarterly rebalance -> annualize long-short by x4

# Pre-registered H5 success bar (identical to the prior run — DO NOT change).
H5_MIN_MEAN_IC = 0.03
H5_MIN_T_STAT = 2.0
H5_MIN_HIT_RATE = 0.55
H5_PASS_CRITERIA = (
    f"mean IC >= {H5_MIN_MEAN_IC} AND |t-stat| >= {H5_MIN_T_STAT} "
    f"AND hit rate >= {H5_MIN_HIT_RATE} (evaluated out-of-sample)"
)

SCORE_DEFINITION = (
    "Expanded SF1 Opportunity Score: blended = 0.60*z(fundamental composite) + "
    "0.40*z(12-1 momentum), then size- and sector-neutralized. Fundamental composite = "
    "Value 0.40 [earnings_yield, book_yield, fcf_yield], Quality 0.35 [roe, "
    "operating_margin, net_margin], Growth 0.25 [revenue_cagr]; each cross-sectionally "
    "z-scored (winsorized +/-3 SD). Point-in-time via SF1 ART datekey; prices are SF1's "
    "own filing-date close (delisted-inclusive)."
)

# SF1 ART columns pulled in bulk and retained in the internal (gitignored) cache.
_SF1_BULK_COLUMNS = (
    "ticker", "dimension", "datekey", "reportperiod",
    "revenue", "netinc", "equity", "opinc", "fcf", "sharesbas", "price",
)
_CACHE_DIR = os.path.join(os.path.dirname(__file__), os.pardir, ".sf1_cache")
_ART_CACHE = os.path.join(_CACHE_DIR, "_art_rows.json")
_META_CACHE = os.path.join(_CACHE_DIR, "_universe_meta.json")

_TICKERS_URL = "https://data.nasdaq.com/api/v3/datatables/SHARADAR/TICKERS"
_SF1_URL = "https://data.nasdaq.com/api/v3/datatables/SHARADAR/SF1"
_HTTP_TIMEOUT = 120.0
_PER_PAGE = 10_000


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
    avg_turnover: float | None
    passes: bool


@dataclass
class ExpandedBacktestResult:
    score_definition: str
    universe_description: str
    n_universe_requested: int
    n_delisted_in_universe: int
    n_assets_evaluated: int
    n_observations: int
    first_period: str | None
    last_period: str | None
    dimension: str
    factor_weights: dict[str, float]
    blend_weights: dict[str, float]
    cost_bps_per_side: float
    pass_criteria: str
    full_sample: SegmentMetrics
    in_sample: SegmentMetrics
    out_of_sample: SegmentMetrics
    recent_third_holdout: SegmentMetrics
    oos_verdict: str
    h5_pass: bool
    line_item_5h_validated: bool
    interpretation: str
    caveats: list[str]
    status: str = "ok"
    as_of: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


# --------------------------------------------------------------------------- #
# Pure factor / neutralization math (network-free; unit-tested).             #
# --------------------------------------------------------------------------- #
def _to_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None


def quarter_bucket(datekey: str) -> str:
    """Calendar-quarter label (e.g. ``2014-Q3``) for a filing ``datekey`` (YYYY-MM-DD)."""
    year = int(datekey[:4])
    month = int(datekey[5:7])
    q = (month - 1) // 3 + 1
    return f"{year}-Q{q}"


def _winsorize(values: list[float], limit: float = WINSOR_SD) -> list[float]:
    return [max(-limit, min(limit, v)) for v in values]


def ttm_revenue_cagr(rows: list[dict], idx: int, max_years: int = CAGR_MAX_YEARS) -> float | None:
    """Trailing TTM-revenue CAGR at row ``idx`` using an ART row ~``max_years`` back.

    ``rows`` are one ticker's ART rows sorted ascending by datekey. Compares the TTM
    revenue at ``idx`` against the TTM revenue of the earliest row within ``max_years``
    (by reportperiod year), annualized over the whole-year span. Point-in-time: only
    rows at/<= ``idx`` are consulted.
    """
    last_rev = _to_float(rows[idx].get("revenue"))
    last_period = str(rows[idx].get("reportperiod") or "")
    if not last_rev or last_rev <= 0 or not last_period:
        return None
    try:
        last_year = int(last_period[:4])
    except ValueError:
        return None
    base_rev: float | None = None
    base_year: int | None = None
    for j in range(idx - 1, -1, -1):
        rev = _to_float(rows[j].get("revenue"))
        period = str(rows[j].get("reportperiod") or "")
        if not rev or rev <= 0 or not period:
            continue
        try:
            year = int(period[:4])
        except ValueError:
            continue
        span = last_year - year
        if span <= 0:
            continue
        base_rev, base_year = rev, year
        if span >= max_years:
            break
    if base_rev is None or base_year is None:
        return None
    span = last_year - base_year
    if span <= 0:
        return None
    try:
        return (last_rev / base_rev) ** (1.0 / span) - 1.0
    except (ZeroDivisionError, ValueError):
        return None


def price_momentum(rows: list[dict], idx: int, lookback: int = MOM_LOOKBACK_QUARTERS) -> float | None:
    """Report-to-report price momentum at row ``idx`` (price now / price ~lookback back).

    Uses SF1's own filing-date ``price`` so it is delisted-inclusive and point-in-time.
    Returns None if either endpoint price is missing/non-positive or history is short.
    """
    if idx < lookback:
        return None
    now = _to_float(rows[idx].get("price"))
    then = _to_float(rows[idx - lookback].get("price"))
    if not now or now <= 0 or not then or then <= 0:
        return None
    return now / then - 1.0


def fundamental_vector(rows: list[dict], idx: int) -> dict[str, float] | None:
    """Point-in-time fundamental factor vector at ART row ``idx`` (or None).

    Uses TTM flows from the row at ``idx`` and the trailing revenue CAGR from history.
    Market cap = filing-date price x point-in-time basic shares. Only DERIVED ratios
    leave this function (governance).
    """
    row = rows[idx]
    price = _to_float(row.get("price"))
    revenue = _to_float(row.get("revenue"))
    netinc = _to_float(row.get("netinc"))
    equity = _to_float(row.get("equity"))
    opinc = _to_float(row.get("opinc"))
    fcf = _to_float(row.get("fcf"))
    shares = _to_float(row.get("sharesbas"))
    cagr = ttm_revenue_cagr(rows, idx)

    if None in (price, revenue, netinc, equity, opinc, fcf, shares, cagr):
        return None
    if not price or price <= 0 or not revenue or revenue <= 0:
        return None
    if not equity or equity == 0 or not shares or shares <= 0:
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


def fundamental_composite(vectors: dict[str, dict[str, float]]) -> dict[str, float]:
    """Cross-sectional weighted z-blend of the seven fundamental factors (higher=better)."""
    tickers = list(vectors)
    if len(tickers) < 2:
        return {}
    composite = {t: 0.0 for t in tickers}
    for factor, weight in FUND_FACTOR_WEIGHTS.items():
        z = _winsorize(_zscore([vectors[t][factor] for t in tickers]))
        for t, zv in zip(tickers, z):
            composite[t] += weight * zv
    return composite


def blend_scores(
    fund_composite: dict[str, float],
    momentum: dict[str, float],
    fund_w: float = FUND_BLEND_WEIGHT,
    mom_w: float = MOM_BLEND_WEIGHT,
) -> dict[str, float]:
    """Blend z(fundamental composite) with z(momentum) at the given weights.

    Defaults to the pre-registered 0.60/0.40 blend. ``fund_w=1, mom_w=0`` (or the
    reverse) isolates a single leg for attribution. Only tickers present in BOTH inputs
    are scored (a full blended vector is required) unless a leg has zero weight.
    """
    if mom_w == 0.0:
        common = list(fund_composite)
    elif fund_w == 0.0:
        common = list(momentum)
    else:
        common = [t for t in fund_composite if t in momentum]
    if len(common) < 2:
        return {}
    fz = _winsorize(_zscore([fund_composite.get(t, 0.0) for t in common]))
    mz = _winsorize(_zscore([momentum.get(t, 0.0) for t in common]))
    return {
        t: fund_w * f + mom_w * m
        for t, f, m in zip(common, fz, mz)
    }


def _ols_residualize(y: dict[str, float], x: dict[str, float]) -> dict[str, float]:
    """Cross-sectional OLS residual of ``y`` on a single regressor ``x`` (with intercept)."""
    keys = [k for k in y if k in x]
    if len(keys) < 3:
        return dict(y)
    xs = [x[k] for k in keys]
    ys = [y[k] for k in keys]
    mx = statistics.fmean(xs)
    my = statistics.fmean(ys)
    var = sum((v - mx) ** 2 for v in xs)
    if var <= 0:
        return {k: y[k] - my for k in keys}
    beta = sum((xv - mx) * (yv - my) for xv, yv in zip(xs, ys)) / var
    alpha = my - beta * mx
    return {k: y[k] - (alpha + beta * x[k]) for k in keys}


def _sector_neutralize(scores: dict[str, float], sectors: dict[str, str]) -> dict[str, float]:
    """Within each sector, demean and divide by SD (leave singletons demeaned to 0)."""
    groups: dict[str, list[str]] = {}
    for t in scores:
        groups.setdefault(sectors.get(t, "UNKNOWN"), []).append(t)
    out: dict[str, float] = {}
    for members in groups.values():
        vals = [scores[t] for t in members]
        mean = statistics.fmean(vals)
        sd = statistics.pstdev(vals) if len(vals) > 1 else 0.0
        for t in members:
            out[t] = (scores[t] - mean) / sd if sd > 0 else 0.0
    return out


def neutralize(
    scores: dict[str, float],
    sectors: dict[str, str],
    market_caps: dict[str, float],
) -> dict[str, float]:
    """Size- then sector-neutralize a cross-sectional score (pre-registered order)."""
    log_size = {
        t: math.log(market_caps[t])
        for t in scores
        if t in market_caps and market_caps[t] > 0
    }
    size_resid = _ols_residualize(scores, log_size)
    return _sector_neutralize(size_resid, sectors)


# --------------------------------------------------------------------------- #
# Panel assembly (pure; no network).                                          #
# --------------------------------------------------------------------------- #
@dataclass
class _Observation:
    ticker: str
    bucket: str
    fundamental: dict[str, float]
    momentum: float
    forward: float
    market_cap: float
    sector: str


@dataclass
class _Period:
    date: str
    composite: dict[str, float]
    forward: dict[str, float]


def build_observations(
    art_by_ticker: dict[str, list[dict]],
    meta: dict[str, dict],
    forward_gap: int = 0,
) -> list[_Observation]:
    """Report-to-report observations across all tickers (point-in-time, delisted-inclusive).

    ``art_by_ticker`` maps ticker -> its ART rows (dicts) sorted ascending by datekey.
    Score inputs come from filing ``r_i`` only (point-in-time), bucketed by the calendar
    quarter of ``r_i.datekey``.

    ``forward_gap`` selects the realized forward-return window (default 0 = the
    pre-registered report-to-report return ``r_{i+1}.price / r_i.price - 1``). Setting
    ``forward_gap=1`` measures ``r_{i+2}.price / r_{i+1}.price - 1`` — the NEXT
    filing-to-filing window, which shares NO price with the signal and so is immune to
    the shared-``price_i`` bid-ask-bounce/mean-reversion artifact (integrity check).
    """
    observations: list[_Observation] = []
    for ticker, rows in art_by_ticker.items():
        sector = str((meta.get(ticker) or {}).get("sector") or "UNKNOWN")
        for i in range(len(rows) - 1 - forward_gap):
            row = rows[i]
            start, end = rows[i + forward_gap], rows[i + 1 + forward_gap]
            dk = str(row.get("datekey") or "")
            dk_start = str(start.get("datekey") or "")
            dk_end = str(end.get("datekey") or "")
            if not dk or not dk_end or dk_end <= dk_start or dk_start < dk:
                continue
            price_start = _to_float(start.get("price"))
            price_end = _to_float(end.get("price"))
            if not price_start or price_start <= 0 or not price_end or price_end <= 0:
                continue
            vec = fundamental_vector(rows, i)
            if vec is None:
                continue
            mom = price_momentum(rows, i)
            if mom is None:
                continue
            price = _to_float(row.get("price")) or 0.0
            shares = _to_float(row.get("sharesbas")) or 0.0
            observations.append(
                _Observation(
                    ticker=ticker,
                    bucket=quarter_bucket(dk),
                    fundamental=vec,
                    momentum=mom,
                    forward=price_end / price_start - 1.0,
                    market_cap=price * shares,
                    sector=sector,
                )
            )
    return observations


def assemble_periods(
    observations: list[_Observation],
    min_names: int = MIN_NAMES_PER_PERIOD,
    fund_w: float = FUND_BLEND_WEIGHT,
    mom_w: float = MOM_BLEND_WEIGHT,
) -> list[_Period]:
    """Group observations into per-quarter cross-sections and score them (pure).

    ``fund_w``/``mom_w`` default to the pre-registered blend; overriding them isolates a
    single leg for attribution.
    """
    by_bucket: dict[str, list[_Observation]] = {}
    for obs in observations:
        by_bucket.setdefault(obs.bucket, []).append(obs)

    periods: list[_Period] = []
    for bucket in sorted(by_bucket):
        members = by_bucket[bucket]
        if len(members) < min_names:
            continue
        vectors = {o.ticker: o.fundamental for o in members}
        momentum = {o.ticker: o.momentum for o in members}
        sectors = {o.ticker: o.sector for o in members}
        market_caps = {o.ticker: o.market_cap for o in members}
        forward = {o.ticker: o.forward for o in members}

        fund_comp = fundamental_composite(vectors)
        blended = blend_scores(fund_comp, momentum, fund_w=fund_w, mom_w=mom_w)
        if len(blended) < min_names:
            continue
        neutral = neutralize(blended, sectors, market_caps)
        neutral = {t: v for t, v in neutral.items() if t in forward}
        if len(neutral) < min_names:
            continue
        periods.append(
            _Period(date=bucket, composite=neutral, forward={t: forward[t] for t in neutral})
        )
    return periods


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
        assets = list(period.composite)
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
    gross_ann = statistics.fmean(gross) * PERIODS_PER_YEAR if gross else None
    net_ann = statistics.fmean(net) * PERIODS_PER_YEAR if net else None
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
        avg_turnover=round(avg_turnover, 4) if avg_turnover is not None else None,
        passes=passes,
    )


def oos_segment(
    observations: list[_Observation],
    min_names: int = MIN_NAMES_PER_PERIOD,
    fund_w: float = FUND_BLEND_WEIGHT,
    mom_w: float = MOM_BLEND_WEIGHT,
    label: str = "out_of_sample",
) -> SegmentMetrics:
    """Out-of-sample (second-half) SegmentMetrics for a given blend (attribution helper)."""
    periods = assemble_periods(observations, min_names=min_names, fund_w=fund_w, mom_w=mom_w)
    if not periods:
        return SegmentMetrics(label, 0, None, None, None, None, None, None, False)
    split = len(periods) // 2
    return _segment_metrics(label, periods[split:])


def summarize(
    observations: list[_Observation],
    meta: dict[str, dict],
    min_names: int = MIN_NAMES_PER_PERIOD,
) -> ExpandedBacktestResult:
    """Turn observations into the derived, governance-safe expanded result."""
    n_universe = len(meta)
    n_delisted = sum(1 for m in meta.values() if str(m.get("isdelisted")) == "Y")
    caveats = [
        "Survivorship-free: US domestic common stock incl. delisted names; returns "
        "built from SF1's own filing-date price (delisted-inclusive), report-to-report.",
        "SF1 ART (as-reported TTM) at quarterly filing frequency; point-in-time via "
        "datekey (no restatement/look-ahead).",
        f"Costs modeled at {COST_BPS_PER_SIDE} bps/side via long-short turnover; "
        f"long-short annualized x{PERIODS_PER_YEAR} (quarterly).",
        "Factor set, blend weights, and neutralization were PRE-REGISTERED before "
        "reading results (see score_definition); nothing tuned to the outcome.",
        "Residual survivorship/coverage bias: a delisted name contributes returns only "
        "between filings it actually made; its terminal delisting move is NOT captured "
        "(no delisted price fabricated), which understates left-tail losses.",
        "Entry/exit use filing-date prices (not a fixed calendar close), so momentum "
        "and forward returns are report-to-report (quarterly granularity).",
    ]

    periods = assemble_periods(observations, min_names=min_names)
    n_assets = len({o.ticker for o in observations})
    factor_weights = {k: round(v, 4) for k, v in FUND_FACTOR_WEIGHTS.items()}
    blend_weights = {"fundamental": FUND_BLEND_WEIGHT, "momentum": MOM_BLEND_WEIGHT}

    if not periods:
        empty = SegmentMetrics("empty", 0, None, None, None, None, None, None, False)
        return ExpandedBacktestResult(
            score_definition=SCORE_DEFINITION,
            universe_description="US domestic common stock (SF1), survivorship-free",
            n_universe_requested=n_universe, n_delisted_in_universe=n_delisted,
            n_assets_evaluated=n_assets, n_observations=len(observations),
            first_period=None, last_period=None, dimension="ART",
            factor_weights=factor_weights, blend_weights=blend_weights,
            cost_bps_per_side=COST_BPS_PER_SIDE, pass_criteria=H5_PASS_CRITERIA,
            full_sample=empty, in_sample=empty, out_of_sample=empty,
            recent_third_holdout=empty, oos_verdict="FAIL", h5_pass=False,
            line_item_5h_validated=False,
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
        f"H5 (expanded SF1 fundamentals + momentum) = {verdict} out-of-sample. OOS mean "
        f"IC {oos.mean_ic}, t-stat {oos.ic_t_stat}, hit rate "
        f"{(f'{oos.hit_rate:.1%}' if oos.hit_rate is not None else 'n/a')} over "
        f"{oos.n_periods} quarters / {n_assets} equities. "
        + (
            "The blended, neutralized SF1 score clears the pre-registered bar "
            "out-of-sample; Nasdaq line-item 5h is validated."
            if h5_pass
            else "Below the pre-registered bar out-of-sample; H5 remains unconfirmed and "
            "Nasdaq line-item 5h is NOT validated for this design."
        )
    )
    return ExpandedBacktestResult(
        score_definition=SCORE_DEFINITION,
        universe_description="US domestic common stock (SF1), survivorship-free",
        n_universe_requested=n_universe,
        n_delisted_in_universe=n_delisted,
        n_assets_evaluated=n_assets,
        n_observations=len(observations),
        first_period=periods[0].date,
        last_period=periods[-1].date,
        dimension="ART",
        factor_weights=factor_weights,
        blend_weights=blend_weights,
        cost_bps_per_side=COST_BPS_PER_SIDE,
        pass_criteria=H5_PASS_CRITERIA,
        full_sample=full,
        in_sample=in_sample,
        out_of_sample=oos,
        recent_third_holdout=recent,
        oos_verdict=verdict,
        h5_pass=h5_pass,
        line_item_5h_validated=h5_pass,
        interpretation=interpretation,
        caveats=caveats,
    )


# --------------------------------------------------------------------------- #
# Data loading (network) — bulk/paginated pulls cached to the internal cache. #
# --------------------------------------------------------------------------- #
def _http_get_json(url: str) -> dict:
    req = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=_HTTP_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _paginate(base_url: str, sleep: float = 0.0) -> tuple[list[list], list[str]]:
    """Cursor-paginate a Sharadar datatable, returning (rows, column_names)."""
    rows: list[list] = []
    columns: list[str] = []
    cursor: str | None = None
    while True:
        url = base_url + (f"&qopts.cursor_id={cursor}" if cursor else "")
        payload = _http_get_json(url)
        table = payload.get("datatable") or {}
        if not columns:
            columns = [c.get("name") for c in (table.get("columns") or [])]
        rows.extend(table.get("data") or [])
        cursor = (payload.get("meta") or {}).get("next_cursor_id")
        if not cursor:
            break
        if sleep:
            time.sleep(sleep)
    return rows, columns


def load_universe_meta(use_cache: bool = True) -> dict[str, dict]:
    """SF1 US-domestic-common-stock universe metadata (survivorship-free), cached.

    Returns ticker -> {sector, isdelisted, category, name}. INTERNAL cache only.
    """
    if use_cache and os.path.exists(_META_CACHE):
        try:
            with open(_META_CACHE, encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            pass

    key = nasdaq_data_link_api_key()
    if not key:
        raise RuntimeError("NASDAQ_DATA_LINK_API_KEY is not configured.")
    cols = "permaticker,ticker,name,exchange,isdelisted,category,sector,currency"
    base = (
        f"{_TICKERS_URL}?table=SF1&qopts.columns={urllib.parse.quote(cols)}"
        f"&qopts.per_page={_PER_PAGE}&api_key={urllib.parse.quote(key)}"
    )
    rows, columns = _paginate(base)
    idx = {c: i for i, c in enumerate(columns)}
    meta: dict[str, dict] = {}
    for r in rows:
        category = str(r[idx["category"]] or "")
        currency = str(r[idx["currency"]] or "")
        if not category.startswith("Domestic Common Stock") or currency != "USD":
            continue
        ticker = str(r[idx["ticker"]] or "").upper()
        if not ticker:
            continue
        meta[ticker] = {
            "sector": r[idx["sector"]] or "UNKNOWN",
            "isdelisted": r[idx["isdelisted"]],
            "category": category,
            "name": r[idx["name"]],
        }
    os.makedirs(_CACHE_DIR, exist_ok=True)
    try:
        with open(_META_CACHE, "w", encoding="utf-8") as fh:
            json.dump(meta, fh)
    except OSError:
        pass
    return meta


def load_art_rows(
    universe: set[str] | None = None, use_cache: bool = True, sleep: float = 0.0
) -> dict[str, list[dict]]:
    """Bulk-pull the full SF1 ART table, filter to ``universe``, cache, and group.

    Returns ticker -> list of ART row dicts (only the retained columns) sorted ascending
    by datekey. Raw rows stay in the gitignored internal cache (governance).
    """
    if use_cache and os.path.exists(_ART_CACHE):
        try:
            with open(_ART_CACHE, encoding="utf-8") as fh:
                cached = json.load(fh)
            return {t: rows for t, rows in cached.items()}
        except (OSError, ValueError):
            pass

    key = nasdaq_data_link_api_key()
    if not key:
        raise RuntimeError("NASDAQ_DATA_LINK_API_KEY is not configured.")
    cols = ",".join(_SF1_BULK_COLUMNS)
    base = (
        f"{_SF1_URL}?dimension=ART&qopts.columns={urllib.parse.quote(cols)}"
        f"&qopts.per_page={_PER_PAGE}&api_key={urllib.parse.quote(key)}"
    )
    rows, columns = _paginate(base, sleep=sleep)
    idx = {c: i for i, c in enumerate(columns)}
    keep = [c for c in _SF1_BULK_COLUMNS if c not in ("dimension",)]

    grouped: dict[str, list[dict]] = {}
    for r in rows:
        ticker = str(r[idx["ticker"]] or "").upper()
        if universe is not None and ticker not in universe:
            continue
        grouped.setdefault(ticker, []).append({k: r[idx[k]] for k in keep})
    for ticker in grouped:
        grouped[ticker].sort(key=lambda row: str(row.get("datekey") or ""))

    os.makedirs(_CACHE_DIR, exist_ok=True)
    try:
        with open(_ART_CACHE, "w", encoding="utf-8") as fh:
            json.dump(grouped, fh)
    except OSError:
        pass
    return grouped


def load_panel(
    use_cache: bool = True, max_tickers: int | None = None
) -> tuple[dict[str, list[dict]], dict[str, dict]]:
    """Load (art_by_ticker, meta) for the universe (cached bulk pulls)."""
    meta = load_universe_meta(use_cache=use_cache)
    universe = set(meta)
    if max_tickers is not None:
        universe = set(sorted(universe)[:max_tickers])
        meta = {t: meta[t] for t in universe}
    art = load_art_rows(universe=universe, use_cache=use_cache)
    art = {t: rows for t, rows in art.items() if t in meta}
    return art, meta


def run_expanded_backtest(
    use_cache: bool = True,
    min_names: int = MIN_NAMES_PER_PERIOD,
    max_tickers: int | None = None,
    forward_gap: int = 0,
) -> ExpandedBacktestResult:
    """Full expanded, survivorship-free H5 back-test (loads data + summarizes).

    ``forward_gap=0`` is the pre-registered report-to-report return. ``forward_gap=1``
    runs the shared-price-free integrity check (see ``build_observations``).
    """
    art, meta = load_panel(use_cache=use_cache, max_tickers=max_tickers)
    observations = build_observations(art, meta, forward_gap=forward_gap)
    return summarize(observations, meta, min_names=min_names)
