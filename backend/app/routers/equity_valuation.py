# JHI-SIG: 69M2705M | Cross-Asset Valuation router (equities) | JHI Research & Analytics Firm, Inc. (proprietary)
from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Query, Response

from app import edgar_services
from app.equity_valuation import EquityValuation, value_equity, value_universe
from app.equity_valuation_workbook import equity_valuation_workbook

router = APIRouter(prefix="/valuation", tags=["valuation"])


@router.get("/equity", response_model=list[EquityValuation])
def valuation_universe(
    n: int = Query(8, ge=1, le=40, description="How many top-by-upside names to return."),
) -> list[EquityValuation]:
    """Cross-Asset Valuation — the large/mid-cap equity screen, ranked by margin of safety."""
    return value_universe(n=n)


@router.get("/equity/{ticker}", response_model=EquityValuation)
def valuation_for_ticker(ticker: str) -> EquityValuation:
    """DCF valuation + expected return + Enter/Accumulate/Sideline call for one ticker."""
    try:
        return value_equity(ticker)
    except edgar_services.ProviderError as exc:
        raise HTTPException(status_code=404, detail=f"No SEC data for '{ticker}': {exc}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/equity/{ticker}/xlsx")
def valuation_workbook(ticker: str) -> Response:
    """Download the DCF valuation as a branded Excel workbook."""
    try:
        report = value_equity(ticker)
    except edgar_services.ProviderError as exc:
        raise HTTPException(status_code=404, detail=f"No SEC data for '{ticker}': {exc}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    now = datetime.now(UTC)
    filename = f"Aegira_{report.ticker}_DCF_Valuation_{now:%Y-%m-%d}.xlsx"
    return Response(
        content=equity_valuation_workbook(report),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
