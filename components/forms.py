from __future__ import annotations

from datetime import date

import streamlit as st
import requests

from services.xano_api import buscar_usuario, cadastro, extrair_token, login
from utils.session import login_session
from utils.styles import LOGIN_IMAGE, asset_data_uri, inject_login_css


def text_field(label: str, *, placeholder: str = "", value: str | None = None, key: str | None = None) -> str:
    return st.text_input(label, value=value or "", placeholder=placeholder, key=key)


def password_field(label: str, *, placeholder: str = "", key: str | None = None) -> str:
    return st.text_input(label, placeholder=placeholder, type="password", key=key)


def text_area(label: str, *, value: str = "", placeholder: str = "", key: str | None = None) -> str:
    return st.text_area(label, value=value, placeholder=placeholder, key=key)


def select_field(label: str, options: list[str], *, key: str | None = None) -> str:
    return st.selectbox(label, options, key=key)


def date_field(
    label: str,
    *,
    value: date | None = None,
    key: str | None = None,
) -> date | None:
    return st.date_input(label, value=value, format="DD/MM/YYYY", key=key)


def select_id_field(
    label: str,
    options: list[tuple[str, int | None]],
    *,
    key: str | None = None,
    default_id: int | None = None,
) -> int | None:
    if not options:
        st.selectbox(label, ["Nenhuma opção disponível"], disabled=True, key=key)
        return None
    labels = [label for label, _ in options]
    index = 0
    if default_id is not None:
        for idx, (_, option_id) in enumerate(options):
            if option_id == default_id:
                index = idx
                break
    selected = st.selectbox(label, labels, index=index, key=key)
    for option_label, option_id in options:
        if option_label == selected:
            return option_id
    return None


def _scoped_button(
    label: str,
    *,
    variant: str,
    key: str | None = None,
    use_container_width: bool = True,
    primary: bool = False,
) -> bool:
    st.markdown(f'<div class="button-scope-{variant}">', unsafe_allow_html=True)
    clicked = st.button(
        label,
        type="primary" if primary else "secondary",
        key=key,
        use_container_width=use_container_width,
    )
    st.markdown("</div>", unsafe_allow_html=True)
    return clicked


def primary_button(label: str, *, key: str | None = None, use_container_width: bool = True) -> bool:
    return _scoped_button(label, variant="save", key=key, use_container_width=use_container_width, primary=True)


def secondary_button(label: str, *, key: str | None = None, use_container_width: bool = True) -> bool:
    return _scoped_button(label, variant="secondary", key=key, use_container_width=use_container_width)


def save_button(label: str = "Salvar", *, key: str | None = None) -> bool:
    return _scoped_button(label, variant="save", key=key, primary=True)


def edit_button(label: str = "Editar", *, key: str | None = None) -> bool:
    return _scoped_button(label, variant="edit", key=key)


def delete_button(label: str = "Excluir", *, key: str | None = None) -> bool:
    return _scoped_button(label, variant="delete", key=key)


def cancel_button(label: str = "Cancelar", *, key: str | None = None) -> bool:
    return _scoped_button(label, variant="cancel", key=key)


