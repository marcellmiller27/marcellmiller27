from fastapi import APIRouter

from app.bea_models import BeaMacroResponse
from app.bea_services import BeaService

router = APIRouter(prefix="/macro/bea", tags=["bea-macro"])


@router.get("", response_model=BeaMacroResponse)
def bea_macro() -> BeaMacroResponse:
    """Headline BEA national-accounts indicators (GDP, PCE, real GDP growth, personal income)."""
    return BeaService().macro()
