from __future__ import annotations

import requests
import streamlit as st

from services.xano_api import XanoRateLimitError


def show_xano_error(
    exc: Exception,
    *,
    default: str = "Não foi possível concluir a operação. Tente novamente.",
) -> None:
    message = default
    details = str(exc)

    if isinstance(exc, XanoRateLimitError):
        message = (
            "Muitas requisições ao Xano em pouco tempo. "
            "Aguarde cerca de 20 segundos e tente novamente."
        )
        if exc.response is not None:
            details = exc.response.text or details
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        details = exc.response.text or details
        status = exc.response.status_code
        if status == 429 or "TOO_MANY_REQUESTS" in details:
            message = (
                "Limite de requisições do Xano atingido (10 a cada 20 segundos no plano gratuito). "
                "Aguarde um momento e recarregue a página."
            )
        elif status in {401, 403}:
            message = "Sessão expirada ou sem permissão. Faça login novamente."
        elif "user_id" in details.lower():
            message = "Não foi possível concluir a operação. Tente novamente ou faça login de novo."
        elif status == 400 and "missing param" in details.lower():
            message = "Dados incompletos ou campos incompatíveis com o Xano. Verifique os detalhes."
        elif status >= 500:
            message = "O servidor Xano retornou um erro. Tente novamente em instantes."

    st.error(message)
    with st.expander("Detalhes do erro"):
        st.code(details)
