from datetime import datetime

from pydantic import BaseModel


class MacroPoint(BaseModel):
    key: str
    label: str
    value: float | None = None
    unit: str = ""
    period: str | None = None
    country: str | None = None
    status: str = "ok"  # "ok" | "unavailable"
    note: str | None = None


class MacroSeriesResponse(BaseModel):
    source: str
    as_of: datetime
    country: str | None = None
    indicators: list[MacroPoint]
