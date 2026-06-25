from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st


from utils.themes import get_theme


BASE_DIR = Path(__file__).resolve().parents[1]
ASSET_DIR = BASE_DIR / "assets"
LOGIN_IMAGE = ASSET_DIR / "images" / "login-cosmos.png"

T = {
    "app_bg": "#F0EBF8",
    "card": "#FFFFFF",
    "border": "rgba(168, 85, 247, 0.18)",
    "border_mid": "rgba(168, 85, 247, 0.30)",
    "text": "#1F2937",
    "muted": "#6B7280",
    "light": "#9CA3AF",
    "accent": "#A855F7",
    "pink": "#EC4899",
    "green": "#059669",
    "amber": "#D97706",
    "red": "#DC2626",
    "blue": "#3B82F6",
    "teal": "#14B8A6",
    "emerald": "#10B981",
}


@st.cache_data
def asset_data_uri(path: str) -> str:
    image_path = Path(path)
    if not image_path.exists():
        return ""
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def inject_css(hide_sidebar: bool = False, theme: dict | None = None) -> None:
    theme_id = st.session_state.get("app_theme") if theme is None else None
    th = theme or get_theme(theme_id)
    sidebar_hide_css = ""
    if hide_sidebar:
        sidebar_hide_css = """
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {
          display: none !important;
        }
        """

    if hide_sidebar:
        button_css = """
        .stButton > button, .stDownloadButton > button {
          border-radius: 12px !important;
          border: 1px solid rgba(255,255,255,0.15) !important;
          font-weight: 700 !important;
          min-height: 2.45rem;
          background: rgba(255,255,255,0.08) !important;
          color: #F8FAFC !important;
          box-shadow: 0 10px 26px rgba(15,23,42,.16);
          backdrop-filter: blur(12px);
        }
        .stButton > button[kind="primary"] {
          background: linear-gradient(90deg, var(--gradient-start) 0%, var(--gradient-end) 100%) !important;
          color: #FFFFFF !important;
        }
        """
    else:
        button_css = """
        .stButton > button, .stDownloadButton > button {
          border-radius: 12px !important;
          font-weight: 700 !important;
          min-height: 2.45rem;
          background: linear-gradient(90deg, var(--gradient-start) 0%, var(--gradient-end) 100%) !important;
          color: #FFFFFF !important;
          border: 1px solid rgba(255,255,255,0.22) !important;
          box-shadow: 0 8px 20px rgba(76,29,149,.18) !important;
          transition: transform .15s ease, box-shadow .15s ease, filter .15s ease;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
          filter: brightness(1.05);
          transform: translateY(-1px);
          color: #FFFFFF !important;
          box-shadow: 0 12px 24px rgba(76,29,149,.24) !important;
        }
        .stButton > button:focus, .stDownloadButton > button:focus {
          color: #FFFFFF !important;
          box-shadow: 0 0 0 3px rgba(168,85,247,.24), 0 12px 24px rgba(76,29,149,.24) !important;
        }
        .button-scope-edit .stButton > button {
          background: #8B5CF6 !important;
          border-color: rgba(255,255,255,0.22) !important;
          color: #FFFFFF !important;
        }
        .button-scope-delete .stButton > button {
          background: #EF4444 !important;
          border-color: rgba(255,255,255,0.22) !important;
          color: #FFFFFF !important;
        }
        .button-scope-cancel .stButton > button,
        .button-scope-secondary .stButton > button {
          background: #6366F1 !important;
          border-color: rgba(255,255,255,0.22) !important;
          color: #FFFFFF !important;
        }
        .sidebar-logout .stButton > button {
          background: #EF4444 !important;
          border-color: rgba(255,255,255,0.18) !important;
          color: #FFFFFF !important;
        }
        """

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');
        [data-testid="stSidebarNav"] {{
          display: none !important;
        }}
        [data-testid="collapsedControl"] {{
          display: none !important;
        }}
        [data-testid="collapsedControl"] * {{
          font-size: 0 !important;
          color: transparent !important;
        }}
        {sidebar_hide_css}
        :root {{
          --app-bg:{th["app_bg"]}; --card:{th["card"]}; --text:{th["text"]};
          --muted:{th["muted"]}; --accent:{th["accent"]}; --pink:{th["pink"]};
          --border:{th["border"]}; --blue:{th["blue"]};
          --gradient-start:{th["gradient_start"]}; --gradient-end:{th["gradient_end"]};
          --sidebar-active:{th["sidebar_active"]}; --sidebar-active-text:{th["sidebar_active_text"]};
        }}
        .stApp {{ background: var(--app-bg); color: var(--text); font-family: Inter, sans-serif; }}
        [data-testid="stSidebar"] {{ background: #fff; border-right: 1px solid var(--border); }}
        [data-testid="stSidebar"] * {{ font-family: Inter, sans-serif; }}
        .block-container {{ max-width: 1240px; padding-top: 1.6rem; padding-bottom: 2.5rem; position: relative; z-index: 1; }}
        h1, h2, h3 {{ font-family: Poppins, Inter, sans-serif; letter-spacing: 0; color: var(--text); }}
        h1 {{ font-size: 1.65rem; font-weight: 800; margin-bottom: .1rem; }}
        h2 {{ font-size: 1.25rem; font-weight: 800; }}
        h3 {{ font-size: 1rem; font-weight: 700; }}
        div[data-testid="stMetric"] {{
          background: #fff; border: 1px solid var(--border); border-radius: 12px;
          padding: 1rem 1.1rem; box-shadow: 0 1px 4px rgba(0,0,0,.04);
        }}
        div[data-testid="stMetric"] label {{ color: var(--muted); font-size: .76rem; }}
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {{ font-family: Poppins, Inter, sans-serif; font-weight: 800; color: var(--accent); }}
        {button_css}
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {{
          border-radius: 10px;
        }}
        .standard-form {{
          display: flex; flex-direction: column; gap: 14px;
        }}
        .form-actions {{
          display: flex; gap: 10px; align-items: center; flex-wrap: wrap; margin-top: 8px;
        }}
        .form-actions > div {{ flex: 1 1 160px; }}
        .button-preview {{
          display: inline-flex; align-items: center; justify-content: center; gap: 8px;
          min-height: 2.45rem; padding: 0 18px; border-radius: 12px;
          border: 1px solid rgba(255,255,255,0.15); color: #fff; font-weight: 800;
          box-shadow: 0 10px 26px rgba(15,23,42,.16); text-decoration: none;
        }}
        .button-save, .button-primary {{
          background: linear-gradient(90deg, #4A5FE7 0%, #7B3FF2 100%);
        }}
        .button-edit {{ background: #8B5CF6; }}
        .button-delete {{ background: #EF4444; }}
        .button-cancel {{ background: rgba(255,255,255,0.08); }}
        .button-secondary {{
          background: rgba(255,255,255,0.08); backdrop-filter: blur(12px);
        }}
        .button-scope-save .stButton > button {{
          background: linear-gradient(90deg, var(--gradient-start) 0%, var(--gradient-end) 100%) !important;
          color: #FFFFFF !important;
        }}
        .disciplina-card {{ padding: 18px; }}
        .disciplina-card-row {{
          display: flex; gap: 14px; align-items: flex-start;
        }}
        .disciplina-card-icon {{
          width: 52px; height: 52px; border-radius: 14px; background: #F3E8FF;
          display: flex; align-items: center; justify-content: center; font-size: 1.7rem; flex-shrink: 0;
        }}
        .disciplina-card-body {{ flex: 1; min-width: 0; }}
        .perf-grid {{
          display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
          gap: 12px; margin-bottom: 16px;
        }}
        .perf-card {{
          background: #fff; border: 1px solid var(--border); border-radius: 14px;
          padding: 16px 18px; box-shadow: 0 2px 8px rgba(0,0,0,.04);
        }}
        .perf-card b {{
          display: block; font-family: Poppins, Inter, sans-serif;
          font-size: 1.45rem; color: var(--accent); margin-bottom: 4px;
        }}
        .perf-card span {{ color: var(--muted); font-size: .78rem; font-weight: 700; }}
        .disc-card {{
          background: #fff; border: 1px solid var(--border); border-radius: 12px;
          padding: 14px 16px; margin-bottom: 10px;
        }}
        .disc-card h4 {{ margin: 0 0 6px; color: var(--text); }}
        .disc-card .muted {{ font-size: .84rem; }}
        .card {{
          background: #fff; border: 1px solid var(--border); border-radius: 12px;
          padding: 18px; box-shadow: 0 1px 4px rgba(0,0,0,.04); height: 100%;
        }}
        .soft-card {{
          background: rgba(255,255,255,0.13); border: 1px solid rgba(255,255,255,0.24);
          border-radius: 22px; padding: 28px; box-shadow: 0 22px 70px rgba(15,23,42,0.34);
          backdrop-filter: blur(16px);
        }}
        .dashboard-hero {{
          position: relative; overflow: hidden; min-height: 214px; margin-bottom: 18px;
          border-radius: 18px; border: 1px solid rgba(255,255,255,.78);
          background:
            radial-gradient(circle at 82% 30%, rgba(168,85,247,.35), transparent 30%),
            linear-gradient(135deg, rgba(255,255,255,.92), rgba(248,245,255,.78));
          box-shadow: 0 20px 60px rgba(110,69,183,.12);
          padding: 26px 30px;
        }}
        .dashboard-hero h2 {{
          font-size: 1.85rem; line-height: 1.18; margin: 0 0 10px;
          max-width: 560px; color: #171044;
        }}
        .dashboard-hero p {{ max-width: 530px; color: #5B4B86; line-height: 1.55; margin: 0; }}
        .hero-kpis {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 22px; max-width: 600px; }}
        .mini-stat {{
          padding: 10px 13px; border-radius: 12px; background: rgba(255,255,255,.78);
          border: 1px solid rgba(168,85,247,.14); min-width: 124px;
        }}
        .mini-stat b {{ display: block; font-family: Poppins, Inter, sans-serif; font-size: 1.05rem; color: #171044; }}
        .mini-stat span {{ color: var(--muted); font-size: .72rem; font-weight: 700; }}
        .brand-mark {{
          width: 42px; height: 42px; border-radius: 12px; display: inline-flex; align-items: center;
          justify-content: center; background: linear-gradient(135deg, var(--pink), var(--accent));
          color: white; font-weight: 800; box-shadow: 0 8px 20px rgba(168,85,247,.28);
        }}
        .pill {{
          display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 99px;
          font-size: .72rem; font-weight: 700;
        }}
        .progress {{ width: 100%; height: 7px; background: #F3E8FF; border-radius: 99px; overflow: hidden; }}
        .progress span {{ display: block; height: 100%; border-radius: 99px; }}
        .muted {{ color: var(--muted); font-size: .86rem; }}
        .topbar {{
          display: flex; align-items: center; justify-content: space-between; gap: 12px;
          background: #fff; border: 1px solid var(--border); border-radius: 12px; padding: 12px 16px;
          margin-bottom: 18px;
        }}
        .task {{
          border: 1px solid var(--border); border-left-width: 4px; background: #fff;
          border-radius: 10px; padding: 13px 14px; margin-bottom: 10px;
        }}
        .avatar {{
          width: 42px; height: 42px; border-radius: 50%; display: inline-flex; align-items: center;
          justify-content: center; color: #fff; font-weight: 800; flex-shrink: 0;
        }}
        .calendar-cell {{
          min-height: 96px; background: #fff; border: 1px solid var(--border); border-radius: 10px;
          padding: 9px; font-size: .78rem;
        }}
        .event-dot {{ display: block; border-radius: 7px; color: #fff; padding: 3px 6px; margin-top: 6px; font-size: .68rem; font-weight: 700; }}
        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] {{
          border-radius: 10px;
          padding: 8px 10px;
          transition: background .15s ease, color .15s ease;
        }}
        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {{
          background: var(--sidebar-active) !important;
          border: 1px solid var(--border);
        }}
        [data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p {{
          color: var(--sidebar-active-text) !important;
          font-weight: 800 !important;
        }}
        .sidebar-logout .stButton > button {{
          background: #EF4444 !important;
          border: 1px solid rgba(255,255,255,0.18) !important;
          color: #FFFFFF !important;
          font-weight: 700 !important;
        }}
        .sidebar-logout .stButton > button:hover {{
          background: #DC2626 !important;
          color: #FFFFFF !important;
        }}
        .calendar-cell-empty {{
          min-height: 96px; background: rgba(243,244,246,.55); border: 1px dashed var(--border);
          border-radius: 10px;
        }}
        @media (max-width: 760px) {{
          .block-container {{ padding-left: 1rem; padding-right: 1rem; }}
          .soft-card {{ padding: 18px; }}
          .dashboard-hero {{ padding: 20px; min-height: 260px; }}
          .calendar-cell {{ min-height: 72px; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_login_css() -> None:
    st.markdown(
        """
        <style>
        /* ── Login: fundo galáxia ───────────────────────────── */
        .login-bg {
          position: fixed;
          inset: 0;
          z-index: 0;
          pointer-events: none;
          background:
            radial-gradient(circle at 18% 20%, rgba(56,189,248,.24), transparent 28%),
            radial-gradient(circle at 82% 72%, rgba(124,58,237,.42), transparent 36%),
            radial-gradient(circle at 55% 45%, rgba(236,72,153,.12), transparent 40%),
            linear-gradient(135deg, #0B1224 0%, #1E1B4B 42%, #312E81 68%, #3B1D5F 100%);
        }
        .login-bg::before {
          content: "";
          position: absolute;
          inset: 0;
          background-image:
            radial-gradient(circle, rgba(255,255,255,.75) 0 1px, transparent 1.6px),
            radial-gradient(circle, rgba(56,189,248,.4) 0 1px, transparent 1.7px);
          background-size: 92px 92px, 138px 138px;
          background-position: 12px 18px, 64px 38px;
          opacity: .34;
        }
        .login-cosmos {
          position: fixed;
          z-index: 0;
          pointer-events: none;
          right: -4vw;
          bottom: -5vh;
          width: min(46vw, 680px);
          opacity: .78;
          filter: drop-shadow(0 24px 48px rgba(15,23,42,.28));
        }

        /* ── Login: container e grid ──────────────────────── */
        .stApp:has(.login-bg) .block-container {
          max-width: 1280px;
          padding: clamp(0.85rem, 2.2vh, 1.6rem) clamp(1.25rem, 3.5vw, 2.75rem) 0.85rem;
          min-height: auto;
        }
        .stApp:has(.login-bg) [data-testid="stAppViewContainer"] > .main {
          overflow-x: hidden;
        }
        .stApp:has(.login-bg) [data-testid="stMainBlockContainer"] {
          padding-bottom: 0.5rem;
        }
        div[data-testid="stHorizontalBlock"]:has(.login-copy-anchor) {
          align-items: stretch;
          gap: clamp(1.25rem, 3vw, 2.75rem);
        }
        .login-copy-anchor,
        .login-panel-anchor {
          display: none !important;
        }

        /* ── Login: coluna esquerda (apresentação) ────────── */
        div[data-testid="column"]:has(.login-copy-anchor) {
          display: flex;
          align-items: center;
          padding-right: 0.5rem !important;
        }
        .login-copy {
          position: relative;
          z-index: 1;
          width: 100%;
          max-width: 560px;
          padding: 0.25rem 0;
        }
        .login-brand {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: clamp(1.25rem, 2.5vh, 1.75rem);
        }
        .login-brand-name {
          font-family: Poppins, Inter, sans-serif;
          font-size: 1.3rem;
          font-weight: 800;
          color: #FFFFFF;
          letter-spacing: -0.01em;
        }
        .login-brand-name span { color: #38BDF8; }
        .login-headline {
          font-family: Poppins, Inter, sans-serif;
          font-size: clamp(2.35rem, 3.6vw, 3.35rem);
          line-height: 1.1;
          font-weight: 800;
          color: #FFFFFF;
          margin: 0 0 0.75rem;
          letter-spacing: -0.025em;
          text-shadow: 0 2px 28px rgba(15, 23, 42, 0.45);
        }
        .login-headline-accent {
          background: linear-gradient(90deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
          text-shadow: none;
        }
        .login-subcopy {
          font-size: clamp(0.95rem, 1.1vw, 1.05rem);
          color: #E8EEFF;
          max-width: 480px;
          line-height: 1.65;
          margin: 0;
        }
        .benefit-grid {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 10px;
          margin-top: clamp(1.25rem, 2.5vh, 1.75rem);
          max-width: 520px;
        }
        .benefit-card {
          padding: 12px 10px;
          border-radius: 14px;
          background: rgba(255,255,255,0.1);
          border: 1px solid rgba(255,255,255,0.22);
          box-shadow: 0 12px 32px rgba(15,23,42,0.22);
          backdrop-filter: blur(14px);
          text-align: center;
          transition: border-color .2s ease, transform .2s ease;
        }
        .benefit-card:hover {
          border-color: rgba(56,189,248,0.35);
          transform: translateY(-1px);
        }
        .benefit-card .benefit-icon {
          margin: 0 auto 8px;
          width: 34px;
          height: 34px;
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, #4A5FE7 0%, #A855F7 100%);
          border: 1px solid rgba(255,255,255,0.2);
          box-shadow: 0 8px 18px rgba(76,29,149,0.28);
          font-size: 0.92rem;
        }
        .benefit-card strong {
          display: block;
          color: #FFFFFF;
          font-family: Poppins, Inter, sans-serif;
          font-size: 0.82rem;
          font-weight: 700;
          margin-bottom: 2px;
        }
        .benefit-card span {
          color: #DDE4FF;
          font-size: 0.72rem;
          line-height: 1.35;
          display: block;
        }

        /* ── Login: coluna direita (painel glass) ─────────── */
        div[data-testid="column"]:has(.login-panel-anchor) {
          display: flex;
          justify-content: flex-end;
          align-items: center;
          padding-top: 0 !important;
          padding-left: 0.5rem !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) > div[data-testid="stVerticalBlock"] {
          width: 100%;
          max-width: 400px;
          margin-left: auto;
          margin-right: 0;
          background: rgba(15, 23, 42, 0.42);
          border: 1px solid rgba(255,255,255,0.18);
          border-radius: 18px;
          padding: 18px 22px 16px;
          box-shadow:
            0 24px 64px rgba(15,23,42,0.38),
            inset 0 1px 0 rgba(255,255,255,0.08);
          backdrop-filter: blur(20px);
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stVerticalBlock"] {
          gap: 0.35rem !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) .stElementContainer {
          margin-bottom: 0 !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stMarkdown"] {
          margin-bottom: 0 !important;
        }

        /* ── Login: formulário ────────────────────────────── */
        .login-form-header h1 {
          color: #FFFFFF;
          font-family: Poppins, Inter, sans-serif;
          font-size: 1.3rem;
          font-weight: 700;
          line-height: 1.2;
          margin: 0 0 2px;
          letter-spacing: -0.01em;
        }
        .login-form-header p {
          color: #E2E8FF;
          font-size: 0.84rem;
          line-height: 1.4;
          margin: 0 0 8px;
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] {
          background: transparent !important;
          border: none !important;
          box-shadow: none !important;
          padding: 0 !important;
          margin-bottom: 0 !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] button p {
          color: #C7D2FE !important;
          font-size: 0.88rem !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] [aria-selected="true"] {
          border-bottom: 2px solid #38BDF8 !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] [aria-selected="true"] p {
          color: #38BDF8 !important;
          font-weight: 700 !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTextInput"] {
          margin-bottom: 0 !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTextInput"] label {
          color: #E8EEFF !important;
          font-size: 0.8rem !important;
          font-weight: 600 !important;
          margin-bottom: 0.12rem !important;
          padding-bottom: 0 !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTextInput"] input {
          background: rgba(255,255,255,0.96) !important;
          color: #1E1B4B !important;
          border: 1px solid rgba(255,255,255,0.28) !important;
          border-radius: 10px !important;
          min-height: 2.45rem;
          font-size: 0.9rem !important;
          box-shadow: 0 2px 8px rgba(15,23,42,0.08);
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTextInput"] input::placeholder {
          color: rgba(30,27,75,0.45) !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTextInput"] input:focus {
          border-color: rgba(56,189,248,0.65) !important;
          box-shadow: 0 0 0 3px rgba(56,189,248,0.18) !important;
        }
        .login-actions-row {
          margin: 0.1rem 0 0.2rem;
        }
        .login-actions-row [data-testid="stCheckbox"] {
          margin: 0 !important;
        }
        .login-actions-row [data-testid="stCheckbox"] label,
        .login-actions-row [data-testid="stCheckbox"] label p,
        .login-actions-row [data-testid="stCheckbox"] label span {
          color: #E2E8FF !important;
          font-size: 0.78rem !important;
        }
        .login-forgot-link-text {
          display: block;
          text-align: right;
          color: rgba(199, 210, 254, 0.75);
          font-size: 0.76rem;
          font-weight: 500;
          text-decoration: none;
          line-height: 1.4;
          letter-spacing: 0.01em;
        }
        .login-forgot-link-text:hover {
          color: #E2E8FF;
          text-decoration: underline;
          text-underline-offset: 2px;
        }
        .login-forgot-hint {
          color: rgba(199, 210, 254, 0.72);
          font-size: 0.74rem;
          line-height: 1.35;
          margin: 0 0 0.15rem;
          text-align: right;
        }
        .login-submit-gap {
          margin-top: 0.15rem;
        }
        .login-submit-gap .stButton {
          margin: 0 !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) .button-scope-save .stButton > button,
        div[data-testid="column"]:has(.login-panel-anchor) .stButton > button[kind="primary"] {
          min-height: 2.5rem !important;
          background: linear-gradient(90deg, #4A5FE7 0%, #7B3FF2 55%, #A855F7 100%) !important;
          border: 1px solid rgba(255,255,255,0.22) !important;
          color: #FFFFFF !important;
          font-weight: 700 !important;
          font-size: 0.9rem !important;
          border-radius: 10px !important;
          box-shadow: 0 8px 22px rgba(76,29,149,0.28) !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) .button-scope-save .stButton > button:hover,
        div[data-testid="column"]:has(.login-panel-anchor) .stButton > button[kind="primary"]:hover {
          background: linear-gradient(90deg, #5B6EFA 0%, #8B5CF6 55%, #C084FC 100%) !important;
          transform: translateY(-1px);
        }

        /* ── Login: responsivo ─────────────────────────────── */
        @media (min-width: 1100px) {
          .stApp:has(.login-bg) .block-container { max-width: 1320px; }
          .benefit-grid { max-width: 540px; }
        }
        @media (max-width: 960px) {
          div[data-testid="stHorizontalBlock"]:has(.login-copy-anchor) {
            flex-direction: column;
            gap: 1.25rem;
          }
          div[data-testid="column"]:has(.login-copy-anchor),
          div[data-testid="column"]:has(.login-panel-anchor) {
            padding-left: 0 !important;
            padding-right: 0 !important;
          }
          div[data-testid="column"]:has(.login-panel-anchor) {
            justify-content: center;
          }
          div[data-testid="column"]:has(.login-panel-anchor) > div[data-testid="stVerticalBlock"] {
            max-width: 100%;
            margin-left: auto;
            margin-right: auto;
          }
          .login-copy { max-width: 100%; }
          .benefit-grid {
            grid-template-columns: repeat(3, minmax(0, 1fr));
            max-width: 100%;
          }
          .login-cosmos {
            width: min(70vw, 520px);
            right: -18vw;
            bottom: -8vh;
            opacity: .55;
          }
        }
        @media (max-width: 640px) {
          .benefit-grid { grid-template-columns: 1fr; }
          .login-headline { font-size: 1.9rem; }
          .login-cosmos { opacity: .4; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_title(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="topbar">
          <div>
            <h1>{title}</h1>
            <div class="muted">{subtitle}</div>
          </div>
          <span class="pill" style="background:var(--sidebar-active);color:var(--accent);">EduTrack AI</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
