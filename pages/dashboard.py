from __future__ import annotations

from datetime import date

import streamlit as st
import requests

from components.cards import card, pick, record_id, task_card
from services.pdf_report import gerar_pdf_desempenho
from services.xano_api import listar_disciplinas, listar_notas, listar_tarefas
from utils.desempenho import desempenho_por_disciplina, recomendacoes_simples, resumo_geral
from utils.errors import show_xano_error
from utils.fields import disciplina_nome, map_by_id, parse_date
from utils.session import get_token
from utils.styles import page_title


def _user_name() -> str:
    user = st.session_state.get("user") or {}
    if isinstance(user, dict):
        return str(user.get("name") or user.get("nome") or "Estudante")
    return "Estudante"


def _tarefas_abertas(tasks: list[dict]) -> int:
    fechados = {"concluido", "concluida", "done", "finalizado"}
    return len([t for t in tasks if pick(t, "status", default="").lower() not in fechados])


def _perf_cards_html(resumo: dict) -> str:
    media = f"{resumo['media_geral']:.1f}" if resumo["media_geral"] is not None else "—"
    items = [
        ("Média geral", media),
        ("Disciplinas", str(resumo["total_disciplinas"])),
        ("Tarefas", str(resumo["total_tarefas"])),
        ("Pendentes", str(resumo["tarefas_pendentes"])),
        ("Concluídas", str(resumo["tarefas_concluidas"])),
        ("Notas", str(resumo["total_notas"])),
    ]
    cards = "".join(
        f'<div class="perf-card"><b>{valor}</b><span>{rotulo}</span></div>'
        for rotulo, valor in items
    )
    return f'<div class="perf-grid">{cards}</div>'


def render() -> None:
    page_title("Dashboard", "Resumo acadêmico, tarefas e desempenho.")
    token = get_token()
    subjects: list[dict] = []
    tasks: list[dict] = []
    notes: list[dict] = []
    load_error: Exception | None = None

    try:
        subjects = listar_disciplinas(token)
        tasks = listar_tarefas(token)
        notes = listar_notas(token)
    except requests.RequestException as exc:
        load_error = exc

    if load_error:
        show_xano_error(load_error, default="Não foi possível carregar os dados do dashboard.")

    resumo = resumo_geral(subjects, tasks, notes)
    media = resumo["media_geral"]
    media_geral = f"{media:.1f}" if media is not None else "—"
    abertas = resumo["tarefas_pendentes"]

    st.markdown(
        f"""
        <div class="dashboard-hero">
          <h2>Seu plano de estudos ficou mais visual e inteligente.</h2>
          <p>Priorize provas, acompanhe entregas e enxergue o semestre com clareza.</p>
          <div class="hero-kpis">
            <div class="mini-stat"><b>{len(subjects)}</b><span>disciplinas</span></div>
            <div class="mini-stat"><b>{len(tasks)}</b><span>tarefas</span></div>
            <div class="mini-stat"><b>{media_geral}</b><span>média geral</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Desempenho")
    st.markdown(_perf_cards_html(resumo), unsafe_allow_html=True)

    col_pdf, _ = st.columns([1.4, 2])
    with col_pdf:
        if st.button("Gerar PDF de desempenho", key="dashboard_pdf", use_container_width=True, type="primary"):
            try:
                pdf_bytes = gerar_pdf_desempenho(
                    nome_usuario=_user_name(),
                    disciplinas=subjects,
                    tarefas=tasks,
                    notas=notes,
                )
                st.session_state["_pdf_desempenho"] = pdf_bytes
            except Exception as exc:
                st.error("Não foi possível gerar o PDF. Tente novamente.")
                st.caption(str(exc))
        if st.session_state.get("_pdf_desempenho"):
            st.download_button(
                label="Baixar PDF de desempenho",
                data=st.session_state["_pdf_desempenho"],
                file_name="desempenho_edutrack.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="dashboard_pdf_download",
            )

    por_disciplina = desempenho_por_disciplina(subjects, tasks, notes)
    if por_disciplina:
        st.markdown("#### Situação por disciplina")
        for linha in por_disciplina:
            media_disc = f"{linha['media']:.1f}" if linha["media"] is not None else "—"
            st.markdown(
                f"""
                <div class="disc-card">
                  <h4>{linha["disciplina"]}</h4>
                  <div class="muted">
                    Média: {media_disc} · Notas: {linha["notas"]} ·
                    Tarefas: {linha["tarefas"]} · Pendentes: {linha["pendentes"]} ·
                    Concluídas: {linha["concluidas"]}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Cadastre disciplinas e notas para ver o desempenho por matéria.")

    dicas = recomendacoes_simples(resumo)
    if dicas:
        st.markdown("#### Recomendações")
        for dica in dicas:
            st.markdown(f"- {dica}")

    disc_map = map_by_id(subjects)
    left, right = st.columns([1.65, 1], gap="large")
    with left:
        st.subheader("Disciplinas cadastradas")
        if not subjects:
            st.info("Nenhuma disciplina cadastrada ainda.")
        else:
            for subject in subjects[:6]:
                card(
                    f'<h3 style="margin:0 0 6px;">{disciplina_nome(subject)}</h3>'
                    f'<div class="muted">Disciplina ativa no seu semestre</div>'
                )
    with right:
        st.subheader("Próximas entregas")
        if not tasks:
            st.info("Nenhuma tarefa cadastrada ainda.")
        else:
            ordenadas = sorted(
                tasks,
                key=lambda t: parse_date(t.get("data")) or date.max,
            )
            for task in ordenadas[:5]:
                task_card(task, disciplinas_map=disc_map)
