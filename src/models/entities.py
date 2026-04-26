from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.db import Base


class FunilStatusCodigo(str, Enum):
    LEAD = "LEAD"
    QUALIFICADO = "QUALIFICADO"
    PROPOSTA = "PROPOSTA"
    NEGOCIACAO = "NEGOCIACAO"
    FECHADO = "FECHADO"
    PERDIDO = "PERDIDO"


class TipoDorOportunidade(str, Enum):
    DOR = "DOR"
    OPORTUNIDADE = "OPORTUNIDADE"


class TipoInteracao(str, Enum):
    IA_ANALISE = "IA_ANALISE"
    REUNIAO = "REUNIAO"
    IA_PROPOSTA = "IA_PROPOSTA"
    FOLLOWUP = "FOLLOWUP"


class TipoRecomendacao(str, Enum):
    RECOMENDACAO_ABORDAGEM = "RECOMENDACAO_ABORDAGEM"
    PROXIMA_ACAO = "PROXIMA_ACAO"
    SUGESTAO_PROPOSTA = "SUGESTAO_PROPOSTA"


class StatusRecomendacao(str, Enum):
    PENDENTE = "PENDENTE"
    RESOLVIDA = "RESOLVIDA"
    IGNORADA = "IGNORADA"


class PerfilUsuario(str, Enum):
    VENDEDOR_B2B = "VENDEDOR_B2B"
    GERENTE_COMERCIAL = "GERENTE_COMERCIAL"
    ANALISTA_MARKETING = "ANALISTA_MARKETING"


class StatusProposta(str, Enum):
    RASCUNHO = "RASCUNHO"
    ENVIADA = "ENVIADA"
    APROVADA = "APROVADA"
    REJEITADA = "REJEITADA"


class FunilStatus(Base):
    __tablename__ = "funil_status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(SAEnum(FunilStatusCodigo), unique=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    ordem: Mapped[int] = mapped_column(Integer, nullable=False)

    clientes: Mapped[list["Cliente"]] = relationship(back_populates="status_atual")
    historico: Mapped[list["ClienteFunilHistorico"]] = relationship(back_populates="status")


