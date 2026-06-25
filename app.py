from __future__ import annotations

import streamlit as st

from components.forms import login_page
from components.sidebar import sidebar
from pages import (
    assistente,
    calendario,
    configuracoes,
    dashboard,
    disciplinas,
    notas,
    perfil,
    professores,
    tarefas,
)
from utils.session import init_session, is_authenticated
from utils.styles import inject_css


ROUTES = {
    "Dashboard": dashboard.render,
    "Disciplinas": disciplinas.render,
    "Tarefas": tarefas.render,
    "Calendario": calendario.render,
    "Notas": notas.render,
    "Professores": professores.render,
    "Perfil": perfil.render,
    "Assistente IA": assistente.render,
    "Configuracoes": configuracoes.render,
}


def main() -> None:
    st.set_page_config(
        page_title="Edutrack IA",
        page_icon="🎓",
        layout="wide",
    )

    init_session()
    inject_css(hide_sidebar=not is_authenticated())

    if not is_authenticated():
        login_page()
        return

    selected_page = sidebar()

    page = ROUTES.get(selected_page)

    if page is None:
        st.error(f"Página não encontrada: {selected_page}")
        return

    page()


if __name__ == "__main__":
    main()