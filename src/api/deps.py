from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.llm_client import LLMClient
from src.models.db import AsyncSessionLocal, get_session
from src.repositories.cliente_repo import ClienteRepo
from src.repositories.dashboard_repo import DashboardRepo
from src.repositories.recomendacao_repo import RecomendacaoRepo
from src.services.cliente_service import ClienteService
from src.services.copiloto_service import CopilotoService
from src.services.dashboard_service import DashboardService
from src.services.kanban_service import KanbanService
from src.services.recomendacao_service import RecomendacaoService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_llm() -> LLMClient:
    return LLMClient()


LLMDep = Annotated[LLMClient, Depends(get_llm)]


def get_kanban_service(session: SessionDep) -> KanbanService:
    return KanbanService(ClienteRepo(session))


def get_dashboard_service() -> DashboardService:
    return DashboardService(AsyncSessionLocal)


def get_recomendacao_service(session: SessionDep) -> RecomendacaoService:
    return RecomendacaoService(RecomendacaoRepo(session))


def get_cliente_service(session: SessionDep, llm: LLMDep) -> ClienteService:
    return ClienteService(ClienteRepo(session), llm)


def get_copiloto_service(session: SessionDep, llm: LLMDep) -> CopilotoService:
    return CopilotoService(ClienteRepo(session), DashboardRepo(session), llm)
