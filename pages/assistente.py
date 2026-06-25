from __future__ import annotations

import streamlit as st

from components.cards import card
from utils.styles import page_title


def render() -> None:
    page_title("Assistente IA", "Chat de estudos com sugestoes rapidas.")
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Ola, Manu! Sou a Luna, sua assistente de estudos. Posso ajudar com revisao, prazos e organizacao da semana."}
        ]
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
