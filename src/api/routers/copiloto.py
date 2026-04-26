from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.deps import get_copiloto_service
from src.models.schemas import ChatRequest, ChatResponse
from src.services.copiloto_service import CopilotoService

router = APIRouter(prefix="/copiloto", tags=["RF06 - Copiloto Chat"])

CopilotoDep = Annotated[CopilotoService, Depends(get_copiloto_service)]


@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest, service: CopilotoDep) -> ChatResponse:
    return await service.chat(body.pergunta)
