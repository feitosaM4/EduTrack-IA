from __future__ import annotations

from typing import Any

import streamlit as st

from services import xano_api


def _extract_token(response: dict[str, Any] | list[Any]) -> str | None:
    if not isinstance(response, dict):
        return None
    for key in ("authToken", "auth_token", "token", "access_token", "jwt"):
        value = response.get(key)
        if value:
            return str(value)
    data = response.get("data")
    if isinstance(data, dict):
        return _extract_token(data)
    return None


def _extract_user(response: dict[str, Any] | list[Any], email: str | None = None) -> dict[str, Any]:
    if isinstance(response, dict):
        for key in ("user", "usuario", "data", "perfil"):
            value = response.get(key)
            if isinstance(value, dict):
                return value
        return {k: v for k, v in response.items() if k not in {"authToken", "auth_token", "token", "access_token", "jwt"}}
    return {"email": email} if email else {}


def login(email: str, senha: str) -> bool:
    response = xano_api.login(email, senha)
    token = _extract_token(response)
    if not token:
        raise ValueError("Login realizado, mas nenhum token foi retornado pelo Xano.")
    st.session_state.authed = True
    st.session_state.token = token
    st.session_state.user = _extract_user(response, email)
    st.session_state.user_email = st.session_state.user.get("email", email)
    return True


def cadastro(dados: dict[str, Any]) -> bool:
    response = xano_api.cadastro(dados)
    token = _extract_token(response)
    if token:
        st.session_state.authed = True
        st.session_state.token = token
        st.session_state.user = _extract_user(response, dados.get("email"))
        st.session_state.user_email = st.session_state.user.get("email", dados.get("email"))
    return True


def logout() -> None:
    st.session_state.authed = False
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.user_email = None
