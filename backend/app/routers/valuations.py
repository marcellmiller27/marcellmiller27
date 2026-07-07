from typing import Annotated

from fastapi import APIRouter, Query

from app.valuation_models import ValuationReport
from app.valuation_services import ValuationService

router = APIRouter(prefix="/valuations", tags=["valuations"])


@router.get("/estimate", response_model=ValuationReport)
def estimate(
    noi: Annotated[float, Query(gt=0, description="Annual net operating income (real estate).")]
    = 100_000.0,
    ebitda: Annotated[float, Query(gt=0, description="EBITDA for the private business.")]
    = 1_000_000.0,
    pe_committed: Annotated[float, Query(gt=0, description="Committed PE capital.")]
    = 1_000_000.0,
) -> ValuationReport:
    return ValuationService().estimate(noi=noi, ebitda=ebitda, pe_committed=pe_committed)
