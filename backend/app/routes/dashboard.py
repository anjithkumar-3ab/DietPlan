"""
Dashboard API Router.

Provides the `/dashboard` endpoint that returns all chart data and
recommendation data needed to render the Diet Recommendation Dashboard.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.services.chart_service import generate_dashboard_charts
from app.services.recommendation_service import get_recommendation_by_id

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# ── Request Schema ──────────────────────────────────────────────────────────

class DashboardRequest(BaseModel):
    """
    Request body for fetching dashboard data.

    Either provide ``recommendation_id`` to load an existing recommendation,
    or provide raw metrics to generate a dashboard without saving.
    """
    recommendation_id: str | None = Field(
        default=None,
        description="MongoDB ObjectId of an existing recommendation.",
    )


# ── Response Schema ─────────────────────────────────────────────────────────

class DashboardResponse(BaseModel):
    """
    Response containing all dashboard data including Plotly chart JSON.
    """
    success: bool
    message: str

    # Health summary
    bmi: float = 0
    bmi_category: str = ""
    bmr: float = 0
    tdee: float = 0
    daily_calories: float = 0
    water_recommendation: float = 0

    # Macro targets
    target_protein: float = 0
    target_carbohydrates: float = 0
    target_fat: float = 0

    # Meal plan data
    meals: Dict[str, Any] = {}
    total_calories: float = 0
    total_protein: float = 0
    total_carbohydrates: float = 0
    total_fat: float = 0
    total_fiber: float = 0
    total_sugar: float = 0
    total_sodium: float = 0

    # User profile
    user_profile: Dict[str, Any] = {}

    # Recommended foods (grouped by meal type)
    recommended_foods: Dict[str, List[str]] = {}
    foods_to_avoid: List[str] = []

    # Nutrition summary extended
    nutrition_summary: Dict[str, float] = {}

    # Health status badges
    health_status: Dict[str, str] = {}

    # Plotly charts (JSON)
    charts: Dict[str, Any] = {}


# ── Helper: Extract profile data ────────────────────────────────────────────

def _extract_profile(recommendation: Dict[str, Any]) -> Dict[str, Any]:
    """Extract user profile from a recommendation document."""
    params = recommendation.get("request_params", {})
    return {
        "name": params.get("name", "User"),
        "age": params.get("age", 0),
        "gender": params.get("gender", ""),
        "height": params.get("height", 0),
        "weight": params.get("weight", 0),
        "goal": params.get("goal", ""),
        "activity_level": params.get("activity_level", ""),
        "food_preference": params.get("food_preference", ""),
        "meals_per_day": params.get("meals_per_day", 4),
        "allergies": params.get("allergies", []),
        "medical_conditions": params.get("medical_conditions", []),
    }


def _build_food_groups(daily_plan: Dict[str, Any]) -> Dict[str, List[str]]:
    """Build recommended food tags grouped by meal type."""
    groups = {}
    meal_map = {
        "breakfast": "Breakfast",
        "lunch": "Lunch",
        "dinner": "Dinner",
        "snacks": "Snacks",
    }
    for key, label in meal_map.items():
        meal = daily_plan.get(key, {})
        items = meal.get("items", [])
        names = [it.get("name", "") for it in items if it.get("name")]
        groups[label] = names
    return groups


def _build_foods_to_avoid(recommendation: Dict[str, Any]) -> List[str]:
    """Return foods to avoid based on allergies and medical conditions."""
    allergens = recommendation.get("allergies", [])
    conditions = recommendation.get("medical_conditions", [])

    # Map common medical conditions to foods to avoid
    condition_foods = {
        "diabetes": ["Sugary Foods", "Refined Carbs", "Soda", "Processed Snacks"],
        "hypertension": ["High-Sodium Foods", "Pickles", "Processed Meats", "Canned Soups"],
        "high cholesterol": ["Fried Foods", "Red Meat", "Butter", "Full-Fat Dairy"],
        "heart disease": ["Saturated Fats", "Trans Fats", "High-Sodium Foods", "Processed Foods"],
        "kidney disease": ["High-Potassium Foods", "High-Phosphorus Foods", "Processed Meats"],
        "thyroid": ["Soy Products", "Cruciferous Vegetables (raw)", "Gluten"],
        "pcos": ["Sugary Foods", "Refined Carbs", "Dairy", "Processed Foods"],
        "anemia": ["Tea/Coffee with meals", "High-Calcium Foods with Iron"],
        "gout": ["Red Meat", "Organ Meats", "Shellfish", "Alcohol", "Sugary Drinks"],
        "none": [],
    }

    avoid = set()
    # Add allergy warnings
    allergy_foods = {
        "peanuts": ["Peanuts", "Peanut Butter", "Peanut Oil"],
        "tree nuts": ["Almonds", "Walnuts", "Cashews", "Pistachios"],
        "dairy": ["Milk", "Cheese", "Yogurt", "Butter", "Cream"],
        "eggs": ["Eggs", "Mayonnaise", "Egg-based Dishes"],
        "gluten": ["Wheat Bread", "Pasta", "Cereal", "Flour Tortillas"],
        "soy": ["Soy Sauce", "Tofu", "Soy Milk", "Edamame"],
        "shellfish": ["Shrimp", "Crab", "Lobster", "Mussels"],
        "fish": ["Salmon", "Tuna", "Mackerel", "Sardines"],
        "wheat": ["Wheat Bread", "Pasta", "Couscous", "Bulgur"],
        "corn": ["Corn", "Corn Syrup", "Popcorn", "Corn Tortillas"],
    }

    for allergy in allergens:
        key = allergy.strip().lower()
        if key in allergy_foods:
            avoid.update(allergy_foods[key])

    for condition in conditions:
        key = condition.strip().lower()
        if key in condition_foods:
            avoid.update(condition_foods[key])

    return sorted(avoid)


def _build_nutrition_summary(daily_plan: Dict[str, Any]) -> Dict[str, float]:
    """Build extended nutrition summary."""
    return {
        "calories": daily_plan.get("total_daily_calories", 0),
        "protein": daily_plan.get("total_protein", 0),
        "carbohydrates": daily_plan.get("total_carbohydrates", 0),
        "fat": daily_plan.get("total_fat", 0),
        "fiber": daily_plan.get("total_fiber", 0),
        "sugar": daily_plan.get("total_sugar", 0) if daily_plan.get("total_sugar") else 0,
        "sodium": daily_plan.get("total_sodium", 0) if daily_plan.get("total_sodium") else 0,
    }


def _build_health_status(recommendation: Dict[str, Any]) -> Dict[str, str]:
    """Build health status badges."""
    params = recommendation.get("request_params", {})
    return {
        "bmi_category": recommendation.get("bmi_category", ""),
        "goal": params.get("goal", ""),
        "activity_level": params.get("activity_level", ""),
        "diet_type": params.get("food_preference", ""),
        "health_status": "Good" if recommendation.get("bmi_category") in ("Normal Weight",) else "Needs Attention",
    }


def _extract_meal_macros(
    meal: Dict[str, Any],
) -> tuple:
    """Extract protein, carbs, fat, and item count from a meal dict."""
    items = meal.get("items", [])
    protein = sum(it.get("protein", 0) or 0 for it in items)
    carbs = sum(it.get("carbohydrates", 0) or 0 for it in items)
    fat = sum(it.get("fat", 0) or 0 for it in items)
    return protein, carbs, fat, len(items)


def _extract_all_meal_macros(
    meals: Dict[str, Any],
) -> Dict[str, Any]:
    """Extract macro values and item counts from all meals."""
    result = {}
    for key in ("breakfast", "lunch", "snacks", "dinner"):
        meal = meals.get(key, {})
        p, c, f, cnt = _extract_meal_macros(meal)
        result[f"{key}_protein"] = p
        result[f"{key}_carbs"] = c
        result[f"{key}_fat"] = f
        result[f"{key}_items"] = cnt
    return result


def _compute_totals(meals: Dict[str, Any]) -> Dict[str, float]:
    """Compute total sugar and sodium from all meals."""
    total_sugar = 0.0
    total_sodium = 0.0
    for key in ("breakfast", "lunch", "snacks", "dinner"):
        for item in meals.get(key, {}).get("items", []):
            total_sugar += item.get("sugar", 0) or 0
            total_sodium += item.get("sodium", 0) or 0
    return {"sugar": total_sugar, "sodium": total_sodium}


# ── Endpoint ────────────────────────────────────────────────────────────────

@router.post("/charts", response_model=DashboardResponse)
async def get_dashboard_data(request: DashboardRequest) -> Any:
    """
    Fetch dashboard data and Plotly charts for a given recommendation.

    Returns all dashboard sections including health metrics, meal plan,
    all 10 Plotly charts.
    """
    if not request.recommendation_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="recommendation_id is required.",
        )

    # Fetch the recommendation
    result = get_recommendation_by_id(request.recommendation_id)
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("message", "Recommendation not found"),
        )

    rec = result["recommendation"]
    daily_plan = rec.get("daily_plan", {})

    # Extract values
    bmi = rec.get("bmi", 0)
    bmi_category = rec.get("bmi_category", "")
    bmr = rec.get("bmr", 0)
    tdee = rec.get("tdee", 0)
    daily_calories = rec.get("daily_calories", 0)
    target_protein = rec.get("target_protein", 0)
    target_carbs = rec.get("target_carbohydrates", 0)
    target_fat = rec.get("target_fat", 0)

    # Meal totals
    meals = {
        "breakfast": daily_plan.get("breakfast", {}),
        "lunch": daily_plan.get("lunch", {}),
        "dinner": daily_plan.get("dinner", {}),
        "snacks": daily_plan.get("snacks", {}),
    }
    total_calories = daily_plan.get("total_daily_calories", 0)
    total_protein = daily_plan.get("total_protein", 0)
    total_carbs = daily_plan.get("total_carbohydrates", 0)
    total_fat = daily_plan.get("total_fat", 0)
    total_fiber = daily_plan.get("total_fiber", 0)
    water = daily_plan.get("recommended_water_liters", 2.0)

    # Extract meal calories for chart
    breakfast_kcal = meals["breakfast"].get("total_calories", 0)
    lunch_kcal = meals["lunch"].get("total_calories", 0)
    snack_kcal = meals["snacks"].get("total_calories", 0)
    dinner_kcal = meals["dinner"].get("total_calories", 0)

    # Per-meal macros and item counts for stacked bar & timeline
    mm = _extract_all_meal_macros(meals)

    # Totals for sunburst
    totals = _compute_totals(meals)

    # Generate all 10 Plotly charts
    charts = generate_dashboard_charts(
        bmi=bmi,
        protein_g=total_protein,
        carbs_g=total_carbs,
        fat_g=total_fat,
        fiber_g=total_fiber,
        breakfast_kcal=breakfast_kcal,
        lunch_kcal=lunch_kcal,
        snack_kcal=snack_kcal,
        dinner_kcal=dinner_kcal,
        current_calories=total_calories,
        target_calories=daily_calories,
        tdee=tdee,
        water_liters=water,
        breakfast_protein=mm["breakfast_protein"],
        breakfast_carbs=mm["breakfast_carbs"],
        breakfast_fat=mm["breakfast_fat"],
        lunch_protein=mm["lunch_protein"],
        lunch_carbs=mm["lunch_carbs"],
        lunch_fat=mm["lunch_fat"],
        snack_protein=mm["snacks_protein"],
        snack_carbs=mm["snacks_carbs"],
        snack_fat=mm["snacks_fat"],
        dinner_protein=mm["dinner_protein"],
        dinner_carbs=mm["dinner_carbs"],
        dinner_fat=mm["dinner_fat"],
        breakfast_items=mm["breakfast_items"],
        lunch_items=mm["lunch_items"],
        snack_items=mm["snacks_items"],
        dinner_items=mm["dinner_items"],
        sugar_g=totals["sugar"],
        sodium_mg=totals["sodium"],
    )

    # Additional dashboard data
    profile = _extract_profile(rec)
    food_groups = _build_food_groups(daily_plan)
    foods_to_avoid = _build_foods_to_avoid(rec)
    nutrition_summary = _build_nutrition_summary(daily_plan)
    health_status = _build_health_status(rec)

    return DashboardResponse(
        success=True,
        message="Dashboard data retrieved successfully",
        bmi=bmi,
        bmi_category=bmi_category,
        bmr=bmr,
        tdee=tdee,
        daily_calories=daily_calories,
        water_recommendation=water,
        target_protein=target_protein,
        target_carbohydrates=target_carbs,
        target_fat=target_fat,
        meals=meals,
        total_calories=total_calories,
        total_protein=total_protein,
        total_carbohydrates=total_carbs,
        total_fat=total_fat,
        total_fiber=total_fiber,
        total_sugar=totals["sugar"],
        total_sodium=totals["sodium"],
        user_profile=profile,
        recommended_foods=food_groups,
        foods_to_avoid=foods_to_avoid,
        nutrition_summary=nutrition_summary,
        health_status=health_status,
        charts=charts,
    )