"""
NutriAI Dashboard Page.

Overview page showing key health metrics, quick stats, and recent activity.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import streamlit as st

from frontend.utils.constants import APP_NAME
from frontend.utils.helpers import (
    get,
    daily_health_tip,
    is_profile_complete,
    format_bmi_category,
    bmi_color,
)
from frontend.components.cards import glass_card, info_card
from frontend.components.navbar import render_header
from frontend.components.metrics import (
    render_bmi_gauge,
    render_health_metrics_row,
)
from frontend.services.api import get_cached_history, api_available


def show() -> None:
    """Render the dashboard page."""
    render_header("Dashboard")

    profile = get("saved_profile")
    diet_plan = get("last_diet_plan")

    # Check if API is available
    api_ok = False
    try:
        api_ok = api_available()
    except Exception:
        pass

    if not api_ok:
        st.warning(
            "⚠️ Backend API is not reachable. Some features will be limited. "
            "Please ensure the backend server is running."
        )

    if not is_profile_complete(profile):
        _render_onboarding()
        return

    if diet_plan:
        _render_dashboard_with_plan(profile, diet_plan)
    else:
        _render_dashboard_without_plan(profile)


def _render_onboarding() -> None:
    """Render the onboarding state when no profile exists."""
    st.markdown(
        f"""
        <div style="text-align: center; padding: 3rem 1rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🥗</div>
            <h2>Welcome to {APP_NAME}</h2>
            <p style="color: #9CA3AF; max-width: 500px; margin: 0.5rem auto;">
                Your AI-powered personalized diet planning assistant. Create your
                health profile to get started.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("👤 Create Health Profile", type="primary", use_container_width=True):
            st.session_state["page"] = "👤 Health Profile"
            st.rerun()

    # Health tip
    tip = daily_health_tip()
    info_card(
        "💡 Daily Health Tip",
        tip,
    )


def _render_dashboard_without_plan(profile: Dict[str, Any]) -> None:
    """Render dashboard with profile but no diet plan yet.

    Args:
        profile: Health profile dict.
    """
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2>Welcome back, {profile.get('full_name', 'User')} 👋</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Age", f"{profile.get('age', '-')} years")
    with col2:
        st.metric("Weight", f"{profile.get('weight', '-')} kg")
    with col3:
        st.metric("Goal", profile.get("goal", "-"))

    st.markdown("### Ready to start?")

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("🥗 Generate Diet Plan", type="primary", use_container_width=True):
            st.session_state["page"] = "🥗 Diet Planner"
            st.rerun()
    with col2:
        if st.button("👤 Update Profile", use_container_width=True):
            st.session_state["page"] = "👤 Health Profile"
            st.rerun()

    # Recent history (if any)
    _render_recent_history()

    # Health tip
    tip = daily_health_tip()
    info_card("💡 Daily Health Tip", tip)


def _render_dashboard_with_plan(
    profile: Dict[str, Any],
    plan: Dict[str, Any],
) -> None:
    """Render dashboard with an active diet plan.

    Args:
        profile: Health profile dict.
        plan: Recommendation response dict.
    """
    name = profile.get("full_name", "User")

    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2>Welcome back, {name} 👋</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # BMI Gauge
    bmi = plan.get("bmi", 0)
    bmr = plan.get("bmr", 0)
    tdee = plan.get("tdee", 0)
    daily_calories = plan.get("daily_calories", 0)
    daily_plan = plan.get("daily_plan", {})
    water_liters = daily_plan.get("recommended_water_liters", 0)

    # Health metrics row
    render_health_metrics_row(bmr, tdee, daily_calories, water_liters)

    # BMI and Macros row
    col1, col2 = st.columns([1, 2])
    with col1:
        render_bmi_gauge(bmi)
    with col2:
        st.markdown("### Macronutrient Targets")
        daily_plan = plan.get("daily_plan", {})
        target_protein = plan.get("target_protein", daily_plan.get("target_protein", 0))
        target_carbs = plan.get(
            "target_carbohydrates", daily_plan.get("target_carbohydrates", 0)
        )
        target_fat = plan.get("target_fat", daily_plan.get("target_fat", 0))

        total_protein = daily_plan.get("total_protein", 0)
        total_carbs = daily_plan.get("total_carbohydrates", 0)
        total_fat = daily_plan.get("total_fat", 0)

        # Macro bars using simple metrics instead of custom HTML
        col_p, col_c, col_f = st.columns(3)
        with col_p:
            st.metric(
                "Protein",
                f"{total_protein:.0f}/{target_protein:.0f}g",
                help="Daily protein target",
            )
        with col_c:
            st.metric(
                "Carbs",
                f"{total_carbs:.0f}/{target_carbs:.0f}g",
                help="Daily carbohydrate target",
            )
        with col_f:
            st.metric(
                "Fat",
                f"{total_fat:.0f}/{target_fat:.0f}g",
                help="Daily fat target",
            )

    # Quick actions
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🥗 View Diet Plan", type="primary", use_container_width=True):
            st.session_state["page"] = "🥗 Diet Planner"
            st.rerun()
    with col2:
        if st.button("📜 View History", use_container_width=True):
            st.session_state["page"] = "📜 Meal History"
            st.rerun()
    with col3:
        if st.button("📈 View Progress", use_container_width=True):
            st.session_state["page"] = "📈 Progress"
            st.rerun()

    # Health tip
    tip = daily_health_tip()
    glass_card("💡 Daily Health Tip", f"<p style='color: #D1D5DB;'>{tip}</p>")


def _render_recent_history() -> None:
    """Render a summary of recent diet plan history."""
    try:
        history = get_cached_history(limit=5)
    except Exception:
        return

    if not history or not history.get("recommendations"):
        return

    recommendations = history["recommendations"]
    if not recommendations:
        return

    st.markdown("### Recent Diet Plans")
    for rec in recommendations[:3]:
        created = rec.get("created_at", "")
        bmi = rec.get("bmi", 0)
        category = format_bmi_category(bmi)
        color = bmi_color(bmi)

        st.markdown(
            f"""
            <div class="glass-card" style="margin-bottom: 0.5rem; padding: 0.75rem 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-weight: 500; color: #F5F5F5;">
                            BMI: {bmi:.1f}
                        </span>
                        <span style="color: {color}; font-size: 0.8rem; margin-left: 0.5rem;">
                            ({category})
                        </span>
                    </div>
                    <div style="font-size: 0.75rem; color: #6B7280;">
                        {created[:10] if created else "N/A"}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )