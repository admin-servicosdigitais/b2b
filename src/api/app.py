from fastapi import FastAPI

from src.api.routers import clientes, copiloto, dashboard, kanban, recomendacoes


def create_app() -> FastAPI:
    app = FastAPI(
        title="Copiloto de Vendas B2B",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(kanban.router, prefix="/api/v1")
    app.include_router(dashboard.router, prefix="/api/v1")
    app.include_router(recomendacoes.router, prefix="/api/v1")
    app.include_router(clientes.router, prefix="/api/v1")
    app.include_router(copiloto.router, prefix="/api/v1")

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok"}

    return app
