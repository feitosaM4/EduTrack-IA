from __future__ import annotations

import streamlit as st

from components.cards import card
from utils.styles import page_title


def _user_first_name() -> str:
    user = st.session_state.get("user") or {}
    if isinstance(user, dict):
        full_name = str(user.get("name") or user.get("nome") or "").strip()
        if full_name:
            return full_name.split()[0]
    email = st.session_state.get("user_email")
    if isinstance(email, str) and email.strip():
        return email.split("@")[0].capitalize()
    return "estudante"


def _greeting_message() -> str:
    nome = _user_first_name()
    return (
        f"Ola, {nome}! Sou a Luna, sua assistente de estudos. "
        "Posso ajudar com revisao, prazos e organizacao da semana."
    )


def _init_messages() -> None:
    user_key = str(
        (st.session_state.get("user") or {}).get("id")
        or st.session_state.get("user_email")
        or ""
    )
    if "messages" not in st.session_state or st.session_state.get("assistant_user_key") != user_key:
        st.session_state.messages = [{"role": "assistant", "content": _greeting_message()}]
        st.session_state.assistant_user_key = user_key


def render() -> None:
    page_title("Assistente IA", "Chat de estudos com sugestoes rapidas.")
    _init_messages()
    left, right = st.columns([1.8, 1], gap="large")
    with left:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        if prompt := st.chat_input("Pergunte algo a Luna..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": "Sugestao: priorize Fisica hoje, reserve 40 minutos para exercicios e feche com um resumo curto."})
            st.rerun()
    with right:
        card(
            """
            <h3>Sugestoes rapidas</h3>
            <p class="muted">Plano de estudos para AP2</p>
            <p class="muted">Resumo de Biologia</p>
            <p class="muted">Revisar tarefas atrasadas</p>
            """
        )
        st.metric("Horas estudadas", "25h", "+3h")
        st.metric("Tarefas concluidas", "4/12", "-33%")
        st.metric("Media atual", "8.2", "+0.3")
