from __future__ import annotations

from typing import Any

from components.cards import pick
from utils.fields import calcular_media_notas, decode_avaliacao_nome, disciplina_nome, format_date_br, parse_date, tarefa_titulo


def _tarefa_concluida(task: dict[str, Any]) -> bool:
    status = pick(task, "status", default="").lower()
    return status in {"concluido", "concluida", "done", "finalizado"}


def resumo_geral(
    disciplinas: list[dict[str, Any]],
    tarefas: list[dict[str, Any]],
    notas: list[dict[str, Any]],
) -> dict[str, Any]:
    concluidas = [t for t in tarefas if _tarefa_concluida(t)]
    pendentes = [t for t in tarefas if not _tarefa_concluida(t)]
    media = calcular_media_notas(notas)
    return {
        "total_disciplinas": len(disciplinas),
        "total_tarefas": len(tarefas),
        "tarefas_pendentes": len(pendentes),
        "tarefas_concluidas": len(concluidas),
        "total_notas": len(notas),
        "media_geral": media,
    }


def desempenho_por_disciplina(
    disciplinas: list[dict[str, Any]],
    tarefas: list[dict[str, Any]],
    notas: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    linhas: list[dict[str, Any]] = []
    for disc in disciplinas:
        disc_id = str(disc.get("id") or "")
        nome = disciplina_nome(disc)
        notas_disc = [n for n in notas if str(n.get("disciplinas_id") or "") == disc_id]
        tarefas_disc = [t for t in tarefas if str(t.get("disc_id") or "") == disc_id]
        valores = []
        for nota in notas_disc:
            try:
                valores.append(float(nota.get("nota") or 0))
            except (TypeError, ValueError):
                continue
        media_disc = sum(valores) / len(valores) if valores else None
        linhas.append(
            {
                "disciplina": nome,
                "notas": len(notas_disc),
                "tarefas": len(tarefas_disc),
                "pendentes": len([t for t in tarefas_disc if not _tarefa_concluida(t)]),
                "concluidas": len([t for t in tarefas_disc if _tarefa_concluida(t)]),
                "media": media_disc,
            }
        )
    return linhas


def recomendacoes_simples(resumo: dict[str, Any]) -> list[str]:
    dicas: list[str] = []
    if resumo["tarefas_pendentes"] > 0:
        dicas.append(f"Você tem {resumo['tarefas_pendentes']} tarefa(s) pendente(s). Priorize as com prazo mais próximo.")
    if resumo["total_notas"] == 0:
        dicas.append("Registre suas notas para acompanhar a evolução por disciplina.")
    media = resumo.get("media_geral")
    if media is not None and media < 6:
        dicas.append("Sua média está abaixo de 6. Revise matérias com notas mais baixas e monte um plano de estudo.")
    elif media is not None and media >= 8:
        dicas.append("Ótimo desempenho! Continue revisando conteúdos para manter a consistência.")
    if not dicas:
        dicas.append("Seu semestre está organizado. Continue registrando tarefas e avaliações.")
    return dicas


def notas_para_relatorio(
    notas: list[dict[str, Any]],
    disciplinas_map: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    linhas: list[dict[str, str]] = []
    for nota in notas:
        meta = decode_avaliacao_nome(pick(nota, "nome"))
        disc = disciplinas_map.get(str(nota.get("disciplinas_id") or ""), {})
        data = parse_date(nota.get("data"))
        linhas.append(
            {
                "disciplina": disciplina_nome(disc) or "Sem disciplina",
                "avaliacao": str(meta["nome_avaliacao"]),
                "tipo": str(meta["tipo"]),
                "nota": str(nota.get("nota") or "—"),
                "data": format_date_br(data),
            }
        )
    return linhas


def tarefas_para_relatorio(
    tarefas: list[dict[str, Any]],
    disciplinas_map: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    pendentes: list[dict[str, str]] = []
    concluidas: list[dict[str, str]] = []
    for task in tarefas:
        disc = disciplinas_map.get(str(task.get("disc_id") or ""), {})
        prazo = format_date_br(parse_date(task.get("data")))
        item = {
            "titulo": tarefa_titulo(task),
            "disciplina": disciplina_nome(disc) or "Sem disciplina",
            "prazo": prazo,
            "status": pick(task, "status", default="A fazer"),
        }
        if _tarefa_concluida(task):
            concluidas.append(item)
        else:
            pendentes.append(item)
    return pendentes, concluidas
