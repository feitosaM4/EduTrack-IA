from __future__ import annotations

from typing import Any

from services import google_calendar, google_drive


def conectar_google_calendar() -> bool:
    return google_calendar.conectar()


def sincronizar_evento_google_calendar(evento: dict[str, Any]):
    return google_calendar.enviar_evento(evento)


def conectar_google_drive() -> bool:
    return google_drive.conectar()


def enviar_arquivo_google_drive(arquivo: Any):
    return google_drive.enviar_arquivo(str(arquivo))
