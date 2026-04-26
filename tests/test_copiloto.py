from unittest.mock import patch

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_chat_retorna_resposta(client: AsyncClient):
    from src.models.schemas import ChatResponse
    mock_resp = ChatResponse(
        pergunta="Quais clientes estão em risco?",
        resposta="Os clientes Acme Corp e Beta Ltd estão sem interação há mais de 30 dias.",
    )
    with patch("src.services.copiloto_service.CopilotoService.chat", return_value=mock_resp):
        response = await client.post("/api/v1/copiloto/chat", json={"pergunta": "Quais clientes estão em risco?"})
    assert response.status_code == 200
    data = response.json()
    assert "pergunta" in data
    assert "resposta" in data


@pytest.mark.asyncio
async def test_chat_pergunta_vazia_invalida(client: AsyncClient):
    response = await client.post("/api/v1/copiloto/chat", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_ecoa_pergunta(client: AsyncClient):
    from src.models.schemas import ChatResponse
    mock_resp = ChatResponse(
        pergunta="Qual segmento tem maior potencial?",
        resposta="O segmento Varejo lidera em score médio.",
    )
    with patch("src.services.copiloto_service.CopilotoService.chat", return_value=mock_resp):
        response = await client.post(
            "/api/v1/copiloto/chat", json={"pergunta": "Qual segmento tem maior potencial?"}
        )
    assert response.json()["pergunta"] == "Qual segmento tem maior potencial?"
