# 📄 PRD — Copiloto de Vendas B2B com IA (MVP)

---

## 1. Assunto

Desenvolvimento de um sistema de **Copiloto de Vendas B2B com IA**, focado em apoiar a tomada de decisão comercial e acelerar o funil de vendas da organização.

---

## 2. Introdução

Este projeto visa criar um sistema que evolui o conceito de CRM tradicional para um **Copiloto Inteligente**, capaz de:

- Interpretar dados comerciais  
- Sugerir ações  
- Apoiar vendedores  
- Gerar insights estratégicos  
- Aumentar taxa de conversão  

O sistema será utilizado por times comerciais B2B, com foco inicial em vendas de mídia e soluções de marketing.

---

## 3. Declaração do Problema

Os times comerciais enfrentam:

- Dificuldade em priorizar leads  
- Falta de visibilidade do funil  
- Baixa padronização na abordagem  
- Perda de oportunidades por falta de follow-up  
- Dificuldade em transformar dados em decisões  
- Processo manual na geração de propostas  

---

## 4. Metas e Objetivos

### Objetivos principais

- Aumentar produtividade do time comercial  
- Melhorar taxa de conversão  
- Reduzir tempo de geração de propostas  
- Apoiar decisões com dados e IA  

### KPIs

- Taxa de conversão (%)  
- Tempo médio de fechamento  
- Ticket médio  
- Número de recomendações aceitas  
- Engajamento com o copiloto  
- Número de clientes sem interação  

---

## 5. Escopo do MVP

### Incluído

- Dashboard B2B  
- Kanban de oportunidades  
- Recomendações de IA  
- Resumo comercial do cliente  
- Próxima melhor ação  
- Perguntas em linguagem natural  
- Base de dados simulada  

### Não incluído

- Autenticação complexa  
- Integrações externas (CRM real)  
- Workflow automatizado completo  

---

## 6. Personas

### 6.1 Vendedor B2B

- Precisa saber quem priorizar  
- Quer entender o cliente rapidamente  
- Quer apoio para abordagem  

### 6.2 Gerente Comercial

- Quer visão do funil  
- Quer identificar gargalos  
- Quer previsibilidade de receita  

---

## 7. Histórias de Usuário

### HU01 — Visualizar funil
Como vendedor, quero visualizar os clientes em um Kanban para entender o estágio de cada oportunidade.

### HU02 — Ver indicadores
Como gerente, quero visualizar métricas do funil para identificar oportunidades de melhoria.

### HU03 — Obter resumo do cliente
Como vendedor, quero um resumo automático do cliente antes de uma reunião.

### HU04 — Receber próxima ação
Como vendedor, quero saber qual é a próxima melhor ação para avançar a venda.

### HU05 — Identificar riscos
Como gerente, quero saber quais negociações estão em risco.

### HU06 — Fazer perguntas para IA
Como usuário, quero perguntar sobre a base de clientes e obter insights.

---

## 8. Requisitos Funcionais

### RF01 — Kanban

- Agrupar clientes por status do funil  
- Exibir cards com:
  - nome  
  - segmento  
  - ticket  
  - score  
  - recomendação principal  

---

### RF02 — Dashboard

Indicadores obrigatórios:

- Total de clientes  
- Clientes por status  
- Ticket total  
- Ticket médio  
- Valor em negociação  
- Valor fechado  
- Taxa de conversão  
- Clientes sem interação  
- Recomendações pendentes  

---

### RF03 — Recomendações IA

- Listar recomendações por cliente  
- Classificar por prioridade  
- Exibir score de confiança  
- Permitir mudança de status  

---

### RF04 — Resumo do Cliente

**Entrada:**
- `cliente_id`

**Saída:**
- resumo comercial  
- histórico  
- dores  
- oportunidades  
- status atual  
- recomendação principal  

---

### RF05 — Próxima Melhor Ação

**Entrada:**
- `cliente_id`

**Saída:**
- ação recomendada  
- justificativa  
- nível de prioridade  

---

### RF06 — Perguntas em Linguagem Natural

**Entrada:**
- pergunta  

**Saída:**
- resposta com base nos dados  

**Exemplos:**

- Quais clientes estão em risco?  
- Qual segmento tem maior potencial?  
- Quem devo priorizar hoje?  

---

## 9. Requisitos Técnicos

- Backend: Python + FastAPI  
- Banco: MySQL 
- Abaixo toda estrutura de tabelas com alguns exemplos de itens:

