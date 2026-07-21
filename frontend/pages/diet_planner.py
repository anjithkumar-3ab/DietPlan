"""
NutriAI Diet Planner Page.

Generate personalized diet plans based on your health profile,
view meal breakdowns, and track nutritional targets.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import streamlit as st

from frontend.utils.helpers import (
    get,
    set_key,
    profile_to_request,
    is_profile_complete,
    format_bmi_category,
    bmi_color,
)
from frontend.components.cards import glass_card, info_card, meal_card, empty_state_card
from frontend.components.navbar import render_header
from frontend.components.metrics import render_health_metrics_row, render_bmi_gauge
from frontend.components.charts import daily_calorie_comparison, macronutrient_pie
from frontend.services.api import generate_diet_plan, api_available


def show() -> None:
    """Render the diet planner page."""
    render_header("Diet Planner")

    profile = get("saved_profile")
    last_plan = get("last_diet_plan")

    # Check if profile exists
    if not is_profile_complete(profile):
        empty_state_card(
            "No Profile Found",
            "Please create your health profile first before generating a diet plan.",
            emoji="👤",
        )
        if st.button("👤 Go to Health Profile", type="primary", use_container_width=True):
            st.session_state["page"] = "👤 Health Profile"
            st.rerun()
        return

    # Generate button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            f"Generate a personalized diet plan for **{profile.get('full_name', 'User')}**"
        )
    with col2:
        if st.button(
            "🔄 Generate New Plan",
            type="primary",
            use_container_width=True,
        ):
            _generate_plan(profile)

    # Show existing plan or generate new one
    if last_plan:
        _display_plan(last_plan)
    else:
        info_card(
            "Ready to Begin?",
            "Click 'Generate New Plan' above to create your personalized "
            "diet plan based on your health profile.",
            emoji="🥗",
        )


def _generate_plan(profile: Dict[str, Any]) -> None:
    """Generate a new diet plan from the profile data.

    Args:
        profile: Health profile dict.
    """
    if not api_available():
        st.error("❌ Backend API is not available. Cannot generate diet plan.")
        return

    # Convert profile to API request format
    request_data = profile_to_request(profile)

    with st.spinner("🧠 Generating your personalized diet plan..."):
        try:
            result = generate_diet_plan(request_data)
        except Exception as exc:
            st.error(f"❌ Failed to generate diet plan: {exc}")
            return

    if result is None:
        st.error("❌ Failed to generate diet plan. Please try again.")
        return

    if not result.get("success", False):
        st.error(f"❌ {result.get('message', 'Failed to generate diet plan.')}")
        return

    # Save to session state
    set_key("last_diet_plan", result)
    st.success("✅ Diet plan generated successfully!")
    st.rerun()


def _display_plan(plan: Dict[str, Any]) -> None:
    """Display the diet plan details.

    Args:
        plan: Recommendation response dict.
    """
    # Metrics row
    bmi = plan.get("bmi", 0)
    bmr = plan.get("bmr", 0)
    tdee = plan.get("tdee", 0)
    daily_calories = plan.get("daily_calories", 0)
    daily_plan = plan.get("daily_plan", {})
    water_liters = daily_plan.get("recommended_water_liters", 0) if daily_plan else 0

    render_health_metrics_row(bmr, tdee, daily_calories, water_liters)

    # BMI and plan info
    col1, col2 = st.columns([1, 2])
    with col1:
        render_bmi_gauge(bmi)
        category = format_bmi_category(bmi)
        color = bmi_color(bmi)
        st.markdown(
            f"""
            <div style="text-align: center; font-size: 0.85rem; color: {color};">
                {category}
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        if daily_plan:
            _render_nutrition_summary(daily_plan)

    # Meal cards
    st.markdown("### Daily Meal Plan")
    if daily_plan:
        meal_tabs = st.tabs(["🌅 Breakfast", "☀️ Lunch", "🌙 Dinner", "🍿 Snacks"])

        with meal_tabs[0]:
            meal = daily_plan.get("breakfast", {})
            if meal and meal.get("items"):
                meal_card(
                    "Breakfast",
                    meal.get("items", []),
                    meal,
                    "🌅",
                )
            else:
                st.info("No breakfast items defined.")

        with meal_tabs[1]:
            meal = daily_plan.get("lunch", {})
            if meal and meal.get("items"):
                meal_card(
                    "Lunch",
                    meal.get("items", []),
                    meal,
                    "☀️",
                )
            else:
                st.info("No lunch items defined.")

        with meal_tabs[2]:
            meal = daily_plan.get("dinner", {})
            if meal and meal.get("items"):
                meal_card(
                    "Dinner",
                    meal.get("items", []),
                    meal,
                    "🌙",
                )
            else:
                st.info("No dinner items defined.")

        with meal_tabs[3]:
            meal = daily_plan.get("snacks", {})
            if meal and meal.get("items"):
                meal_card(
                    "Snacks",
                    meal.get("items", []),
                    meal,
                    "🍿",
                )
            else:
                st.info("No snack items defined.")

    # Calorie distribution chart
    st.markdown("### Calorie Distribution")
    if daily_plan:
        breakfast_cal = daily_plan.get("breakfast", {}).get("total_calories", 0)
        lunch_cal = daily_plan.get("lunch", {}).get("total_calories", 0)
        dinner_cal = daily_plan.get("dinner", {}).get("total_calories", 0)
        snack_cal = daily_plan.get("snacks", {}).get("total_calories", 0)

        daily_calorie_comparison(
            breakfast_cal, lunch_cal, dinner_cal, snack_cal, daily_calories
        )

    # Regenerate option
    if st.button("🔄 Regenerate Plan", type="secondary"):
        profile = get("saved_profile")
        if profile:
            _generate_plan(profile)


def _render_nutrition_summary(daily_plan: Dict[str, Any]) -> None:
    """Render the daily nutrition targets summary.

    Args:
        daily_plan: DailyPlan dict.
    """
    st.markdown("### Daily Nutrition Targets")

    target_protein = daily_plan.get("target_protein", 0)
    target_carbs = daily_plan.get("target_carbohydrates", 0)
    target_fat = daily_plan.get("target_fat", 0)
    target_calories = daily_plan.get("target_daily_calories", 0)

    total_protein = daily_plan.get("total_protein", 0)
    total_carbs = daily_plan.get("total_carbohydrates", 0)
    total_fat = daily_plan.get("total_fat", 0)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Protein",
            f"{total_protein:.0f}/{target_protein:.0f}g",
            help="Daily protein target",
        )
    with col2:
        st.metric(
            "Carbohydrates",
            f"{total_carbs:.0f}/{target_carbs:.0f}g",
            help="Daily carbohydrate target",
        )
    with col3:
        st.metric(
            "Fat",
            f"{total_fat:.0f}/{target_fat:.0f}g",
            help="Daily fat target",
        )

    # Macro breakdown
    st.markdown("#### Macronutrient Breakdown")
    macronutrient_pie(total_protein, total_carbs, total_fat)

    # Fiber and water
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Fiber",
            f"{daily_plan.get('total_fiber', 0):.1f}g",
            help="Daily fiber intake",
        )
    with col2:
        st.metric(
            "Water",
            f"{daily_plan.get('recommended_water_liters', 0):.1f}L",
            help="Recommended water intake",
        )