from fastapi import APIRouter, HTTPException

from app.edgar_models import EdgarFinancials
from app.edgar_services import EdgarService, ProviderError

router = APIRouter(prefix="/fundamentals/edgar", tags=["edgar-fundamentals"])


@router.get("/{ticker}", response_model=EdgarFinancials)
def edgar_financials(ticker: str) -> EdgarFinancials:
    """Normalized headline annual financials for a US filer from SEC EDGAR (no key)."""
    try:
        return EdgarService().financials(ticker)
    except ProviderError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
