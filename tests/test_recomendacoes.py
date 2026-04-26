import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_recomendacoes(client: AsyncClient, seed_data):
    response = await client.get("/api/v1/recomendacoes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_list_recomendacoes_campos(client: AsyncClient, seed_data):
    response = await client.get("/api/v1/recomendacoes")
    rec = response.json()[0]
    assert "id" in rec
    assert "titulo" in rec
    assert "status" in rec
    assert "score_confianca" in rec


@pytest.mark.asyncio
async def test_list_por_cliente(client: AsyncClient, seed_data):
    cliente_id = seed_data["cliente_id"]
    response = await client.get(f"/api/v1/recomendacoes/{cliente_id}")
    assert response.status_code == 200
    data = response.json()
    assert all(r["cliente_id"] == cliente_id for r in data)


@pytest.mark.asyncio
async def test_update_status_para_resolvida(client: AsyncClient, seed_data):
    rec_id = seed_data["rec_id"]
    response = await client.patch(f"/api/v1/recomendacoes/{rec_id}/status", json={"status": "RESOLVIDA"})
    assert response.status_code == 200
    assert response.json()["status"] == "RESOLVIDA"


@pytest.mark.asyncio
async def test_update_status_nao_encontrado(client: AsyncClient):
    response = await client.patch("/api/v1/recomendacoes/99999/status", json={"status": "RESOLVIDA"})
    assert response.status_code == 404
