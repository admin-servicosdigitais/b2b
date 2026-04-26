from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.entities import RecomendacaoIA, StatusRecomendacao


PRIORIDADE_ORDEM = {"ALTA": 0, "MEDIA": 1, "BAIXA": 2}


class RecomendacaoRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[RecomendacaoIA]:
        result = await self._session.execute(
            select(RecomendacaoIA).order_by(RecomendacaoIA.criada_em.desc())
        )
        items = list(result.scalars().all())
        return sorted(items, key=lambda r: (PRIORIDADE_ORDEM.get(r.prioridade or "", 9), -(r.score_confianca or 0)))

    async def list_by_cliente(self, cliente_id: int) -> list[RecomendacaoIA]:
        result = await self._session.execute(
            select(RecomendacaoIA)
            .where(RecomendacaoIA.cliente_id == cliente_id)
            .order_by(RecomendacaoIA.criada_em.desc())
        )
        items = list(result.scalars().all())
        return sorted(items, key=lambda r: (PRIORIDADE_ORDEM.get(r.prioridade or "", 9), -(r.score_confianca or 0)))

    async def get(self, rec_id: int) -> RecomendacaoIA | None:
        result = await self._session.execute(
            select(RecomendacaoIA).where(RecomendacaoIA.id == rec_id)
        )
        return result.scalar_one_or_none()

    async def update_status(self, rec_id: int, status: StatusRecomendacao) -> RecomendacaoIA | None:
        await self._session.execute(
            update(RecomendacaoIA)
            .where(RecomendacaoIA.id == rec_id)
            .values(status=status)
        )
        await self._session.commit()
        return await self.get(rec_id)

    async def count_pendentes(self) -> int:
        result = await self._session.execute(
            select(RecomendacaoIA).where(RecomendacaoIA.status == StatusRecomendacao.PENDENTE)
        )
        return len(result.scalars().all())
