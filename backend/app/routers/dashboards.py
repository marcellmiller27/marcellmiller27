from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DashboardSnapshot
from app.reporting_services import DashboardService

router = APIRouter(prefix="/dashboards", tags=["dashboards"])
dashboard_service = DashboardService()


@router.get("/executive", response_model=DashboardSnapshot)
def get_executive_dashboard(db: Annotated[Session, Depends(get_db)]) -> DashboardSnapshot:
    return dashboard_service.executive_snapshot(db)
