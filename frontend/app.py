"""
NutriAI — AI-Based Personalized Diet Planning & Recommendation System.

Streamlit Frontend Entry Point.

Run with:
    streamlit run frontend/app.py

Design: Dark Healthcare Theme with Glassmorphism
Inspired by: Apple Health, Google Fit, Fitbit, MyFitnessPal
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, Optional

import streamlit as st

# Ensure frontend directory is on Python path for clean imports
_frontend_dir = Path(__file__).resolve().parent
if str(_frontend_dir) not in sys.path:
    sys.path.insert(0, str(_frontend_dir))

from frontend.utils.constants import APP_NAME, APP_ICON, PAGES, DEFAULT_PAGE
from frontend.utils.helpers import init_session_state, get
from frontend.utils.styles import inject_global_css
from frontend.components.sidebar import render_sidebar


# ---------------------------------------------------------------------------
# Page Configuration (must be the first Streamlit command)
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title=f"{APP_NAME} — AI Diet Planner",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Global CSS Injection
# ---------------------------------------------------------------------------

inject_global_css()


# ---------------------------------------------------------------------------
# Lazy-loaded Page Module Cache
# ---------------------------------------------------------------------------

_PAGE_MODULE_MAP: Dict[str, str] = {
    label: f"frontend.pages.{module}"
    for label, module in PAGES.items()
}


@st.cache_resource(ttl=3600)
def _get_page_module(module_name: str):
    """Cache page module imports to avoid repeated imports.

    Args:
        module_name: Fully qualified module path.

    Returns:
        Imported module.
    """
    return __import__(module_name, fromlist=["show"])


def _render_page(selected: str) -> None:
    """Dynamically import and render the selected page module.

    Args:
        selected: Sidebar navigation label (e.g. "🏠 Dashboard").
    """
    module_name = _PAGE_MODULE_MAP.get(selected)
    if module_name is None:
        st.error(f"Unknown page: {selected}")
        return

    try:
        page = _get_page_module(module_name)
        page.show()
    except Exception as exc:
        st.error(f"Failed to load page **{selected}**. Please try again.")
        st.exception(exc)


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------


def main() -> None:
    """Application entry point."""
    # Initialize all session state variables
    init_session_state()

    # Render sidebar navigation and get selected page
    selected_page = render_sidebar()

    # Render the selected page content
    _render_page(selected_page)


if __name__ == "__main__":
    main()