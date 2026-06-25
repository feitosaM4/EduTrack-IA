from __future__ import annotations

from datetime import date, datetime
from typing import Any

from components.cards import pick, record_id


EVENT_COLORS = {
    "Tarefa": "#A855F7",
    "Prova": "#EF4444",
    "Entrega": "#F59E0B",
    "Estudo": "#3B82F6",
    "Outro": "#6B7280",
}

TIPOS_AVALIACAO = ["Prova", "Trabalho", "Projeto", "Atividade", "Participação", "Outro"]
TIPOS_EVENTO = ["Tarefa", "Prova", "Entrega", "Estudo", "Outro"]
STATUS_TAREFA = ["A fazer", "Em progresso", "Concluido"]
PRIORIDADES = ["Alta", "Media", "Baixa"]


def disciplina_nome(item: dict[str, Any]) -> str:
    return pick(item, "nome_disciplina", "name", "nome", default="")


def tarefa_titulo(item: dict[str, Any]) -> str:
    return pick(item, "nome_tarefa", "titulo", "title", "nome", default="Tarefa")


def format_date_br(value: date | None) -> str:
    if value is None:
        return "—"
    return value.strftime("%d/%m/%Y")


def parse_date(value: Any) -> date | None:
    if value is None or value == "":
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    text = str(value).strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).date()
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(text[:10], fmt).date()
        except ValueError:
            continue
    return None


def encode_avaliacao_nome(tipo: str, nome: str) -> str:
    return f"{tipo.strip()}::{nome.strip()}"


def decode_avaliacao_nome(raw: str) -> dict[str, str]:
    base = (raw or "").split("||")[0]
    parts = base.split("::")
    if len(parts) >= 2:
        return {
            "tipo": parts[0] or "Outro",
            "nome_avaliacao": parts[1] or base or "Avaliação",
        }
    return {
        "tipo": "Outro",
        "nome_avaliacao": base or "Avaliação",
    }


def calcular_media_notas(notas: list[dict[str, Any]]) -> float | None:
    valores: list[float] = []
    for nota in notas:
        try:
            valores.append(float(nota.get("nota") or 0))
        except (TypeError, ValueError):
            continue
    if not valores:
        return None
    return sum(valores) / len(valores)


def map_by_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    mapped: dict[str, dict[str, Any]] = {}
    for item in items:
        item_id = record_id(item)
        if item_id:
            mapped[item_id] = item
    return mapped


def disciplina_label_options(disciplinas: list[dict[str, Any]]) -> list[tuple[str, int | None]]:
    options: list[tuple[str, int | None]] = []
    for disc in disciplinas:
        nome = disciplina_nome(disc)
        disc_id = record_id(disc)
        if nome and disc_id:
            options.append((nome, int(disc_id)))
    return options


def professor_label_options(professores: list[dict[str, Any]]) -> list[tuple[str, int | None]]:
    options: list[tuple[str, int | None]] = [("Nenhum", None)]
    for prof in professores:
        nome = pick(prof, "nome", "name")
        prof_id = record_id(prof)
        if nome and prof_id:
            options.append((nome, int(prof_id)))
    return options
