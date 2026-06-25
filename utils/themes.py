from __future__ import annotations

from typing import Any

THEMES: dict[str, dict[str, Any]] = {
    "rosa_lilas": {
        "label": "Rosa / Lilás padrão",
        "app_bg": "#F0EBF8",
        "card": "#FFFFFF",
        "border": "rgba(168, 85, 247, 0.18)",
        "text": "#1F2937",
        "muted": "#6B7280",
        "accent": "#A855F7",
        "pink": "#EC4899",
        "blue": "#6366F1",
        "gradient_start": "#4A5FE7",
        "gradient_end": "#7B3FF2",
        "sidebar_active": "#F3E8FF",
        "sidebar_active_text": "#7C3AED",
    },
    "azul_suave": {
        "label": "Azul suave",
        "app_bg": "#EEF4FF",
        "card": "#FFFFFF",
        "border": "rgba(59, 130, 246, 0.18)",
        "text": "#1E293B",
        "muted": "#64748B",
        "accent": "#3B82F6",
        "pink": "#60A5FA",
        "blue": "#2563EB",
        "gradient_start": "#3B82F6",
        "gradient_end": "#6366F1",
        "sidebar_active": "#DBEAFE",
        "sidebar_active_text": "#1D4ED8",
    },
    "roxo_moderno": {
        "label": "Roxo moderno",
        "app_bg": "#F3EEFF",
        "card": "#FFFFFF",
        "border": "rgba(124, 58, 237, 0.18)",
        "text": "#1F1B2E",
        "muted": "#6B7280",
        "accent": "#7C3AED",
        "pink": "#A855F7",
        "blue": "#8B5CF6",
        "gradient_start": "#7C3AED",
        "gradient_end": "#A855F7",
        "sidebar_active": "#EDE9FE",
        "sidebar_active_text": "#6D28D9",
    },
    "verde_menta": {
        "label": "Verde menta",
        "app_bg": "#ECFDF5",
        "card": "#FFFFFF",
        "border": "rgba(16, 185, 129, 0.18)",
        "text": "#134E4A",
        "muted": "#64748B",
        "accent": "#14B8A6",
        "pink": "#2DD4BF",
        "blue": "#0D9488",
        "gradient_start": "#14B8A6",
        "gradient_end": "#059669",
        "sidebar_active": "#D1FAE5",
        "sidebar_active_text": "#047857",
    },
    "claro_elegante": {
        "label": "Modo claro elegante",
        "app_bg": "#F8FAFC",
        "card": "#FFFFFF",
        "border": "rgba(148, 163, 184, 0.28)",
        "text": "#0F172A",
        "muted": "#64748B",
        "accent": "#475569",
        "pink": "#94A3B8",
        "blue": "#334155",
        "gradient_start": "#475569",
        "gradient_end": "#64748B",
        "sidebar_active": "#F1F5F9",
        "sidebar_active_text": "#334155",
    },
}

DEFAULT_THEME = "rosa_lilas"


def get_theme(theme_id: str | None) -> dict[str, Any]:
    return THEMES.get(theme_id or DEFAULT_THEME, THEMES[DEFAULT_THEME])


def theme_options() -> list[tuple[str, str]]:
    return [(meta["label"], theme_id) for theme_id, meta in THEMES.items()]
