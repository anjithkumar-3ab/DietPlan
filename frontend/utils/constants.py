"""
NutriAI Frontend Constants.

Centralized application constants, configuration, and enum mappings.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# Application Metadata
# ---------------------------------------------------------------------------

APP_NAME: str = "NutriAI"
APP_TAGLINE: str = "AI-Powered Personalized Diet Planning"
APP_VERSION: str = "2.0.0"
APP_ICON: str = "🥗"

# ---------------------------------------------------------------------------
# Backend API
# ---------------------------------------------------------------------------

API_BASE_URL: str = "http://localhost:8000"
API_TIMEOUT: int = 30

# API Paths
API_HEALTH: str = "/health"
API_PROFILE: str = "/profile/"
API_RECOMMENDATION_GENERATE: str = "/recommendation/generate"
API_RECOMMENDATION_HISTORY: str = "/recommendation/history"
API_RECOMMENDATION_BY_ID: str = "/recommendation/{recommendation_id}"
API_RECOMMENDATION_REGENERATE: str = "/recommendation/{recommendation_id}/regenerate"
API_FOODS: str = "/foods/"
API_FOODS_SEARCH: str = "/foods/search"
API_FOODS_CATEGORY: str = "/foods/category/{category}"
API_FOOD_BY_ID: str = "/foods/{food_id}"

# ---------------------------------------------------------------------------
# Navigation Pages
# ---------------------------------------------------------------------------

PAGES: Dict[str, str] = {
    "🏠 Dashboard": "dashboard",
    "👤 Health Profile": "profile",
    "🥗 Diet Planner": "diet_planner",
    "📜 Meal History": "meal_history",
    "📈 Progress": "progress",
    "⚙ Settings": "settings",
}

DEFAULT_PAGE: str = "🏠 Dashboard"

# ---------------------------------------------------------------------------
# Profile Enums (matches backend HealthProfile schema)
# ---------------------------------------------------------------------------

GENDER_OPTIONS: List[str] = ["Male", "Female"]

ACTIVITY_LEVELS: List[str] = [
    "Sedentary",
    "Lightly Active",
    "Moderately Active",
    "Very Active",
    "Athlete",
]

GOAL_OPTIONS: List[str] = [
    "Lose Weight",
    "Maintain Weight",
    "Gain Weight",
    "Muscle Gain",
    "Healthy Lifestyle",
]

FOOD_PREFERENCES: List[str] = [
    "Vegetarian",
    "Non Vegetarian",
    "Vegan",
    "Eggetarian",
    "Jain",
]

ALLERGY_OPTIONS: List[str] = [
    "Dairy",
    "Eggs",
    "Peanuts",
    "Tree Nuts",
    "Soy",
    "Wheat",
    "Fish",
    "Shellfish",
    "Sesame",
    "Gluten",
    "Lactose",
]

MEDICAL_CONDITIONS: List[str] = [
    "Diabetes",
    "Hypertension",
    "High Cholesterol",
    "Thyroid Disorders",
    "PCOS",
    "IBS",
    "GERD / Acid Reflux",
    "Anemia",
    "Kidney Disease",
    "Liver Disease",
    "Heart Disease",
]

EXCLUDE_INGREDIENTS: List[str] = [
    "Sugar",
    "Salt",
    "Oil",
    "Butter",
    "Cheese",
    "Cream",
    "Rice",
    "Wheat Flour",
    "Red Meat",
    "Processed Meat",
]

# ---------------------------------------------------------------------------
# Activity Level → Backend ActivityLevel mapping
# ---------------------------------------------------------------------------

ACTIVITY_MAP: Dict[str, str] = {
    "Sedentary": "Sedentary",
    "Lightly Active": "Light",
    "Moderately Active": "Moderate",
    "Very Active": "Active",
    "Athlete": "Very Active",
}

# ---------------------------------------------------------------------------
# Goal → Backend Goal mapping
# ---------------------------------------------------------------------------

GOAL_MAP: Dict[str, str] = {
    "Lose Weight": "Weight Loss",
    "Maintain Weight": "Maintenance",
    "Gain Weight": "Weight Gain",
    "Muscle Gain": "Weight Gain",
    "Healthy Lifestyle": "Maintenance",
}

# ---------------------------------------------------------------------------
# Food Preference → Backend FoodPreference mapping
# ---------------------------------------------------------------------------

FOOD_MAP: Dict[str, str] = {
    "Vegetarian": "Vegetarian",
    "Non Vegetarian": "Non-Vegetarian",
    "Vegan": "Vegan",
    "Eggetarian": "Vegetarian",
    "Jain": "Vegetarian",
}

# ---------------------------------------------------------------------------
# Cache TTLs (seconds)
# ---------------------------------------------------------------------------

CACHE_TTL_HEALTH: int = 60
CACHE_TTL_PROFILE: int = 300
CACHE_TTL_HISTORY: int = 300
CACHE_TTL_FOODS: int = 600
CACHE_TTL_PAGE_MODULE: int = 3600

# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------

DEFAULT_PAGE_SIZE: int = 10
MAX_HISTORY_LIMIT: int = 100

# ---------------------------------------------------------------------------
# Health Tips
# ---------------------------------------------------------------------------

HEALTH_TIPS: List[str] = [
    "Drink a glass of water before each meal to help control appetite.",
    "Aim for at least 7-8 hours of quality sleep each night.",
    "Include protein with every meal to maintain muscle mass.",
    "Walk for 30 minutes daily to boost cardiovascular health.",
    "Eat at least 5 portions of fruits and vegetables every day.",
    "Limit added sugar to less than 10% of your daily calories.",
    "Practice mindful eating — chew slowly and savour each bite.",
    "Choose whole grains over refined carbohydrates.",
    "Stay hydrated — dehydration often masquerades as hunger.",
    "Plan your meals ahead of time to avoid impulsive eating.",
    "Include healthy fats like nuts, seeds, and olive oil.",
    "Don't skip breakfast — it kick-starts your metabolism.",
    "Eat the rainbow: variety of colours means variety of nutrients.",
    "Reduce sodium intake by seasoning with herbs and spices.",
    "Take short breaks to stretch if you sit for long hours.",
]

# ---------------------------------------------------------------------------
# BMI Categories & Colors
# ---------------------------------------------------------------------------

BMI_CATEGORIES: List[Tuple[float, float, str, str]] = [
    (0, 18.5, "Underweight", "#3498db"),
    (18.5, 25.0, "Normal Weight", "#27ae60"),
    (25.0, 30.0, "Overweight", "#f39c12"),
    (30.0, float("inf"), "Obese", "#e74c3c"),
]

# ---------------------------------------------------------------------------
# Settings Defaults
# ---------------------------------------------------------------------------

DEFAULT_SETTINGS: Dict[str, object] = {
    "theme": "Healthcare (Default)",
    "weight_unit": "Metric (kg)",
    "height_unit": "Metric (cm)",
    "notify_meal": True,
    "notify_water": True,
    "notify_progress": False,
}

THEME_OPTIONS: List[str] = [
    "Healthcare (Default)",
    "Dark Contrast",
    "Soft Green",
    "High Contrast",
]

UNIT_OPTIONS: List[str] = [
    "Metric (kg, cm)",
    "Imperial (lbs, ft/in)",
]