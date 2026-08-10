#!/usr/bin/env python
# JHI-SIG: 69M2705M | Daily data-refresh entrypoint | JHI Research & Analytics Firm, Inc. (proprietary)
"""Lightweight scheduled-refresh entrypoint for the Data Foundation.

Pulls every registry-backed series into the in-process cache + last-good store so the
on-demand path serves warm, cadence-aware, as-of-disclosed values (and last-good on any
transient outage). Real scheduler wiring can be minimal — cron/systemd-timer this script,
or call ``POST /api/v1/market/refresh``; the on-demand + last-good path is the priority.

Usage (from the ``backend/`` directory, via the project venv):

    ../.venv/bin/python -m scripts.refresh_data_cache            # all registry series
    ../.venv/bin/python -m scripts.refresh_data_cache BTC SPX    # a subset

Governance: derived-only; never pulls or persists raw licensed SF1 rows (SF1/EDGAR are
excluded from the refresh set and pulled by their own governed harnesses).
"""

from __future__ import annotations

import json
import sys

from app.market_services import MarketDataService


def main(argv: list[str]) -> int:
    symbols = argv or None
    summary = MarketDataService().refresh_all(symbols)
    print(json.dumps(summary, indent=2))
    # Non-zero exit if every requested series failed to deliver (nothing warmed).
    delivered = summary["current"] + summary["overdue"] + summary["fetch_failed"]
    return 0 if delivered > 0 or summary["requested"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
