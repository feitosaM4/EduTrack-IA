from __future__ import annotations

import streamlit as st
import requests

from components.cards import disciplina_card, pick, record_id
from components.forms import delete_button, edit_button, save_button, select_id_field, text_field
from services.xano_api import criar_disciplina, editar_disciplina, excluir_disciplina, listar_disciplinas, listar_professores
from utils.errors import show_xano_error
from utils.fields import disciplina_nome, map_by_id, professor_label_options
from utils.session import get_token
from utils.styles import page_title

_CARGA_LOCAL_KEY = "disciplina_carga_local"


def _carga_local() -> dict[str, str]:
    if _CARGA_LOCAL_KEY not in st.session_state:
        st.session_state[_CARGA_LOCAL_KEY] = {}
    return st.session_state[_CARGA_LOCAL_KEY]


def _build_payload(nome_disciplina: str, prof_id: int | None) -> dict:
    payload: dict = {"nome_disciplina": nome_disciplina.strip()}
    if prof_id is not None:
        payload["prof_id"] = prof_id
    return payload


def render() -> None:
    page_title("Disciplinas", "Organize suas matérias e professores responsáveis.")
    token = get_token()
    carga_local = _carga_local()

    try:
        professores = listar_professores(token)
    except requests.RequestException as exc:
        show_xano_error(exc, default="Não foi possível carregar professores.")
        professores = []

    prof_options = professor_label_options(professores)

    with st.expander("Nova disciplina", expanded=False):
        nome_disciplina = text_field("Nome da disciplina", placeholder="Matemática", key="disciplina_nome")
        prof_id = select_id_field(
            "Professor responsável (opcional)",
            prof_options,
            key="disciplina_prof_id",
        )
        carga_horaria = text_field(
            "Carga horária (opcional)",
            placeholder="60",
            key="disciplina_carga",
        )
        if save_button("Criar disciplina", key="disciplina_criar"):
            if not nome_disciplina.strip():
                st.warning("Informe o nome da disciplina.")
            else:
                payload = _build_payload(nome_disciplina, prof_id)
                try:
                    criada = criar_disciplina(payload, token)
                    novo_id = record_id(criada)
                    if novo_id and carga_horaria.strip():
                        carga_local[str(novo_id)] = carga_horaria.strip()
                    st.success("Disciplina criada com sucesso.")
                    st.rerun()
                except requests.RequestException as exc:
                    show_xano_error(exc, default="Não foi possível criar a disciplina.")

    try:
        disciplinas = listar_disciplinas(token)
    except requests.RequestException as exc:
        show_xano_error(exc, default="Não foi possível carregar disciplinas.")
        disciplinas = []

    if not disciplinas:
        st.info("Nenhuma disciplina cadastrada ainda.")
        return

    prof_map = map_by_id(professores)
    query = text_field("Pesquisar disciplina", placeholder="Digite o nome da disciplina", key="subject_search")
    filtered = [
        d for d in disciplinas
        if query.lower() in disciplina_nome(d).lower()
    ]

    if not filtered:
        st.warning("Nenhuma disciplina encontrada para a busca.")
        return

    cols = st.columns(2)
    for idx, disciplina in enumerate(filtered):
        nome = disciplina_nome(disciplina)
        prof = prof_map.get(str(disciplina.get("prof_id") or ""), {})
        prof_nome = pick(prof, "nome", "name", default="Sem professor")
        sid = record_id(disciplina)
        carga = carga_local.get(str(sid), "") if sid else ""
        with cols[idx % 2]:
            disciplina_card(nome, prof_nome, carga)
            if sid:
                with st.expander(f"Editar {nome}"):
                    novo_nome = text_field("Nome da disciplina", value=nome, key=f"disciplina_edit_nome_{sid}")
                    novo_prof_id = select_id_field(
                        "Professor responsável (opcional)",
                        prof_options,
                        key=f"disciplina_edit_prof_{sid}",
                        default_id=int(disciplina.get("prof_id")) if disciplina.get("prof_id") else None,
                    )
                    nova_carga = text_field(
                        "Carga horária (opcional)",
                        value=carga,
                        key=f"disciplina_edit_carga_{sid}",
                    )
                    if edit_button("Salvar edição", key=f"disciplina_editar_{sid}"):
                        dados = _build_payload(novo_nome, novo_prof_id)
                        try:
                            editar_disciplina(sid, dados, token)
                            if nova_carga.strip():
                                carga_local[str(sid)] = nova_carga.strip()
                            else:
                                carga_local.pop(str(sid), None)
                            st.success("Disciplina atualizada com sucesso.")
                            st.rerun()
                        except requests.RequestException as exc:
                            show_xano_error(exc, default="Não foi possível editar a disciplina.")
                    if delete_button("Excluir disciplina", key=f"disciplina_excluir_{sid}"):
                        try:
                            excluir_disciplina(sid, token)
                            carga_local.pop(str(sid), None)
                            st.success("Disciplina excluída com sucesso.")
                            st.rerun()
                        except requests.RequestException as exc:
                            show_xano_error(exc, default="Não foi possível excluir a disciplina.")
