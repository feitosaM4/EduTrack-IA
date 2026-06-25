from __future__ import annotations

import requests
import streamlit as st

from components.cards import card
from components.forms import save_button, text_field
from services.xano_api import atualizar_perfil, atualizar_usuario, buscar_perfil, buscar_usuario, criar_perfil
from utils.errors import show_xano_error
from utils.session import get_token, logout_session
from utils.styles import T, page_title


def _pick(data: dict, *keys: str, default: str = "") -> str:
    for key in keys:
        value = data.get(key)
        if value is not None:
            return str(value)
    return default


def render() -> None:
    page_title("Perfil", "Dados do aluno e informações acadêmicas.")
    token = get_token()
    user: dict = {}
    perfil: dict = {}

    if token:
        try:
            user = buscar_usuario(token)
        except requests.RequestException:
            user = st.session_state.get("user") or {}
        try:
            perfil = buscar_perfil(token)
        except requests.RequestException:
            perfil = {}

    nome = _pick(user, "name", "nome") or _pick(perfil, "nome", default="Estudante")
    email = st.session_state.get("user_email") or _pick(user, "email") or _pick(perfil, "email", default="")
    curso = _pick(perfil, "curso", default="")
    instituicao = _pick(perfil, "objetivo", default="")
    semestre = _pick(perfil, "semestre", default="")
    initials = (nome[:2] or "E").upper()

    left, right = st.columns([1, 1.4], gap="large")
    with left:
        card(
            f"""
            <div style="text-align:center;">
              <span class="avatar" style="width:86px;height:86px;font-size:2rem;background:linear-gradient(135deg,{T["pink"]},{T["accent"]});">{initials}</span>
              <h2 style="margin-bottom:0;">{nome}</h2>
              <div class="muted">{curso or "Curso não informado"}</div>
              <div class="muted" style="margin-top:6px;">{email}</div>
            </div>
            """
        )
    with right:
        novo_nome = text_field("Nome", value=nome, key="profile_name")
        novo_email = text_field("E-mail", value=email, key="profile_email")
        novo_curso = text_field("Curso", placeholder="Ex.: Engenharia de Software", value=curso, key="profile_course")
        nova_instituicao = text_field("Instituição (opcional)", value=instituicao, key="profile_institution")
        novo_semestre = text_field("Semestre atual (opcional)", value=semestre, key="profile_semester")
        if save_button("Salvar alterações", key="profile_save"):
            if not token:
                st.warning("Sessão expirada. Faça login novamente.")
            else:
                try:
                    if novo_nome.strip():
                        atualizar_usuario(token, {"name": novo_nome.strip()})
                    dados_perfil = {
                        "nome": novo_nome.strip(),
                        "email": novo_email.strip(),
                        "curso": novo_curso.strip(),
                        "semestre": novo_semestre.strip(),
                        "objetivo": nova_instituicao.strip(),
                        "lembretes": perfil.get("lembretes", True),
                    }
                    if perfil.get("id"):
                        atualizar_perfil(token, {**dados_perfil, "id": perfil["id"]})
                    else:
                        criar_perfil(token, dados_perfil)
                    st.session_state.user = {
                        **(user if isinstance(user, dict) else {}),
                        "name": novo_nome.strip(),
                        "email": novo_email.strip(),
                    }
                    st.session_state.user_email = novo_email.strip()
                    st.success("Perfil atualizado com sucesso.")
                    st.rerun()
                except requests.RequestException as exc:
                    show_xano_error(exc, default="Não foi possível atualizar o perfil.")
