from src.models.entities import FunilStatusCodigo
from src.models.schemas import ClienteKanbanCard, FunilStatusOut, KanbanColuna, KanbanResponse
from src.repositories.cliente_repo import ClienteRepo

_PRIORIDADE_STATUS = [s.value for s in FunilStatusCodigo]


class KanbanService:
    def __init__(self, repo: ClienteRepo) -> None:
        self._repo = repo

    async def get_kanban(self) -> KanbanResponse:
        todos_status = await self._repo.list_all_status()
        clientes = await self._repo.list_with_status()

        por_status: dict[int, list[ClienteKanbanCard]] = {s.id: [] for s in todos_status}

        for cliente in clientes:
            if cliente.status_atual_id is None:
                continue
            rec_principal = next(
                (r.titulo for r in sorted(
                    cliente.recomendacoes,
                    key=lambda r: ({"ALTA": 0, "MEDIA": 1, "BAIXA": 2}.get(r.prioridade or "", 9), -(r.score_confianca or 0)),
                ) if r.status == "PENDENTE"),
                None,
            )
            card = ClienteKanbanCard(
                id=cliente.id,
                nome_empresa=cliente.nome_empresa,
                segmento=cliente.segmento,
                ticket_estimado=cliente.ticket_estimado,
                score_conversao=cliente.score_conversao,
                recomendacao_principal=rec_principal,
            )
            por_status.setdefault(cliente.status_atual_id, []).append(card)

        colunas = [
            KanbanColuna(status=FunilStatusOut.model_validate(s), clientes=por_status.get(s.id, []))
            for s in todos_status
        ]
        return KanbanResponse(colunas=colunas)
