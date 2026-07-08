# JHI-SIG: 69M2705M | PDF Memo Export | John Henry Investments (proprietary)
"""Branded one-page PDF deal memos for Deal X-Ray (Business Quality Assessment) and
Quality of Earnings — the client-ready leave-behind (for sellers, lenders, LPs).

Serif headline for institutional gravitas; every page carries a provenance footer
(legal disclaimer reference + JHI-SIG: 69M2705M + JHI Research & Analytics Firm, Inc.
+ "not for redistribution"). Built with reportlab.
"""

from __future__ import annotations

from datetime import date
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.deal_xray_models import DealInput, DealXRayReport
from app.financial_diligence_models import DiligenceInput, DiligenceReport

SIG = "JHI-SIG: 69M2705M"
ENTITY = "JHI Research & Analytics Firm, Inc."
_NAVY = colors.HexColor("#0C1F33")
_GRID = colors.HexColor("#D5DEE8")
_HEAD = colors.HexColor("#EAEFF6")
_MUTED = colors.HexColor("#5A6B7D")

_DISCLAIMER = (
    "Decision-support analysis from user-supplied figures — NOT investment advice, a "
    "valuation/appraisal, a fairness opinion, an audit, a review, a CPA opinion, or "
    "brokerage. Verify all figures with a quality-of-earnings review and licensed "
    "professionals before making an offer."
)

_styles = getSampleStyleSheet()
_TITLE = ParagraphStyle("JHITitle", parent=_styles["Title"], fontName="Times-Bold",
                        fontSize=18, textColor=_NAVY, spaceAfter=2, alignment=0)
_SUB = ParagraphStyle("JHISub", parent=_styles["Heading2"], fontName="Times-Roman",
                      fontSize=13, textColor=_NAVY, spaceAfter=2)
_META = ParagraphStyle("JHIMeta", parent=_styles["Normal"], fontSize=8, textColor=_MUTED)
_H = ParagraphStyle("JHIH", parent=_styles["Heading3"], fontName="Helvetica-Bold",
                    fontSize=11, textColor=_NAVY, spaceBefore=10, spaceAfter=4)
_BODY = ParagraphStyle("JHIBody", parent=_styles["Normal"], fontSize=9, leading=13)
_SMALL = ParagraphStyle("JHISmall", parent=_styles["Normal"], fontSize=7.5,
                        textColor=_MUTED, leading=10)


def _m(n: float) -> str:
    return f"${n:,.0f}"


def _footer(canvas, doc) -> None:  # noqa: ANN001
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(_MUTED)
    text = (
        f"© {date.today().year} {ENTITY}  ·  {SIG}  ·  "
        f"Confidential — not for redistribution  ·  Page {doc.page}"
    )
    canvas.drawCentredString(letter[0] / 2, 0.4 * inch, text)
    canvas.restoreState()


def _table(rows: list[list[str]], col_widths: list[float], header: bool = True) -> Table:
    t = Table(rows, colWidths=col_widths, hAlign="LEFT")
    style = [
        ("GRID", (0, 0), (-1, -1), 0.5, _GRID),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), _HEAD),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("TEXTCOLOR", (0, 0), (-1, 0), _NAVY),
        ]
    t.setStyle(TableStyle(style))
    return t


def _header_block(business: str, subtitle: str) -> list:
    return [
        Paragraph(ENTITY, _TITLE),
        Paragraph(subtitle, _SUB),
        Paragraph(f"{business}  ·  generated {date.today().isoformat()}  ·  {SIG}", _META),
        Spacer(1, 8),
    ]


def _build(flow: list) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.7 * inch, bottomMargin=0.7 * inch,
        title="JHI deal memo",
    )
    doc.build(flow, onFirstPage=_footer, onLaterPages=_footer)
    return buf.getvalue()


