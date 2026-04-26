import json

from src.ai.llm_client import LLMClient
from src.ai.prompt_engine import build_proxima_acao_context, build_resumo_context
from src.models.entities import TipoDorOportunidade
from src.models.schemas import (
    DorOportunidadeOut,
    InteracaoResumo,
    ProximaAcaoResponse,
    ResumoClienteResponse,
)
from src.repositories.cliente_repo import ClienteRepo


class ClienteService:
    def __init__(self, repo: ClienteRepo, llm: LLMClient) -> None:
        self._repo = repo
        self._llm = llm

    async def get_resumo(self, cliente_id: int) -> ResumoClienteResponse | None:
        cliente = await self._repo.get_with_context(cliente_id)
        if cliente is None:
            return None

        prompt = build_resumo_context(cliente)
        resumo_texto = self._llm.complete(prompt)

        dores = [
            DorOportunidadeOut.model_validate(d)
            for d in cliente.dores_oportunidades
            if d.tipo == TipoDorOportunidade.DOR
        ]
        oportunidades = [
            DorOportunidadeOut.model_validate(d)
            for d in cliente.dores_oportunidades
            if d.tipo == TipoDorOportunidade.OPORTUNIDADE
        ]
        historico = [InteracaoResumo.model_validate(i) for i in sorted(
            cliente.interacoes, key=lambda i: i.realizada_em, reverse=True
        )]

        rec_principal = next(
            (r.titulo for r in sorted(
                [r for r in cliente.recomendacoes if r.status == "PENDENTE"],
                key=lambda r: ({"ALTA": 0, "MEDIA": 1, "BAIXA": 2}.get(r.prioridade or "", 9),),
            )),
            None,
        )

        return ResumoClienteResponse(
            cliente_id=cliente.id,
            nome_empresa=cliente.nome_empresa,
            status_atual=cliente.status_atual.nome if cliente.status_atual else None,
            resumo_comercial=resumo_texto,
            historico=historico,
            dores=dores,
            oportunidades=oportunidades,
            recomendacao_principal=rec_principal,
        )

    async def get_proxima_acao(self, cliente_id: int) -> ProximaAcaoResponse | None:
        cliente = await self._repo.get_with_context(cliente_id)
        if cliente is None:
            return None

        prompt = build_proxima_acao_context(cliente)
        resposta_raw = self._llm.complete(prompt)

        try:
            data = json.loads(resposta_raw)
            return ProximaAcaoResponse(
                acao=data["acao"],
                justificativa=data["justificativa"],
                prioridade=data.get("prioridade", "MEDIA"),
            )
        except (json.JSONDecodeError, KeyError):
            return ProximaAcaoResponse(
                acao=resposta_raw,
                justificativa="Resposta gerada pelo copiloto",
                prioridade="MEDIA",
            )
