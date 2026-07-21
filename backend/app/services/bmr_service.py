def calculate_bmr(age, gender, height, weight):
    """
    Mifflin-St Jeor Equation
    height -> cm
    weight -> kg
    """

    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    return round(bmr, 2)


def calculate_tdee(bmr, activity_level):

    # Normalise activity level keys to handle both recommendation_schema enum
    # values and profile_schema values.
    _ACTIVITY_MAP = {
        # recommendation_schema.ActivityLevel values
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9,
        # profile_schema.HealthProfile.activity_level values
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.9,  # same factor as "Active" in enums, but we use the profile mapping
        "Athlete": 1.9,
    }

    return round(bmr * _ACTIVITY_MAP[activity_level], 2)


def calorie_goal(tdee, goal):

    # Normalise goal to handle both recommendation_schema.Goal enum values
    # and profile_schema.HealthProfile.goal values.
    if goal in ("Weight Loss", "Lose Weight"):
        return round(tdee - 500, 2)

    elif goal in ("Weight Gain", "Gain Weight", "Muscle Gain"):
        return round(tdee + 500, 2)

    return round(tdee, 2)
