import asyncio
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.models.schemas import DashboardResponse
from src.repositories.dashboard_repo import DashboardRepo
from src.repositories.recomendacao_repo import RecomendacaoRepo


class DashboardService:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._factory = session_factory

    async def get_dashboard(self) -> DashboardResponse:
        async def _dash(fn):
            async with self._factory() as s:
                return await fn(DashboardRepo(s))

        async def _rec(fn):
            async with self._factory() as s:
                return await fn(RecomendacaoRepo(s))

        (
            total,
            por_status,
            ticket_total,
            ticket_medio,
            em_negociacao,
            fechado,
            taxa,
            sem_interacao,
            rec_pendentes,
        ) = await asyncio.gather(
            _dash(lambda r: r.total_clientes()),
            _dash(lambda r: r.clientes_por_status()),
            _dash(lambda r: r.ticket_total()),
            _dash(lambda r: r.ticket_medio()),
            _dash(lambda r: r.valor_em_negociacao()),
            _dash(lambda r: r.valor_fechado()),
            _dash(lambda r: r.taxa_conversao()),
            _dash(lambda r: r.clientes_sem_interacao()),
            _rec(lambda r: r.count_pendentes()),
        )

        return DashboardResponse(
            total_clientes=total,
            clientes_por_status=por_status,
            ticket_total=Decimal(str(ticket_total)),
            ticket_medio=Decimal(str(ticket_medio)),
            valor_em_negociacao=Decimal(str(em_negociacao)),
            valor_fechado=Decimal(str(fechado)),
            taxa_conversao=taxa,
            clientes_sem_interacao=sem_interacao,
            recomendacoes_pendentes=rec_pendentes,
        )
