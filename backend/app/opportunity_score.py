# JHI-SIG: 69M2705M | Research & Opportunity Score | John Henry Investments (proprietary)
"""John Henry Opportunity Score — a defined, testable multi-factor model.

OBJECTIVE: replace the undefined/ad-hoc score with a transparent, reproducible
0-100 cross-sectional score whose predictive validity can be measured (thesis H5).

The score blends four well-documented equity-style factors, each computed from a
monthly close-price series and standardized cross-sectionally (z-score) within the
scoring date, then combined with fixed published weights:

  - momentum_12_1 (weight 0.50): return from t-12 to t-1 (skip the most recent
    month to avoid short-term reversal). The most robust cross-sectional factor.
  - low_volatility (weight 0.20): negative of trailing 12-month return volatility
    (the low-volatility premium).
  - trend (weight 0.20): +1 if price is above its 10-month moving average, else 0
    (a time-series trend filter).
  - reversal_guard (weight 0.10): negative of the last 1-month return (penalize
    one-month spikes likely to revert).

`composite_scores` returns the raw blended factor per asset; `opportunity_scores`
maps those to a 0-100 percentile (the published "Opportunity Score").

All functions are pure (operate on plain price lists), so the model is unit-testable
without any network access and is reused by both the live scorer and the back-test.
"""

from __future__ import annotations

import statistics

WEIGHTS = {
    "momentum_12_1": 0.50,
    "low_volatility": 0.20,
    "trend": 0.20,
    "reversal_guard": 0.10,
}
MIN_HISTORY = 13  # need t-12 .. t


def _zscore(values: list[float]) -> list[float]:
    if len(values) < 2:
        return [0.0] * len(values)
    mean = statistics.fmean(values)
    sd = statistics.pstdev(values)
    if sd == 0:
        return [0.0] * len(values)
    return [(v - mean) / sd for v in values]


def _factors_at(closes: list[float], t: int) -> dict[str, float] | None:
    """Raw (un-standardized) factor values for one asset at month index ``t``."""
    if t < 12 or t >= len(closes):
        return None
    momentum = closes[t - 1] / closes[t - 12] - 1.0
    rets = [closes[i] / closes[i - 1] - 1.0 for i in range(t - 11, t + 1)]
    volatility = statistics.pstdev(rets) if len(rets) > 1 else 0.0
    window = closes[t - 9 : t + 1] if t >= 9 else closes[: t + 1]
    sma = statistics.fmean(window)
    trend = 1.0 if closes[t] > sma else 0.0
    reversal_guard = -(closes[t] / closes[t - 1] - 1.0)
    return {
        "momentum_12_1": momentum,
        "low_volatility": -volatility,
        "trend": trend,
        "reversal_guard": reversal_guard,
    }


def composite_scores(series_by_asset: dict[str, list[float]], t: int) -> dict[str, float]:
    """Cross-sectional blended factor score per asset at month index ``t``."""
    raw: dict[str, dict[str, float]] = {}
    for asset, closes in series_by_asset.items():
        factors = _factors_at(closes, t)
        if factors is not None:
            raw[asset] = factors
    if len(raw) < 2:
        return {}

    assets = list(raw.keys())
    composite = {asset: 0.0 for asset in assets}
    for factor, weight in WEIGHTS.items():
        zs = _zscore([raw[asset][factor] for asset in assets])
        for asset, z in zip(assets, zs):
            composite[asset] += weight * z
    return composite


def opportunity_scores(series_by_asset: dict[str, list[float]], t: int) -> dict[str, float]:
    """0-100 percentile-ranked Opportunity Score per asset at month index ``t``."""
    composite = composite_scores(series_by_asset, t)
    if not composite:
        return {}
    ordered = sorted(composite.items(), key=lambda kv: kv[1])
    n = len(ordered)
    if n == 1:
        return {ordered[0][0]: 50.0}
    return {asset: round(rank / (n - 1) * 100.0, 1) for rank, (asset, _v) in enumerate(ordered)}
