def calculate_macros(calories, goal):
    """
    Calculate daily macronutrients.

    Normalises goal strings to handle both recommendation_schema.Goal enum
    values and profile_schema.HealthProfile.goal values.

    Protein = 4 kcal/g
    Carbs   = 4 kcal/g
    Fat     = 9 kcal/g
    """

    # Normalise goal string
    if goal in ("Weight Loss", "Lose Weight"):
        protein_ratio = 0.35
        carbs_ratio = 0.35
        fat_ratio = 0.30

    elif goal in ("Weight Gain", "Gain Weight", "Muscle Gain"):
        protein_ratio = 0.25
        carbs_ratio = 0.50
        fat_ratio = 0.25

    else:
        protein_ratio = 0.30
        carbs_ratio = 0.45
        fat_ratio = 0.25

    protein = round((calories * protein_ratio) / 4, 1)
    carbs = round((calories * carbs_ratio) / 4, 1)
    fat = round((calories * fat_ratio) / 9, 1)

    return {
        "protein": protein,
        "carbohydrates": carbs,
        "fat": fat
    }