class UsuarioCRM(Base):
    __tablename__ = "usuarios_crm"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    perfil: Mapped[str] = mapped_column(SAEnum(PerfilUsuario), nullable=False)
    ativo: Mapped[bool] = mapped_column(default=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    interacoes: Mapped[list["Interacao"]] = relationship(back_populates="usuario")
    recomendacoes: Mapped[list["RecomendacaoIA"]] = relationship(back_populates="usuario")


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome_empresa: Mapped[str] = mapped_column(String(300), nullable=False)
    cnpj: Mapped[str | None] = mapped_column(String(18), unique=True)
    segmento: Mapped[str | None] = mapped_column(String(100))
    porte: Mapped[str | None] = mapped_column(String(50))
    cidade: Mapped[str | None] = mapped_column(String(100))
    estado: Mapped[str | None] = mapped_column(String(2))
    origem_lead: Mapped[str | None] = mapped_column(String(100))
    ticket_estimado: Mapped[Decimal | None] = mapped_column(Numeric(15, 2))
    status_atual_id: Mapped[int | None] = mapped_column(ForeignKey("funil_status.id"))
    score_conversao: Mapped[int | None] = mapped_column(Integer)
    observacao: Mapped[str | None] = mapped_column(Text)
    criado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    status_atual: Mapped["FunilStatus | None"] = relationship(back_populates="clientes")
    historico_funil: Mapped[list["ClienteFunilHistorico"]] = relationship(back_populates="cliente")
    dores_oportunidades: Mapped[list["DorOportunidade"]] = relationship(back_populates="cliente")
    interacoes: Mapped[list["Interacao"]] = relationship(back_populates="cliente")
    propostas: Mapped[list["Proposta"]] = relationship(back_populates="cliente")
    recomendacoes: Mapped[list["RecomendacaoIA"]] = relationship(back_populates="cliente")
    vendas: Mapped[list["Venda"]] = relationship(back_populates="cliente")


class ClienteFunilHistorico(Base):
    __tablename__ = "clientes_funil_historico"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    status_id: Mapped[int] = mapped_column(ForeignKey("funil_status.id"), nullable=False)
    data_entrada: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    data_saida: Mapped[datetime | None] = mapped_column(DateTime)
    motivo_mudanca: Mapped[str | None] = mapped_column(Text)

    cliente: Mapped["Cliente"] = relationship(back_populates="historico_funil")
    status: Mapped["FunilStatus"] = relationship(back_populates="historico")


class DorOportunidade(Base):
    __tablename__ = "dores_oportunidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(SAEnum(TipoDorOportunidade), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    impacto: Mapped[str | None] = mapped_column(String(50))
    prioridade: Mapped[int | None] = mapped_column(Integer)
    origem: Mapped[str | None] = mapped_column(String(100))

    cliente: Mapped["Cliente"] = relationship(back_populates="dores_oportunidades")


class Interacao(Base):
    __tablename__ = "interacoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios_crm.id"))
    tipo: Mapped[str] = mapped_column(SAEnum(TipoInteracao), nullable=False)
    canal: Mapped[str | None] = mapped_column(String(100))
    resumo: Mapped[str | None] = mapped_column(Text)
    sentimento: Mapped[str | None] = mapped_column(String(50))
    proximos_passos: Mapped[str | None] = mapped_column(Text)
    realizada_em: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    cliente: Mapped["Cliente"] = relationship(back_populates="interacoes")
    usuario: Mapped["UsuarioCRM | None"] = relationship(back_populates="interacoes")


class Proposta(Base):
    __tablename__ = "propostas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    titulo: Mapped[str] = mapped_column(String(300), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    valor_mensal: Mapped[Decimal | None] = mapped_column(Numeric(15, 2))
    valor_total: Mapped[Decimal | None] = mapped_column(Numeric(15, 2))
    status: Mapped[str] = mapped_column(SAEnum(StatusProposta), default=StatusProposta.RASCUNHO)
    gerada_por_ia: Mapped[bool] = mapped_column(default=False)
    score_aderencia: Mapped[int | None] = mapped_column(Integer)
    criada_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    enviada_em: Mapped[datetime | None] = mapped_column(DateTime)

    cliente: Mapped["Cliente"] = relationship(back_populates="propostas")
    vendas: Mapped[list["Venda"]] = relationship(back_populates="proposta")


class RecomendacaoIA(Base):
    __tablename__ = "recomendacoes_ia"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    usuario_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios_crm.id"))
    tipo: Mapped[str] = mapped_column(SAEnum(TipoRecomendacao), nullable=False)
    titulo: Mapped[str] = mapped_column(String(300), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text)
    justificativa: Mapped[str | None] = mapped_column(Text)
    prioridade: Mapped[str | None] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(SAEnum(StatusRecomendacao), default=StatusRecomendacao.PENDENTE)
    score_confianca: Mapped[int | None] = mapped_column(Integer)
    criada_em: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    resolvida_em: Mapped[datetime | None] = mapped_column(DateTime)

    cliente: Mapped["Cliente"] = relationship(back_populates="recomendacoes")
    usuario: Mapped["UsuarioCRM | None"] = relationship(back_populates="recomendacoes")


class Venda(Base):
    __tablename__ = "vendas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    proposta_id: Mapped[int | None] = mapped_column(ForeignKey("propostas.id"))
    valor_fechado: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    recorrencia: Mapped[str | None] = mapped_column(String(50))
    data_fechamento: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    cliente: Mapped["Cliente"] = relationship(back_populates="vendas")
    proposta: Mapped["Proposta | None"] = relationship(back_populates="vendas")
