from __future__ import annotations

import streamlit as st


def card(html: str) -> None:
    st.markdown(f'<div class="card">{html}</div>', unsafe_allow_html=True)


def disciplina_card(nome: str, prof_nome: str, carga: str = "") -> None:
    carga_html = (
        f'<p class="muted" style="margin:4px 0 0;">Carga horária: {carga}h</p>'
        if carga
        else ""
    )
    st.markdown(
        (
            f'<div class="card disciplina-card">'
            f'<div class="disciplina-card-row">'
            f'<span class="disciplina-card-icon">📘</span>'
            f'<div class="disciplina-card-body">'
            f'<h3 style="margin:0;">{nome}</h3>'
            f'<p class="muted" style="margin:4px 0 0;">Professor: {prof_nome}</p>'
            f"{carga_html}"
            f"</div></div></div>"
        ),
        unsafe_allow_html=True,
    )


def progress(value: int, color: str) -> str:
    return f'<div class="progress"><span style="width:{value}%; background:{color};"></span></div>'


def pick(data: dict, *keys: str, default: str = "") -> str:
    for key in keys:
        value = data.get(key)
        if value is not None:
            return str(value)
    return default


def record_id(data: dict) -> str:
    item_id = pick(data, "id", "_id", "uuid")
    return item_id


def task_card(
    task: dict,
    *,
    show_description: bool = False,
    disciplinas_map: dict[str, dict] | None = None,
) -> None:
    from utils.fields import parse_date, tarefa_titulo

    color = pick(task, "color", "cor", default="#A855F7")
    title = tarefa_titulo(task)
    disc_id = str(task.get("disc_id") or "")
    if disciplinas_map and disc_id in disciplinas_map:
        from utils.fields import disciplina_nome

        subject = disciplina_nome(disciplinas_map[disc_id])
    else:
        subject = pick(task, "subject", "disciplina", default="Sem disciplina")

    prazo = task.get("data") or task.get("prazo") or task.get("due") or ""
    prazo_date = parse_date(prazo)
    prazo_label = prazo_date.strftime("%d/%m/%Y") if prazo_date else str(prazo)
    priority = pick(task, "tipo", "priority", "prioridade", default="Media")
    status = pick(task, "status", default="A fazer")
    desc_text = pick(task, "nome", "desc", "descricao")
    if desc_text == title:
        desc_text = ""
    desc = (
        f'<p style="font-size:.83rem;margin:.55rem 0;color:#1F2937;">{desc_text}</p>'
        if show_description and desc_text
        else ""
    )
    st.markdown(
        f"""
        <div class="task" style="border-left-color:{color};">
          <div style="font-weight:800;">{title}</div>
          <div class="muted">{subject} · {prazo_label}</div>
          {desc}
          <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;">
            <span class="pill" style="background:#F3E8FF;color:{color};">{priority}</span>
            <span class="pill" style="background:#EEF2FF;color:#4338CA;">{status}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
