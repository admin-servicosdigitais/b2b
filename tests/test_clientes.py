from unittest.mock import MagicMock, patch

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_resumo_cliente_nao_encontrado(client: AsyncClient):
    with patch("src.services.cliente_service.ClienteService.get_resumo", return_value=None):
        response = await client.get("/api/v1/clientes/99999/resumo")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_proxima_acao_nao_encontrado(client: AsyncClient):
    with patch("src.services.cliente_service.ClienteService.get_proxima_acao", return_value=None):
        response = await client.get("/api/v1/clientes/99999/proxima-acao")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_resumo_cliente_retorna_campos(client: AsyncClient, seed_data):
    from src.models.schemas import ResumoClienteResponse
    mock_resumo = ResumoClienteResponse(
        cliente_id=1,
        nome_empresa="Acme Corp",
        status_atual="Lead",
        resumo_comercial="Cliente com alto potencial no segmento Varejo.",
        historico=[],
        dores=[],
        oportunidades=[],
        recomendacao_principal="Agendar reunião",
    )
    with patch("src.services.cliente_service.ClienteService.get_resumo", return_value=mock_resumo):
        response = await client.get("/api/v1/clientes/1/resumo")
    assert response.status_code == 200
    data = response.json()
    assert "resumo_comercial" in data
    assert "dores" in data
    assert "oportunidades" in data


@pytest.mark.asyncio
async def test_proxima_acao_retorna_campos(client: AsyncClient, seed_data):
    from src.models.schemas import ProximaAcaoResponse
    mock_acao = ProximaAcaoResponse(
        acao="Enviar proposta",
        justificativa="Score alto e interesse demonstrado",
        prioridade="ALTA",
    )
    with patch("src.services.cliente_service.ClienteService.get_proxima_acao", return_value=mock_acao):
        response = await client.get("/api/v1/clientes/1/proxima-acao")
    assert response.status_code == 200
    data = response.json()
    assert data["acao"] == "Enviar proposta"
    assert data["prioridade"] == "ALTA"
