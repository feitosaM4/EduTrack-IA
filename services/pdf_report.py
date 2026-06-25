from __future__ import annotations

import io
from datetime import datetime
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from utils.desempenho import (
    desempenho_por_disciplina,
    notas_para_relatorio,
    recomendacoes_simples,
    resumo_geral,
    tarefas_para_relatorio,
)
from utils.fields import map_by_id


def gerar_pdf_desempenho(
    *,
    nome_usuario: str,
    disciplinas: list[dict[str, Any]],
    tarefas: list[dict[str, Any]],
    notas: list[dict[str, Any]],
) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="Relatório de Desempenho",
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=20,
        textColor=colors.HexColor("#4A5FE7"),
        spaceAfter=12,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=18,
    )
    heading_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#7C3AED"),
        spaceBefore=14,
        spaceAfter=8,
    )
    body_style = styles["Normal"]

    resumo = resumo_geral(disciplinas, tarefas, notas)
    disc_map = map_by_id(disciplinas)
    por_disciplina = desempenho_por_disciplina(disciplinas, tarefas, notas)
    notas_linhas = notas_para_relatorio(notas, disc_map)
    pendentes, concluidas = tarefas_para_relatorio(tarefas, disc_map)
    dicas = recomendacoes_simples(resumo)
    media_txt = f"{resumo['media_geral']:.1f}" if resumo["media_geral"] is not None else "—"
    gerado_em = datetime.now().strftime("%d/%m/%Y %H:%M")

    story: list[Any] = [
        Paragraph("Relatório de Desempenho — EduTrack AI", title_style),
        Paragraph(f"Aluno(a): <b>{nome_usuario or 'Estudante'}</b>", body_style),
        Paragraph(f"Gerado em: {gerado_em}", subtitle_style),
        Paragraph("Resumo geral", heading_style),
        Paragraph(
            f"Média geral: <b>{media_txt}</b> · "
            f"Disciplinas: <b>{resumo['total_disciplinas']}</b> · "
            f"Tarefas: <b>{resumo['total_tarefas']}</b> · "
            f"Pendentes: <b>{resumo['tarefas_pendentes']}</b> · "
            f"Concluídas: <b>{resumo['tarefas_concluidas']}</b> · "
            f"Notas: <b>{resumo['total_notas']}</b>",
            body_style,
        ),
        Spacer(1, 0.4 * cm),
    ]

    if por_disciplina:
        story.append(Paragraph("Desempenho por disciplina", heading_style))
        tabela_disc = [["Disciplina", "Notas", "Tarefas", "Pendentes", "Média"]]
        for linha in por_disciplina:
            media_disc = f"{linha['media']:.1f}" if linha["media"] is not None else "—"
            tabela_disc.append(
                [
                    linha["disciplina"],
                    str(linha["notas"]),
                    str(linha["tarefas"]),
                    str(linha["pendentes"]),
                    media_disc,
                ]
            )
        story.append(_styled_table(tabela_disc))
        story.append(Spacer(1, 0.3 * cm))

    if notas_linhas:
        story.append(Paragraph("Notas cadastradas", heading_style))
        tabela_notas = [["Disciplina", "Avaliação", "Tipo", "Nota", "Data"]]
        for linha in notas_linhas:
            tabela_notas.append(
                [linha["disciplina"], linha["avaliacao"], linha["tipo"], linha["nota"], linha["data"]]
            )
        story.append(_styled_table(tabela_notas))
        story.append(Spacer(1, 0.3 * cm))

    if pendentes or concluidas:
        story.append(Paragraph("Tarefas", heading_style))
        if pendentes:
            story.append(Paragraph("Pendentes", body_style))
            tabela_pend = [["Título", "Disciplina", "Prazo", "Status"]]
            for item in pendentes:
                tabela_pend.append([item["titulo"], item["disciplina"], item["prazo"], item["status"]])
            story.append(_styled_table(tabela_pend))
            story.append(Spacer(1, 0.2 * cm))
        if concluidas:
            story.append(Paragraph("Concluídas", body_style))
            tabela_done = [["Título", "Disciplina", "Prazo", "Status"]]
            for item in concluidas:
                tabela_done.append([item["titulo"], item["disciplina"], item["prazo"], item["status"]])
            story.append(_styled_table(tabela_done))
            story.append(Spacer(1, 0.2 * cm))

    story.append(Paragraph("Recomendações", heading_style))
    for dica in dicas:
        story.append(Paragraph(f"• {dica}", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def _styled_table(data: list[list[str]]) -> Table:
    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDE9FE")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#5B21B6")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#E5E7EB")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FAFAFA")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table
