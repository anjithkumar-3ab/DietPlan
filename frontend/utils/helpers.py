"""
NutriAI Frontend Helper Functions.

Shared helper functions used across Streamlit pages and components.
"""

from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Any, Dict, List, Optional

import streamlit as st

from frontend.utils.constants import (
    ACTIVITY_MAP,
    BMI_CATEGORIES,
    GOAL_MAP,
    FOOD_MAP,
    HEALTH_TIPS,
    DEFAULT_PAGE,
    DEFAULT_SETTINGS,
)


# ---------------------------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------------------------


def init_session_state() -> None:
    """Initialize all required session state variables with safe defaults.

    This must be called once at application startup in app.py.
    """
    session_defaults: Dict[str, object] = {
        "page": DEFAULT_PAGE,
        "saved_profile": None,
        "last_diet_plan": None,
        "profile_loaded": False,
        **DEFAULT_SETTINGS,
    }
    for key, value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get(key: str, default: Any = None) -> Any:
    """Safely retrieve a session state value.

    Args:
        key: Session state key name.
        default: Fallback value if key doesn't exist.

    Returns:
        Stored value or default.
    """
    return st.session_state.get(key, default)


def set_key(key: str, value: Any) -> None:
    """Set a session state value safely.

    Args:
        key: Session state key name.
        value: Value to store.
    """
    st.session_state[key] = value


# ---------------------------------------------------------------------------
# Profile → Recommendation Request Mapping
# ---------------------------------------------------------------------------


def profile_to_request(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a HealthProfile dict to a RecommendationRequest dict.

    Normalises frontend enum values to backend enum values.

    Args:
        profile: HealthProfile dictionary from the profile form.

    Returns:
        RecommendationRequest dictionary ready for the API.
    """
    return {
        "age": profile.get("age", 25),
        "gender": profile.get("gender", "Male"),
        "height": profile.get("height", 170),
        "weight": profile.get("weight", 70),
        "activity_level": ACTIVITY_MAP.get(
            profile.get("activity_level", "Sedentary"), "Sedentary"
        ),
        "goal": GOAL_MAP.get(
            profile.get("goal", "Maintain Weight"), "Maintenance"
        ),
        "food_preference": FOOD_MAP.get(
            profile.get("food_preference", "Non Vegetarian"), "Non-Vegetarian"
        ),
        "allergies": profile.get("allergies", []),
        "medical_conditions": profile.get("medical_conditions", []),
        "meals_per_day": profile.get("meals_per_day", 4),
    }


# ---------------------------------------------------------------------------
# Formatting Helpers
# ---------------------------------------------------------------------------


def format_calories(value: float) -> str:
    """Format a calorie number with a comma separator.

    Args:
        value: Calorie count.

    Returns:
        Formatted string like "2,000 kcal".
    """
    return f"{value:,.0f} kcal"


def format_grams(value: float) -> str:
    """Format a gram value to one decimal place.

    Args:
        value: Grams.

    Returns:
        Formatted string like "45.2 g".
    """
    return f"{value:.1f} g"


def format_date(iso_string: str) -> str:
    """Convert an ISO datetime string to a readable format.

    Args:
        iso_string: ISO 8601 datetime string.

    Returns:
        Formatted string like "21 Jul 2026, 2:30 PM".
    """
    try:
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y, %I:%M %p")
    except (ValueError, AttributeError, TypeError):
        return str(iso_string)


def format_bmi_category(bmi: float) -> str:
    """Return the WHO BMI category for a given BMI value.

    Args:
        bmi: Body Mass Index value.

    Returns:
        Category string.
    """
    for lower, upper, label, _ in BMI_CATEGORIES:
        if lower <= bmi < upper:
            return label
    return "Unknown"


def bmi_color(bmi: float) -> str:
    """Return hex colour for the given BMI value.

    Args:
        bmi: Body Mass Index value.

    Returns:
        Hex colour string.
    """
    for lower, upper, _, color in BMI_CATEGORIES:
        if lower <= bmi < upper:
            return color
    return "#9CA3AF"


# ---------------------------------------------------------------------------
# Health Tip
# ---------------------------------------------------------------------------


def daily_health_tip() -> str:
    """Get a deterministic daily health tip based on today's date.

    Returns:
        A health tip string.
    """
    today = datetime.utcnow().strftime("%Y-%m-%d")
    index = int(hashlib.md5(today.encode()).hexdigest(), 16) % len(HEALTH_TIPS)
    return HEALTH_TIPS[index]


# ---------------------------------------------------------------------------
# Profile helpers
# ---------------------------------------------------------------------------


def is_profile_complete(profile: Optional[Dict[str, Any]]) -> bool:
    """Check if a profile dict has the minimum required fields.

    Args:
        profile: Profile dict or None.

    Returns:
        True if profile exists and has required fields.
    """
    if not profile:
        return False
    required = ["age", "gender", "height", "weight"]
    return all(profile.get(field) for field in required)


def safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert a value to float.

    Args:
        value: Value to convert.
        default: Fallback value.

    Returns:
        Float value or default.
    """
    try:
        return float(value)
    except (ValueError, TypeError, AttributeError):
        return default