"""
NutriAI Frontend Validators.

Input validation functions for profile forms and user inputs.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple


def validate_age(age: Any) -> Tuple[bool, Optional[str]]:
    """Validate age input.

    Args:
        age: Age value to validate.

    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        value = int(age)
        if value <= 0 or value > 120:
            return False, "Age must be between 1 and 120 years."
        return True, None
    except (ValueError, TypeError):
        return False, "Age must be a valid number."


def validate_height(height: Any) -> Tuple[bool, Optional[str]]:
    """Validate height input (cm).

    Args:
        height: Height value to validate.

    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        value = float(height)
        if value <= 0 or value > 250:
            return False, "Height must be between 1 and 250 cm."
        return True, None
    except (ValueError, TypeError):
        return False, "Height must be a valid number."


def validate_weight(weight: Any) -> Tuple[bool, Optional[str]]:
    """Validate weight input (kg).

    Args:
        weight: Weight value to validate.

    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        value = float(weight)
        if value <= 0 or value > 500:
            return False, "Weight must be between 1 and 500 kg."
        return True, None
    except (ValueError, TypeError):
        return False, "Weight must be a valid number."


def validate_name(name: str) -> Tuple[bool, Optional[str]]:
    """Validate full name input.

    Args:
        name: Name string to validate.

    Returns:
        Tuple of (is_valid, error_message).
    """
    if not name or not name.strip():
        return False, "Name cannot be empty."
    if len(name.strip()) > 100:
        return False, "Name must be 100 characters or fewer."
    return True, None


def validate_meals_per_day(value: Any) -> Tuple[bool, Optional[str]]:
    """Validate meals per day input.

    Args:
        value: Meals per day value.

    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        meals = int(value)
        if meals < 3 or meals > 6:
            return False, "Meals per day must be between 3 and 6."
        return True, None
    except (ValueError, TypeError):
        return False, "Meals per day must be a valid number."


def validate_profile_data(data: Dict[str, Any]) -> List[str]:
    """Validate a complete profile data dictionary.

    Args:
        data: Profile data dictionary.

    Returns:
        List of validation error messages. Empty list if valid.
    """
    errors: List[str] = []

    # Age
    is_valid, msg = validate_age(data.get("age"))
    if not is_valid and msg:
        errors.append(msg)

    # Height
    is_valid, msg = validate_height(data.get("height"))
    if not is_valid and msg:
        errors.append(msg)

    # Weight
    is_valid, msg = validate_weight(data.get("weight"))
    if not is_valid and msg:
        errors.append(msg)

    # Name (optional but validate if present)
    name = data.get("full_name")
    if name:
        is_valid, msg = validate_name(name)
        if not is_valid and msg:
            errors.append(msg)

    # Meals per day (optional but validate if present)
    meals = data.get("meals_per_day")
    if meals is not None:
        is_valid, msg = validate_meals_per_day(meals)
        if not is_valid and msg:
            errors.append(msg)

    # Required enums
    if data.get("gender") not in ("Male", "Female"):
        errors.append("Gender must be 'Male' or 'Female'.")

    valid_activity = [
        "Sedentary", "Lightly Active", "Moderately Active",
        "Very Active", "Athlete",
    ]
    if data.get("activity_level") not in valid_activity:
        errors.append(f"Activity level must be one of: {', '.join(valid_activity)}.")

    valid_goals = [
        "Lose Weight", "Maintain Weight", "Gain Weight",
        "Muscle Gain", "Healthy Lifestyle",
    ]
    if data.get("goal") not in valid_goals:
        errors.append(f"Goal must be one of: {', '.join(valid_goals)}.")

    valid_food = [
        "Vegetarian", "Non Vegetarian", "Vegan",
        "Eggetarian", "Jain",
    ]
    if data.get("food_preference") not in valid_food:
        errors.append(f"Food preference must be one of: {', '.join(valid_food)}.")

    return errors