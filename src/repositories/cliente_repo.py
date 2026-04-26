from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.entities import Cliente, FunilStatus


class ClienteRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_with_status(self) -> list[Cliente]:
        result = await self._session.execute(
            select(Cliente)
            .options(
                selectinload(Cliente.status_atual),
                selectinload(Cliente.recomendacoes),
            )
            .order_by(Cliente.nome_empresa)
        )
        return list(result.scalars().all())

    async def get_with_context(self, cliente_id: int) -> Cliente | None:
        result = await self._session.execute(
            select(Cliente)
            .where(Cliente.id == cliente_id)
            .options(
                selectinload(Cliente.status_atual),
                selectinload(Cliente.dores_oportunidades),
                selectinload(Cliente.interacoes),
                selectinload(Cliente.recomendacoes),
            )
        )
        return result.scalar_one_or_none()

    async def list_all_status(self) -> list[FunilStatus]:
        result = await self._session.execute(select(FunilStatus).order_by(FunilStatus.ordem))
        return list(result.scalars().all())
