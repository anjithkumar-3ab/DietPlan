"""
NutriAI Sidebar Component.

Professional navigation sidebar with health profile summary and app branding.
"""

from __future__ import annotations

import streamlit as st
from typing import Optional, Dict, Any

from frontend.utils.constants import APP_NAME, APP_TAGLINE, PAGES, APP_ICON
from frontend.utils.helpers import get, is_profile_complete


def render_sidebar() -> str:
    """Render the navigation sidebar.

    Returns:
        The selected page label (e.g. "🏠 Dashboard").
    """
    with st.sidebar:
        # ── Branding ──
        st.markdown(
            f"""
            <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
                <div style="font-size: 2.5rem;">{APP_ICON}</div>
                <div style="font-weight: 700; font-size: 1.3rem; color: #F5F5F5;">
                    {APP_NAME}
                </div>
                <div style="font-size: 0.7rem; color: #9CA3AF; margin-top: 0.2rem;">
                    {APP_TAGLINE}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # ── Navigation ──
        page_labels = list(PAGES.keys())
        current_page = get("page", page_labels[0])

        selected = st.radio(
            "Navigation",
            options=page_labels,
            index=page_labels.index(current_page) if current_page in page_labels else 0,
            label_visibility="collapsed",
            key="nav_radio",
        )

        # Update session state
        if selected != current_page:
            st.session_state["page"] = selected
            st.rerun()

        st.divider()

        # ── Profile Summary ──
        _render_profile_summary()

        # ── Version ──
        st.markdown(
            """
            <div style="position: fixed; bottom: 1rem; text-align: center; width: 200px;
                        font-size: 0.65rem; color: #6B7280;">
                NutriAI v2.0.0
            </div>
            """,
            unsafe_allow_html=True,
        )

    return selected


def _render_profile_summary() -> None:
    """Render a compact profile summary card in the sidebar."""
    profile = get("saved_profile")

    if not profile or not is_profile_complete(profile):
        st.markdown(
            """
            <div style="padding: 0.75rem; border-radius: 12px;
                        border: 1px solid rgba(255,255,255,0.08);
                        background: rgba(22, 27, 34, 0.5);">
                <div style="font-size: 0.7rem; color: #9CA3AF; margin-bottom: 0.3rem;">
                    PROFILE
                </div>
                <div style="font-size: 0.8rem; color: #6B7280;">
                    No profile saved yet.
                </div>
                <div style="margin-top: 0.4rem;">
                    <a href="#" onclick="alert('Go to Health Profile to create one');"
                       style="font-size: 0.75rem; color: #66BB6A !important;">
                        Create Profile →
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    name = profile.get("full_name", "User")
    age = profile.get("age", "-")
    weight = profile.get("weight", "-")
    goal = profile.get("goal", "-")

    st.markdown(
        f"""
        <div style="padding: 0.75rem; border-radius: 12px;
                    border: 1px solid rgba(46, 125, 50, 0.2);
                    background: rgba(22, 27, 34, 0.5);">
            <div style="font-size: 0.7rem; color: #9CA3AF; margin-bottom: 0.3rem;">
                PROFILE
            </div>
            <div style="font-weight: 600; font-size: 0.9rem; color: #F5F5F5;">
                {name}
            </div>
            <div style="font-size: 0.75rem; color: #D1D5DB; margin-top: 0.3rem;">
                Age {age} · {weight} kg
            </div>
            <div style="font-size: 0.7rem; color: #66BB6A; margin-top: 0.2rem;">
                🎯 {goal}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )