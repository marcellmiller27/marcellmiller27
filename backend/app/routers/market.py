from typing import Annotated

from fastapi import APIRouter, Query

from app import data_registry as dr
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


@router.get("/registry")
def registry() -> dict:
    """The series registry: id, source, cadence, unit, and license class for every
    macro/market/fundamentals series the platform tracks (Data Foundation, Phase 1)."""
    return {
        "count": len(dr.all_series()),
        "series": [
            {
                "series_id": spec.series_id,
                "name": spec.name,
                "source": spec.source.value,
                "cadence": spec.cadence.value,
                "unit": spec.unit,
                "license_class": spec.license_class.value,
                "last_release": spec.last_release,
                "next_release": spec.next_release,
            }
            for spec in dr.all_series()
        ],
    }


@router.post("/refresh")
def refresh(
    symbols: Annotated[
        str | None,
        Query(description="Optional comma-separated subset; defaults to all registry series."),
    ] = None,
) -> dict:
    """Daily refresh hook: pull all registry sources into the cache + last-good store.

    Lightweight, on-demand entrypoint for a scheduler; the on-demand + last-good path is
    the priority, so this simply warms the cache and reports per-series freshness."""
    return MarketDataService().refresh_all(_parse_symbols(symbols))
