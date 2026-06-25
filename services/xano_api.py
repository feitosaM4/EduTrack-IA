from __future__ import annotations

import json
import time
from collections import deque
from typing import Any

import pandas as pd
import requests
import streamlit as st


BASE_URL_XANO = "https://x8ki-letl-twmt.n7.xano.io/api:HRRA97nd"
DEFAULT_TIMEOUT = 20
MAX_REQUESTS_PER_WINDOW = 8
RATE_WINDOW_SECONDS = 20
MAX_RETRIES = 3

_request_timestamps: deque[float] = deque()


class XanoRateLimitError(requests.HTTPError):
    """Erro quando o limite de requisições do Xano é atingido."""


def invalidar_cache_xano() -> None:
    _cached_get.clear()


def _wait_for_rate_limit() -> None:
    now = time.monotonic()
    while _request_timestamps and now - _request_timestamps[0] >= RATE_WINDOW_SECONDS:
        _request_timestamps.popleft()

    if len(_request_timestamps) >= MAX_REQUESTS_PER_WINDOW:
        wait_seconds = RATE_WINDOW_SECONDS - (now - _request_timestamps[0]) + 0.25
        if wait_seconds > 0:
            time.sleep(wait_seconds)

    _request_timestamps.append(time.monotonic())


def _is_rate_limit_response(response: requests.Response) -> bool:
    if response.status_code == 429:
        return True
    try:
        payload = response.json()
    except ValueError:
        return False
    if not isinstance(payload, dict):
        return False
    code = str(payload.get("code", "")).upper()
    message = str(payload.get("message", "")).lower()
    return "TOO_MANY_REQUESTS" in code or "too many" in message or "rate limit" in message


def _retry_delay(response: requests.Response | None, attempt: int) -> float:
    if response is not None:
        retry_after = response.headers.get("Retry-After")
        if retry_after and retry_after.isdigit():
            return float(retry_after)
    return min(RATE_WINDOW_SECONDS, 2 ** attempt + 1)


@st.cache_data(ttl=60, show_spinner=False)
def _cached_get(path: str, token_key: str) -> str:
    return json.dumps(_request_raw("GET", path, token=token_key or None))


def _get_json(path: str, token: str | None = None, *, use_cache: bool = True) -> dict[str, Any] | list[Any]:
    if use_cache:
        return json.loads(_cached_get(path, token or ""))
    return _request_raw("GET", path, token=token)


def _headers(token: str | None = None) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


def _endpoint(path: str) -> str:
    if not BASE_URL_XANO:
        raise ValueError("BASE_URL_XANO ainda não foi configurada.")

    return f"{BASE_URL_XANO.rstrip('/')}/{path.lstrip('/')}"


def _request(
    method: str,
    path: str,
    *,
    token: str | None = None,
    payload: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    use_cache: bool = True,
) -> dict[str, Any] | list[Any]:
    if method.upper() == "GET" and use_cache:
        return _get_json(path, token, use_cache=True)

    result = _request_raw(method, path, token=token, payload=payload, params=params)
    if method.upper() != "GET":
        invalidar_cache_xano()
    return result


def _request_raw(
    method: str,
    path: str,
    *,
    token: str | None = None,
    payload: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
) -> dict[str, Any] | list[Any]:
    last_response: requests.Response | None = None

    for attempt in range(MAX_RETRIES):
        _wait_for_rate_limit()
        response = requests.request(
            method=method,
            url=_endpoint(path),
            headers=_headers(token),
            json=payload,
            params=params,
            timeout=DEFAULT_TIMEOUT,
        )
        last_response = response

        if _is_rate_limit_response(response):
            if attempt < MAX_RETRIES - 1:
                time.sleep(_retry_delay(response, attempt))
                continue
            raise XanoRateLimitError(
                "Limite de requisições do Xano atingido.",
                response=response,
            )

        response.raise_for_status()
        if not response.content:
            return {}
        return response.json()

    if last_response is not None:
        last_response.raise_for_status()
    return {}


def _as_list(response: dict[str, Any] | list[Any]) -> list[dict[str, Any]]:
    if isinstance(response, list):
        return [item for item in response if isinstance(item, dict)]

    for key in ("items", "data", "records", "result"):
        value = response.get(key)

        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]

    return []


def _as_dict(response: dict[str, Any] | list[Any]) -> dict[str, Any]:
    if isinstance(response, dict):
        for key in ("data", "user", "perfil", "result"):
            value = response.get(key)

            if isinstance(value, dict):
                return value

        return response

    return {}


def _is_user_id_backend_error(exc: requests.HTTPError) -> bool:
    if exc.response is None:
        return False
    text = (exc.response.text or "").lower()
    return "user_id" in text or "unable to locate input" in text


