"""Build a client-ready Excel workbook of a company's SEC EDGAR financials.

Premium (T1 Enterprise / T2 Professional) deliverable. Data is public-domain SEC
XBRL (freely redistributable). Pure function -> xlsx bytes (unit-testable).
"""

from __future__ import annotations

import io

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from app.edgar_models import EdgarFinancials

NAVY = "0C1F33"
GOLD = "9A6B12"
LIGHT = "EAEFF6"
WHITE = "FFFFFF"

_thin = Side(style="thin", color="C9D3DF")
_BORDER = Border(left=_thin, right=_thin, top=_thin, bottom=_thin)


def _pct(value: float | None) -> str:
    return f"{value * 100:.1f}%" if value is not None else "—"


def company_workbook(fin: EdgarFinancials, branded: bool = False) -> bytes:
    """Return xlsx bytes for one company's headline annual financials.

    branded=True adds the JHI mark line (Enterprise/T1 client-ready output).
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Company Financials"

    # --- Title block ---
    ws.merge_cells("A1:C1")
    ws["A1"] = f"{fin.entity_name} ({fin.ticker})"
    ws["A1"].font = Font(bold=True, size=15, color=NAVY)
    ws.merge_cells("A2:C2")
    ws["A2"] = (
        f"CIK {fin.cik} · FY{fin.fiscal_year or '—'} "
        f"(period ended {fin.period_end or '—'}) · {fin.currency}"
    )
    ws["A2"].font = Font(italic=True, size=9, color="5A6B7D")
    if branded:
        ws.merge_cells("A3:C3")
        ws["A3"] = "John Henry Investments — prepared for client review"
        ws["A3"].font = Font(bold=True, size=9, color=GOLD)

    header_row = 5

    def header(row: int) -> None:
        for col, label in enumerate(["Line item", "Value", "Notes"], start=1):
            c = ws.cell(row=row, column=col, value=label)
            c.font = Font(bold=True, color=WHITE, size=11)
            c.fill = PatternFill("solid", fgColor=NAVY)
            c.alignment = Alignment(horizontal="left", vertical="center")
            c.border = _BORDER

    header(header_row)

    def money(v: float | None) -> str:
        if v is None:
            return "—"
        a = abs(v)
        if a >= 1e12:
            return f"${v / 1e12:.2f}T"
        if a >= 1e9:
            return f"${v / 1e9:.2f}B"
        if a >= 1e6:
            return f"${v / 1e6:.1f}M"
        return f"${v:,.0f}"

    rows = [
        ("Revenue", money(fin.revenue), ""),
        ("Cost of revenue", money(fin.cost_of_revenue), ""),
        ("Gross profit", money(fin.gross_profit), f"Gross margin {_pct(fin.gross_margin)}"),
        ("Operating income", money(fin.operating_income), f"Operating margin {_pct(fin.operating_margin)}"),
        ("Net income", money(fin.net_income), f"Net margin {_pct(fin.net_margin)}"),
        ("Total assets", money(fin.total_assets), ""),
        ("Total liabilities", money(fin.total_liabilities), ""),
        ("Stockholders' equity", money(fin.stockholders_equity), ""),
        ("Cash & equivalents", money(fin.cash_and_equivalents), ""),
    ]
    for i, (label, value, note) in enumerate(rows):
        r = header_row + 1 + i
        ws.cell(row=r, column=1, value=label).font = Font(bold=True, size=10, color=NAVY)
        ws.cell(row=r, column=2, value=value).font = Font(size=10)
        ws.cell(row=r, column=3, value=note).font = Font(size=9, color="5A6B7D")
        fill = PatternFill("solid", fgColor=LIGHT) if i % 2 else PatternFill()
        for col in range(1, 4):
            cell = ws.cell(row=r, column=col)
            cell.border = _BORDER
            if i % 2:
                cell.fill = fill
            cell.alignment = Alignment(vertical="top", wrap_text=True)

    footer = header_row + 1 + len(rows) + 1
    ws.merge_cells(start_row=footer, start_column=1, end_row=footer, end_column=3)
    ws.cell(
        row=footer, column=1,
        value=(
            f"Source: {fin.source}. {fin.disclaimer} "
            "Public SEC data; verify against the original filing."
        ),
    ).font = Font(italic=True, size=8, color="5A6B7D")

    ws.column_dimensions[get_column_letter(1)].width = 24
    ws.column_dimensions[get_column_letter(2)].width = 16
    ws.column_dimensions[get_column_letter(3)].width = 30
    ws.freeze_panes = ws.cell(row=header_row + 1, column=1)

    buffer = io.BytesIO()
    wb.save(buffer)
    return buffer.getvalue()
