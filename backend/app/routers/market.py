# JHI-SIG: 69M2705M | Market Data | John Henry Investments (proprietary)
from typing import Annotated

from fastapi import APIRouter, Query

from app.market_models import (
    InflationResponse,
    ProvidersResponse,
    QuotesResponse,
    SymbolsResponse,
)
from app.market_services import MarketDataService

router = APIRouter(prefix="/market", tags=["market-data"])


def _parse_symbols(symbols: str | None) -> list[str] | None:
    if not symbols:
        return None
    parsed = [item.strip() for item in symbols.split(",") if item.strip()]
    return parsed or None


@router.get("/quotes", response_model=QuotesResponse)
def quotes(
    symbols: Annotated[
        str | None,
        Query(description="Comma-separated symbols, e.g. BTC,ETH,GOLD,SPX,UST10Y,INFLATION."),
    ] = None,
) -> QuotesResponse:
    return MarketDataService().quotes(_parse_symbols(symbols))


@router.get("/providers", response_model=ProvidersResponse)
def providers() -> ProvidersResponse:
    return MarketDataService().providers()


@router.get("/symbols", response_model=SymbolsResponse)
def symbols() -> SymbolsResponse:
    return MarketDataService().symbols()


@router.get("/inflation", response_model=InflationResponse)
def inflation() -> InflationResponse:
    return MarketDataService().inflation()
