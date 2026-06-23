from fastapi import APIRouter

from app.models import DashboardSnapshot
from app.services import DashboardService
from app.store import store

router = APIRouter(prefix="/dashboards", tags=["dashboards"])
dashboard_service = DashboardService(store)


@router.get("/executive", response_model=DashboardSnapshot)
def get_executive_dashboard() -> DashboardSnapshot:
    return dashboard_service.executive_snapshot()
