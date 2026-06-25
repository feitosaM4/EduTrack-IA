from __future__ import annotations

import streamlit as st

from components.forms import secondary_button
from services import google_calendar, google_drive
from utils.session import get_token, logout_session
from utils.styles import page_title
from utils.themes import theme_options


def render() -> None:
    page_title("Configurações", "Conta, preferências e integrações.")
    token = get_token()
    user = st.session_state.get("user") or {}

    tab_conta, tab_pref, tab_int = st.tabs(["Conta", "Preferências", "Integrações"])

    with tab_conta:
        st.text_input("Nome", value=str(user.get("name") or user.get("nome") or ""), disabled=True, key="settings_name")
        st.text_input("E-mail", value=str(st.session_state.get("user_email") or ""), disabled=True, key="settings_email")
        st.caption("Para alterar nome e e-mail, use a página Perfil.")
        if st.button("Sair da conta", type="primary", key="settings_logout"):
            logout_session()
            st.rerun()

    with tab_pref:
        labels, ids = zip(*theme_options())
        atual = st.session_state.get("app_theme", "rosa_lilas")
        indice = list(ids).index(atual) if atual in ids else 0
        escolha = st.selectbox("Tema de cores do painel", labels, index=indice, key="settings_theme")
        novo_tema = ids[list(labels).index(escolha)]
        if st.button("Aplicar tema", key="settings_apply_theme"):
            st.session_state.app_theme = novo_tema
            st.success("Tema atualizado.")
            st.rerun()

    with tab_int:
        st.markdown("#### Google Calendar")
        st.write("Sincronize tarefas e eventos acadêmicos com seu calendário.")
        if secondary_button("Conectar Google Calendar", key="connect_gcal"):
            google_calendar.conectar()
            st.info("Conexão com Google Calendar em breve.")

        st.divider()
        st.markdown("#### Google Drive")
        st.write("Salve relatórios e materiais de estudo na nuvem.")
        if secondary_button("Conectar Google Drive", key="connect_gdrive"):
            google_drive.conectar()
            st.info("Conexão com Google Drive em breve.")

    if not token:
        st.warning("Sessão expirada.")
