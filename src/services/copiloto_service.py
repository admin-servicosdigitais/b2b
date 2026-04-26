from decimal import Decimal

from src.ai.llm_client import LLMClient
from src.ai.prompt_engine import build_chat_context
from src.models.schemas import ChatResponse
from src.repositories.cliente_repo import ClienteRepo
from src.repositories.dashboard_repo import DashboardRepo


class CopilotoService:
    def __init__(self, cliente_repo: ClienteRepo, dashboard_repo: DashboardRepo, llm: LLMClient) -> None:
        self._clientes = cliente_repo
        self._dash = dashboard_repo
        self._llm = llm

    async def chat(self, pergunta: str) -> ChatResponse:
        resumo = await self._build_resumo_dados()
        prompt = build_chat_context(pergunta, resumo)
        resposta = self._llm.complete(prompt)
        return ChatResponse(pergunta=pergunta, resposta=resposta)

    async def _build_resumo_dados(self) -> str:
        clientes = await self._clientes.list_with_status()
        por_status = await self._dash.clientes_por_status()
        valor_fechado = await self._dash.valor_fechado()

        linhas = [
            f"Total de clientes: {len(clientes)}",
            "Distribuição por status: " + ", ".join(f"{k}={v}" for k, v in por_status.items()),
            f"Valor total fechado: R$ {Decimal(str(valor_fechado)):,.2f}",
            "",
            "Clientes com score mais alto:",
        ]
        top = sorted([c for c in clientes if c.score_conversao], key=lambda c: c.score_conversao, reverse=True)[:5]
        for c in top:
            linhas.append(
                f"- {c.nome_empresa} | {c.segmento or 'N/A'} | score={c.score_conversao} "
                f"| status={c.status_atual.nome if c.status_atual else 'N/A'}"
            )

        return "\n".join(linhas)
