from src.models.entities import Cliente


def build_resumo_context(cliente: Cliente) -> str:
    dores = [d for d in cliente.dores_oportunidades if d.tipo == "DOR"]
    oportunidades = [d for d in cliente.dores_oportunidades if d.tipo == "OPORTUNIDADE"]
    interacoes = sorted(cliente.interacoes, key=lambda i: i.realizada_em, reverse=True)[:5]

    linhas = [
        f"## Cliente: {cliente.nome_empresa}",
        f"Segmento: {cliente.segmento or 'N/A'} | Porte: {cliente.porte or 'N/A'}",
        f"Status: {cliente.status_atual.nome if cliente.status_atual else 'N/A'}",
        f"Ticket estimado: R$ {cliente.ticket_estimado or 0:,.2f}",
        f"Score de conversão: {cliente.score_conversao or 'N/A'}",
        "",
        "### Dores identificadas:",
    ]
    linhas += [f"- {d.descricao} (impacto: {d.impacto or 'N/A'})" for d in dores] or ["- Nenhuma registrada"]

    linhas += ["", "### Oportunidades:"]
    linhas += [f"- {o.descricao}" for o in oportunidades] or ["- Nenhuma registrada"]

    linhas += ["", "### Últimas interações:"]
    for i in interacoes:
        linhas.append(f"- [{i.realizada_em.date()}] {i.tipo}: {i.resumo or 'sem resumo'}")
    if not interacoes:
        linhas.append("- Nenhuma registrada")

    linhas += [
        "",
        "Com base nesses dados, gere um resumo comercial objetivo (máximo 3 parágrafos) cobrindo: "
        "situação atual, principais dores/oportunidades, e recomendação principal de próximo passo.",
    ]
    return "\n".join(linhas)


def build_proxima_acao_context(cliente: Cliente) -> str:
    interacoes = sorted(cliente.interacoes, key=lambda i: i.realizada_em, reverse=True)[:3]
    dores = [d.descricao for d in cliente.dores_oportunidades if d.tipo == "DOR"]
    recs_pendentes = [r for r in cliente.recomendacoes if r.status == "PENDENTE"]

    linhas = [
        f"## Próxima melhor ação para: {cliente.nome_empresa}",
        f"Status atual: {cliente.status_atual.nome if cliente.status_atual else 'N/A'}",
        f"Score: {cliente.score_conversao or 'N/A'}",
        "",
        f"Dores: {'; '.join(dores) or 'nenhuma'}",
        "",
        "Últimas interações:",
    ]
    for i in interacoes:
        linhas.append(f"- {i.realizada_em.date()}: {i.resumo or i.tipo}")
    if not interacoes:
        linhas.append("- Sem interações recentes")

    if recs_pendentes:
        linhas += ["", "Recomendações IA pendentes:"]
        linhas += [f"- {r.titulo}" for r in recs_pendentes[:3]]

    linhas += [
        "",
        "Responda APENAS com JSON no formato:",
        '{"acao": "...", "justificativa": "...", "prioridade": "ALTA|MEDIA|BAIXA"}',
    ]
    return "\n".join(linhas)


def build_chat_context(pergunta: str, resumo_dados: str) -> str:
    return (
        f"## Dados atuais do CRM:\n{resumo_dados}\n\n"
        f"## Pergunta do vendedor:\n{pergunta}\n\n"
        "Responda de forma objetiva baseando-se apenas nos dados acima. "
        "Se não houver dados suficientes, diga explicitamente."
    )
