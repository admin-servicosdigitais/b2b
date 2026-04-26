import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.api.app import create_app
from src.models.db import Base, get_session
from src.models.entities import Cliente, FunilStatus, FunilStatusCodigo, RecomendacaoIA, StatusRecomendacao, TipoRecomendacao

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSession = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
async def seed_data(create_tables):
    async with TestSession() as s:
        status_lead = FunilStatus(codigo=FunilStatusCodigo.LEAD, nome="Lead", ordem=1)
        status_proposta = FunilStatus(codigo=FunilStatusCodigo.PROPOSTA, nome="Proposta", ordem=3)
        s.add_all([status_lead, status_proposta])
        await s.flush()

        cliente = Cliente(
            nome_empresa="Acme Corp",
            segmento="Varejo",
            ticket_estimado=5000,
            score_conversao=80,
            status_atual_id=status_lead.id,
        )
        s.add(cliente)
        await s.flush()

        rec = RecomendacaoIA(
            cliente_id=cliente.id,
            tipo=TipoRecomendacao.PROXIMA_ACAO,
            titulo="Agendar reunião de diagnóstico",
            prioridade="ALTA",
            status=StatusRecomendacao.PENDENTE,
            score_confianca=90,
        )
        s.add(rec)
        await s.commit()

        await s.refresh(status_lead)
        await s.refresh(cliente)
        await s.refresh(rec)

        return {"status_lead_id": status_lead.id, "cliente_id": cliente.id, "rec_id": rec.id}


@pytest.fixture
async def session() -> AsyncSession:
    async with TestSession() as s:
        yield s


@pytest.fixture
async def client(session: AsyncSession, seed_data):
    app = create_app()

    async def override_session():
        yield session

    app.dependency_overrides[get_session] = override_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
