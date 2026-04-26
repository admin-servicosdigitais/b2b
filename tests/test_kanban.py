import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_kanban_returns_colunas(client: AsyncClient):
    response = await client.get("/api/v1/kanban")
    assert response.status_code == 200
    data = response.json()
    assert "colunas" in data
    assert isinstance(data["colunas"], list)


@pytest.mark.asyncio
async def test_kanban_coluna_has_status_and_clientes(client: AsyncClient):
    response = await client.get("/api/v1/kanban")
    data = response.json()
    for coluna in data["colunas"]:
        assert "status" in coluna
        assert "clientes" in coluna
        assert "codigo" in coluna["status"]
        assert "ordem" in coluna["status"]


@pytest.mark.asyncio
async def test_kanban_cliente_card_fields(client: AsyncClient):
    response = await client.get("/api/v1/kanban")
    data = response.json()
    clientes = [c for col in data["colunas"] for c in col["clientes"]]
    assert len(clientes) > 0
    card = clientes[0]
    assert "id" in card
    assert "nome_empresa" in card
    assert "score_conversao" in card
