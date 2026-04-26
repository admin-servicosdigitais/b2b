from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.deps import get_cliente_service
from src.models.schemas import ProximaAcaoResponse, ResumoClienteResponse
from src.services.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["RF04/RF05 - Clientes"])

ClienteDep = Annotated[ClienteService, Depends(get_cliente_service)]


@router.get("/{cliente_id}/resumo", response_model=ResumoClienteResponse)
async def get_resumo(cliente_id: int, service: ClienteDep) -> ResumoClienteResponse:
    result = await service.get_resumo(cliente_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    return result


@router.get("/{cliente_id}/proxima-acao", response_model=ProximaAcaoResponse)
async def get_proxima_acao(cliente_id: int, service: ClienteDep) -> ProximaAcaoResponse:
    result = await service.get_proxima_acao(cliente_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    return result
