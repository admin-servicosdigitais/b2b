from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.deps import get_dashboard_service
from src.models.schemas import DashboardResponse
from src.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["RF02 - Dashboard"])

DashboardDep = Annotated[DashboardService, Depends(get_dashboard_service)]


@router.get("", response_model=DashboardResponse)
async def get_dashboard(service: DashboardDep) -> DashboardResponse:
    return await service.get_dashboard()
