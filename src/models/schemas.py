from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from src.models.entities import (
    FunilStatusCodigo,
    StatusRecomendacao,
    TipoDorOportunidade,
    TipoRecomendacao,
)


# --- Shared ---

class FunilStatusOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    codigo: FunilStatusCodigo
    nome: str
    ordem: int


# --- RF01: Kanban ---

class ClienteKanbanCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome_empresa: str
    segmento: str | None
    ticket_estimado: Decimal | None
    score_conversao: int | None
    recomendacao_principal: str | None


class KanbanColuna(BaseModel):
    status: FunilStatusOut
    clientes: list[ClienteKanbanCard]


class KanbanResponse(BaseModel):
    colunas: list[KanbanColuna]


# --- RF02: Dashboard ---

class DashboardResponse(BaseModel):
    total_clientes: int
    clientes_por_status: dict[str, int]
    ticket_total: Decimal
    ticket_medio: Decimal
    valor_em_negociacao: Decimal
    valor_fechado: Decimal
    taxa_conversao: float
    clientes_sem_interacao: int
    recomendacoes_pendentes: int


# --- RF03: Recomendações IA ---

class RecomendacaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cliente_id: int
    tipo: TipoRecomendacao
    titulo: str
    descricao: str | None
    justificativa: str | None
    prioridade: str | None
    status: StatusRecomendacao
    score_confianca: int | None
    criada_em: datetime


class RecomendacaoStatusUpdate(BaseModel):
    status: StatusRecomendacao


# --- RF04: Resumo do Cliente ---

class DorOportunidadeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    tipo: TipoDorOportunidade
    descricao: str
    impacto: str | None
    prioridade: int | None


class InteracaoResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    tipo: str
    resumo: str | None
    sentimento: str | None
    realizada_em: datetime


class ResumoClienteResponse(BaseModel):
    cliente_id: int
    nome_empresa: str
    status_atual: str | None
    resumo_comercial: str
    historico: list[InteracaoResumo]
    dores: list[DorOportunidadeOut]
    oportunidades: list[DorOportunidadeOut]
    recomendacao_principal: str | None


# --- RF05: Próxima Melhor Ação ---

class ProximaAcaoResponse(BaseModel):
    acao: str
    justificativa: str
    prioridade: str


# --- RF06: Chat em Linguagem Natural ---

class ChatRequest(BaseModel):
    pergunta: str


class ChatResponse(BaseModel):
    pergunta: str
    resposta: str