def deal_xray_pdf(deal: DealInput, report: DealXRayReport) -> bytes:
    v = report.valuation
    flow = _header_block(deal.business_name, "Business Quality Assessment — deal memo")

    # Headline metrics
    flow.append(_table(
        [["Deal Score", "Recommendation", "Ethic rating", "Valuation verdict"],
         [str(report.deal_score), report.recommendation, str(report.ethic_rating), v.verdict.title()]],
        [1.6 * inch] * 4,
    ))
    flow.append(Spacer(1, 6))

    # Key metrics
    km_rows = [["Metric", "Value"]] + [[k, val] for k, val in report.key_metrics.items()]
    flow.append(Paragraph("Key metrics", _H))
    flow.append(_table(km_rows, [3.2 * inch, 3.2 * inch]))

    # Business Quality Assessment
    flow.append(Paragraph("Business Quality Assessment", _H))
    seg_rows = [["Segment", "Weight", "Score"]]
    seg_rows += [[s.segment, f"{s.weight*100:.0f}%", f"{s.score}/100"] for s in report.segments]
    flow.append(_table(seg_rows, [3.0 * inch, 1.6 * inch, 1.8 * inch]))

    # Valuation
    flow.append(Paragraph("Valuation", _H))
    flow.append(_table(
        [["Basis", "Multiple low", "Multiple base", "Multiple high", "DCF", "Asking"],
         [_m(v.normalized_ebitda), _m(v.multiple_value_low), _m(v.multiple_value_base),
          _m(v.multiple_value_high), _m(v.dcf_enterprise_value), _m(v.asking_price)]],
        [1.05 * inch] * 6,
    ))

    # Financing
    flow.append(Paragraph("Financing / offer alternatives", _H))
    fin_rows = [["Structure", "Equity", "Loan", "Seller note", "DSCR", "SBA fit"]]
    for f in report.financing_options:
        fin_rows.append([f.label, _m(f.equity_required), _m(f.loan_amount), _m(f.seller_note),
                         f"{f.dscr:.2f}" if f.dscr is not None else "—", "Yes" if f.sba_fit else "Review"])
    flow.append(_table(fin_rows, [1.9 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch, 0.7 * inch, 0.8 * inch]))

    # Diligence questions
    flow.append(Paragraph("Diligence questions", _H))
    for q in report.diligence_questions:
        flow.append(Paragraph(f"•&nbsp; {q}", _BODY))

    flow.append(Spacer(1, 8))
    flow.append(Paragraph(f"Ethic note: {report.ethic_note}", _SMALL))
    flow.append(Paragraph(_DISCLAIMER, _SMALL))
    flow.append(Paragraph(f"{ENTITY}  ·  {SIG}  ·  All rights reserved.", _SMALL))
    return _build(flow)


def diligence_pdf(deal: DiligenceInput, report: DiligenceReport) -> bytes:
    flow = _header_block(deal.business_name, "Quality of Earnings — deal memo")

    flow.append(_table(
        [["Financial Integrity Score", "Recommended tier", "Adjusted EBITDA"],
         [str(report.financial_integrity_score), report.recommended_tier, _m(report.adjusted_ebitda)]],
        [2.1 * inch] * 3,
    ))
    flow.append(Spacer(1, 4))
    flow.append(Paragraph(report.recommended_action, _BODY))

    flow.append(Paragraph("Procedures", _H))
    pc = report.proof_of_cash
    flow.append(_table(
        [["Procedure", "Result"],
         ["Proof of cash", pc.flag],
         ["Net working capital", f"{_m(report.working_capital.net_working_capital)} "
                                 f"({report.working_capital.nwc_pct_of_revenue:.1f}% of revenue)"],
         ["Quality of revenue", f"{report.revenue_quality.score}/100 — {report.revenue_quality.note}"],
         ["Adjusted EBITDA", f"{_m(report.adjusted_ebitda)} (from {_m(report.reported_ebitda)})"]],
        [1.8 * inch, 4.6 * inch],
    ))

    if report.red_flags:
        flow.append(Paragraph("Red flags", _H))
        for f in report.red_flags:
            flow.append(Paragraph(f"•&nbsp; {f}", _BODY))

    flow.append(Paragraph("Recommended QoE add-on", _H))
    p = report.add_on_pricing
    flow.append(Paragraph(
        f"{p.band}: JHI platform {_m(p.platform_low)}–{_m(p.platform_high)} "
        f"(manual market {_m(p.manual_low)}–{_m(p.manual_high)}).", _BODY))

    flow.append(Spacer(1, 8))
    flow.append(Paragraph(report.disclaimer, _SMALL))
    flow.append(Paragraph(f"{ENTITY}  ·  {SIG}  ·  All rights reserved.", _SMALL))
    return _build(flow)
