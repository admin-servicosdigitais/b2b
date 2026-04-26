import anthropic

from src.config import settings

_SYSTEM_COPILOTO = """Você é um copiloto de vendas B2B especializado em mídia e marketing.
Analise os dados fornecidos e sugira ações para aumentar a conversão de clientes.
Regras:
- Nunca invente dados. Baseie-se apenas no contexto fornecido.
- Seja objetivo e direto. Respostas concisas em português brasileiro.
- Priorize impacto comercial nas sugestões."""


class LLMClient:
    def __init__(self) -> None:
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self._model = settings.llm_model

    def complete(self, user_message: str, system: str = _SYSTEM_COPILOTO) -> str:
        message = self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user_message}],
        )
        return message.content[0].text
