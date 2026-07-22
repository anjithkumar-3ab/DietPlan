from pydantic import BaseModel, Field
from typing import Literal


class Food(BaseModel):
    name: str = Field(..., min_length=2)

    meal_type: Literal[
        "Breakfast",
        "Lunch",
        "Dinner",
        "Snack"
    ]

    food_preference: Literal[
        "Veg",
        "Non-Veg",
        "Any"
    ]

    calories: float
    protein: float
    carbohydrates: float
    fat: float