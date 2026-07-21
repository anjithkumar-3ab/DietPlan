"""
NutriAI Chart Components.

Reusable chart elements for displaying nutritional data and progress.
Uses Streamlit's built-in charting capabilities.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import streamlit as st
import pandas as pd


def macronutrient_pie(
    protein_g: float,
    carbs_g: float,
    fat_g: float,
    fiber_g: float = 0,
) -> None:
    """Display a macronutrient breakdown as a DataFrame-based visual.

    Args:
        protein_g: Protein in grams.
        carbs_g: Carbohydrates in grams.
        fat_g: Fat in grams.
        fiber_g: Fiber in grams (optional).
    """
    # Convert grams to calories (4 cal/g for protein & carbs, 9 cal/g for fat)
    protein_cal = protein_g * 4
    carbs_cal = carbs_g * 4
    fat_cal = fat_g * 9

    data = pd.DataFrame(
        {
            "Macronutrient": ["Protein", "Carbohydrates", "Fat"],
            "Grams": [protein_g, carbs_g, fat_g],
            "Calories": [protein_cal, carbs_cal, fat_cal],
        }
    )

    st.dataframe(
        data,
        column_config={
            "Macronutrient": "Macronutrient",
            "Grams": st.column_config.NumberColumn("Grams", format="%.1f g"),
            "Calories": st.column_config.NumberColumn("Calories", format="%.0f kcal"),
        },
        hide_index=True,
        use_container_width=True,
    )

    # Bar chart for visual representation
    chart_data = pd.DataFrame(
        {
            "Macronutrient": ["Protein", "Carbs", "Fat"],
            "Calories": [protein_cal, carbs_cal, fat_cal],
        }
    )
    st.bar_chart(chart_data, x="Macronutrient", y="Calories", height=250)


def daily_calorie_comparison(
    breakfast_cal: float,
    lunch_cal: float,
    dinner_cal: float,
    snack_cal: float,
    target_cal: float,
) -> None:
    """Display a daily calorie distribution chart.

    Args:
        breakfast_cal: Breakfast calories.
        lunch_cal: Lunch calories.
        dinner_cal: Dinner calories.
        snack_cal: Snack calories.
        target_cal: Target daily calories.
    """
    meals = ["Breakfast", "Lunch", "Dinner", "Snacks"]
    calories = [breakfast_cal, lunch_cal, dinner_cal, snack_cal]
    total = sum(calories)

    data = pd.DataFrame(
        {
            "Meal": meals,
            "Calories": calories,
            "% of Target": [round((c / target_cal) * 100, 1) if target_cal > 0 else 0
                            for c in calories],
        }
    )

    col1, col2 = st.columns([2, 1])
    with col1:
        st.bar_chart(data, x="Meal", y="Calories", height=250)
    with col2:
        st.metric("Total Consumed", f"{total:,.0f} kcal")
        st.metric("Target", f"{target_cal:,.0f} kcal")
        delta = total - target_cal
        st.metric("Difference", f"{delta:+,.0f} kcal")


def calories_over_time(
    history_records: List[Dict[str, Any]],
) -> None:
    """Display a line chart of calorie intake over time.

    Args:
        history_records: List of recommendation history records.
    """
    if not history_records:
        st.info("No history data available for charting.")
        return

    rows = []
    for record in history_records:
        created = record.get("created_at", "")
        daily_cal = record.get("daily_calories", 0)
        tdee = record.get("tdee", 0)
        bmi = record.get("bmi", 0)
        rows.append(
            {
                "date": created,
                "daily_calories": daily_cal,
                "tdee": tdee,
                "bmi": bmi,
            }
        )

    if not rows:
        st.info("Insufficient data for time series chart.")
        return

    df = pd.DataFrame(rows)

    # Convert date strings to datetime
    try:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
    except Exception:
        pass

    tab1, tab2 = st.tabs(["Calories", "BMI Trend"])

    with tab1:
        if "daily_calories" in df.columns and "tdee" in df.columns:
            chart_df = df[["date", "daily_calories", "tdee"]].copy()
            chart_df = chart_df.set_index("date")
            st.line_chart(chart_df, height=300)
        else:
            st.info("Calorie data not available.")

    with tab2:
        if "bmi" in df.columns:
            bmi_df = df[["date", "bmi"]].copy()
            bmi_df = bmi_df.set_index("date")
            st.line_chart(bmi_df, height=300)
        else:
            st.info("BMI data not available.")