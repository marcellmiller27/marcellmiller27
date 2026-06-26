#!/usr/bin/env python3
"""Straight-line amortization schedule generator for capitalized IP.

Illustrative defaults — replace `CAPITALIZED_AMOUNT` with the real capitalized cost
once determined with your CPA. Pure standard library.
Run: python3 docs/ip/generate_amortization.py
"""

from __future__ import annotations

import csv
import os
from decimal import ROUND_HALF_UP, Decimal

# --- Assumptions (edit these) -------------------------------------------------
CAPITALIZED_AMOUNT = Decimal("180000.00")  # internally-developed platform IP (ASC 350-40)
USEFUL_LIFE_MONTHS = 36                      # straight-line useful life
IN_SERVICE_YEAR = 2026
IN_SERVICE_MONTH = 7                         # first month amortization is recorded
HERE = os.path.dirname(os.path.abspath(__file__))


def _money(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def schedule() -> list[dict]:
    monthly = (CAPITALIZED_AMOUNT / USEFUL_LIFE_MONTHS).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    rows = []
    opening = CAPITALIZED_AMOUNT
    accumulated = Decimal("0.00")
    year, month = IN_SERVICE_YEAR, IN_SERVICE_MONTH
    for i in range(USEFUL_LIFE_MONTHS):
        # Final period absorbs rounding so closing NBV lands exactly at 0.
        amort = monthly if i < USEFUL_LIFE_MONTHS - 1 else opening
        accumulated += amort
        closing = opening - amort
        rows.append(
            {
                "period": f"{year:04d}-{month:02d}",
                "opening_nbv": _money(opening),
                "amortization": _money(amort),
                "accumulated_amortization": _money(accumulated),
                "closing_nbv": _money(closing),
            }
        )
        opening = closing
        month += 1
        if month > 12:
            month = 1
            year += 1
    return rows


def main() -> None:
    rows = schedule()
    path = os.path.join(HERE, "amortization_schedule.csv")
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(
        f"Capitalized {CAPITALIZED_AMOUNT} over {USEFUL_LIFE_MONTHS} months "
        f"=> {rows[0]['amortization']}/mo. Wrote {path}"
    )


if __name__ == "__main__":
    main()