```
CREATE TABLE `clientes` ( `id` bigint NOT NULL AUTO_INCREMENT, `nome_empresa` varchar(150) NOT NULL, `cnpj` varchar(20) DEFAULT NULL, `segmento` varchar(80) DEFAULT NULL, `porte` varchar(50) DEFAULT NULL, `cidade` varchar(100) DEFAULT NULL, `estado` char(2) DEFAULT NULL, `origem_lead` varchar(80) DEFAULT NULL, `ticket_estimado` decimal(12,2) DEFAULT NULL, `status_atual_id` bigint DEFAULT NULL, `score_conversao` decimal(5,2) DEFAULT NULL, `observacao` text, `criado_em` datetime DEFAULT CURRENT_TIMESTAMP, `atualizado_em` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, PRIMARY KEY (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

{"id": 1, "score": 42.00, "empresa": "AgroVale Insumos", "segmento": "Agronegócio"}
{"id": 2, "score": 48.00, "empresa": "TechWave Sistemas", "segmento": "Tecnologia B2B"}
{"id": 3, "score": 37.00, "empresa": "Clínica Vida Plena", "segmento": "Saúde"}

CREATE TABLE `clientes_funil_historico` ( `id` bigint NOT NULL AUTO_INCREMENT, `cliente_id` bigint NOT NULL, `status_id` bigint NOT NULL, `data_entrada` datetime DEFAULT CURRENT_TIMESTAMP, `data_saida` datetime DEFAULT NULL, `motivo_mudanca` text, PRIMARY KEY (`id`), KEY `cliente_id` (`cliente_id`), KEY `status_id` (`status_id`), CONSTRAINT `clientes_funil_historico_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`), CONSTRAINT `clientes_funil_historico_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `funil_status` (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

{"id": 1, "status_id": 1, "cliente_id": 1, "data_entrada": "2026-01-10 09:00:00.000000"}
{"id": 2, "status_id": 1, "cliente_id": 2, "data_entrada": "2026-01-12 10:30:00.000000"}
{"id": 3, "status_id": 1, "cliente_id": 3, "data_entrada": "2026-01-15 14:00:00.000000"}

CREATE TABLE `dores_oportunidades` ( `id` bigint NOT NULL AUTO_INCREMENT, `cliente_id` bigint NOT NULL, `tipo` varchar(50) NOT NULL, `descricao` text NOT NULL, `impacto` varchar(50) DEFAULT NULL, `prioridade` varchar(50) DEFAULT NULL, `origem` varchar(50) DEFAULT NULL, `criado_em` datetime DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`id`), KEY `cliente_id` (`cliente_id`), CONSTRAINT `dores_oportunidades_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

{"id": 1, "tipo": "OPORTUNIDADE", "descricao": "Campanhas sazonais associadas à safra agrícola.", "cliente_id": 1, "prioridade": "MEDIA"}
{"id": 2, "tipo": "DOR", "descricao": "Dificuldade em gerar leads B2B qualificados.", "cliente_id": 2, "prioridade": "ALTA"}
{"id": 3, "tipo": "OPORTUNIDADE", "descricao": "Fortalecimento de marca local para serviços de saúde.", "cliente_id": 3, "prioridade": "MEDIA"}

CREATE TABLE `funil_status` ( `id` bigint NOT NULL AUTO_INCREMENT, `codigo` varchar(50) NOT NULL, `nome` varchar(80) NOT NULL, `ordem` int NOT NULL, PRIMARY KEY (`id`), UNIQUE KEY `codigo` (`codigo`) ) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

{"id": 1, "nome": "Lead cadastrado", "ordem": 1, "codigo": "LEAD"}
{"id": 2, "nome": "Lead qualificado", "ordem": 2, "codigo": "QUALIFICADO"}
{"id": 3, "nome": "Proposta criada", "ordem": 3, "codigo": "PROPOSTA"}
{"id": 4, "nome": "Em negociação", "ordem": 4, "codigo": "NEGOCIACAO"}
{"id": 5, "nome": "Venda fechada", "ordem": 5, "codigo": "FECHADO"}
{"id": 6, "nome": "Oportunidade perdida", "ordem": 6, "codigo": "PERDIDO"}

CREATE TABLE `interacoes` ( `id` bigint NOT NULL AUTO_INCREMENT, `cliente_id` bigint NOT NULL, `usuario_id` bigint DEFAULT NULL, `tipo` varchar(50) NOT NULL, `canal` varchar(50) DEFAULT NULL, `resumo` text NOT NULL, `sentimento` varchar(50) DEFAULT NULL, `proximos_passos` text, `realizada_em` datetime DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`id`), KEY `cliente_id` (`cliente_id`), CONSTRAINT `interacoes_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

{"id": 1, "tipo": "IA_ANALISE", "resumo": "IA identificou potencial de campanhas ligadas ao calendário agrícola e períodos de safra.", "cliente_id": 1, "sentimento": "POSITIVO"}
{"id": 2, "tipo": "REUNIAO", "resumo": "Cliente relatou baixa conversão em campanhas digitais e dificuldade de mensurar retorno.", "cliente_id": 5, "sentimento": "NEUTRO"}
{"id": 3, "tipo": "IA_ANALISE", "resumo": "IA sugeriu campanha integrada com digital, rádio e mídia local baseada em comportamento de compra regional.", "cliente_id": 5, "sentimento": "POSITIVO"}
{"id": 4, "tipo": "REUNIAO", "resumo": "Cliente demonstrou interesse em campanha omnichannel para fortalecimento regional da marca.", "cliente_id": 9, "sentimento": "POSITIVO"}
{"id": 5, "tipo": "IA_PROPOSTA", "resumo": "Copiloto gerou proposta inicial considerando ticket estimado, segmentação regional e histórico de campanhas.", "cliente_id": 9, "sentimento": "POSITIVO"}
{"id": 6, "tipo": "REUNIAO", "resumo": "Cliente questionou custo da campanha e pediu melhor demonstração de ROI.", "cliente_id": 13, "sentimento": "NEUTRO"}
{"id": 7, "tipo": "IA_ANALISE", "resumo": "IA identificou que a objeção principal é preço, mas o cliente valoriza previsibilidade de retorno.", "cliente_id": 13, "sentimento": "NEUTRO"}
{"id": 8, "tipo": "REUNIAO", "resumo": "Cliente aprovou proposta após ajuste de canais digitais e meta de conversão.", "cliente_id": 17, "sentimento": "POSITIVO"}
{"id": 9, "tipo": "FOLLOWUP", "resumo": "Contrato assinado e campanha aprovada para início no mês seguinte.", "cliente_id": 17, "sentimento": "POSITIVO"}

CREATE TABLE `propostas` ( `id` bigint NOT NULL AUTO_INCREMENT, `cliente_id` bigint NOT NULL, `titulo` varchar(150) NOT NULL, `descricao` text, `valor_mensal` decimal(12,2) DEFAULT NULL, `valor_total` decimal(12,2) DEFAULT NULL, `status` varchar(50) DEFAULT NULL, `gerada_por_ia` tinyint(1) DEFAULT '0', `score_aderencia` decimal(5,2) DEFAULT NULL, `criada_em` datetime DEFAULT CURRENT_TIMESTAMP, `enviada_em` datetime DEFAULT NULL, PRIMARY KEY (`id`), KEY `cliente_id` (`cliente_id`), CONSTRAINT `propostas_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

{"id": 1, "valor": 210000.00, "titulo": "Campanha Omnichannel FarmaMais", "aderencia": 86.00}
{"id": 2, "valor": 168000.00, "titulo": "Campanha de Leads B2B FinX", "aderencia": 79.00}
{"id": 3, "valor": 60000.00, "titulo": "Campanha Local PowerFit", "aderencia": 73.00}
	
CREATE TABLE `recomendacoes_ia` ( `id` bigint NOT NULL AUTO_INCREMENT, `cliente_id` bigint NOT NULL, `usuario_id` bigint DEFAULT NULL, `tipo` varchar(60) NOT NULL, `titulo` varchar(150) NOT NULL, `descricao` text NOT NULL, `justificativa` text, `prioridade` varchar(30) DEFAULT NULL, `status` varchar(30) DEFAULT 'PENDENTE', `score_confianca` decimal(5,2) DEFAULT NULL, `criada_em` datetime DEFAULT CURRENT_TIMESTAMP, `resolvida_em` datetime DEFAULT NULL, PRIMARY KEY (`id`), KEY `cliente_id` (`cliente_id`), KEY `usuario_id` (`usuario_id`), CONSTRAINT `recomendacoes_ia_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`), CONSTRAINT `recomendacoes_ia_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios_crm` (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

{"id": 1, "tipo": "RECOMENDACAO_ABORDAGEM", "titulo": "Abordar AgroVale com campanha sazonal", "confianca": 78.00}
{"id": 2, "tipo": "PROXIMA_ACAO", "titulo": "Qualificar necessidade de geração de leads", "confianca": 81.00}
{"id": 3, "tipo": "SUGESTAO_PROPOSTA", "titulo": "Criar campanha local para fortalecimento de marca", "confianca": 69.00}

CREATE TABLE `usuarios_crm` ( `id` bigint NOT NULL AUTO_INCREMENT, `nome` varchar(120) NOT NULL, `email` varchar(150) DEFAULT NULL, `perfil` varchar(50) DEFAULT NULL, `ativo` tinyint(1) DEFAULT '1', `criado_em` datetime DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

{"id": 1, "nome": "Mariana Costa", "email": "mariana.costa@rbs.com.br", "perfil": "VENDEDOR_B2B"}
{"id": 2, "nome": "Rafael Martins", "email": "rafael.martins@rbs.com.br", "perfil": "GERENTE_COMERCIAL"}
{"id": 3, "nome": "Camila Rocha", "email": "camila.rocha@rbs.com.br", "perfil": "ANALISTA_MARKETING"}

CREATE TABLE `vendas` ( `id` bigint NOT NULL AUTO_INCREMENT, `cliente_id` bigint NOT NULL, `proposta_id` bigint DEFAULT NULL, `valor_fechado` decimal(12,2) DEFAULT NULL, `recorrencia` varchar(50) DEFAULT NULL, `data_fechamento` date DEFAULT NULL, `observacao` text, PRIMARY KEY (`id`), KEY `cliente_id` (`cliente_id`), KEY `proposta_id` (`proposta_id`), CONSTRAINT `vendas_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`), CONSTRAINT `vendas_ibfk_2` FOREIGN KEY (`proposta_id`) REFERENCES `propostas` (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

{"id": 1, "data": "2025-10-05", "valor": 60000.00, "cliente_id": 17}
{"id": 2, "data": "2025-10-12", "valor": 18000.00, "cliente_id": 18}
{"id": 3, "data": "2025-10-20", "valor": 25000.00, "cliente_id": 19}
```

### Arquitetura

- Camada de serviços  
- Repositórios  
- Orquestração de IA  

### Integração com IA

- Inicial: regras + prompts estruturados  
- Evolução: integração com LLM (Vertex AI)  

---

## 10. Arquitetura Lógica

```
[API FastAPI]
↓
[Services Layer]
↓
[Repositórios]
↓
[MySQL]

[Copiloto Service]
↓
[Prompt Engine / LLM]
↓
[Dados estruturados + contexto]
```

## 11. Prompt Base do Copiloto

---

### Role
Você é um copiloto de vendas B2B especializado em mídia e marketing.

### Task
Analisar dados de clientes e sugerir ações para aumentar conversão.

### Input

- dados do cliente  
- histórico de interações  
- dores e oportunidades  
- status do funil  

### Output

- resumo objetivo  
- recomendação clara  
- justificativa baseada em dados  

### Constraints

- Não inventar dados  
- Basear-se apenas no contexto fornecido  
- Priorizar objetividade  

---

## 12. Fluxos Principais

### Fluxo 1 — Kanban

1. Buscar clientes  
2. Agrupar por status  
3. Enriquecer com recomendação  

---

### Fluxo 2 — Próxima Ação

1. Buscar cliente  
2. Buscar interações  
3. Buscar dores  
4. Buscar recomendações  
5. Gerar ação  

---

### Fluxo 3 — Pergunta Livre

1. Receber pergunta  
2. Buscar dados relevantes  
3. Montar contexto  
4. Enviar para IA  
5. Retornar resposta  

---

## 13. Benefícios

- Redução de esforço manual  
- Aumento de eficiência comercial  
- Melhoria na tomada de decisão  
- Padronização da abordagem de vendas  

---

## 14. Riscos

- Recomendações pouco assertivas  
- Dependência de qualidade de dados  
- Resistência do time comercial  

---

## 15. Conclusão

Este MVP demonstra como transformar um CRM tradicional em um **Copiloto Inteligente**, gerando valor direto ao negócio com baixo investimento inicial e alto potencial de evolução.