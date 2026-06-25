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
        .social-login-row {{
          display: flex; justify-content: center; align-items: center;
        }}
        .social-login-row .stButton {{
          width: 220px; max-width: 100%;
        }}
        .social-login-row .stButton > button {{
          background: rgba(255,255,255,0.08) !important;
          border-color: rgba(255,255,255,0.15) !important;
          color: #FFFFFF !important;
        }}
        .social-login-row .stButton > button:hover {{
          background: rgba(255,255,255,0.15) !important;
          color: #FFFFFF !important;
        }}
        .card {{
          background: #fff; border: 1px solid var(--border); border-radius: 12px;
          padding: 18px; box-shadow: 0 1px 4px rgba(0,0,0,.04); height: 100%;
        }}
        .soft-card {{
          background: rgba(255,255,255,0.13); border: 1px solid rgba(255,255,255,0.24);
          border-radius: 22px; padding: 28px; box-shadow: 0 22px 70px rgba(15,23,42,0.34);
          backdrop-filter: blur(16px);
        }}
        .login-bg {{
          position: fixed; inset: 0; z-index: 0; pointer-events: none;
          background:
            radial-gradient(circle at 20% 18%, rgba(56,189,248,.22), transparent 24%),
            radial-gradient(circle at 78% 70%, rgba(76,29,149,.58), transparent 34%),
            linear-gradient(135deg, #0F172A 0%, #312E81 46%, #1E1B4B 72%, #3B1D5F 100%);
        }}
        .login-bg::before {{
          content: ""; position: absolute; inset: 0;
          background-image:
            radial-gradient(circle, rgba(255,255,255,.82) 0 1px, transparent 1.7px),
            radial-gradient(circle, rgba(56,189,248,.48) 0 1px, transparent 1.8px);
          background-size: 96px 96px, 142px 142px;
          background-position: 10px 20px, 70px 42px;
          opacity: .38;
        }}
        .login-cosmos {{
          position: fixed; z-index: 0; pointer-events: none; right: -60px; bottom: -46px;
          width: min(58vw, 900px); opacity: .94; filter: drop-shadow(0 28px 48px rgba(15,23,42,.34));
        }}
        .login-copy {{
          position: relative; z-index: 1; min-height: 78vh; display: flex;
          flex-direction: column; justify-content: center; padding: 34px 0 10px;
        }}
        .login-panel {{ position: relative; z-index: 1; padding-top: 34px; }}
        .benefit-grid {{
          display: flex; align-items: stretch; gap: 12px; flex-wrap: wrap;
          max-width: 680px; margin-top: 34px;
        }}
        .benefit-card {{
          flex: 1 1 160px; min-width: 152px;
          padding: 15px 16px; border-radius: 18px;
          background: rgba(255,255,255,0.13);
          border: 1px solid rgba(255,255,255,0.24);
          box-shadow: 0 16px 36px rgba(15,23,42,0.24);
          backdrop-filter: blur(16px);
          text-align: center;
        }}
        .benefit-card .benefit-icon {{
          margin: 0 auto 12px auto;
          width: 42px; height: 42px; border-radius: 14px;
          display: flex; align-items: center; justify-content: center;
          background: linear-gradient(135deg, #4A5FE7 0%, #7B3FF2 100%);
          color: #FFFFFF;
          border: 1px solid rgba(255,255,255,0.24);
          box-shadow: 0 10px 24px rgba(76,29,149,0.25);
          font-size: 1.05rem;
        }}
        .benefit-card strong {{
          display: block; color: #F8FAFC; font-family: Poppins, Inter, sans-serif;
          font-size: .98rem; margin-bottom: 3px; text-align: center;
        }}
        .benefit-card span {{ color: #D7DDFB; font-size: .82rem; line-height: 1.35; text-align: center; display: block; }}
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
          .login-cosmos {{ width: 920px; right: -540px; bottom: -120px; opacity: .72; }}
          .login-copy {{ min-height: auto; padding-top: 18px; }}
          .login-panel {{ padding-top: 8px; }}
          .benefit-grid {{ gap: 10px; margin-top: 24px; }}
          .benefit-card {{ flex-basis: 100%; }}
          .social-login-row {{ justify-content: center; }}
          .social-login-row .stButton {{ width: 100%; max-width: 220px; }}
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
        div[data-testid="column"]:has(.login-panel-anchor) {
          padding-top: 34px;
        }
        div[data-testid="column"]:has(.login-panel-anchor) > div[data-testid="stVerticalBlock"] {
          background: rgba(255,255,255,0.13);
          border: 1px solid rgba(255,255,255,0.24);
          border-radius: 22px;
          padding: 24px 28px 28px;
          box-shadow: 0 22px 70px rgba(15,23,42,0.34);
          backdrop-filter: blur(16px);
        }
        .login-panel-anchor {
          display: none !important;
        }
        [data-testid="stTextInput"] label,
        [data-testid="stTabs"] button p,
        .stCaptionContainer {
          color: #D7DDFB !important;
        }
        [data-testid="stCheckbox"] label,
        [data-testid="stCheckbox"] label p,
        [data-testid="stCheckbox"] label span,
        [data-testid="stCheckbox"] p {
          color: #D7DDFB !important;
        }
        [data-testid="stTextInput"] input {
          background: rgba(255,255,255,0.94) !important;
          color: #241B33 !important;
          border: 1px solid rgba(255,255,255,0.32) !important;
        }
        [data-testid="stTextInput"] input::placeholder {
          color: rgba(36,27,51,.58) !important;
        }
        [data-testid="stTabs"] [aria-selected="true"] p {
          color: #38BDF8 !important;
          font-weight: 800 !important;
        }
        [data-testid="stTabs"] {
          background: transparent !important;
          border: none !important;
          box-shadow: none !important;
          padding: 0 !important;
        }
        .social-login-row .stButton > button,
        div[data-testid="column"]:has(.social-login-row) div[data-testid="stButton"] > button {
          width: 100%;
          background: rgba(255,255,255,0.08) !important;
          border: 1px solid rgba(255,255,255,0.15) !important;
          color: #FFFFFF !important;
          backdrop-filter: blur(12px);
          border-radius: 12px !important;
        }
        .social-login-row .stButton > button:hover,
        div[data-testid="column"]:has(.social-login-row) div[data-testid="stButton"] > button:hover {
          background: rgba(255,255,255,0.15) !important;
          color: #FFFFFF !important;
        }
        .stButton > button[kind="primary"] {
          background: linear-gradient(90deg, #4A5FE7 0%, #7B3FF2 100%) !important;
          border: 1px solid rgba(255,255,255,0.26) !important;
          color: #F8FAFC !important;
        }
        .stButton > button[kind="primary"]:hover {
          background: linear-gradient(90deg, #5B6EFA 0%, #8B5CF6 100%) !important;
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
