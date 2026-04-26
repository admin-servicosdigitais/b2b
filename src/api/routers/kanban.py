from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.deps import get_kanban_service
from src.models.schemas import KanbanResponse
from src.services.kanban_service import KanbanService

router = APIRouter(prefix="/kanban", tags=["RF01 - Kanban"])

KanbanDep = Annotated[KanbanService, Depends(get_kanban_service)]


@router.get("", response_model=KanbanResponse)
async def get_kanban(service: KanbanDep) -> KanbanResponse:
    return await service.get_kanban()
