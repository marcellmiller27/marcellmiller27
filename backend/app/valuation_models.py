# JHI-SIG: 69M2705M | Valuations | John Henry Investments (proprietary)
from datetime import datetime

from pydantic import BaseModel, Field


class ValuationEstimate(BaseModel):
    asset_class: str
    method: str
    estimated_value: float | None
    unit: str
    live_inputs: dict[str, float]
    assumptions: dict[str, float]
    type: str = "modeled_estimate"
    status: str = "ok"
    note: str | None = None


class ValuationReport(BaseModel):
    as_of: datetime
    disclaimer: str
    estimates: list[ValuationEstimate] = Field(default_factory=list)
