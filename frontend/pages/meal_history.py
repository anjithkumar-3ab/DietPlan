"""
NutriAI Meal History Page.

View past diet plan recommendations, including meal breakdowns,
nutritional data, and options to regenerate or delete.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import streamlit as st

from frontend.utils.helpers import (
    get,
    set_key,
    format_date,
    format_bmi_category,
    bmi_color,
)
from frontend.components.cards import glass_card, info_card, empty_state_card, meal_card
from frontend.components.navbar import render_header
from frontend.services.api import (
    get_history,
    get_cached_history,
    delete_recommendation,
    regenerate_diet_plan,
    api_available,
)


def show() -> None:
    """Render the meal history page."""
    render_header("Meal History")

    if not api_available():
        st.warning(
            "⚠️ Backend API is not reachable. History data may not be available."
        )

    # Load history
    with st.spinner("Loading meal history..."):
        try:
            history = get_history(limit=50)
        except Exception as exc:
            st.error(f"❌ Failed to load history: {exc}")
            history = None

    if not history or not history.get("recommendations"):
        empty_state_card(
            "No Meal History",
            "You haven't generated any diet plans yet. Create your first diet "
            "plan from the Diet Planner page.",
            emoji="📜",
        )
        if st.button("🥗 Go to Diet Planner", type="primary", use_container_width=True):
            st.session_state["page"] = "🥗 Diet Planner"
            st.rerun()
        return

    recommendations = history.get("recommendations", [])
    count = history.get("count", len(recommendations))

    st.markdown(f"Showing **{len(recommendations)}** of **{count}** past plans")

    # Display history items
    for i, rec in enumerate(recommendations):
        _render_history_item(rec, i)


def _render_history_item(rec: Dict[str, Any], index: int) -> None:
    """Render a single history item as an expandable card.

    Args:
        rec: Recommendation record dict.
        index: Index for unique expander key.
    """
    rec_id = rec.get("recommendation_id", rec.get("_id", ""))
    created = rec.get("created_at", "")
    bmi = rec.get("bmi", 0)
    daily_calories = rec.get("daily_calories", 0)
    category = format_bmi_category(bmi)
    color = bmi_color(bmi)

    # Format the date
    date_str = format_date(created) if created else "Unknown date"

    with st.expander(
        f"📋 Plan from {date_str} — BMI: {bmi:.1f} ({category})",
        expanded=(index == 0),
    ):
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("BMI", f"{bmi:.1f}", help=category)
        with col2:
            st.metric("Daily Calories", f"{daily_calories:,.0f} kcal")
        with col3:
            st.metric(
                "Protein",
                f"{rec.get('target_protein', 0):.0f}g",
            )
        with col4:
            st.metric(
                "Water",
                f"{rec.get('daily_plan', {}).get('recommended_water_liters', 0):.1f}L",
            )

        # Meal breakdown
        daily_plan = rec.get("daily_plan", {})
        if daily_plan:
            meal_tabs = st.tabs(["🌅 Breakfast", "☀️ Lunch", "🌙 Dinner", "🍿 Snacks"])

            with meal_tabs[0]:
                meal = daily_plan.get("breakfast", {})
                if meal and meal.get("items"):
                    meal_card("Breakfast", meal.get("items", []), meal, "🌅")

            with meal_tabs[1]:
                meal = daily_plan.get("lunch", {})
                if meal and meal.get("items"):
                    meal_card("Lunch", meal.get("items", []), meal, "☀️")

            with meal_tabs[2]:
                meal = daily_plan.get("dinner", {})
                if meal and meal.get("items"):
                    meal_card("Dinner", meal.get("items", []), meal, "🌙")

            with meal_tabs[3]:
                meal = daily_plan.get("snacks", {})
                if meal and meal.get("items"):
                    meal_card("Snacks", meal.get("items", []), meal, "🍿")

        # Actions
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(
                "🔄 Regenerate",
                key=f"regenerate_{rec_id}",
                type="primary",
                use_container_width=True,
            ):
                _handle_regenerate(rec_id)
        with col2:
            if st.button(
                "📋 Use as Current",
                key=f"use_{rec_id}",
                use_container_width=True,
            ):
                set_key("last_diet_plan", rec)
                st.success("✅ Plan set as current! Go to Diet Planner to view.")
                st.rerun()
        with col3:
            if st.button(
                "🗑️ Delete",
                key=f"delete_{rec_id}",
                type="secondary",
                use_container_width=True,
            ):
                _handle_delete(rec_id)


def _handle_regenerate(rec_id: str) -> None:
    """Handle regenerating a diet plan from history.

    Args:
        rec_id: Recommendation ID to regenerate.
    """
    if not rec_id:
        st.error("❌ Cannot regenerate: missing recommendation ID.")
        return

    if not api_available():
        st.error("❌ Backend API is not available.")
        return

    with st.spinner("🔄 Regenerating diet plan..."):
        try:
            result = regenerate_diet_plan(rec_id)
        except Exception as exc:
            st.error(f"❌ Failed to regenerate: {exc}")
            return

    if result and result.get("success", False):
        set_key("last_diet_plan", result)
        st.success("✅ Diet plan regenerated successfully!")
        st.rerun()
    else:
        msg = result.get("message", "Failed to regenerate diet plan.") if result else "API returned no data."
        st.error(f"❌ {msg}")


def _handle_delete(rec_id: str) -> None:
    """Handle deleting a recommendation from history.

    Args:
        rec_id: Recommendation ID to delete.
    """
    if not rec_id:
        st.error("❌ Cannot delete: missing recommendation ID.")
        return

    if not api_available():
        st.error("❌ Backend API is not available.")
        return

    try:
        result = delete_recommendation(rec_id)
    except Exception as exc:
        st.error(f"❌ Failed to delete: {exc}")
        return

    if result and result.get("success", False):
        # Clear cached history
        st.cache_data.clear()
        st.success("✅ Recommendation deleted!")
        st.rerun()
    else:
        msg = result.get("message", "Failed to delete.") if result else "API returned no data."
        st.error(f"❌ {msg}")