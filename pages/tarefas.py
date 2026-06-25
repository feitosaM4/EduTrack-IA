from __future__ import annotations

from datetime import date

import streamlit as st
import requests

from components.cards import pick, record_id, task_card
from components.forms import (
    date_field,
    delete_button,
    edit_button,
    save_button,
    select_field,
    select_id_field,
    text_area,
    text_field,
)
from services.xano_api import criar_tarefa, editar_tarefa, excluir_tarefa, listar_disciplinas, listar_tarefas
from utils.errors import show_xano_error
from utils.fields import PRIORIDADES, STATUS_TAREFA, disciplina_label_options, map_by_id, parse_date, tarefa_titulo
from utils.session import get_token
from utils.styles import page_title


def _status_normalizado(status: str) -> str:
    return status.strip().lower()


def render() -> None:
    page_title("Tarefas", "Organize prazos por etapa e prioridade.")
    token = get_token()

    try:
        disciplinas = listar_disciplinas(token)
    except requests.RequestException as exc:
        show_xano_error(exc, default="Não foi possível carregar disciplinas.")
        disciplinas = []

    disc_options = disciplina_label_options(disciplinas)
    disc_map = map_by_id(disciplinas)

    with st.expander("Nova tarefa", expanded=False):
        if not disc_options:
            st.warning("Cadastre uma disciplina antes de criar tarefas.")
        else:
            titulo = text_field("Título", placeholder="Lista de exercícios", key="task_titulo")
            disciplina_id = select_id_field("Disciplina", disc_options, key="task_disciplina_id")
            prazo = date_field("Prazo", value=date.today(), key="task_prazo")
            prioridade = select_field("Prioridade", PRIORIDADES, key="task_prioridade")
            status = select_field("Status", STATUS_TAREFA, key="task_status")
            descricao = text_area("Descrição (opcional)", placeholder="Detalhes da tarefa", key="task_descricao")
            if save_button("Criar tarefa", key="task_criar"):
                if not titulo.strip():
                    st.warning("Informe o título da tarefa.")
                elif disciplina_id is None:
                    st.warning("Selecione uma disciplina.")
                elif prazo is None:
                    st.warning("Informe o prazo da tarefa.")
                else:
                    payload = {
                        "nome_tarefa": titulo.strip(),
                        "disc_id": disciplina_id,
                        "data": prazo.isoformat(),
                        "tipo": prioridade.lower(),
                        "status": _status_normalizado(status),
                        "nome": descricao.strip() or titulo.strip(),
                    }
                    try:
                        criar_tarefa(payload, token)
                        st.success("Tarefa criada com sucesso.")
                        st.rerun()
                    except requests.RequestException as exc:
                        show_xano_error(exc, default="Não foi possível criar a tarefa.")

    try:
        tasks = listar_tarefas(token)
    except requests.RequestException as exc:
        show_xano_error(exc, default="Não foi possível carregar tarefas.")
        tasks = []

    if not tasks:
        st.info("Nenhuma tarefa cadastrada ainda.")
        return

    status_filter = st.radio("Status", ["Todas", *STATUS_TAREFA], horizontal=True)
    items = tasks
    if status_filter != "Todas":
        items = [t for t in tasks if _status_normalizado(pick(t, "status")) == _status_normalizado(status_filter)]

    columns = st.columns(3)
    for col, status in zip(columns, STATUS_TAREFA):
        with col:
            st.markdown(f"### {status}")
            col_tasks = [t for t in items if _status_normalizado(pick(t, "status")) == _status_normalizado(status)]
            if not col_tasks:
                st.caption("Nenhuma tarefa nesta coluna.")
            for task in col_tasks:
                task_card(task, show_description=True, disciplinas_map=disc_map)
                tid = record_id(task)
                if tid:
                    with st.expander(f"Editar {tarefa_titulo(task)}"):
                        novo_titulo = text_field(
                            "Título",
                            value=tarefa_titulo(task),
                            key=f"task_edit_titulo_{tid}",
                        )
                        prazo_atual = parse_date(task.get("data")) or date.today()
                        novo_prazo = date_field(
                            "Prazo",
                            value=prazo_atual,
                            key=f"task_edit_prazo_{tid}",
                        )
                        novo_status = select_field("Status", STATUS_TAREFA, key=f"task_edit_status_{tid}")
                        if edit_button("Salvar edição", key=f"task_editar_{tid}"):
                            try:
                                editar_tarefa(
                                    tid,
                                    {
                                        "nome_tarefa": novo_titulo.strip(),
                                        "status": _status_normalizado(novo_status),
                                        "data": novo_prazo.isoformat() if novo_prazo else None,
                                    },
                                    token,
                                )
                                st.success("Tarefa atualizada com sucesso.")
                                st.rerun()
                            except requests.RequestException as exc:
                                show_xano_error(exc, default="Não foi possível editar a tarefa.")
                        if delete_button("Excluir tarefa", key=f"task_excluir_{tid}"):
                            try:
                                excluir_tarefa(tid, token)
                                st.success("Tarefa excluída com sucesso.")
                                st.rerun()
                            except requests.RequestException as exc:
                                show_xano_error(exc, default="Não foi possível excluir a tarefa.")
