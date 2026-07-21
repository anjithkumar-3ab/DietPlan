"""
NutriAI Metrics Components.

Reusable metric display components for health and nutrition data.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import streamlit as st

from frontend.utils.helpers import bmi_color


def render_bmi_gauge(bmi: float) -> None:
    """Render a BMI gauge with colour-coded category.

    Args:
        bmi: Body Mass Index value.
    """
    color = bmi_color(bmi)
    category = _bmi_label(bmi)

    st.markdown(
        f"""
        <div style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 0.75rem; color: #9CA3AF; text-transform: uppercase;
                        letter-spacing: 1px; margin-bottom: 0.25rem;">
                BMI
            </div>
            <div style="font-size: 2.5rem; font-weight: 800; color: {color};">
                {bmi:.1f}
            </div>
            <div style="font-size: 0.85rem; color: {color}; font-weight: 500;
                        margin-top: 0.25rem;">
                {category}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _bmi_label(bmi: float) -> str:
    """Return the BMI category label.

    Args:
        bmi: Body Mass Index value.

    Returns:
        Category string.
    """
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25.0:
        return "Normal Weight"
    if bmi < 30.0:
        return "Overweight"
    return "Obese"


def render_macro_bar(
    current: float,
    target: float,
    label: str,
    unit: str = "g",
    color: str = "#66BB6A",
) -> None:
    """Render a macro nutrient progress bar.

    Args:
        current: Current intake value.
        target: Target intake value.
        label: Macro name (e.g. Protein).
        unit: Unit string (g).
        color: Bar colour hex.
    """
    pct = min((current / target) * 100, 100) if target > 0 else 0
    st.markdown(
        f"""
        <div style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem;
                        margin-bottom: 0.3rem;">
                <span style="color: #D1D5DB;">{label}</span>
                <span style="color: #F5F5F5; font-weight: 600;">
                    {current:.1f} / {target:.1f} {unit}
                </span>
            </div>
            <div style="width: 100%; height: 8px; background: rgba(255,255,255,0.08);
                        border-radius: 4px; overflow: hidden;">
                <div style="width: {pct:.1f}%; height: 100%;
                            background: {color}; border-radius: 4px;
                            transition: width 0.5s ease;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_health_metrics_row(
    bmr: float,
    tdee: float,
    daily_calories: float,
    water_liters: float,
) -> None:
    """Render a row of health metric cards.

    Args:
        bmr: Basal Metabolic Rate.
        tdee: Total Daily Energy Expenditure.
        daily_calories: Target daily calories.
        water_liters: Recommended water intake.
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="BMR",
            value=f"{bmr:,.0f} kcal",
            help="Basal Metabolic Rate — calories at complete rest",
        )
    with col2:
        st.metric(
            label="TDEE",
            value=f"{tdee:,.0f} kcal",
            help="Total Daily Energy Expenditure",
        )
    with col3:
        st.metric(
            label="Daily Target",
            value=f"{daily_calories:,.0f} kcal",
            delta=f"{daily_calories - tdee:+,.0f} kcal vs TDEE",
            help="Recommended daily calorie intake",
        )
    with col4:
        st.metric(
            label="Water Intake",
            value=f"{water_liters:.1f} L",
            help="Recommended daily water consumption",
        )