from __future__ import annotations

import streamlit as st
import requests

from components.cards import card, pick, record_id
from components.forms import delete_button, edit_button, save_button, text_field
from services.xano_api import criar_professor, editar_professor, excluir_professor, listar_professores
from utils.errors import show_xano_error
from utils.session import get_token
from utils.styles import page_title


def render() -> None:
    page_title("Professores", "Contatos e áreas de atuação.")
    token = get_token()

    with st.expander("Novo professor", expanded=False):
        nome = text_field("Nome", placeholder="Carlos Mendes", key="prof_nome")
        disciplina = text_field("Disciplina/Área", placeholder="Matemática", key="prof_disciplina")
        email = text_field("E-mail", placeholder="professor@edu.br", key="prof_email")
        telefone = text_field("Telefone (opcional)", placeholder="(11) 99999-9999", key="prof_telefone")
        if save_button("Criar professor", key="prof_criar"):
            if not nome.strip():
                st.warning("Informe o nome do professor.")
            else:
                payload = {"nome": nome.strip()}
                if email.strip():
                    payload["email"] = email.strip()
                try:
                    criar_professor(payload, token)
                    st.success("Professor criado com sucesso.")
                    st.rerun()
                except requests.RequestException as exc:
                    show_xano_error(exc, default="Não foi possível criar o professor.")

    try:
        professores = listar_professores(token)
    except requests.RequestException as exc:
        show_xano_error(exc, default="Não foi possível carregar professores.")
        professores = []

    if not professores:
        st.info("Nenhum professor cadastrado ainda.")
        return

    cols = st.columns(2)
    for idx, prof in enumerate(professores):
        with cols[idx % 2]:
            name = pick(prof, "nome", "name", default="Professor")
            initials = (name[:2] or "PR").upper()
            card(
                f"""
                <div style="display:flex;gap:14px;align-items:center;">
                  <span class="avatar" style="background:#A855F7;">{initials}</span>
                  <div>
                    <h3 style="margin:0;">{name}</h3>
                    <div class="muted">{pick(prof, 'email', default='Sem e-mail')}</div>
                  </div>
                </div>
                """
            )
            pid = record_id(prof)
            if pid:
                with st.expander(f"Editar {name}"):
                    novo_nome = text_field("Nome", value=name, key=f"prof_edit_nome_{pid}")
                    novo_email = text_field("E-mail", value=pick(prof, "email"), key=f"prof_edit_email_{pid}")
                    if edit_button("Salvar edição", key=f"prof_editar_{pid}"):
                        try:
                            editar_professor(pid, {"nome": novo_nome.strip(), "email": novo_email.strip()}, token)
                            st.success("Professor atualizado com sucesso.")
                            st.rerun()
                        except requests.RequestException as exc:
                            show_xano_error(exc, default="Não foi possível editar o professor.")
                    if delete_button("Excluir professor", key=f"prof_excluir_{pid}"):
                        try:
                            excluir_professor(pid, token)
                            st.success("Professor excluído com sucesso.")
                            st.rerun()
                        except requests.RequestException as exc:
                            show_xano_error(exc, default="Não foi possível excluir o professor.")
