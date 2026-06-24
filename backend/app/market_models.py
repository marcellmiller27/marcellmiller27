from datetime import datetime

from pydantic import BaseModel, Field


class Quote(BaseModel):
    symbol: str
    name: str
    asset_class: str
    price: float | None = None
    currency: str = "USD"
    unit: str = "USD"
    change_percent: float | None = None
    source: str
    as_of: datetime | None = None
    status: str = "ok"
    note: str | None = None


class QuotesResponse(BaseModel):
    as_of: datetime
    count: int
    sources: list[str]
    quotes: list[Quote]


class ProviderInfo(BaseModel):
    key: str
    name: str
    asset_classes: list[str]
    status: str  # "live" | "requires_credentials" | "unsupported"
    requires_key: bool
    notes: str


class ProvidersResponse(BaseModel):
    providers: list[ProviderInfo]


class InflationResponse(BaseModel):
    series: str
    period: str
    yoy_percent: float | None
    index_value: float | None
    source: str
    as_of: datetime
    status: str = "ok"
    note: str | None = None


class SymbolInfo(BaseModel):
    symbol: str
    name: str
    asset_class: str
    provider: str
    unit: str
    aliases: list[str] = Field(default_factory=list)


class SymbolsResponse(BaseModel):
    default: list[str]
    symbols: list[SymbolInfo]
