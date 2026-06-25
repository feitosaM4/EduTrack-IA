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
        .stApp:has(.login-bg) {
          color: #FFFFFF !important;
          background: transparent !important;
        }
        .stApp:has(.login-bg) label,
        .stApp:has(.login-bg) label p,
        .stApp:has(.login-bg) label span,
        .stApp:has(.login-bg) [data-testid="stWidgetLabel"],
        .stApp:has(.login-bg) [data-testid="stWidgetLabel"] p {
          color: #FFFFFF !important;
          -webkit-text-fill-color: #FFFFFF !important;
        }
        .stApp:has(.login-bg) [data-testid="stTabs"] button,
        .stApp:has(.login-bg) [data-testid="stTabs"] button p,
        .stApp:has(.login-bg) [data-testid="stTabs"] button [data-testid="stMarkdownContainer"] p {
          color: #FFFFFF !important;
          -webkit-text-fill-color: #FFFFFF !important;
        }
        .stApp:has(.login-bg) [data-testid="stTabs"] [aria-selected="true"] p {
          font-weight: 700 !important;
          text-shadow: 0 0 16px rgba(249, 168, 212, 0.4);
        }
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
        .stApp:has(.login-bg) h1,
        .stApp:has(.login-bg) h2,
        .stApp:has(.login-bg) h3 {{
          color: #FFFFFF !important;
        }}
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
        .stApp:has(.login-bg) .login-headline,
        .stApp:has(.login-bg) .login-headline-main {
          color: #FFFFFF !important;
        }
        .login-headline {
          font-family: Poppins, Inter, sans-serif;
          font-size: clamp(2.35rem, 3.6vw, 3.35rem);
          line-height: 1.1;
          font-weight: 800;
          margin: 0 0 0.75rem;
          letter-spacing: -0.025em;
          text-shadow: 0 2px 32px rgba(15, 23, 42, 0.5);
        }
        .login-headline-main {
          color: #FFFFFF !important;
        }
        .login-headline-accent {
          background: linear-gradient(90deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent !important;
        }
        .login-subcopy {
          font-size: clamp(0.95rem, 1.1vw, 1.05rem);
          color: #F1F5FF;
          max-width: 480px;
          line-height: 1.6;
          margin: 0;
        }
        .benefit-grid {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 14px;
          margin-top: clamp(1.25rem, 2.5vh, 1.75rem);
          max-width: 640px;
        }
        .benefit-card {
          padding: 22px 16px;
          border-radius: 16px;
          background: rgba(255,255,255,0.1);
          border: 1px solid rgba(255,255,255,0.22);
          box-shadow: 0 12px 32px rgba(15,23,42,0.22);
          backdrop-filter: blur(14px);
          text-align: center;
          transition: border-color .2s ease, transform .2s ease;
          min-height: 132px;
        }
        .benefit-card:hover {
          border-color: rgba(56,189,248,0.35);
          transform: translateY(-1px);
        }
        .benefit-card .benefit-icon {
          margin: 0 auto 12px;
          width: 48px;
          height: 48px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, #4A5FE7 0%, #A855F7 100%);
          border: 1px solid rgba(255,255,255,0.2);
          box-shadow: 0 8px 18px rgba(76,29,149,0.28);
          color: #FFFFFF;
        }
        .benefit-card .benefit-icon svg {
          width: 24px;
          height: 24px;
          display: block;
          fill: currentColor;
        }
        .benefit-card strong {
          display: block;
          color: #FFFFFF;
          font-family: Poppins, Inter, sans-serif;
          font-size: 1rem;
          font-weight: 700;
          margin-bottom: 5px;
        }
        .benefit-card span {
          color: #F1F5FF;
          font-size: 0.84rem;
          line-height: 1.4;
          display: block;
        }

        /* ── Login: tokens de contraste ───────────────────── */
        .stApp:has(.login-bg) {
          --login-title: #FFFFFF;
          --login-muted: #D7D9E5;
          --login-label: #E6E8F2;
          --login-link: #A5B4FC;
          --login-link-hover: #C7D2FE;
        }
        .stApp:has(.login-bg) .main,
        .stApp:has(.login-bg) [data-testid="stAppViewContainer"] {
          color: #D7D9E5;
        }
        .stApp:has(.login-bg) h1,
        .stApp:has(.login-bg) h2,
        .stApp:has(.login-bg) h3 {
          color: #FFFFFF !important;
        }
        .stApp:has(.login-bg) .login-headline-accent {
          color: transparent !important;
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
          max-width: 392px;
          margin-left: auto;
          margin-right: 0;
          background: linear-gradient(
            160deg,
            rgba(255, 255, 255, 0.14) 0%,
            rgba(255, 255, 255, 0.06) 55%,
            rgba(15, 23, 42, 0.28) 100%
          );
          border: 1px solid rgba(255, 255, 255, 0.26);
          border-radius: 16px;
          padding: 16px 20px 14px;
          box-shadow:
            0 20px 50px rgba(15, 23, 42, 0.34),
            inset 0 1px 0 rgba(255, 255, 255, 0.14);
          backdrop-filter: blur(18px);
          -webkit-backdrop-filter: blur(18px);
          gap: 0.2rem !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) .stElementContainer {
          margin-bottom: 0 !important;
          padding-bottom: 0 !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stMarkdown"] {
          margin-bottom: 0 !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabContent"] {
          padding-top: 0.3rem !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabContent"] > div[data-testid="stVerticalBlock"] {
          gap: 0.15rem !important;
        }

        /* ── Login: formulário ────────────────────────────── */
        .stApp:has(.login-bg) .login-form-header h1 {
          color: #FFFFFF !important;
        }
        .login-form-header h1 {
          font-family: Poppins, Inter, sans-serif;
          font-size: 1.25rem;
          font-weight: 700;
          line-height: 1.2;
          margin: 0 0 2px;
          letter-spacing: -0.01em;
          color: #FFFFFF;
        }
        .login-form-header p {
          color: #F1F5FF;
          font-size: 0.83rem;
          line-height: 1.35;
          margin: 0 0 6px;
        }

        /* Abas — branco sólido (sem gradiente que escurece em alguns browsers) */
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] {
          background: transparent !important;
          border: none !important;
          box-shadow: none !important;
          padding: 0 !important;
          margin-bottom: 0 !important;
        }
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] button,
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] [data-baseweb="tab"],
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] button * {
          background: transparent !important;
          color: #FFFFFF !important;
          -webkit-text-fill-color: #FFFFFF !important;
          opacity: 1 !important;
        }
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] button:not([aria-selected="true"]),
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] button:not([aria-selected="true"]) p,
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] button:not([aria-selected="true"]) [data-testid="stMarkdownContainer"] p,
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] button[aria-selected="false"] p {
          color: #FFFFFF !important;
          -webkit-text-fill-color: #FFFFFF !important;
          font-size: 0.92rem !important;
          font-weight: 500 !important;
          opacity: 0.92 !important;
        }
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] [aria-selected="true"] {
          border-bottom: 2px solid #F9A8D4 !important;
        }
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] [aria-selected="true"],
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] [aria-selected="true"] p,
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTabs"] [aria-selected="true"] [data-testid="stMarkdownContainer"] p {
          color: #FFFFFF !important;
          -webkit-text-fill-color: #FFFFFF !important;
          background: none !important;
          font-size: 0.92rem !important;
          font-weight: 700 !important;
          opacity: 1 !important;
          text-shadow: 0 0 18px rgba(249, 168, 212, 0.45);
        }

        /* Labels E-mail / Senha — branco puro */
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) label,
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) label p,
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) label span,
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stWidgetLabel"],
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stWidgetLabel"] p,
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stWidgetLabel"] span,
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTextInput"] label,
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTextInput"] label p,
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTextInput"] label span,
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTextInput"] [data-testid="stWidgetLabel"],
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTextInput"] [data-testid="stWidgetLabel"] p {
          color: #FFFFFF !important;
          -webkit-text-fill-color: #FFFFFF !important;
          font-size: 0.82rem !important;
          font-weight: 600 !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTextInput"] {
          margin-bottom: 0 !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stTextInput"] label {
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
          margin: 0 !important;
          padding-bottom: 0 !important;
        }
        .login-actions-row [data-testid="stHorizontalBlock"] {
          margin-bottom: 0 !important;
        }
        .login-actions-row [data-testid="stCheckbox"] {
          margin: 0 !important;
          padding: 0 !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) .login-actions-row + div,
        div[data-testid="column"]:has(.login-panel-anchor) .login-actions-row ~ div:has(.login-submit-gap),
        div[data-testid="column"]:has(.login-panel-anchor) .login-submit-gap {
          margin-top: -0.55rem !important;
          padding-top: 0 !important;
        }
        .login-submit-gap {
          margin-top: -0.55rem !important;
          padding-top: 0 !important;
        }
        .login-submit-gap .stButton {
          margin: 0 !important;
          padding-top: 0 !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) .button-scope-save {
          margin-top: 0 !important;
          padding-top: 0 !important;
        }
        .stApp:has(.login-bg) .login-actions-row [data-testid="stCheckbox"] label,
        .stApp:has(.login-bg) .login-actions-row [data-testid="stCheckbox"] label p,
        .stApp:has(.login-bg) .login-actions-row [data-testid="stCheckbox"] label span,
        .stApp:has(.login-bg) .login-actions-row [data-testid="stCheckbox"] [data-testid="stMarkdownContainer"] p {
          color: #FFFFFF !important;
          -webkit-text-fill-color: #FFFFFF !important;
          font-size: 0.82rem !important;
        }
        .login-forgot-link-text {
          display: block;
          text-align: right;
          color: #E0E7FF !important;
          font-size: 0.84rem;
          font-weight: 500;
          text-decoration: none;
          line-height: 1.4;
          transition: color 0.15s ease;
        }
        .login-forgot-link-text:hover {
          color: #FFFFFF !important;
          text-decoration: underline;
          text-underline-offset: 2px;
        }
        .login-forgot-hint {
          color: #F1F5FF;
          font-size: 0.75rem;
          line-height: 1.35;
          margin: 0 0 -0.2rem;
          text-align: right;
        }

        /* Remove herança de cinza escuro do Streamlit */
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stCaptionContainer"],
        .stApp:has(.login-bg) div[data-testid="column"]:has(.login-panel-anchor) [data-testid="stCaptionContainer"] p {
          color: #F1F5FF !important;
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
          transition: transform 0.22s ease, box-shadow 0.22s ease, background 0.22s ease, filter 0.22s ease !important;
          cursor: pointer !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) .button-scope-save .stButton > button:hover,
        div[data-testid="column"]:has(.login-panel-anchor) .stButton > button[kind="primary"]:hover {
          background: linear-gradient(90deg, #6B7EF9 0%, #9B6FFA 50%, #C084FC 100%) !important;
          transform: translateY(-3px) scale(1.01) !important;
          box-shadow: 0 14px 32px rgba(124, 58, 237, 0.42) !important;
          filter: brightness(1.06) !important;
          border-color: rgba(255,255,255,0.35) !important;
          color: #FFFFFF !important;
        }
        div[data-testid="column"]:has(.login-panel-anchor) .button-scope-save .stButton > button:active,
        div[data-testid="column"]:has(.login-panel-anchor) .stButton > button[kind="primary"]:active {
          transform: translateY(-1px) scale(0.99) !important;
          box-shadow: 0 6px 16px rgba(76,29,149,0.32) !important;
          transition-duration: 0.1s !important;
        }

        /* ── Login: responsivo ─────────────────────────────── */
        @media (min-width: 1100px) {
          .stApp:has(.login-bg) .block-container { max-width: 1320px; }
          .benefit-grid { max-width: 660px; }
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
