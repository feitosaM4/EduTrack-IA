from __future__ import annotations

import streamlit as st

from utils.session import logout_session
from utils.themes import theme_options


NAV_ITEMS = [
    "Dashboard",
    "Professores",
    "Disciplinas",
    "Tarefas",
    "Calendario",
    "Notas",
    "Perfil",
    "Assistente IA",
    "Configuracoes",
]

NAV_LABELS = {
    "Calendario": "Calendário",
    "Configuracoes": "Configurações",
}


def _user_display_name() -> str:
    user = st.session_state.get("user") or {}
    if isinstance(user, dict):
        return str(user.get("name") or user.get("nome") or "Estudante")
    return "Estudante"


def _user_initials() -> str:
    name = _user_display_name()
    parts = name.split()
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[1][0]}".upper()
    return (name[:2] or "E").upper()


def sidebar() -> str:
    st.sidebar.markdown(
        """
        <div style="display:flex;align-items:center;gap:10px;margin:8px 0 18px;">
          <span class="brand-mark">🎓</span>
          <div>
            <div style="font-family:Poppins;font-size:1.08rem;font-weight:800;">Edutrack <span style="color:var(--accent);">IA</span></div>
            <div class="muted" style="font-size:.72rem;">Academic Platform</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    page = st.sidebar.radio(
        "Navegacao",
        NAV_ITEMS,
        format_func=lambda item: NAV_LABELS.get(item, item),
        label_visibility="collapsed",
    )
    st.sidebar.divider()

    labels, ids = zip(*theme_options()) if theme_options() else ([], [])
    if labels:
        atual = st.session_state.get("app_theme", "rosa_lilas")
        indice = list(ids).index(atual) if atual in ids else 0
        escolha = st.sidebar.selectbox("Tema de cores", labels, index=indice, key="sidebar_theme")
        novo_tema = ids[list(labels).index(escolha)]
        if novo_tema != st.session_state.get("app_theme"):
            st.session_state.app_theme = novo_tema
            st.rerun()

    display_name = _user_display_name()
    user_initials = _user_initials()
    email = st.session_state.get("user_email") or ""
    user_card_html = (
        '<div style="display:flex;align-items:center;gap:10px;background:var(--sidebar-active);'
        'border-radius:12px;padding:10px;margin-bottom:10px;">'
        '<span class="avatar" style="width:36px;height:36px;'
        'background:linear-gradient(135deg,var(--pink),var(--accent));">'
        "__INITIALS__</span>"
        '<div><div style="font-weight:700;font-size:.9rem;">__NAME__</div>'
        '<div class="muted" style="font-size:.72rem;">__EMAIL__</div></div></div>'
    )
    user_card_html = (
        user_card_html.replace("__INITIALS__", user_initials)
        .replace("__NAME__", display_name)
        .replace("__EMAIL__", email)
    )
    st.sidebar.markdown(user_card_html, unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-logout">', unsafe_allow_html=True)
    if st.sidebar.button("Sair", use_container_width=True, key="sidebar_logout"):
        logout_session()
        st.rerun()
    st.sidebar.markdown('<div style="display:none"></div>', unsafe_allow_html=True)
    return page
