# JHI-SIG: 69M2705M | Sales Commission Model | John Henry Investments (proprietary)
"""Generate the interactive Sales Commission Excel model.

A 100%-commission ground-floor rep on Tier 1 ($1,500) + Tier 2 ($299), paid a
monthly residual (% of MRR) while subscriptions stay active. Editable assumptions
drive a live 24-month schedule and a Year-1-by-mix table. No macros.

Run:  python scripts/sales_commission_model.py [output.xlsx]
"""

from __future__ import annotations

import sys
from datetime import date

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.worksheet import Worksheet

SIG = "JHI-SIG: 69M2705M"
ENTITY = "JHI Research & Analytics Firm, Inc."
_ENTITY_HF = ENTITY.replace("&", "&&")

_NAVY_FILL = PatternFill("solid", fgColor="0C1F33")
_SUB_FILL = PatternFill("solid", fgColor="EAEFF6")
_INPUT_FILL = PatternFill("solid", fgColor="FFF6D5")
_WHITE = Font(color="FFFFFF", bold=True)
_BOLD = Font(bold=True)
_MUTED = Font(color="5A6B7D", italic=True, size=9)
_MONEY = '"$"#,##0'
_PCT = '0.0%'
_NAVY = "0C1F33"


def _watermark(ws: Worksheet) -> None:
    ws.oddFooter.left.text = f"&8© {_ENTITY_HF}  ·  {SIG}"
    ws.oddFooter.center.text = "&8Confidential — not for redistribution"
    ws.oddFooter.right.text = "&8Page &P of &N"


def _title(ws: Worksheet, subtitle: str) -> None:
    ws.merge_cells("A1:D1")
    ws["A1"] = ENTITY
    ws["A1"].font = _WHITE
    ws["A1"].fill = _NAVY_FILL
    ws.merge_cells("A2:D2")
    ws["A2"] = subtitle
    ws["A2"].font = Font(bold=True, size=13, color=_NAVY)
    ws.merge_cells("A3:D3")
    ws["A3"] = f"generated {date.today().isoformat()}  ·  {SIG}"
    ws["A3"].font = _MUTED


