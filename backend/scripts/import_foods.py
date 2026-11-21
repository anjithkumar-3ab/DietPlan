import os
import sys
from pathlib import Path
import pandas as pd

backend_root = Path(__file__).resolve().parents[1]
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

from app.database.database import client, db

collection = db["foods"]

project_root = Path(__file__).resolve().parents[2]
processed_path = project_root / "backend" / "data" / "processed" / "foods_clean.csv"
dataset_candidates = [
    processed_path,
    project_root / "Dataset" / "Nutri.csv",
    project_root / "Dataset" / "Food.csv",
]
csv_path = next((path for path in dataset_candidates if path.exists()), None)
if csv_path is None:
    raise FileNotFoundError(
        "No food dataset found. Add Dataset/Food.csv or Dataset/Nutri.csv."
    )

print(f"Loading: {csv_path}")

df = pd.read_csv(csv_path)

# The repository ships Nutri.csv as the source dataset. Normalize it when a
# preprocessed export is not available yet.
df.rename(
    columns={
        "food": "food_name",
        "Caloric Value": "calories",
        "Protein": "protein",
        "Carbohydrates": "carbohydrates",
        "Fat": "fat",
        "Dietary Fiber": "fiber",
        "Sugars": "sugar",
        "Sodium": "sodium",
    },
    inplace=True,
)

required_columns = [
    "food_name", "calories", "protein", "carbohydrates", "fat",
    "fiber", "sugar", "sodium",
]
missing_columns = [column for column in required_columns if column not in df]
if missing_columns:
    raise ValueError(f"Dataset is missing required columns: {missing_columns}")

for column in required_columns[1:]:
    df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

df["food_name"] = df["food_name"].astype(str).str.strip().str.title()
df["meal_type"] = "Lunch"
df["food_preference"] = "Veg"
df["allergens"] = "None"
df["category"] = "General"

breakfast_keywords = ("Egg", "Bread", "Milk", "Oat", "Cereal", "Yogurt", "Cheese")
snack_keywords = ("Apple", "Banana", "Orange", "Grape", "Peanut", "Almond", "Cashew", "Walnut")
non_veg_keywords = ("Chicken", "Fish", "Beef", "Pork", "Turkey", "Shrimp", "Crab", "Lamb", "Mutton")
dinner_keywords = ("Rice", "Pasta", "Curry", "Soup", "Noodle", "Pizza", "Stew")

for index, food_name in df["food_name"].items():
    if any(keyword in food_name for keyword in breakfast_keywords):
        df.at[index, "meal_type"] = "Breakfast"
    elif any(keyword in food_name for keyword in snack_keywords):
        df.at[index, "meal_type"] = "Snack"
    elif any(keyword in food_name for keyword in dinner_keywords):
        df.at[index, "meal_type"] = "Dinner"
    if any(keyword in food_name for keyword in non_veg_keywords):
        df.at[index, "food_preference"] = "Non-Veg"

records = df.to_dict(orient="records")

collection.delete_many({})

if records:
    collection.insert_many(records)

print(f"✅ Imported {len(records)} food records into MongoDB Atlas.")