"""
NutriAI Settings Page.

Application settings including theme, units, notifications, and data management.
"""

from __future__ import annotations

from typing import Any, Dict

import streamlit as st

from frontend.utils.helpers import get, set_key
from frontend.utils.constants import DEFAULT_SETTINGS
from frontend.components.cards import glass_card, info_card
from frontend.components.navbar import render_header
from frontend.components.forms import settings_form


def show() -> None:
    """Render the settings page."""
    render_header("Settings")

    tab1, tab2 = st.tabs(["⚙ Preferences", "🔧 Advanced"])

    with tab1:
        _render_preferences()

    with tab2:
        _render_advanced_settings()


def _render_preferences() -> None:
    """Render the preferences settings tab."""
    current = {key: get(key, default) for key, default in DEFAULT_SETTINGS.items()}

    settings_form(current_settings=current, on_save=_handle_settings_save)


def _handle_settings_save(updated: Dict[str, Any]) -> None:
    """Handle settings form save.

    Args:
        updated: Updated settings dict.
    """
    for key, value in updated.items():
        set_key(key, value)

    st.success("✅ Settings saved successfully!")
    st.rerun()


def _render_advanced_settings() -> None:
    """Render advanced settings and data management options."""
    st.markdown("### Data Management")

    col1, col2 = st.columns(2)

    with col1:
        glass_card(
            "🗑️ Clear Local Data",
            """
            <p style="color: #D1D5DB; font-size: 0.85rem;">
                Remove all locally stored profile data, cached diet plans, and
                session data. This will not affect data stored on the server.
            </p>
            """,
        )
        if st.button("Clear Local Data", type="secondary", use_container_width=True):
            _clear_local_data()

    with col2:
        glass_card(
            "🔄 Reset Application",
            """
            <p style="color: #D1D5DB; font-size: 0.85rem;">
                Reset all settings to their default values. This will restore
                the default theme, units, and notification preferences.
            </p>
            """,
        )
        if st.button("Reset to Defaults", type="secondary", use_container_width=True):
            _reset_to_defaults()

    # About section
    st.markdown("### About")
    glass_card(
        "NutriAI — AI-Based Personalized Diet Planning",
        f"""
        <div style="font-size: 0.85rem; color: #D1D5DB;">
            <p><strong>Version:</strong> 2.0.0</p>
            <p><strong>Framework:</strong> Streamlit</p>
            <p><strong>Backend:</strong> FastAPI + MongoDB</p>
            <p><strong>Design:</strong> Dark Healthcare Theme with Glassmorphism</p>
            <p style="margin-top: 0.75rem; color: #9CA3AF;">
                NutriAI uses AI to generate personalized diet plans based on your
                health profile, goals, and preferences. All calculations comply
                with WHO and standard nutritional guidelines.
            </p>
        </div>
        """,
    )


def _clear_local_data() -> None:
    """Clear all locally stored session data."""
    keys_to_clear = ["saved_profile", "last_diet_plan", "profile_loaded"]
    for key in keys_to_clear:
        set_key(key, None)

    st.cache_data.clear()
    st.success("✅ Local data cleared successfully!")
    st.rerun()


def _reset_to_defaults() -> None:
    """Reset settings to their default values."""
    for key, value in DEFAULT_SETTINGS.items():
        set_key(key, value)

    st.success("✅ Settings reset to defaults!")
    st.rerun()