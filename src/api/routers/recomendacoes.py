from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.deps import get_recomendacao_service
from src.models.schemas import RecomendacaoOut, RecomendacaoStatusUpdate
from src.services.recomendacao_service import RecomendacaoService

router = APIRouter(prefix="/recomendacoes", tags=["RF03 - Recomendações IA"])

RecDep = Annotated[RecomendacaoService, Depends(get_recomendacao_service)]


@router.get("", response_model=list[RecomendacaoOut])
async def list_recomendacoes(service: RecDep) -> list[RecomendacaoOut]:
    return await service.list_all()


@router.get("/{cliente_id}", response_model=list[RecomendacaoOut])
async def list_por_cliente(cliente_id: int, service: RecDep) -> list[RecomendacaoOut]:
    return await service.list_by_cliente(cliente_id)


@router.patch("/{rec_id}/status", response_model=RecomendacaoOut)
async def update_status(rec_id: int, body: RecomendacaoStatusUpdate, service: RecDep) -> RecomendacaoOut:
    result = await service.update_status(rec_id, body.status)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recomendação não encontrada")
    return result
