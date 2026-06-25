from __future__ import annotations

from typing import Any


def conectar() -> bool:
    """Inicia fluxo OAuth com Google Calendar (implementação futura)."""
    return False


def esta_conectado() -> bool:
    """Verifica se há credenciais válidas salvas."""
    return False


def enviar_evento(evento: dict[str, Any]) -> dict[str, Any] | None:
    """
    Envia tarefa/evento com data para o Google Calendar.

    evento esperado:
      - titulo
      - data (YYYY-MM-DD ou datetime)
      - descricao (opcional)
      - tipo (opcional)
    """
    return None


def sincronizar_tarefas(tarefas: list[dict[str, Any]]) -> int:
    """Sincroniza lista de tarefas com calendário. Retorna quantidade enviada."""
    return 0
