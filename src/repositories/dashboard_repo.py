from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.entities import Cliente, FunilStatus, FunilStatusCodigo, Interacao, Venda


class DashboardRepo:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def total_clientes(self) -> int:
        result = await self._session.execute(select(func.count(Cliente.id)))
        return result.scalar_one() or 0

    async def clientes_por_status(self) -> dict[str, int]:
        result = await self._session.execute(
            select(FunilStatus.codigo, func.count(Cliente.id))
            .join(Cliente, Cliente.status_atual_id == FunilStatus.id, isouter=True)
            .group_by(FunilStatus.codigo)
        )
        return {row[0]: row[1] for row in result.all()}

    async def ticket_total(self) -> Decimal:
        result = await self._session.execute(select(func.sum(Cliente.ticket_estimado)))
        return result.scalar_one() or Decimal("0")

    async def ticket_medio(self) -> Decimal:
        result = await self._session.execute(select(func.avg(Cliente.ticket_estimado)))
        return result.scalar_one() or Decimal("0")

    async def valor_em_negociacao(self) -> Decimal:
        result = await self._session.execute(
            select(func.sum(Cliente.ticket_estimado))
            .join(FunilStatus, Cliente.status_atual_id == FunilStatus.id)
            .where(FunilStatus.codigo == FunilStatusCodigo.NEGOCIACAO)
        )
        return result.scalar_one() or Decimal("0")

    async def valor_fechado(self) -> Decimal:
        result = await self._session.execute(select(func.sum(Venda.valor_fechado)))
        return result.scalar_one() or Decimal("0")

    async def taxa_conversao(self) -> float:
        total = await self.total_clientes()
        if total == 0:
            return 0.0
        result = await self._session.execute(
            select(func.count(Venda.id.distinct()))
        )
        fechados = result.scalar_one() or 0
        return round(fechados / total, 4)

    async def clientes_sem_interacao(self, dias: int = 30) -> int:
        limite = datetime.now(UTC) - timedelta(days=dias)
        subquery = (
            select(Interacao.cliente_id)
            .where(Interacao.realizada_em >= limite)
            .distinct()
            .scalar_subquery()
        )
        result = await self._session.execute(
            select(func.count(Cliente.id)).where(Cliente.id.not_in(subquery))
        )
        return result.scalar_one() or 0