def _login_actions_row() -> None:
    st.markdown('<div class="login-actions-row">', unsafe_allow_html=True)
    remember_col, forgot_col = st.columns([1.2, 1], vertical_alignment="center")
    with remember_col:
        st.checkbox("Lembrar de mim", value=False, key="login_remember")
    with forgot_col:
        st.markdown(
            '<a class="login-forgot-link-text" href="?forgot=1" target="_self">Esqueceu sua senha?</a>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)
    if st.query_params.get("forgot"):
        st.markdown(
            '<p class="login-forgot-hint">A recuperação de senha por e-mail estará disponível em breve.</p>',
            unsafe_allow_html=True,
        )


def button_style_reference() -> None:
    st.markdown(
        """
        <div class="form-actions">
          <span class="button-preview button-primary">Principal</span>
          <span class="button-preview button-secondary">Secundario</span>
          <span class="button-preview button-save">Salvar</span>
          <span class="button-preview button-edit">Editar</span>
          <span class="button-preview button-delete">Excluir</span>
          <span class="button-preview button-cancel">Cancelar</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _friendly_http_error(exc: requests.HTTPError, *, invalid_credentials: str) -> str:
    if exc.response is not None:
        if exc.response.status_code == 429:
            return "Limite de requisições do Xano atingido. Aguarde cerca de 20 segundos e tente novamente."
        if exc.response.status_code in {401, 403}:
            return invalid_credentials
        return f"Erro do servidor ({exc.response.status_code}). Tente novamente."
    return "Erro ao comunicar com o Xano."


def _complete_auth(
    resposta: dict | list,
    email: str,
    *,
    nome: str | None = None,
) -> bool:
    token = extrair_token(resposta)
    if not token:
        return False

    user = resposta.get("user") if isinstance(resposta, dict) else None
    if not user and isinstance(resposta, dict) and resposta.get("user_id"):
        user = {"id": resposta["user_id"], "email": email}
        if nome:
            user["name"] = nome

    login_session(token, user=user, email=email)
    try:
        perfil_api = buscar_usuario(token)
        if perfil_api:
            login_session(
                token,
                user=perfil_api,
                email=perfil_api.get("email", email),
            )
    except requests.RequestException:
        pass
    return True


def login_page() -> None:
    login_src = asset_data_uri(str(LOGIN_IMAGE))
    inject_login_css()
    st.markdown('<div class="login-bg"></div>', unsafe_allow_html=True)
    if login_src:
        st.markdown(f'<img class="login-cosmos" src="{login_src}" alt="">', unsafe_allow_html=True)

    left, right = st.columns([1.22, 0.78], gap="large")
    with left:
        st.markdown('<div class="login-copy-anchor"></div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="login-copy">
              <div class="login-brand">
                <span class="brand-mark">🎓</span>
                <div class="login-brand-name">EduTrack <span>AI</span></div>
              </div>
              <h1 class="login-headline">
                <span class="login-headline-main">Seu semestre sob</span><br>
                <span class="login-headline-accent">controle</span>
              </h1>
              <p class="login-subcopy">
                Organize disciplinas, tarefas e notas em um painel acadêmico inteligente
                feito para acompanhar seu semestre com clareza.
              </p>
              <div class="benefit-grid">
                <div class="benefit-card">
                  <div class="benefit-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2 4 5v6.09c0 5.05 3.41 9.76 8 10.91 4.59-1.15 8-5.86 8-10.91V5l-8-3zm0 2.18 6 2.25V11.1c0 3.72-2.55 7.18-6 8.17-3.45-.99-6-4.45-6-8.17V6.43l6-2.25z"/></svg>
                  </div>
                  <strong>Seguro</strong>
                  <span>Seus dados protegidos</span>
                </div>
                <div class="benefit-card">
                  <div class="benefit-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7z"/></svg>
                  </div>
                  <strong>Inteligente</strong>
                  <span>IA para apoiar seus estudos</span>
                </div>
                <div class="benefit-card">
                  <div class="benefit-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
                  </div>
                  <strong>Personalizado</strong>
                  <span>Feito para sua rotina</span>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown('<div class="login-panel-anchor"></div>', unsafe_allow_html=True)
        tab_login, tab_create = st.tabs(["Entrar", "Criar minha conta"])
        with tab_login:
            st.markdown(
                '<div class="login-form-header">'
                '<h1>Bem-vindo de volta!</h1>'
                '<p>Entre na sua conta para continuar sua jornada.</p>'
                '</div>',
                unsafe_allow_html=True,
            )
            email = text_field("E-mail", placeholder="seu@email.com", key="login_email")
            senha = password_field("Senha", placeholder="Digite sua senha", key="login_password")
            _login_actions_row()
            st.markdown('<div class="login-submit-gap">', unsafe_allow_html=True)
            if primary_button("Acessar meu painel  →", key="login_submit"):
                if not email or not senha:
                    st.warning("Informe e-mail e senha para entrar.")
                else:
                    try:
                        resposta = login(email, senha)
                        if _complete_auth(resposta, email):
                            st.rerun()
                        else:
                            st.error("Token não encontrado na resposta do Xano.")
                    except requests.HTTPError as exc:
                        st.error(_friendly_http_error(exc, invalid_credentials="Credenciais inválidas."))
                    except requests.RequestException:
                        st.error("Erro de conexão com Xano. Verifique sua internet e tente novamente.")
            st.markdown("</div>", unsafe_allow_html=True)
        with tab_create:
            nome = text_field("Nome", placeholder=" Nome completo", key="signup_name")
            email = text_field("E-mail", placeholder="seu@email.com", key="signup_email")
            senha = password_field("Senha", placeholder="Crie uma senha", key="signup_password")
            confirmar = password_field("Confirmar senha", placeholder="Confirmar senha", key="signup_confirm")
            if primary_button("Criar conta", key="signup_submit"):
                if not nome:
                    st.warning("Informe seu nome para criar a conta.")
                elif not email:
                    st.warning("Informe seu e-mail para criar a conta.")
                elif not senha:
                    st.warning("Informe uma senha para criar a conta.")
                elif senha != confirmar:
                    st.warning("As senhas não coincidem.")
                else:
                    try:
                        resposta = cadastro({"name": nome, "email": email, "password": senha})
                        if _complete_auth(resposta, email, nome=nome):
                            st.rerun()
                        else:
                            st.error("Conta criada, mas o token de acesso não foi retornado. Tente fazer login.")
                    except requests.HTTPError as exc:
                        st.error(_friendly_http_error(exc, invalid_credentials="Não foi possível criar a conta. Verifique os dados."))
                    except requests.RequestException:
                        st.error("Erro de conexão com Xano. Verifique sua internet e tente novamente.")
