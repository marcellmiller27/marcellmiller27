# JHI-SIG: 69M2705M | H5 EXPANDED validation runner | JHI Research & Analytics Firm, Inc. (proprietary)
"""Run the expanded, survivorship-free SF1 fundamentals+momentum H5 validation and print
a derived metrics table (governance-safe: no raw SF1 rows leave this process).

Usage (from repo root, with the backend venv):

    /workspace/.venv/bin/python backend/scripts/run_h5_expanded_validation.py
    /workspace/.venv/bin/python backend/scripts/run_h5_expanded_validation.py --refresh
    /workspace/.venv/bin/python backend/scripts/run_h5_expanded_validation.py --json out.json

Requires NASDAQ_DATA_LINK_API_KEY (Sharadar SF1/TICKERS). Bulk pulls are cached in the
gitignored backend/.sf1_cache/ so reruns are deterministic/fast.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

from app.sf1_expanded_backtest import SegmentMetrics, run_expanded_backtest  # noqa: E402


def _fmt(value: object) -> str:
    return "n/a" if value is None else str(value)


def _row(m: SegmentMetrics) -> str:
    return (
        f"| {m.label:<28} | {m.n_periods:>3} | {_fmt(m.mean_ic):>7} | "
        f"{_fmt(m.ic_t_stat):>6} | {_fmt(m.hit_rate):>6} | "
        f"{_fmt(m.gross_annualized_long_short):>8} | "
        f"{_fmt(m.net_annualized_long_short):>8} | {_fmt(m.avg_turnover):>8} | "
        f"{'PASS' if m.passes else 'FAIL':>4} |"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="H5 expanded SF1 validation")
    parser.add_argument("--refresh", action="store_true", help="force fresh bulk SF1 pulls")
    parser.add_argument("--min-names", type=int, default=None, help="min names per quarter")
    parser.add_argument("--max-tickers", type=int, default=None, help="cap universe (debug)")
    parser.add_argument("--json", metavar="PATH", help="also write the derived result as JSON")
    args = parser.parse_args()

    kwargs = {"use_cache": not args.refresh}
    if args.min_names is not None:
        kwargs["min_names"] = args.min_names
    if args.max_tickers is not None:
        kwargs["max_tickers"] = args.max_tickers
    result = run_expanded_backtest(**kwargs)

    print("=" * 104)
    print("H5 EXPANDED VALIDATION — SURVIVORSHIP-FREE SF1 FUNDAMENTALS + MOMENTUM (point-in-time)")
    print("=" * 104)
    print(f"Score definition : {result.score_definition}")
    print(f"Pre-registered   : {result.pass_criteria}")
    print(f"Fund. weights    : {result.factor_weights}")
    print(f"Blend weights    : {result.blend_weights}")
    print(
        f"Universe         : {result.n_assets_evaluated} equities evaluated "
        f"(of {result.n_universe_requested} US common stocks; "
        f"{result.n_delisted_in_universe} delisted) — dimension {result.dimension}"
    )
    print(f"Observations     : {result.n_observations} report-to-report pairs")
    print(f"Panel window     : {result.first_period} -> {result.last_period}")
    print(f"Costs            : {result.cost_bps_per_side} bps/side")
    print("-" * 104)
    header = (
        f"| {'segment':<28} | {'N':>3} | {'meanIC':>7} | {'t-stat':>6} | "
        f"{'hit':>6} | {'grossLS':>8} | {'netLS':>8} | {'turnovr':>8} | {'H5?':>4} |"
    )
    print(header)
    print("|" + "-" * (len(header) - 2) + "|")
    for seg in (
        result.full_sample,
        result.in_sample,
        result.out_of_sample,
        result.recent_third_holdout,
    ):
        print(_row(seg))
    print("-" * 104)
    print(f"OUT-OF-SAMPLE VERDICT (decisive) : {result.oos_verdict}  (h5_pass={result.h5_pass})")
    print(f"Nasdaq line-item 5h validated    : {result.line_item_5h_validated}")
    print()
    print(result.interpretation)
    print()
    print("Caveats:")
    for caveat in result.caveats:
        print(f"  - {caveat}")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(asdict(result), fh, indent=2, default=str)
        print(f"\nWrote derived JSON -> {args.json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
