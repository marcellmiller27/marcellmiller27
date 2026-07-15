from fastapi import APIRouter

from app.public_macro_models import MacroSeriesResponse
from app.public_macro_services import PublicMacroService

router = APIRouter(prefix="/macro", tags=["public-macro"])


@router.get("/treasury", response_model=MacroSeriesResponse)
def treasury() -> MacroSeriesResponse:
    """US Treasury Fiscal Data: total public debt + debt held by the public."""
    return PublicMacroService().treasury()


@router.get("/world-bank", response_model=MacroSeriesResponse)
def world_bank(country: str = "US") -> MacroSeriesResponse:
    """World Bank WDI: GDP, growth, inflation, unemployment, population (by country)."""
    return PublicMacroService().world_bank(country)


@router.get("/imf", response_model=MacroSeriesResponse)
def imf(country: str = "USA") -> MacroSeriesResponse:
    """IMF WEO: real GDP growth, inflation, unemployment, govt debt (by country)."""
    return PublicMacroService().imf(country)


@router.get("/oecd", response_model=MacroSeriesResponse)
def oecd(country: str = "USA") -> MacroSeriesResponse:
    """OECD Composite Leading Indicator (amplitude-adjusted) by country."""
    return PublicMacroService().oecd(country)
