from datetime import datetime

from pydantic import BaseModel


class BeaIndicator(BaseModel):
    key: str
    label: str
    value: float | None = None
    unit: str = "USD mn"
    period: str | None = None
    status: str = "ok"  # "ok" | "unavailable" | "requires_credentials"
    note: str | None = None


class BeaMacroResponse(BaseModel):
    as_of: datetime
    source: str = "US Bureau of Economic Analysis (BEA)"
    indicators: list[BeaIndicator]
