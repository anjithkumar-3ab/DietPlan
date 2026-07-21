"""
NutriAI Form Components.

Reusable form elements for profile creation and settings.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Callable

import streamlit as st

from frontend.utils.constants import (
    GENDER_OPTIONS,
    ACTIVITY_LEVELS,
    GOAL_OPTIONS,
    FOOD_PREFERENCES,
    ALLERGY_OPTIONS,
    MEDICAL_CONDITIONS,
    EXCLUDE_INGREDIENTS,
)


def profile_form(
    existing_data: Optional[Dict[str, Any]] = None,
    on_submit: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> None:
    """Render the health profile creation/editing form.

    Args:
        existing_data: Pre-filled profile data for editing.
        on_submit: Callback with form data dict on submission.
    """
    data = existing_data or {}

    with st.form("profile_form", clear_on_submit=False):
        st.markdown("#### Personal Information")

        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input(
                "Full Name",
                value=data.get("full_name", ""),
                placeholder="e.g. John Doe",
            )
        with col2:
            age = st.number_input(
                "Age",
                min_value=1,
                max_value=120,
                value=data.get("age", 25),
                step=1,
            )

        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox(
                "Gender",
                options=GENDER_OPTIONS,
                index=GENDER_OPTIONS.index(data.get("gender", "Male"))
                if data.get("gender") in GENDER_OPTIONS
                else 0,
            )
        with col2:
            date_of_birth_val = data.get("date_of_birth")
            date_of_birth = st.text_input(
                "Date of Birth (optional)",
                value=date_of_birth_val if date_of_birth_val else "",
                placeholder="YYYY-MM-DD",
            )

        st.divider()
        st.markdown("#### Body Measurements")

        col1, col2, col3 = st.columns(3)
        with col1:
            height = st.number_input(
                "Height (cm)",
                min_value=50.0,
                max_value=250.0,
                value=float(data.get("height", 170)),
                step=0.5,
                format="%.1f",
            )
        with col2:
            weight = st.number_input(
                "Weight (kg)",
                min_value=10.0,
                max_value=300.0,
                value=float(data.get("weight", 70)),
                step=0.5,
                format="%.1f",
            )
        with col3:
            target_weight = st.number_input(
                "Target Weight (kg, optional)",
                min_value=10.0,
                max_value=300.0,
                value=float(data.get("target_weight", 0))
                if data.get("target_weight")
                else 0.0,
                step=0.5,
                format="%.1f",
            )

        st.divider()
        st.markdown("#### Lifestyle & Goals")

        col1, col2 = st.columns(2)
        with col1:
            activity_level = st.selectbox(
                "Activity Level",
                options=ACTIVITY_LEVELS,
                index=ACTIVITY_LEVELS.index(data.get("activity_level", "Sedentary"))
                if data.get("activity_level") in ACTIVITY_LEVELS
                else 0,
                help="Choose the option that best describes your daily activity.",
            )
        with col2:
            goal = st.selectbox(
                "Fitness Goal",
                options=GOAL_OPTIONS,
                index=GOAL_OPTIONS.index(data.get("goal", "Maintain Weight"))
                if data.get("goal") in GOAL_OPTIONS
                else 0,
            )

        food_preference = st.selectbox(
            "Food Preference",
            options=FOOD_PREFERENCES,
            index=FOOD_PREFERENCES.index(data.get("food_preference", "Non Vegetarian"))
            if data.get("food_preference") in FOOD_PREFERENCES
            else 0,
        )

        st.divider()
        st.markdown("#### Dietary Restrictions")

        allergies = st.multiselect(
            "Allergies (optional)",
            options=ALLERGY_OPTIONS,
            default=data.get("allergies", []),
        )

        medical_conditions = st.multiselect(
            "Medical Conditions (optional)",
            options=MEDICAL_CONDITIONS,
            default=data.get("medical_conditions", []),
        )

        exclude_ingredients = st.multiselect(
            "Exclude Ingredients (optional)",
            options=EXCLUDE_INGREDIENTS,
            default=data.get("exclude_ingredients", []),
        )

        st.divider()
        st.markdown("#### Daily Habits")

        col1, col2 = st.columns(2)
        with col1:
            meals_per_day = st.selectbox(
                "Meals Per Day",
                options=[3, 4, 5, 6],
                index=[3, 4, 5, 6].index(data.get("meals_per_day", 4))
                if data.get("meals_per_day") in [3, 4, 5, 6]
                else 1,
            )
        with col2:
            water_intake = st.number_input(
                "Water Intake Goal (glasses/day, optional)",
                min_value=1,
                max_value=20,
                value=data.get("water_intake_goal", 8),
                step=1,
            )

        col1, col2 = st.columns(2)
        with col1:
            sleep_hours = st.slider(
                "Sleep (hours/night)",
                min_value=0.0,
                max_value=24.0,
                value=float(data.get("sleep_hours", 7.5)),
                step=0.5,
            )
        with col2:
            wake_up_time = st.text_input(
                "Wake Up Time (optional)",
                value=data.get("wake_up_time", ""),
                placeholder="HH:MM (e.g. 06:30)",
            )

        bed_time = st.text_input(
            "Bed Time (optional)",
            value=data.get("bed_time", ""),
            placeholder="HH:MM (e.g. 22:30)",
        )

        st.divider()

        submitted = st.form_submit_button(
            "💾 Save Profile",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            form_data = {
                "full_name": (full_name or "").strip() or "User",
                "age": age,
                "gender": gender,
                "date_of_birth": date_of_birth.strip() or None if date_of_birth else None,
                "height": height,
                "weight": weight,
                "target_weight": target_weight if target_weight > 0 else None,
                "activity_level": activity_level,
                "goal": goal,
                "food_preference": food_preference,
                "allergies": allergies,
                "medical_conditions": medical_conditions,
                "exclude_ingredients": exclude_ingredients,
                "water_intake_goal": water_intake,
                "meals_per_day": meals_per_day,
                "sleep_hours": sleep_hours,
                "wake_up_time": wake_up_time.strip() or None if wake_up_time else None,
                "bed_time": bed_time.strip() or None if bed_time else None,
            }
            if on_submit:
                on_submit(form_data)


def settings_form(
    current_settings: Dict[str, Any],
    on_save: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> None:
    """Render the settings form.

    Args:
        current_settings: Current settings dict.
        on_save: Callback with updated settings dict on save.
    """
    with st.form("settings_form", clear_on_submit=False):
        st.markdown("#### Preferences")

        theme = st.selectbox(
            "Theme",
            options=[
                "Healthcare (Default)",
                "Dark Contrast",
                "Soft Green",
                "High Contrast",
            ],
            index=0,
        )

        col1, col2 = st.columns(2)
        with col1:
            weight_unit = st.selectbox(
                "Weight Unit",
                options=["Metric (kg)", "Imperial (lbs)"],
            )
        with col2:
            height_unit = st.selectbox(
                "Height Unit",
                options=["Metric (cm)", "Imperial (ft/in)"],
            )

        st.divider()
        st.markdown("#### Notifications")

        notify_meal = st.checkbox(
            "Meal reminders",
            value=current_settings.get("notify_meal", True),
        )
        notify_water = st.checkbox(
            "Water intake reminders",
            value=current_settings.get("notify_water", True),
        )
        notify_progress = st.checkbox(
            "Weekly progress summary",
            value=current_settings.get("notify_progress", False),
        )

        st.divider()

        saved = st.form_submit_button(
            "💾 Save Settings",
            type="primary",
            use_container_width=True,
        )

        if saved:
            updated = {
                "theme": theme,
                "weight_unit": weight_unit,
                "height_unit": height_unit,
                "notify_meal": notify_meal,
                "notify_water": notify_water,
                "notify_progress": notify_progress,
            }
            if on_save:
                on_save(updated)