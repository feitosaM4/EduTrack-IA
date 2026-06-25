from __future__ import annotations

from typing import Any

import streamlit as st


def init_session() -> None:
    st.session_state.setdefault("authed", False)
    st.session_state.setdefault("token", None)
    st.session_state.setdefault("user", None)
    st.session_state.setdefault("user_email", None)
    st.session_state.setdefault("app_theme", "rosa_lilas")


def is_authenticated() -> bool:
    return bool(st.session_state.get("authed", False) and st.session_state.get("token"))


def get_token() -> str | None:
    token = st.session_state.get("token")
    return str(token) if token else None


def login_session(
    token: str,
    user: dict[str, Any] | None = None,
    email: str | None = None,
) -> None:
    st.session_state.authed = True
    st.session_state.token = token
    st.session_state.user = user
    st.session_state.user_email = email or (user.get("email") if user else None)


def logout_session() -> None:
    st.session_state.authed = False
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.user_email = None
