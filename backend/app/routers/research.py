from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_principal
from app.foundation_models import Principal
from app.research_models import (
    AcquisitionValidation,
    AdoptionStudy,
    BacktestResult,
    DataCoverageReport,
    OpportunityScoreSnapshot,
)
from app.research_services import ResearchService

router = APIRouter(prefix="/research", tags=["research"])


@router.get("/score-backtest", response_model=BacktestResult)
def score_backtest() -> BacktestResult:
    return ResearchService().score_backtest()


@router.get("/opportunity-scores", response_model=OpportunityScoreSnapshot)
def opportunity_scores() -> OpportunityScoreSnapshot:
    return ResearchService().opportunity_score_snapshot()


@router.get("/acquisition-validation", response_model=AcquisitionValidation)
def acquisition_validation() -> AcquisitionValidation:
    return ResearchService().acquisition_validation()


@router.get("/data-coverage", response_model=DataCoverageReport)
def data_coverage() -> DataCoverageReport:
    return ResearchService().data_coverage()


@router.get("/adoption", response_model=AdoptionStudy)
def adoption(
    _principal: Annotated[Principal, Depends(get_current_principal)],
    db: Annotated[Session, Depends(get_db)],
) -> AdoptionStudy:
    return ResearchService(db).adoption_study()
