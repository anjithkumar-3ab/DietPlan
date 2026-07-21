"""
NutriAI Health Profile Page.

Create and manage your health profile with personal info, measurements,
lifestyle choices, dietary restrictions, and daily habits.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import streamlit as st

from frontend.utils.helpers import get, set_key, is_profile_complete
from frontend.utils.validators import validate_profile_data
from frontend.components.forms import profile_form
from frontend.components.cards import glass_card, info_card
from frontend.components.navbar import render_header
from frontend.services.api import save_profile, api_available


def show() -> None:
    """Render the health profile page."""
    render_header("Health Profile")

    profile = get("saved_profile")
    has_profile = is_profile_complete(profile)

    # Check API availability
    api_ok = False
    try:
        api_ok = api_available()
    except Exception:
        pass

    if not api_ok:
        st.warning(
            "⚠️ Backend API is not reachable. Your profile data will be saved "
            "locally but not persisted to the server."
        )

    # Page layout
    col1, col2 = st.columns([2, 1])

    with col1:
        if has_profile:
            st.markdown(
                f"""
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3>Edit Your Health Profile</h3>
                    <span style="font-size: 0.8rem; color: #27ae60;">
                        ✓ Profile Saved
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown("### Create Your Health Profile")
            st.markdown(
                "<p style='color: #9CA3AF;'>Fill in the details below to get "
                "personalized diet recommendations.</p>",
                unsafe_allow_html=True,
            )

        # Render the profile form
        profile_form(
            existing_data=profile if has_profile else None,
            on_submit=_handle_profile_submit,
        )

    with col2:
        _render_profile_sidebar(profile, has_profile)


def _handle_profile_submit(form_data: Dict[str, Any]) -> None:
    """Handle profile form submission.

    Args:
        form_data: Validated form data dict.
    """
    # Validate
    errors = validate_profile_data(form_data)
    if errors:
        for error in errors:
            st.error(f"❌ {error}")
        return

    # Save locally first
    set_key("saved_profile", form_data)
    set_key("profile_loaded", True)
    st.success("✅ Profile saved locally!")

    # Try to persist to backend
    try:
        if api_available():
            result = save_profile(form_data)
            if result:
                st.success("✅ Profile saved to server successfully!")
            else:
                st.warning(
                    "⚠️ Profile saved locally but could not be synced to server."
                )
        else:
            st.info(
                "ℹ️ Profile saved locally. Connect to the backend server to "
                "persist data."
            )
    except Exception as exc:
        st.warning(f"⚠️ Local save successful. Server sync failed: {exc}")

    st.rerun()


def _render_profile_sidebar(
    profile: Optional[Dict[str, Any]],
    has_profile: bool,
) -> None:
    """Render the profile summary sidebar card.

    Args:
        profile: Profile dict or None.
        has_profile: Whether a complete profile exists.
    """
    if has_profile and profile:
        st.markdown("### Profile Summary")
        glass_card(
            "Profile Overview",
            f"""
            <div style="font-size: 0.9rem;">
                <p><strong>Name:</strong> {profile.get('full_name', 'N/A')}</p>
                <p><strong>Age:</strong> {profile.get('age', 'N/A')}</p>
                <p><strong>Gender:</strong> {profile.get('gender', 'N/A')}</p>
                <p><strong>Height:</strong> {profile.get('height', 'N/A')} cm</p>
                <p><strong>Weight:</strong> {profile.get('weight', 'N/A')} kg</p>
                <p><strong>Activity:</strong> {profile.get('activity_level', 'N/A')}</p>
                <p><strong>Goal:</strong> {profile.get('goal', 'N/A')}</p>
                <p><strong>Diet:</strong> {profile.get('food_preference', 'N/A')}</p>
            </div>
            """,
        )

        if profile.get("allergies"):
            st.markdown("### Allergies")
            for allergy in profile["allergies"]:
                st.markdown(
                    f"<span style='background: rgba(231, 76, 60, 0.15); "
                    f"color: #e74c3c; padding: 0.15rem 0.5rem; border-radius: 8px; "
                    f"font-size: 0.75rem; margin: 0.15rem; display: inline-block;'>"
                    f"⚠ {allergy}</span>",
                    unsafe_allow_html=True,
                )

        if profile.get("medical_conditions"):
            st.markdown("### Medical Conditions")
            for condition in profile["medical_conditions"]:
                st.markdown(
                    f"<span style='background: rgba(243, 156, 18, 0.15); "
                    f"color: #f39c12; padding: 0.15rem 0.5rem; border-radius: 8px; "
                    f"font-size: 0.75rem; margin: 0.15rem; display: inline-block;'>"
                    f"🏥 {condition}</span>",
                    unsafe_allow_html=True,
                )

        if st.button("🗑️ Clear Profile", type="secondary", use_container_width=True):
            set_key("saved_profile", None)
            set_key("profile_loaded", False)
            st.rerun()

    else:
        info_card(
            "📋 Why Create a Profile?",
            "A complete health profile helps our AI generate accurate, "
            "personalized diet recommendations tailored to your body, "
            "lifestyle, and goals.",
        )