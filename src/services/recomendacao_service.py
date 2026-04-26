from src.models.entities import StatusRecomendacao
from src.models.schemas import RecomendacaoOut
from src.repositories.recomendacao_repo import RecomendacaoRepo


class RecomendacaoService:
    def __init__(self, repo: RecomendacaoRepo) -> None:
        self._repo = repo

    async def list_all(self) -> list[RecomendacaoOut]:
        items = await self._repo.list_all()
        return [RecomendacaoOut.model_validate(r) for r in items]

    async def list_by_cliente(self, cliente_id: int) -> list[RecomendacaoOut]:
        items = await self._repo.list_by_cliente(cliente_id)
        return [RecomendacaoOut.model_validate(r) for r in items]

    async def update_status(self, rec_id: int, status: StatusRecomendacao) -> RecomendacaoOut | None:
        rec = await self._repo.update_status(rec_id, status)
        if rec is None:
            return None
        return RecomendacaoOut.model_validate(rec)