def _payload_disciplina(dados: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    nome = dados.get("nome_disciplina")
    if nome:
        out["nome_disciplina"] = str(nome).strip()
    if dados.get("prof_id") is not None:
        out["prof_id"] = dados["prof_id"]
    return out


def _payload_professor(dados: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    if dados.get("nome"):
        out["nome"] = str(dados["nome"]).strip()
    if dados.get("email"):
        out["email"] = str(dados["email"]).strip()
    return out


def _payload_tarefa(dados: dict[str, Any]) -> dict[str, Any]:
    allowed = ("disc_id", "nome_tarefa", "nome", "status", "tipo", "data", "nota")
    return {k: dados[k] for k in allowed if k in dados and dados[k] is not None}


def _payload_nota(dados: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    disc_id = dados.get("disciplinas_id") or dados.get("disc_id")
    if disc_id is not None:
        out["disciplinas_id"] = disc_id
    for key in ("nome", "nota", "data"):
        if key in dados and dados[key] is not None and dados[key] != "":
            out[key] = dados[key]
    return out


def _payload_perfil(dados: dict[str, Any]) -> dict[str, Any]:
    allowed = ("nome", "email", "curso", "semestre", "objetivo", "lembretes")
    return {k: dados[k] for k in allowed if k in dados and dados[k] is not None}


def _nota_para_tarefa(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "nome_tarefa": str(payload.get("nome") or "Avaliação"),
        "disc_id": payload.get("disciplinas_id"),
        "nota": payload.get("nota"),
        "data": payload.get("data"),
        "tipo": "nota",
        "status": "concluída",
        "nome": str(payload.get("nome") or ""),
    }


def _notas_de_tarefas(tarefas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    notas: list[dict[str, Any]] = []
    for tarefa in tarefas:
        if str(tarefa.get("tipo") or "").lower() != "nota":
            continue
        notas.append(
            {
                "id": tarefa.get("id"),
                "disciplinas_id": tarefa.get("disc_id"),
                "nome": tarefa.get("nome") or tarefa.get("nome_tarefa"),
                "nota": tarefa.get("nota"),
                "data": tarefa.get("data"),
                "_origem": "tarefa",
            }
        )
    return notas


# ------------------------------------------------
# AUTENTICAÇÃO
# ------------------------------------------------

def login(email: str, senha: str) -> dict[str, Any] | list[Any]:
    return _request(
        "POST",
        "/auth/login",
        payload={
            "email": email,
            "password": senha,
        },
    )


def cadastro(dados: dict[str, Any]) -> dict[str, Any] | list[Any]:
    return _request(
        "POST",
        "/auth/signup",
        payload=dados,
    )


def extrair_token(resposta: dict[str, Any] | list[Any]) -> str | None:
    if not isinstance(resposta, dict):
        return None

    return (
        resposta.get("authToken")
        or resposta.get("auth_token")
        or resposta.get("token")
        or resposta.get("jwt")
    )


def buscar_usuario(token: str) -> dict[str, Any]:
    return _as_dict(_request("GET", "/auth/me", token=token, use_cache=False))


def atualizar_usuario(token: str, dados: dict[str, Any]) -> dict[str, Any]:
    return _as_dict(_request("PATCH", "/auth/me", token=token, payload=dados))


# ------------------------------------------------
# PERFIL
# ------------------------------------------------

def buscar_perfil(token: str) -> dict[str, Any]:
    response = _request("GET", "/perfil", token=token)
    if isinstance(response, list):
        return response[0] if response and isinstance(response[0], dict) else {}
    return _as_dict(response)


def criar_perfil(token: str, dados: dict[str, Any]) -> dict[str, Any]:
    payload = _payload_perfil(dados)
    return _as_dict(_request("POST", "/perfil", token=token, payload=payload))


def atualizar_perfil(token: str, dados: dict[str, Any]) -> dict[str, Any]:
    payload = _payload_perfil(dados)
    perfil_id = dados.get("id") or dados.get("perfil_id")
    if not perfil_id:
        raise ValueError("ID do perfil não informado.")
    return _as_dict(
        _request("PATCH", f"/perfil/{perfil_id}", token=token, payload=payload)
    )


# ------------------------------------------------
# PROFESSORES
# ------------------------------------------------

def listar_professores(token: str | None = None) -> list[dict[str, Any]]:
    return _as_list(
        _request("GET", "/professores", token=token)
    )


def criar_professor(
    dados: dict[str, Any],
    token: str | None = None,
) -> dict[str, Any]:
    return _as_dict(
        _request("POST", "/professores", token=token, payload=_payload_professor(dados))
    )


def editar_professor(
    professor_id: int | str,
    dados: dict[str, Any],
    token: str | None = None,
) -> dict[str, Any]:
    return _as_dict(
        _request(
            "PATCH",
            f"/professores/{professor_id}",
            token=token,
            payload=_payload_professor(dados),
        )
    )


def excluir_professor(
    professor_id: int | str,
    token: str | None = None,
) -> dict[str, Any]:
    return _as_dict(
        _request("DELETE", f"/professores/{professor_id}", token=token)
    )


# ------------------------------------------------
# DISCIPLINAS
# ------------------------------------------------

def listar_disciplinas(token: str | None = None) -> list[dict[str, Any]]:
    return _as_list(
        _request("GET", "/disciplinas", token=token)
    )


def criar_disciplina(
    dados: dict[str, Any],
    token: str | None = None,
) -> dict[str, Any]:
    return _as_dict(
        _request("POST", "/disciplinas", token=token, payload=_payload_disciplina(dados))
    )


def editar_disciplina(
    disciplina_id: int | str,
    dados: dict[str, Any],
    token: str | None = None,
) -> dict[str, Any]:
    return _as_dict(
        _request(
            "PATCH",
            f"/disciplinas/{disciplina_id}",
            token=token,
            payload=_payload_disciplina(dados),
        )
    )


def excluir_disciplina(
    disciplina_id: int | str,
    token: str | None = None,
) -> dict[str, Any]:
    return _as_dict(
        _request("DELETE", f"/disciplinas/{disciplina_id}", token=token)
    )


# ------------------------------------------------
# TAREFAS
# ------------------------------------------------

def listar_tarefas(token: str | None = None) -> list[dict[str, Any]]:
    return _as_list(
        _request("GET", "/tarefas", token=token)
    )


def criar_tarefa(
    dados: dict[str, Any],
    token: str | None = None,
) -> dict[str, Any]:
    return _as_dict(
        _request("POST", "/tarefas", token=token, payload=_payload_tarefa(dados))
    )


def editar_tarefa(
    tarefa_id: int | str,
    dados: dict[str, Any],
    token: str | None = None,
) -> dict[str, Any]:
    return _as_dict(
        _request(
            "PATCH",
            f"/tarefas/{tarefa_id}",
            token=token,
            payload=_payload_tarefa(dados),
        )
    )


def excluir_tarefa(
    tarefa_id: int | str,
    token: str | None = None,
) -> dict[str, Any]:
    return _as_dict(
        _request("DELETE", f"/tarefas/{tarefa_id}", token=token)
    )


# ------------------------------------------------
# NOTAS
# ------------------------------------------------

def listar_notas(token: str | None = None) -> list[dict[str, Any]]:
    try:
        return _as_list(_request("GET", "/notas", token=token))
    except requests.HTTPError as exc:
        if _is_user_id_backend_error(exc):
            return _notas_de_tarefas(listar_tarefas(token))
        raise


def criar_nota(
    dados: dict[str, Any],
    token: str | None = None,
) -> dict[str, Any]:
    payload = _payload_nota(dados)
    try:
        return _as_dict(_request("POST", "/notas", token=token, payload=payload))
    except requests.HTTPError as exc:
        if _is_user_id_backend_error(exc):
            return criar_tarefa(_nota_para_tarefa(payload), token)
        raise


def editar_nota(
    nota_id: int | str,
    dados: dict[str, Any],
    token: str | None = None,
) -> dict[str, Any]:
    if dados.get("_origem") == "tarefa":
        return editar_tarefa(nota_id, {"nota": dados.get("nota")}, token)
    payload = _payload_nota(dados)
    try:
        return _as_dict(
            _request("PATCH", f"/notas/{nota_id}", token=token, payload=payload)
        )
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code in {400, 404}:
            return editar_tarefa(nota_id, {"nota": dados.get("nota")}, token)
        raise


def excluir_nota(
    nota_id: int | str,
    token: str | None = None,
    *,
    origem: str | None = None,
) -> dict[str, Any]:
    if origem == "tarefa":
        return excluir_tarefa(nota_id, token)
    try:
        return _as_dict(_request("DELETE", f"/notas/{nota_id}", token=token))
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code in {400, 404}:
            return excluir_tarefa(nota_id, token)
        raise


# ------------------------------------------------
# CALENDÁRIO
# TODO: criar endpoint /calendario no Xano para eventos personalizados.
# Enquanto isso, o app agrega tarefas e notas com data.
# ------------------------------------------------

def _eventos_de_tarefas_e_notas(
    token: str | None,
    *,
    year: int,
    month: int,
) -> dict[int, list[dict[str, Any]]]:
    from utils.fields import decode_avaliacao_nome, disciplina_nome, map_by_id, parse_date, tarefa_titulo

    eventos: dict[int, list[dict[str, Any]]] = {}
    disciplinas = map_by_id(listar_disciplinas(token))

    for tarefa in listar_tarefas(token):
        data_tarefa = parse_date(tarefa.get("data"))
        if not data_tarefa or data_tarefa.year != year or data_tarefa.month != month:
            continue
        disc = disciplinas.get(str(tarefa.get("disc_id") or ""), {})
        eventos.setdefault(data_tarefa.day, []).append(
            {
                "id": tarefa.get("id"),
                "titulo": tarefa_titulo(tarefa),
                "tipo": tarefa.get("tipo") or "Tarefa",
                "cor": "#A855F7",
                "origem": "tarefa",
                "descricao": tarefa.get("nome") or "",
                "disciplina": disciplina_nome(disc),
            }
        )

    for nota in listar_notas(token):
        data_nota = parse_date(nota.get("data"))
        if not data_nota or data_nota.year != year or data_nota.month != month:
            continue
        meta = decode_avaliacao_nome(str(nota.get("nome") or ""))
        disc = disciplinas.get(str(nota.get("disciplinas_id") or ""), {})
        eventos.setdefault(data_nota.day, []).append(
            {
                "id": nota.get("id"),
                "titulo": str(meta["nome_avaliacao"]),
                "tipo": str(meta["tipo"]) or "Prova",
                "cor": "#EF4444",
                "origem": "nota",
                "descricao": f"Nota: {nota.get('nota')}",
                "disciplina": disciplina_nome(disc),
            }
        )

    return eventos


def listar_eventos_calendario(
    token: str | None = None,
    *,
    year: int | None = None,
    month: int | None = None,
) -> dict[int, list[dict[str, Any]]]:
    from datetime import date

    from utils.fields import EVENT_COLORS, parse_date

    hoje = date.today()
    year = year or hoje.year
    month = month or hoje.month
    eventos = _eventos_de_tarefas_e_notas(token, year=year, month=month)

    if not st.session_state.get("_xano_calendario_indisponivel"):
        try:
            api_eventos = _as_list(_get_json("/calendario", token))
        except requests.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 404:
                st.session_state["_xano_calendario_indisponivel"] = True
            api_eventos = []
    else:
        api_eventos = []

    for item in api_eventos:
        data_evento = parse_date(item.get("data") or item.get("dia") or item.get("day"))
        if not data_evento or data_evento.year != year or data_evento.month != month:
            continue
        tipo = str(item.get("tipo") or "Outro")
        eventos.setdefault(data_evento.day, []).append(
            {
                "id": item.get("id"),
                "titulo": str(item.get("titulo") or item.get("label") or "Evento"),
                "tipo": tipo,
                "cor": str(item.get("color") or EVENT_COLORS.get(tipo, "#6B7280")),
                "origem": "calendario",
                "descricao": str(item.get("descricao") or item.get("description") or ""),
                "disciplina": "",
            }
        )

    return eventos


def criar_evento_calendario(
    dados: dict[str, Any],
    token: str | None = None,
) -> dict[str, Any]:
    # TODO: criar endpoint /calendario no Xano
    try:
        return _as_dict(_request("POST", "/calendario", token=token, payload=dados))
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 404:
            return criar_tarefa(
                {
                    "nome_tarefa": dados.get("titulo"),
                    "data": dados.get("data"),
                    "tipo": dados.get("tipo"),
                    "status": "a fazer",
                    "nome": dados.get("descricao") or dados.get("titulo"),
                },
                token,
            )
        raise


def editar_evento_calendario(
    evento_id: int | str,
    dados: dict[str, Any],
    token: str | None = None,
) -> dict[str, Any]:
    # TODO: criar endpoint PATCH /calendario/{id} no Xano
    try:
        return _as_dict(
            _request("PATCH", f"/calendario/{evento_id}", token=token, payload=dados)
        )
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 404:
            return editar_tarefa(evento_id, dados, token)
        raise


def excluir_evento_calendario(
    evento_id: int | str,
    token: str | None = None,
) -> dict[str, Any]:
    # TODO: criar endpoint DELETE /calendario/{id} no Xano
    try:
        return _as_dict(_request("DELETE", f"/calendario/{evento_id}", token=token))
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 404:
            return excluir_tarefa(evento_id, token)
        raise


# ------------------------------------------------
# DASHBOARD
# Nota: /estudo-semanal pode não existir no Xano ainda.
# ------------------------------------------------

def listar_estudo_semanal(token: str | None = None) -> pd.DataFrame:
    if st.session_state.get("_xano_estudo_semanal_indisponivel"):
        return pd.DataFrame()
    try:
        data = _as_list(_get_json("/estudo-semanal", token))
        return pd.DataFrame(data)
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code == 404:
            st.session_state["_xano_estudo_semanal_indisponivel"] = True
        return pd.DataFrame()


def get_calendar_events(
    token: str | None = None,
    *,
    year: int | None = None,
    month: int | None = None,
) -> dict[int, list[dict[str, Any]]]:
    return listar_eventos_calendario(token, year=year, month=month)