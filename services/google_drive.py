from __future__ import annotations

from typing import Any


def conectar() -> bool:
    """Inicia fluxo OAuth com Google Drive (implementação futura)."""
    return False


def esta_conectado() -> bool:
    """Verifica se há credenciais válidas salvas."""
    return False


def enviar_pdf(nome_arquivo: str, conteudo: bytes, *, pasta: str | None = None) -> dict[str, Any] | None:
    """Envia PDF de desempenho para o Google Drive."""
    return None


def enviar_arquivo(caminho_local: str, *, pasta: str | None = None) -> dict[str, Any] | None:
    """Upload genérico de arquivo para o Drive."""
    return None
