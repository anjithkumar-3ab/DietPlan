from datetime import datetime, timezone

from app.database.database import db
from app.services.bmi_service import calculate_bmi, ideal_weight_range
from app.services.bmr_service import (
    calculate_bmr,
    calculate_tdee,
    calorie_goal
)
from app.services.macro_service import calculate_macros


profiles = db["health_profiles"]


def save_profile(profile, user_id=None):

    data = profile.model_dump()

    bmi_result = calculate_bmi(
        profile.height,
        profile.weight
    )

    data["bmi"] = bmi_result["bmi"]
    data["bmi_category"] = bmi_result["category"]

    min_ideal, max_ideal = ideal_weight_range(profile.height)
    data["ideal_weight_min"] = min_ideal
    data["ideal_weight_max"] = max_ideal

    bmr = calculate_bmr(
        profile.age,
        profile.gender,
        profile.height,
        profile.weight
    )

    tdee = calculate_tdee(
        bmr,
        profile.activity_level
    )

    daily_calories = calorie_goal(
        tdee,
        profile.goal
    )

    macros = calculate_macros(
        daily_calories,
        profile.goal
    )

    data["protein"] = macros["protein"]
    data["carbohydrates"] = macros["carbohydrates"]
    data["fat"] = macros["fat"]

    data["bmr"] = bmr
    data["tdee"] = tdee
    data["daily_calories"] = daily_calories

    # Compute weight difference & estimated days to goal
    weight_diff = 0
    estimated_days = 0
    if profile.target_weight:
        weight_diff = abs(profile.weight - profile.target_weight)
        # Assume 0.5 kg/week max healthy loss/gain
        caloric_diff = abs(tdee - daily_calories)
        if caloric_diff > 0:
            # 7700 kcal ≈ 1 kg body fat
            estimated_days = round((weight_diff * 7700) / caloric_diff)

    data["weight_difference"] = weight_diff if profile.target_weight else None
    data["estimated_days_to_goal"] = estimated_days if profile.target_weight else None

    if user_id:
        data["user_id"] = user_id
        data["updated_at"] = datetime.now(timezone.utc)
        profiles.update_one(
            {"user_id": user_id},
            {"$set": data, "$setOnInsert": {"created_at": datetime.now(timezone.utc)}},
            upsert=True,
        )
        profile_id = profiles.find_one({"user_id": user_id})["_id"]
    else:
        result = profiles.insert_one(data)
        profile_id = result.inserted_id

    return {
        "success": True,
        "message": "Health profile saved successfully.",
        "bmi": bmi_result["bmi"],
        "category": bmi_result["category"],
        "bmr": bmr,
        "tdee": tdee,
        "daily_calories": daily_calories,
        "id": str(profile_id),
        "protein": macros["protein"],
        "carbohydrates": macros["carbohydrates"],
        "fat": macros["fat"],
        "ideal_weight_min": min_ideal,
        "ideal_weight_max": max_ideal,
        "weight_difference": data["weight_difference"],
        "estimated_days_to_goal": data["estimated_days_to_goal"],
    }
