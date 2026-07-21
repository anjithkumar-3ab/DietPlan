"""
NutriAI Top Navigation Bar Component.

Clean header with app branding, page title, and API status indicator.
"""

from __future__ import annotations

import streamlit as st

from frontend.utils.constants import APP_NAME, APP_ICON
from frontend.utils.helpers import get
from frontend.services.api import api_available


def render_header(page_title: str = "") -> None:
    """Render the top navigation bar with branding and status.

    Args:
        page_title: Optional page-specific title to display.
    """
    api_status = _get_api_status_indicator()

    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center;
                    padding: 0.5rem 0; margin-bottom: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <span style="font-size: 1.8rem;">{APP_ICON}</span>
                <div>
                    <span style="font-weight: 700; font-size: 1.1rem; color: #F5F5F5;">
                        {APP_NAME}
                    </span>
                    {f'<span style="color: #9CA3AF; font-size: 0.85rem; margin-left: 0.5rem;">| {page_title}</span>'
                     if page_title else ''}
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                {api_status}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "<hr style='margin: 0 0 1rem 0; border-color: rgba(255,255,255,0.06);'>",
        unsafe_allow_html=True,
    )


def _get_api_status_indicator() -> str:
    """Return an HTML indicator for backend API status.

    Returns:
        HTML string with coloured status dot and label.
    """
    try:
        available = api_available()
    except Exception:
        available = False

    if available:
        return (
            '<span style="display: flex; align-items: center; gap: 0.35rem; '
            'font-size: 0.75rem; color: #9CA3AF;">'
            '<span style="width: 8px; height: 8px; border-radius: 50%; '
            'background: #27ae60; display: inline-block;"></span>'
            'API Connected</span>'
        )
    return (
        '<span style="display: flex; align-items: center; gap: 0.35rem; '
        'font-size: 0.75rem; color: #9CA3AF;">'
        '<span style="width: 8px; height: 8px; border-radius: 50%; '
        'background: #e74c3c; display: inline-block;"></span>'
        'API Offline</span>'
    )