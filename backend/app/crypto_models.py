from datetime import datetime

from pydantic import BaseModel, Field

WATCH_ONLY_NOTICE = (
    "Non-custodial: this platform stores only public, watch-only data "
    "(networks, asset symbols, public addresses, quantities). It never stores "
    "private keys, seed phrases, or any secret that can move funds."
)


class SupportedNetwork(BaseModel):
    key: str
    label: str
    assets: list[str]


class NetworksResponse(BaseModel):
    custody_model: str
    notice: str
    networks: list[SupportedNetwork]


class CryptoHoldingCreate(BaseModel):
    network: str
    asset_symbol: str
    address: str | None = None
    quantity: str = "0"
    label: str = ""
    notes: str | None = Field(default=None, max_length=500)


class CryptoHoldingRead(BaseModel):
    id: str
    network: str
    asset_symbol: str
    address: str | None
    quantity: str
    label: str
    notes: str | None
    custody_model: str
    created_at: datetime
    updated_at: datetime


class CryptoHoldingsSummary(BaseModel):
    custody_model: str
    total_holdings: int
    networks: int
    by_asset: dict[str, str]
