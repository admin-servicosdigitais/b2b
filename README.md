# RBS B2B — Backend

API REST para o Copiloto B2B: gestão de clientes, kanban, recomendações e copiloto com IA (Claude).

---

## Stack

| Camada | Tecnologia |
|---|---|
| Framework | FastAPI 0.115+ |
| ORM | SQLAlchemy 2.0 (async) |
| Driver DB | aiomysql |
| Validação | Pydantic v2 |
| IA | Anthropic SDK (`claude-sonnet-4-6`) |
| Runtime | Python 3.12+ |
| Gerenciador de pacotes | uv |
| Linter / formatter | Ruff |
| Testes | pytest + pytest-asyncio + httpx |

---

## Pré-requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) instalado globalmente
- MySQL 8.0+ acessível

---

## Setup

```bash
# 1. Instalar dependências (cria .venv automaticamente)
uv sync --extra dev

# 2. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com as credenciais reais

# 3. Subir a aplicação
uv run uvicorn main:app --reload --port 8000
```

---

## Variáveis de ambiente

| Variável | Descrição | Exemplo |
|---|---|---|
| `DATABASE_URL` | DSN completo do MySQL | `mysql+aiomysql://user:pass@localhost:3306/rbs_b2b` |
| `ANTHROPIC_API_KEY` | Chave da API Anthropic | `sk-ant-...` |
| `LLM_MODEL` | Modelo Claude a usar | `claude-sonnet-4-6` |

> **Nunca commitar `.env`.** Use `.env.example` como template versionado.

---

## Estrutura

```
backend/
├── main.py                  # Entrypoint — inicializa uvicorn
├── pyproject.toml           # Dependências, ruff, pytest
├── src/
│   ├── config.py            # Pydantic Settings (leitura de .env)
│   ├── api/
│   │   ├── app.py           # Factory do FastAPI, registro de routers
│   │   ├── deps.py          # Dependency injection (sessão DB, etc.)
│   │   └── routers/         # Um arquivo por domínio
│   ├── models/
│   │   ├── db.py            # Engine async, Base declarativa
│   │   ├── entities.py      # Tabelas ORM
│   │   └── schemas.py       # Schemas Pydantic (request/response)
│   ├── services/            # Regras de negócio — sem acesso direto ao DB
│   ├── repositories/        # Queries SQL — sem lógica de negócio
│   └── ai/
│       ├── llm_client.py    # Cliente Anthropic (injetável)
│       └── prompt_engine.py # Montagem e gestão de prompts
└── tests/
    ├── conftest.py          # Fixtures globais (app, db in-memory)
    └── test_*.py            # Um arquivo por router/domínio
```

### Fluxo de dependências

```
Router → Service → Repository → DB
              ↓
           AI (llm_client)
```

Serviços nunca importam outros serviços diretamente — composição via injeção em `deps.py`.

---

## Desenvolvimento

### Linting e formatação

```bash
# Verificar
uv run ruff check .

# Corrigir automaticamente
uv run ruff check . --fix

# Formatar
uv run ruff format .
```

### Testes

```bash
# Todos os testes
uv run pytest

# Um módulo específico
uv run pytest tests/test_clientes.py -v

# Com cobertura
uv run pytest --cov=src --cov-report=term-missing
```

O banco de testes usa SQLite em memória (via `aiosqlite`) — sem dependência de MySQL para CI.

---

## Padrões de código

- **Funções**: máximo 50 linhas, complexidade ciclomática ≤ 10
- **Linhas**: máximo 120 caracteres (configurado no `pyproject.toml`)
- **Tipagem**: type hints obrigatórios em todas as assinaturas públicas
- **Error handling**: exceções explícitas — zero `except: pass`
- **Commits**: atômicos, formato `tipo(escopo): descrição` em português

### Adicionando um novo domínio

1. Criar entidade em `src/models/entities.py`
2. Criar schemas em `src/models/schemas.py`
3. Criar `src/repositories/<dominio>_repo.py` (apenas I/O)
4. Criar `src/services/<dominio>_service.py` (regras de negócio)
5. Criar `src/api/routers/<dominio>.py` e registrar em `app.py`
6. Criar `tests/test_<dominio>.py` com pelo menos os casos feliz e de erro

---

## Segurança

- Secrets exclusivamente via variáveis de ambiente — nunca hardcoded
- `.env` está no `.gitignore` e nunca deve ser commitado
- Dependências auditadas com `uv run pip-audit` antes de releases
- Inputs externos validados pelo Pydantic antes de qualquer processamento

---

## API Docs

Com a aplicação rodando:

- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
