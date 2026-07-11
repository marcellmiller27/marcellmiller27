# JHI-SIG: 69M2705M | Deal Pipeline | John Henry Investments (proprietary)
"""Pydantic models for the Deal Pipeline (save & revisit acquisition analyses)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

# Pipeline stages, in order (Screen → BQA → QoE → Financing → Offer → Closed / Passed).
STAGES: list[str] = ["screen", "analysis", "qoe", "financing", "offer", "closed", "passed"]
DEAL_TYPES: list[str] = ["deal_xray", "qoe"]


class DealRecordCreate(BaseModel):
    business_name: str = Field(min_length=1)
    deal_type: str = Field(default="deal_xray")
    stage: str = Field(default="analysis")
    score: int | None = Field(default=None, ge=0, le=100)
    recommendation: str = ""
    headline: str = ""
    inputs: dict[str, Any] = Field(default_factory=dict)
    notes: str = ""


class DealRecordUpdate(BaseModel):
    stage: str | None = None
    notes: str | None = None
    headline: str | None = None


class DealRecord(BaseModel):
    id: str
    business_name: str
    deal_type: str
    stage: str
    score: int | None
    recommendation: str
    headline: str
    inputs: dict[str, Any]
    notes: str
    created_at: datetime
    updated_at: datetime