def build() -> Workbook:
    wb = Workbook()

    # --- Assumptions (editable) ---
    a = wb.active
    a.title = "Assumptions"
    a.column_dimensions["A"].width = 36
    a.column_dimensions["B"].width = 14
    a.column_dimensions["C"].width = 40
    _title(a, "Sales Commission Model — assumptions")
    rows = [
        ("Tier 1 price ($/mo)", 1500, "Enterprise / Family Office"),
        ("Tier 2 price ($/mo)", 299, "Professional"),
        ("Tier 1 mix (% of closes)", 0, "0 = all Tier 2; try 10 or 20"),
        ("Closes per month", 100, "New subs signed each month"),
        ("Residual commission (% of MRR)", 10, "Paid monthly while active"),
        ("Monthly churn (%)", 0, "Subs lost per month"),
        ("Blended gross margin (%)", 96, "For JHI contribution"),
    ]
    r = 5
    for label, val, note in rows:
        a.cell(row=r, column=1, value=label).font = _BOLD
        c = a.cell(row=r, column=2, value=val)
        c.fill = _INPUT_FILL
        a.cell(row=r, column=3, value=note).font = _MUTED
        r += 1
    # cell refs
    p1, p2, mix, closes, resid, churn, gm = (f"B{i}" for i in range(5, 12))

    a.cell(row=13, column=1, value="Avg MRR / sub").font = _BOLD
    a.cell(row=13, column=2, value=f"=${p1[0]}${p1[1:]}*${mix[0]}${mix[1:]}/100+${p2[0]}${p2[1:]}*(1-${mix[0]}${mix[1:]}/100)").number_format = _MONEY

    # Operating assumptions (editable) for the EBITDA view.
    a.cell(row=15, column=1, value="OPERATING ASSUMPTIONS (editable)").font = _BOLD
    a.cell(row=15, column=1).fill = _SUB_FILL
    opex = [
        ("Payment processing (% of revenue)", 3),
        ("Infra / support (% of revenue)", 2),
        ("Data license — SF1 ($/yr, fixed)", 18000),
        ("Marketing ($/yr)", 36000),
        ("Legal & accounting ($/yr)", 18000),
        ("Software & AI tools ($/yr)", 12000),
        ("Founder / ops comp ($/yr)", 60000),
    ]
    rr = 16
    for label, val in opex:
        a.cell(row=rr, column=1, value=label).font = _BOLD
        cc = a.cell(row=rr, column=2, value=val)
        cc.fill = _INPUT_FILL
        cc.number_format = _MONEY if val >= 1000 else "0.0"
        rr += 1
    # Assumptions refs: proc=B16, infra=B17, dataSF1=B18, mktg=B19, legal=B20, sw=B21, founder=B22

    # --- Monthly Model (live 24-month schedule) ---
    m = wb.create_sheet("Monthly Model")
    for col, w in zip("ABCDEFG", (8, 12, 12, 12, 14, 14, 18)):
        m.column_dimensions[col].width = w
    _title(m, "24-month commission schedule (live)")
    headers = ["Month", "New subs", "Active subs", "Avg MRR", "Billed MRR", "Commission", "JHI GM after comm."]
    for c, h in enumerate(headers, start=1):
        cell = m.cell(row=5, column=c, value=h)
        cell.font = _WHITE
        cell.fill = _NAVY_FILL
    first = 6
    for i in range(24):
        row = first + i
        m.cell(row=row, column=1, value=i + 1)
        m.cell(row=row, column=2, value=f"=Assumptions!${closes[0]}${closes[1:]}")
        if i == 0:
            active = f"=B{row}"
        else:
            active = f"=C{row-1}*(1-Assumptions!${churn[0]}${churn[1:]}/100)+B{row}"
        m.cell(row=row, column=3, value=active).number_format = "#,##0"
        m.cell(row=row, column=4, value="=Assumptions!$B$13").number_format = _MONEY
        m.cell(row=row, column=5, value=f"=C{row}*D{row}").number_format = _MONEY
        m.cell(row=row, column=6, value=f"=E{row}*Assumptions!${resid[0]}${resid[1:]}/100").number_format = _MONEY
        m.cell(row=row, column=7, value=f"=E{row}*Assumptions!${gm[0]}${gm[1:]}/100-F{row}").number_format = _MONEY
    last = first + 23
    y1 = first + 11
    # Summary
    s = last + 2
    m.cell(row=s, column=1, value="Year-1 commission").font = _BOLD
    m.cell(row=s, column=6, value=f"=SUM(F{first}:F{y1})").number_format = _MONEY
    m.cell(row=s + 1, column=1, value="Year-2 commission").font = _BOLD
    m.cell(row=s + 1, column=6, value=f"=SUM(F{y1+1}:F{last})").number_format = _MONEY
    m.cell(row=s + 2, column=1, value="Exit run-rate (mo 12 × 12)").font = _BOLD
    m.cell(row=s + 2, column=6, value=f"=F{y1}*12").number_format = _MONEY
    m.cell(row=s + 3, column=1, value="Year-1 JHI GM after commission").font = _BOLD
    m.cell(row=s + 3, column=7, value=f"=SUM(G{first}:G{y1})").number_format = _MONEY

    # --- Year-1 by mix (reference; no-churn ramp = residual% × avgMRR × closes × 78) ---
    x = wb.create_sheet("Year-1 by Mix")
    for col, w in zip("ABCD", (18, 16, 22, 22)):
        x.column_dimensions[col].width = w
    _title(x, "Year-1 commission by Tier 1 / Tier 2 mix")
    x.cell(row=5, column=1, value="Ramp basis: 100 closes/mo → sub-months = closes × (1+2+…+12) = closes × 78 (no churn).").font = _MUTED
    hdr = ["Mix (T1 / T2)", "Avg MRR", "Year-1 commission", "Exit run-rate (yr)"]
    for c, h in enumerate(hdr, start=1):
        cell = x.cell(row=7, column=c, value=h)
        cell.font = _WHITE
        cell.fill = _NAVY_FILL
    mixes = [(0, "0% / 100%"), (10, "10% / 90%"), (20, "20% / 80%")]
    rr = 8
    for pct, label in mixes:
        avg = f"=Assumptions!$B$5*{pct}/100+Assumptions!$B$6*(1-{pct}/100)"
        # note: B5/B6 are prices? prices are B5=Tier1,B6=Tier2 -> yes rows 5,6
        x.cell(row=rr, column=1, value=label).font = _BOLD
        x.cell(row=rr, column=2, value=avg).number_format = _MONEY
        x.cell(row=rr, column=3,
               value=f"=Assumptions!$B$9/100*B{rr}*Assumptions!$B$8*78").number_format = _MONEY
        x.cell(row=rr, column=4,
               value=f"=Assumptions!$B$8*12*B{rr}*Assumptions!$B$9/100*12").number_format = _MONEY
        rr += 1
    x.cell(row=rr + 1, column=1,
           value="~All-Tier-2 Year-1 ≈ $233K (a light Tier-1 sprinkle → ~$236K).").font = _MUTED

    # --- Year-1 EBITDA by Mix (live P&L parallel to the commission table) ---
    e = wb.create_sheet("Year-1 EBITDA by Mix")
    for col, w in zip("ABCD", (30, 16, 16, 16)):
        e.column_dimensions[col].width = w
    _title(e, "Year-1 EBITDA by Tier 1 / Tier 2 mix")
    e.cell(row=5, column=1, value="Same 100/mo ramp (7,800 sub-months). Aggressive 'ceiling' scenario — see notes.").font = _MUTED
    e.cell(row=6, column=1, value="Tier-1 mix %").font = _BOLD
    for col, pct in zip("BCD", (0, 10, 20)):
        e[f"{col}6"] = pct
        e[f"{col}6"].font = _BOLD
    lines = [
        ("Avg MRR / sub", "=Assumptions!$B$5*{c}6/100+Assumptions!$B$6*(1-{c}6/100)", _MONEY),
        ("Revenue (Year-1)", "={c}7*Assumptions!$B$8*78", _MONEY),
        ("COGS (proc+infra % + SF1)", "={c}8*(Assumptions!$B$16+Assumptions!$B$17)/100+Assumptions!$B$18", _MONEY),
        ("Gross profit", "={c}8-{c}9", _MONEY),
        ("Sales commission (residual)", "={c}8*Assumptions!$B$9/100", _MONEY),
        ("Marketing", "=Assumptions!$B$19", _MONEY),
        ("Legal & accounting", "=Assumptions!$B$20", _MONEY),
        ("Software & AI tools", "=Assumptions!$B$21", _MONEY),
        ("Founder / ops comp", "=Assumptions!$B$22", _MONEY),
        ("Total operating expenses", "=SUM({c}11:{c}15)", _MONEY),
        ("EBITDA", "={c}10-{c}16", _MONEY),
        ("EBITDA margin", "=IF({c}8=0,0,{c}17/{c}8)", _PCT),
    ]
    for i, (label, formula, fmt) in enumerate(lines):
        row = 7 + i
        lc = e.cell(row=row, column=1, value=label)
        if label in ("Gross profit", "Total operating expenses", "EBITDA", "Revenue (Year-1)"):
            lc.font = _BOLD
        for ci, col in enumerate("BCD", start=2):
            cell = e.cell(row=row, column=ci, value=formula.format(c=col))
            cell.number_format = fmt
            if label in ("EBITDA",):
                cell.font = _BOLD

    # --- Legal ---
    lg = wb.create_sheet("Legal & Provenance")
    lg.column_dimensions["A"].width = 100
    lg.cell(row=1, column=1, value=ENTITY).font = Font(bold=True, size=13, color=_NAVY)
    for i, line in enumerate([
        "Internal planning model from user-supplied assumptions — illustrative only, not a forecast, "
        "offer of employment, or compensation guarantee.",
        "Residual commission is paid on active, collected subscriptions only. Consider a residual cap / "
        "step-down and a <90-day churn clawback to protect long-term margin.",
        f"Founder signature of provenance: {SIG}",
        f"© {date.today().year} {ENTITY}. All rights reserved. Confidential.",
    ], start=3):
        cell = lg.cell(row=i, column=1, value=line)
        cell.alignment = Alignment(wrap_text=True, vertical="top")

    for ws in wb.worksheets:
        _watermark(ws)
    return wb


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "JHI_Sales_Commission_Model.xlsx"
    build().save(out)
    print(f"wrote {out}")
