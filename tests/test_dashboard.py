import pytest
from httpx import AsyncClient

CAMPOS_OBRIGATORIOS = [
    "total_clientes",
    "clientes_por_status",
    "ticket_total",
    "ticket_medio",
    "valor_em_negociacao",
    "valor_fechado",
    "taxa_conversao",
    "clientes_sem_interacao",
    "recomendacoes_pendentes",
]


@pytest.mark.asyncio
async def test_dashboard_status_ok(client: AsyncClient):
    response = await client.get("/api/v1/dashboard")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_dashboard_campos_obrigatorios(client: AsyncClient):
    response = await client.get("/api/v1/dashboard")
    data = response.json()
    for campo in CAMPOS_OBRIGATORIOS:
        assert campo in data, f"Campo ausente: {campo}"


@pytest.mark.asyncio
async def test_dashboard_total_clientes_positivo(client: AsyncClient):
    response = await client.get("/api/v1/dashboard")
    data = response.json()
    assert data["total_clientes"] >= 0


@pytest.mark.asyncio
async def test_dashboard_taxa_conversao_entre_0_e_1(client: AsyncClient):
    response = await client.get("/api/v1/dashboard")
    data = response.json()
    assert 0.0 <= data["taxa_conversao"] <= 1.0
