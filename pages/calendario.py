from __future__ import annotations

import calendar
from datetime import date

import streamlit as st
import requests

from components.forms import date_field, save_button, select_field, text_area, text_field
from services.xano_api import criar_evento_calendario, listar_eventos_calendario
from utils.errors import show_xano_error
from utils.fields import EVENT_COLORS, TIPOS_EVENTO, format_date_br
from utils.session import get_token
from utils.styles import T, page_title

MESES = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
]


def render() -> None:
    page_title("Calendário", "Visualize prazos, provas e eventos acadêmicos.")
    token = get_token()
    hoje = date.today()

    if "cal_year" not in st.session_state:
        st.session_state.cal_year = hoje.year
    if "cal_month" not in st.session_state:
        st.session_state.cal_month = hoje.month

    nav1, nav2, nav3 = st.columns([1, 3, 1])
    if nav1.button("◀ Mês anterior", use_container_width=True):
        if st.session_state.cal_month == 1:
            st.session_state.cal_month = 12
            st.session_state.cal_year -= 1
        else:
            st.session_state.cal_month -= 1
        st.rerun()
    nav2.markdown(
        f"<h3 style='text-align:center;margin:0;'>{MESES[st.session_state.cal_month - 1]} {st.session_state.cal_year}</h3>",
        unsafe_allow_html=True,
    )
    if nav3.button("Próximo mês ▶", use_container_width=True):
        if st.session_state.cal_month == 12:
            st.session_state.cal_month = 1
            st.session_state.cal_year += 1
        else:
            st.session_state.cal_month += 1
        st.rerun()

    try:
        eventos = listar_eventos_calendario(
            token,
            year=st.session_state.cal_year,
            month=st.session_state.cal_month,
        )
    except requests.RequestException as exc:
        show_xano_error(exc, default="Não foi possível carregar eventos do calendário.")
        eventos = {}

    cols = st.columns(7)
    for i, dia in enumerate(["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]):
        cols[i].markdown(
            f"<div style='text-align:center;font-weight:800;color:{T['muted']};'>{dia}</div>",
            unsafe_allow_html=True,
        )

    for semana in calendar.monthcalendar(st.session_state.cal_year, st.session_state.cal_month):
        cols = st.columns(7)
        for col, dia in zip(cols, semana):
            if dia == 0:
                col.markdown('<div class="calendar-cell-empty"></div>', unsafe_allow_html=True)
                continue
            dia_eventos = eventos.get(dia, [])
            eventos_html = "".join(
                f'<span class="event-dot" style="background:{ev.get("cor", "#A855F7")};">{ev.get("titulo", "Evento")}</span>'
                for ev in dia_eventos[:3]
            )
            extra = f'<div class="muted" style="font-size:.65rem;">+{len(dia_eventos)-3} mais</div>' if len(dia_eventos) > 3 else ""
            destaque = "border:2px solid #A855F7;" if dia == hoje.day and st.session_state.cal_month == hoje.month and st.session_state.cal_year == hoje.year else ""
            col.markdown(
                f'<div class="calendar-cell" style="{destaque}"><b>{dia}</b>{eventos_html}{extra}</div>',
                unsafe_allow_html=True,
            )

    with st.expander("Adicionar evento"):
        titulo = text_field("Título", placeholder="Prova de Cálculo", key="cal_titulo")
        data_evento = date_field("Data", value=hoje, key="cal_data")
        tipo = select_field("Tipo", TIPOS_EVENTO, key="cal_tipo")
        descricao = text_area("Descrição (opcional)", key="cal_descricao")
        if save_button("Salvar evento", key="cal_salvar"):
            if not titulo.strip():
                st.warning("Informe o título do evento.")
            elif data_evento is None:
                st.warning("Informe a data do evento.")
            else:
                payload = {
                    "titulo": titulo.strip(),
                    "data": data_evento.isoformat(),
                    "tipo": tipo,
                    "descricao": descricao.strip(),
                    "color": EVENT_COLORS.get(tipo, "#6B7280"),
                }
                try:
                    criar_evento_calendario(payload, token)
                    st.success("Evento adicionado ao calendário.")
                    st.rerun()
                except requests.RequestException as exc:
                    show_xano_error(exc, default="Não foi possível salvar o evento.")

    if eventos:
        st.subheader("Eventos do mês")
        for dia in sorted(eventos):
            for ev in eventos[dia]:
                st.markdown(
                    f"**{format_date_br(date(st.session_state.cal_year, st.session_state.cal_month, dia))}** · "
                    f"{ev.get('tipo', 'Evento')} · {ev.get('titulo', 'Sem título')} "
                    f"{'· ' + ev.get('disciplina') if ev.get('disciplina') else ''}"
                )
