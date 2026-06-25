from __future__ import annotations

from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st
import requests

from components.cards import pick, record_id
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
from services.xano_api import criar_nota, editar_nota, excluir_nota, listar_disciplinas, listar_notas
from utils.errors import show_xano_error
from utils.fields import (
    TIPOS_AVALIACAO,
    calcular_media_notas,
    decode_avaliacao_nome,
    disciplina_label_options,
    disciplina_nome,
    encode_avaliacao_nome,
    format_date_br,
    map_by_id,
    parse_date,
)
from utils.session import get_token
from utils.styles import T, page_title


def _nota_para_linha(nota: dict, disciplinas_map: dict[str, dict]) -> dict:
    meta = decode_avaliacao_nome(pick(nota, "nome"))
    disc = disciplinas_map.get(str(nota.get("disciplinas_id") or ""), {})
    nota_obtida = float(nota.get("nota") or 0)
    data_avaliacao = parse_date(nota.get("data"))
    return {
        "id": record_id(nota),
        "Disciplina": disciplina_nome(disc) or "Sem disciplina",
        "Avaliação": str(meta["nome_avaliacao"]),
        "Tipo": str(meta["tipo"]),
        "Nota": f"{nota_obtida:g}",
        "Data": format_date_br(data_avaliacao),
    }


def render() -> None:
    page_title("Notas", "Registre avaliações por disciplina.")
    token = get_token()

    try:
        disciplinas = listar_disciplinas(token)
    except requests.RequestException as exc:
        show_xano_error(exc, default="Não foi possível carregar disciplinas.")
        disciplinas = []

    disc_options = disciplina_label_options(disciplinas)
    disc_map = map_by_id(disciplinas)

    with st.expander("Nova avaliação", expanded=False):
        if not disc_options:
            st.warning("Cadastre uma disciplina antes de registrar notas.")
        else:
            disciplina_id = select_id_field("Disciplina", disc_options, key="nota_disciplina_id")
            nome_avaliacao = text_field("Descrição da avaliação", placeholder="Prova 1", key="nota_nome")
            tipo = select_field("Tipo da avaliação", TIPOS_AVALIACAO, key="nota_tipo")
            nota_obtida = text_field("Nota", placeholder="8.5", key="nota_obtida")
            incluir_data = st.checkbox("Informar data da avaliação", key="nota_incluir_data")
            data_avaliacao = date_field("Data da avaliação", value=date.today(), key="nota_data") if incluir_data else None
            observacoes = text_area("Observações (opcional)", placeholder="Comentários sobre a avaliação", key="nota_obs")
            if save_button("Salvar avaliação", key="nota_criar"):
                if disciplina_id is None:
                    st.warning("Selecione uma disciplina.")
                elif not nome_avaliacao.strip():
                    st.warning("Informe a descrição da avaliação.")
                elif not nota_obtida.strip():
                    st.warning("Informe a nota.")
                else:
                    try:
                        nome_codificado = encode_avaliacao_nome(tipo, nome_avaliacao.strip())
                        if observacoes.strip():
                            nome_codificado = f"{nome_codificado}||{observacoes.strip()}"
                        payload = {
                            "disciplinas_id": disciplina_id,
                            "nome": nome_codificado,
                            "nota": float(nota_obtida),
                        }
                        if data_avaliacao:
                            payload["data"] = data_avaliacao.isoformat()
                        criar_nota(payload, token)
                        st.success("Avaliação registrada com sucesso.")
                        st.rerun()
                    except ValueError:
                        st.warning("Informe um valor numérico válido para a nota.")
                    except requests.RequestException as exc:
                        show_xano_error(exc, default="Não foi possível salvar a avaliação.")

    try:
        notas = listar_notas(token)
    except requests.RequestException as exc:
        show_xano_error(exc, default="Não foi possível carregar notas.")
        notas = []

    if not notas:
        st.info("Nenhuma avaliação registrada ainda.")
        return

    rows = [_nota_para_linha(nota, disc_map) for nota in notas]
    df = pd.DataFrame(rows)
    media = calcular_media_notas(notas)
    if media is not None:
        st.metric("Média geral", f"{media:.1f}")

    chart_df = df.copy()
    chart_df["Valor"] = chart_df["Nota"].astype(float)
    fig = px.bar(chart_df, x="Avaliação", y="Valor", color="Disciplina", color_discrete_sequence=[T["accent"], T["pink"], T["blue"]])
    fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df.drop(columns=["id"]), use_container_width=True, hide_index=True)

    st.subheader("Gerenciar avaliações")
    for nota in notas:
        nota_id = record_id(nota)
        if not nota_id:
            continue
        meta = decode_avaliacao_nome(pick(nota, "nome"))
        disc = disc_map.get(str(nota.get("disciplinas_id") or ""), {})
        with st.expander(f"{disciplina_nome(disc) or 'Disciplina'} · {meta['nome_avaliacao']}"):
            nova_nota = text_field("Nota", value=str(nota.get("nota") or ""), key=f"nota_edit_valor_{nota_id}")
            if edit_button("Salvar edição", key=f"nota_editar_{nota_id}"):
                try:
                    editar_nota(
                        nota_id,
                        {"nota": float(nova_nota), "_origem": nota.get("_origem")},
                        token,
                    )
                    st.success("Avaliação atualizada com sucesso.")
                    st.rerun()
                except ValueError:
                    st.warning("Informe um valor numérico válido.")
                except requests.RequestException as exc:
                    show_xano_error(exc, default="Não foi possível editar a avaliação.")
            if delete_button("Excluir avaliação", key=f"nota_excluir_{nota_id}"):
                try:
                    excluir_nota(nota_id, token, origem=nota.get("_origem"))
                    st.success("Avaliação excluída com sucesso.")
                    st.rerun()
                except requests.RequestException as exc:
                    show_xano_error(exc, default="Não foi possível excluir a avaliação.")
