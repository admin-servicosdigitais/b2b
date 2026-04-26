from decimal import Decimal

from src.models.schemas import DashboardResponse
from src.repositories.dashboard_repo import DashboardRepo
from src.repositories.recomendacao_repo import RecomendacaoRepo


class DashboardService:
    def __init__(self, dashboard_repo: DashboardRepo, rec_repo: RecomendacaoRepo) -> None:
        self._dash = dashboard_repo
        self._rec = rec_repo

    async def get_dashboard(self) -> DashboardResponse:
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
        ) = await _gather(
            self._dash.total_clientes(),
            self._dash.clientes_por_status(),
            self._dash.ticket_total(),
            self._dash.ticket_medio(),
            self._dash.valor_em_negociacao(),
            self._dash.valor_fechado(),
            self._dash.taxa_conversao(),
            self._dash.clientes_sem_interacao(),
            self._rec.count_pendentes(),
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


async def _gather(*coros):
    import asyncio
    return await asyncio.gather(*coros)
