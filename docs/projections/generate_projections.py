#!/usr/bin/env python3
"""Generate 12-month cash-flow CSV projections and break-even SVG charts.

Reproducible model behind docs/CASHFLOW_PROJECTION_12MO.md. Pure standard library
(no dependencies). Run: `python3 docs/projections/generate_projections.py`.
"""

from __future__ import annotations

import csv
import math
import os

ARPU = 70.0
TICKETS_PER_USER = 0.5
SCENARIOS = {
    "conservative": (50, 0.177),
    "base": (100, 0.234),
    "optimistic": (150, 0.308),
}
HERE = os.path.dirname(os.path.abspath(__file__))


def cloud_tier(users: int) -> int:
    if users < 500:
        return 450
    if users < 1500:
        return 800
    if users < 3000:
        return 1300
    return 2200


def lean_cost(users: int, tickets: int) -> float:
    human = 0 if users < 500 else (1500 if users < 2000 else 3000)
    return cloud_tier(users) + tickets * 0.05 + human


def staffed_cost(users: int, tickets: int) -> float:
    agents = max(3, math.ceil(tickets / 900))
    return cloud_tier(users) + agents * 4800 + 5200


def stripe_fees(revenue: float, users: int) -> float:
    return revenue * 0.029 + users * 0.30


def project(start: int, growth: float) -> list[dict]:
    rows = []
    cum_lean = cum_staffed = 0.0
    for m in range(1, 13):
        users = round(start * (1 + growth) ** (m - 1))
        tickets = round(users * TICKETS_PER_USER)
        revenue = users * ARPU
        sf = stripe_fees(revenue, users)
        lc = lean_cost(users, tickets)
        sc = staffed_cost(users, tickets)
        net_lean = revenue - lc - sf
        net_staffed = revenue - sc - sf
        cum_lean += net_lean
        cum_staffed += net_staffed
        rows.append(
            {
                "month": m,
                "users": users,
                "revenue": round(revenue),
                "lean_cost": round(lc),
                "staffed_cost": round(sc),
                "stripe_fees": round(sf),
                "net_lean": round(net_lean),
                "net_staffed": round(net_staffed),
                "cum_lean": round(cum_lean),
                "cum_staffed": round(cum_staffed),
            }
        )
    return rows


def write_csv(name: str, rows: list[dict]) -> None:
    path = os.path.join(HERE, f"cashflow_{name}.csv")
    with open(path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def svg_chart(name: str, rows: list[dict]) -> None:
    w, h = 760, 420
    ml, mr, mt, mb = 70, 20, 50, 50
    pw, ph = w - ml - mr, h - mt - mb
    lean = [r["cum_lean"] for r in rows]
    staffed = [r["cum_staffed"] for r in rows]
    ys = lean + staffed + [0]
    ymin, ymax = min(ys), max(ys)
    pad = (ymax - ymin) * 0.08 or 1
    ymin -= pad
    ymax += pad

    def px(m: int) -> float:
        return ml + (m - 1) / 11 * pw

    def py(v: float) -> float:
        return mt + (ymax - v) / (ymax - ymin) * ph

    def line(vals, color):
        pts = " ".join(f"{px(i + 1):.1f},{py(v):.1f}" for i, v in enumerate(vals))
        return f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{pts}"/>'

    def dots(vals, color):
        return "".join(
            f'<circle cx="{px(i + 1):.1f}" cy="{py(v):.1f}" r="3.2" fill="{color}"/>'
            for i, v in enumerate(vals)
        )

    zero_y = py(0)
    grid = ""
    for gx in range(1, 13):
        grid += f'<line x1="{px(gx):.1f}" y1="{mt}" x2="{px(gx):.1f}" y2="{mt+ph}" stroke="#19324a" stroke-width="0.5"/>'
        grid += f'<text x="{px(gx):.1f}" y="{mt+ph+18}" fill="#9db0c0" font-size="11" text-anchor="middle">M{gx}</text>'
    yticks = ""
    for i in range(5):
        v = ymin + (ymax - ymin) * i / 4
        yy = py(v)
        yticks += f'<line x1="{ml}" y1="{yy:.1f}" x2="{ml+pw}" y2="{yy:.1f}" stroke="#19324a" stroke-width="0.5"/>'
        yticks += f'<text x="{ml-8}" y="{yy+4:.1f}" fill="#9db0c0" font-size="11" text-anchor="end">${v/1000:.0f}k</text>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Inter,Arial,sans-serif">
<rect width="{w}" height="{h}" fill="#06121f"/>
<text x="{ml}" y="28" fill="#eef5fb" font-size="17" font-weight="700">Cumulative cash flow — {name.title()} scenario (Lean vs Staffed)</text>
{grid}{yticks}
<line x1="{ml}" y1="{zero_y:.1f}" x2="{ml+pw}" y2="{zero_y:.1f}" stroke="#e3b765" stroke-width="1.5" stroke-dasharray="5 4"/>
<text x="{ml+pw}" y="{zero_y-6:.1f}" fill="#e3b765" font-size="11" text-anchor="end">break-even ($0)</text>
{line(staffed, "#ff8a6e")}{dots(staffed, "#ff8a6e")}
{line(lean, "#1fc585")}{dots(lean, "#1fc585")}
<rect x="{ml+10}" y="{mt+8}" width="12" height="12" fill="#1fc585"/><text x="{ml+28}" y="{mt+18}" fill="#eef5fb" font-size="12">Lean (cloud + AI)</text>
<rect x="{ml+150}" y="{mt+8}" width="12" height="12" fill="#ff8a6e"/><text x="{ml+168}" y="{mt+18}" fill="#eef5fb" font-size="12">Staffed + office</text>
</svg>
'''
    with open(os.path.join(HERE, f"breakeven_{name}.svg"), "w") as fh:
        fh.write(svg)


def main() -> None:
    summary = []
    for name, (start, growth) in SCENARIOS.items():
        rows = project(start, growth)
        write_csv(name, rows)
        svg_chart(name, rows)
        last = rows[-1]
        be = next((r["month"] for r in rows if r["cum_staffed"] > 0), None)
        summary.append(
            {
                "scenario": name,
                "m12_users": last["users"],
                "m12_mrr": last["revenue"],
                "cum_lean_12mo": last["cum_lean"],
                "cum_staffed_12mo": last["cum_staffed"],
                "staffed_breakeven_month": be if be else "none<=12",
            }
        )
    with open(os.path.join(HERE, "summary.csv"), "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)
    print("Generated CSVs and SVG charts in", HERE)


if __name__ == "__main__":
    main()
