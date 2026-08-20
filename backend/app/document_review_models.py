# JHI-SIG: 69M2705M | Document Review module | JHI Research & Analytics Firm, Inc. (proprietary)
"""Pydantic models for the Document Review module.

Document Review is the operational intake for real acquisition documents (tax
returns, P&L statements, balance sheets, bank statements). A subscriber uploads a
file; the engine extracts what it can (CSV/XLSX tables, PDF text), runs deterministic
risk/fraud indicators, and returns a 0-100 risk score, flags, and a list of
diligence questions.

IMPORTANT: this is decision-support only — NOT an audit, review, or CPA opinion.
Figures are never fabricated: if a file cannot be parsed, the review is returned with
a `manual_review_required` status and no invented numbers.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class DocType(StrEnum):
    TAX_RETURNS = "tax_returns"
    PNL = "pnl"
    BALANCE_SHEET = "balance_sheet"
    BANK_STATEMENTS = "bank_statements"


DOC_TYPE_LABELS: dict[str, str] = {
    DocType.TAX_RETURNS: "Tax returns",
    DocType.PNL: "P&L statements",
    DocType.BALANCE_SHEET: "Balance sheets",
    DocType.BANK_STATEMENTS: "Bank statements",
}


class ReviewStatus(StrEnum):
    ANALYZED = "analyzed"
    MANUAL_REVIEW_REQUIRED = "manual_review_required"


class DocumentReviewResult(BaseModel):
    """The analysis produced for one uploaded document (before/after persistence)."""

    id: str
    doc_type: DocType
    doc_type_label: str
    filename: str
    content_type: str = ""
    size_bytes: int = 0
    uploaded_by: str
    status: ReviewStatus
    # None only when the file could not be parsed (manual_review_required).
    risk_score: int | None = Field(default=None, ge=0, le=100)
    risk_band: str = ""
    summary: str = ""
    flags: list[str] = Field(default_factory=list)
    questions: list[str] = Field(default_factory=list)
    disclaimer: str = ""
    uploaded_at: datetime
