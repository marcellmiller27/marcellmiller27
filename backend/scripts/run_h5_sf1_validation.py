# JHI-SIG: 69M2705M | H5 SF1 validation runner | JHI Research & Analytics Firm, Inc. (proprietary)
"""Run the point-in-time SF1 fundamental-factor H5 validation back-test and print a
derived metrics table (governance-safe: no raw SF1 rows leave this process).

Usage (from repo root, with the backend venv):

    /workspace/.venv/bin/python backend/scripts/run_h5_sf1_validation.py
    /workspace/.venv/bin/python backend/scripts/run_h5_sf1_validation.py --no-cache
    /workspace/.venv/bin/python backend/scripts/run_h5_sf1_validation.py --json out.json

Requires NASDAQ_DATA_LINK_API_KEY (Sharadar SF1) + network (Yahoo prices). Raw pulls
are cached in the gitignored backend/.sf1_cache/ so reruns are deterministic/fast.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

from app.sf1_factor_backtest import SegmentMetrics, run_backtest  # noqa: E402


def _fmt(value: object) -> str:
    return "n/a" if value is None else str(value)


def _row(m: SegmentMetrics) -> str:
    return (
        f"| {m.label:<28} | {m.n_periods:>3} | {_fmt(m.mean_ic):>7} | "
        f"{_fmt(m.ic_t_stat):>6} | {_fmt(m.hit_rate):>6} | "
        f"{_fmt(m.gross_annualized_long_short):>8} | "
        f"{_fmt(m.net_annualized_long_short):>8} | {_fmt(m.avg_monthly_turnover):>8} | "
        f"{'PASS' if m.passes else 'FAIL':>4} |"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="H5 SF1 fundamental-factor validation")
    parser.add_argument("--no-cache", action="store_true", help="force fresh SF1/Yahoo pulls")
    parser.add_argument("--json", metavar="PATH", help="also write the derived result as JSON")
    args = parser.parse_args()

    result = run_backtest(use_cache=not args.no_cache)

    print("=" * 96)
    print("H5 VALIDATION — SF1 FUNDAMENTAL-FACTOR OPPORTUNITY SCORE (point-in-time)")
    print("=" * 96)
    print(f"Score definition : {result.score_definition}")
    print(f"Pre-registered   : {result.pass_criteria}")
    print(f"Weights          : {result.factor_weights}")
    print(
        f"Universe         : {result.n_assets} equities with usable PIT data "
        f"(of {len(result.universe)} requested)"
    )
    print(f"Panel window     : {result.first_period} -> {result.last_period}")
    print(f"Costs            : {result.cost_bps_per_side} bps/side")
    print("-" * 96)
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
    print("-" * 96)
    print(f"OUT-OF-SAMPLE VERDICT (decisive) : {result.oos_verdict}  (h5_pass={result.h5_pass})")
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
