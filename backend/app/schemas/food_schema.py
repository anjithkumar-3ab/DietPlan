from pydantic import BaseModel, Field
from typing import Literal, Optional


class Food(BaseModel):
    food_name: str = Field(..., min_length=2)
    name: Optional[str] = None

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
    fiber: Optional[float] = 0
    sugar: Optional[float] = 0
    sodium: Optional[float] = 0
    allergens: Optional[str] = "None"
    category: Optional[str] = "General"