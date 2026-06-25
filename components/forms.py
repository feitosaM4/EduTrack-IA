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


def social_login_buttons() -> None:
    _, center, _ = st.columns([1, 1.4, 1])
    with center:
        st.markdown('<div class="social-login-row">', unsafe_allow_html=True)
        st.button("Google", key="login_google", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


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


def login_page() -> None:
    login_src = asset_data_uri(str(LOGIN_IMAGE))
    inject_login_css()
    st.markdown('<div class="login-bg"></div>', unsafe_allow_html=True)
    if login_src:
        st.markdown(f'<img class="login-cosmos" src="{login_src}" alt="">', unsafe_allow_html=True)

    left, right = st.columns([1.05, 1], gap="large")
    with left:
        st.markdown(
            """
            <div class="login-copy">
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:50px;">
                <span class="brand-mark">🎓</span>
                <div style="font-family:Poppins;font-size:1.35rem;font-weight:800;color:#F8FAFC;">EduTrack <span style="color:#38BDF8;">AI</span></div>
              </div>
              <h1 style="font-size:3rem;line-height:1.18;color:#F8FAFC;margin-bottom:18px;">Seu semestre<br/>sob controle</h1>
              <p style="font-size:1.05rem;color:#D7DDFB;max-width:420px;line-height:1.65;">
                Planeje seus estudos, acompanhe suas tarefas e alcance seus objetivos.
              </p>
              <div class="benefit-grid">
                <div class="benefit-card">
                  <div class="benefit-icon">🛡️</div>
                  <strong>Seguro</strong>
                  <span>Seus dados protegidos</span>
                </div>
                <div class="benefit-card">
                  <div class="benefit-icon">🧠</div>
                  <strong>Inteligente</strong>
                  <span>IA para apoiar seus estudos</span>
                </div>
                <div class="benefit-card">
                  <div class="benefit-icon">👤</div>
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
                '<h1 style="color:#F8FAFC;">Bem-vindo de volta!</h1>'
                '<p style="color:#D7DDFB;">Entre na sua conta para continuar sua jornada.</p>',
                unsafe_allow_html=True,
            )
            email = text_field("E-mail", placeholder="seu@email.com", key="login_email")
            senha = password_field("Senha", placeholder="Digite sua senha", key="login_password")
            st.checkbox("Lembrar de mim", value=False)
            if primary_button("Acessar meu painel  →", key="login_submit"):
                if not email or not senha:
                    st.warning("Informe e-mail e senha para entrar.")
                else:
                    try:
                        resposta = login(email, senha)
                        token = extrair_token(resposta)
                        if token:
                            user = resposta.get("user") if isinstance(resposta, dict) else None
                            if not user and isinstance(resposta, dict) and resposta.get("user_id"):
                                user = {"id": resposta["user_id"], "email": email}
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
                            st.rerun()
                        else:
                            st.error("Token não encontrado na resposta do Xano.")
                    except requests.HTTPError as exc:
                        st.error(_friendly_http_error(exc, invalid_credentials="Credenciais inválidas."))
                    except requests.RequestException:
                        st.error("Erro de conexão com Xano. Verifique sua internet e tente novamente.")
            st.caption("ou continue com")
            social_login_buttons()
        with tab_create:
            nome = text_field("Nome", placeholder="Manu Silva", key="signup_name")
            email = text_field("E-mail", placeholder="seu@email.com", key="signup_email")
            senha = password_field("Senha", placeholder="Crie uma senha", key="signup_password")
            confirmar = password_field("Confirmar senha", placeholder="Repita a senha", key="signup_confirm")
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
                        cadastro({"name": nome, "email": email, "password": senha})
                        st.success("Conta criada com sucesso! Agora faça login.")
                    except requests.HTTPError as exc:
                        st.error(_friendly_http_error(exc, invalid_credentials="Não foi possível criar a conta. Verifique os dados."))
                    except requests.RequestException:
                        st.error("Erro de conexão com Xano. Verifique sua internet e tente novamente.")
