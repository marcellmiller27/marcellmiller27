# JHI-SIG: 69M2705M | US government economic data (api.data.gov) router | JHI Research & Analytics Firm, Inc. (proprietary)
from fastapi import APIRouter

from app.data_gov_models import GovSeriesResponse
from app.data_gov_services import DataGovService

router = APIRouter(prefix="/macro/gov", tags=["gov-economic-data"])


@router.get("/treasury-fiscal", response_model=GovSeriesResponse)
def treasury_fiscal() -> GovSeriesResponse:
    """US Treasury Fiscal Data (keyless): debt to the penny + average interest rates on
    marketable Treasury securities (bills/notes/bonds)."""
    return DataGovService().treasury_fiscal()


@router.get("/banking", response_model=GovSeriesResponse)
def banking() -> GovSeriesResponse:
    """FDIC BankFind Suite (keyless): count of active FDIC-insured institutions."""
    return DataGovService().banking()


@router.get("/banking/institution/{cert}", response_model=GovSeriesResponse)
def institution(cert: str) -> GovSeriesResponse:
    """FDIC per-institution financial health by FDIC certificate number: assets,
    deposits, net income, ROA, ROE — as-of the latest call report."""
    return DataGovService().institution_financials(cert)


@router.get("/energy", response_model=GovSeriesResponse)
def energy() -> GovSeriesResponse:
    """EIA energy/commodities (needs DATA_GOV_API_KEY or EIA_API_KEY): WTI crude,
    Henry Hub natural gas, and US retail electricity price. Returns
    ``requires_credentials`` per indicator when no key is configured."""
    return DataGovService().energy()
