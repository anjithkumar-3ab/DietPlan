"""
Chart Service – generates all Plotly chart JSON for the diet recommendation dashboard.

Each function returns a Plotly figure serialized as a JSON dict, ready to be
rendered on the frontend using Plotly.js. Uses Plotly dark theme consistently.
"""

from __future__ import annotations

import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import math
from typing import Any, Dict, List, Optional

# ── Colour palette (healthcare / dark theme) ─────────────────────────────

GREEN_PRIMARY = "#4ade80"
GREEN_DARK = "#22c55e"
GREEN_LIGHT = "#a3e635"
BLUE_INFO = "#60a5fa"
BLUE_LIGHT = "#93c5fd"
YELLOW_WARN = "#f59e0b"
YELLOW_LIGHT = "#fde68a"
RED_DANGER = "#ef4444"
RED_LIGHT = "#fca5a5"
PURPLE = "#a78bfa"
TEAL = "#2dd4bf"
ORANGE = "#fb923c"
PINK = "#f472b6"
CYAN = "#22d3ee"

# Theme colours
CARD_BG = "#1e1e32"
TEXT_LIGHT = "#e8e8f0"
TEXT_MUTED = "#6b6b80"
BORDER_COLOR = "#2a2a45"
PLOT_BG = "rgba(0,0,0,0)"
PAPER_BG = "rgba(0,0,0,0)"

# ── Unified dark-template layout helper ─────────────────────────────────

FONT_FAMILY = "'Segoe UI', system-ui, -apple-system, sans-serif"


def _theme_layout(
    title: str = "",
    height: int = 300,
    show_legend: bool = False,
    margin: Optional[Dict[str, int]] = None,
) -> Dict[str, Any]:
    """Return a consistent dark-themed layout dict for all charts."""
    if margin is None:
        margin = dict(l=40, r=40, t=50, b=40)
    return {
        "title": {
            "text": title,
            "font": {"color": TEXT_LIGHT, "size": 14, "family": FONT_FAMILY},
            "x": 0.5,
            "xanchor": "center",
        },
        "paper_bgcolor": PAPER_BG,
        "plot_bgcolor": PLOT_BG,
        "font": {"color": TEXT_MUTED, "size": 11, "family": FONT_FAMILY},
        "margin": margin,
        "height": height,
        "showlegend": show_legend,
        "hovermode": "closest",
        "transition": {"duration": 500, "easing": "cubic-in-out"},
        "xaxis": {
            "gridcolor": BORDER_COLOR,
            "zerolinecolor": BORDER_COLOR,
            "color": TEXT_MUTED,
            "automargin": True,
        },
        "yaxis": {
            "gridcolor": BORDER_COLOR,
            "zerolinecolor": BORDER_COLOR,
            "color": TEXT_MUTED,
            "automargin": True,
        },
    }


# ═══════════════════════════════════════════════════════════════════════
# 1. Macronutrient Doughnut Chart
# ═══════════════════════════════════════════════════════════════════════

def create_macro_chart(
    protein_g: float,
    carbs_g: float,
    fat_g: float,
) -> Dict[str, Any]:
    """
    Plotly Doughnut Chart showing Protein / Carbohydrates / Fat split.
    Shows total calories in centre annotation.
    """
    total = protein_g + carbs_g + fat_g
    total_cal = (protein_g * 4) + (carbs_g * 4) + (fat_g * 9)
    if total == 0:
        total = 1

    labels = [
        f"Protein ({protein_g:.1f}g)",
        f"Carbohydrates ({carbs_g:.1f}g)",
        f"Fat ({fat_g:.1f}g)",
    ]
    values = [protein_g, carbs_g, fat_g]
    colors = [BLUE_INFO, YELLOW_WARN, RED_DANGER]

    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        hole=0.65,
        marker=dict(colors=colors, line=dict(color=CARD_BG, width=3)),
        textinfo="label+percent",
        textfont=dict(color=TEXT_LIGHT, size=10, family=FONT_FAMILY),
        hoverinfo="label+value+percent",
        hovertemplate="<b>%{label}</b><br>Grams: %{value:.1f}g<br>%{percent}<extra></extra>",
        sort=False,
        direction="clockwise",
        rotation=90,
    ))

    # Total calories annotation in centre
    fig.add_annotation(
        text=f"<b>{total_cal:,.0f}</b><br><span style='font-size:10px;color:{TEXT_MUTED};'>kcal</span>",
        x=0.5, y=0.5,
        xref="paper", yref="paper",
        showarrow=False,
        font=dict(color=TEXT_LIGHT, size=20, family=FONT_FAMILY),
        align="center",
    )

    fig.update_layout(
        **_theme_layout("Macronutrient Split", height=320, show_legend=False,
                        margin=dict(l=10, r=10, t=50, b=10)),
    )
    return fig.to_dict()


# ═══════════════════════════════════════════════════════════════════════
# 2. Calorie Distribution Bar Chart
# ═══════════════════════════════════════════════════════════════════════

def create_calorie_chart(
    breakfast_kcal: float,
    lunch_kcal: float,
    snack_kcal: float,
    dinner_kcal: float,
) -> Dict[str, Any]:
    """
    Plotly Bar Chart with rounded bars, value labels, and hover.
    """
    meals = ["Breakfast", "Lunch", "Snack", "Dinner"]
    cals = [breakfast_kcal, lunch_kcal, snack_kcal, dinner_kcal]
    colors_list = [YELLOW_WARN, BLUE_INFO, GREEN_PRIMARY, RED_DANGER]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=meals,
        y=cals,
        marker=dict(
            color=colors_list,
            line=dict(color=TEXT_LIGHT, width=0),
            # Simulate rounded corners via border-radius-like shape
            cornerradius=8,
        ),
        text=[f"{c:.0f} kcal" for c in cals],
        textposition="outside",
        textfont=dict(color=TEXT_LIGHT, size=11, family=FONT_FAMILY),
        hovertemplate="<b>%{x}</b><br>Calories: %{y:.0f} kcal<extra></extra>",
    ))

    layout = _theme_layout("Calorie Distribution per Meal", height=300, show_legend=False)
    layout["yaxis"] = dict(
        title=dict(text="Calories (kcal)", font=dict(color=TEXT_MUTED, size=11, family=FONT_FAMILY)),
        gridcolor=BORDER_COLOR,
        color=TEXT_MUTED,
        rangemode="nonnegative",
    )
    layout["xaxis"] = dict(
        title=dict(text="", font=dict(color=TEXT_MUTED)),
        color=TEXT_MUTED,
    )
    layout["bargap"] = 0.45
    fig.update_layout(**layout)
    return fig.to_dict()


# ═══════════════════════════════════════════════════════════════════════
# 3. Nutrition Balance Radar Chart
# ═══════════════════════════════════════════════════════════════════════

def create_radar_chart(
    protein_g: float,
    carbs_g: float,
    fat_g: float,
    fiber_g: float,
    iron_mg: float = 8.0,
    calcium_mg: float = 500.0,
    vitamin_c_mg: float = 60.0,
) -> Dict[str, Any]:
    """
    Plotly Radar (Scatterpolar) showing nutrition balance.
    Fill polygon with transparency.
    """
    targets = {
        "Protein": 60, "Carbs": 250, "Fat": 65, "Fiber": 30,
        "Iron": 18, "Calcium": 1000, "Vitamin C": 90,
    }
    actual_values = {
        "Protein": min(100, (protein_g / targets["Protein"]) * 100),
        "Carbs": min(100, (carbs_g / targets["Carbs"]) * 100),
        "Fat": min(100, (fat_g / targets["Fat"]) * 100),
        "Fiber": min(100, (fiber_g / targets["Fiber"]) * 100),
        "Iron": min(100, (iron_mg / targets["Iron"]) * 100),
        "Calcium": min(100, (calcium_mg / targets["Calcium"]) * 100),
        "Vitamin C": min(100, (vitamin_c_mg / targets["Vitamin C"]) * 100),
    }
    categories = list(targets.keys())
    current_r = [actual_values[c] for c in categories]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=current_r,
        theta=categories,
        fill="toself",
        name="Current Intake",
        line=dict(color=GREEN_PRIMARY, width=2),
        fillcolor="rgba(74, 222, 128, 0.15)",
        hovertemplate="<b>%{theta}</b><br>%{r:.1f}% of target<extra></extra>",
    ))
    fig.add_trace(go.Scatterpolar(
        r=[100] * len(categories),
        theta=categories,
        fill="toself",
        name="Target (100%)",
        line=dict(color=TEXT_MUTED, width=1, dash="dash"),
        fillcolor="rgba(107, 107, 128, 0.08)",
        hovertemplate="<b>%{theta}</b><br>Target<extra></extra>",
    ))

    fig.update_layout(
        **_theme_layout("Nutrition Balance", height=340, show_legend=True,
                        margin=dict(l=60, r=60, t=50, b=50)),
        polar=dict(
            bgcolor=PLOT_BG,
            angularaxis=dict(
                color=TEXT_MUTED, linecolor=BORDER_COLOR,
                gridcolor=BORDER_COLOR, dtick=1,
            ),
            radialaxis=dict(
                range=[0, 110], color=TEXT_MUTED,
                gridcolor=BORDER_COLOR, linecolor=BORDER_COLOR,
                showticklabels=True, ticksuffix="%",
            ),
        ),
        legend=dict(
            font=dict(color=TEXT_MUTED, size=9, family=FONT_FAMILY),
            orientation="h", yanchor="bottom", y=-0.3,
            xanchor="center", x=0.5,
        ),
    )
    return fig.to_dict()


# ═══════════════════════════════════════════════════════════════════════
# 4. BMI Gauge Chart
# ═══════════════════════════════════════════════════════════════════════

def create_bmi_gauge(bmi: float) -> Dict[str, Any]:
    """
    Plotly Gauge Indicator for BMI with color-coded ranges.
    Blue (underweight) → Green (normal) → Orange (overweight) → Red (obese).
    """
    # Determine dominant colour
    if bmi < 18.5:
        dominant_color = BLUE_INFO
    elif bmi < 25:
        dominant_color = GREEN_PRIMARY
    elif bmi < 30:
        dominant_color = YELLOW_WARN
    else:
        dominant_color = RED_DANGER

    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=bmi,
        number={
            "suffix": "",
            "font": {"color": TEXT_LIGHT, "size": 32, "family": FONT_FAMILY},
            "valueformat": ".1f",
        },
        gauge={
            "axis": {
                "range": [10, 45],
                "tickwidth": 1, "tickcolor": TEXT_MUTED,
                "tickfont": {"color": TEXT_MUTED, "size": 9, "family": FONT_FAMILY},
                "dtick": 5,
            },
            "bar": {"color": dominant_color, "thickness": 0.45,
                    "line": {"color": dominant_color, "width": 2}},
            "bgcolor": PLOT_BG,
            "borderwidth": 0,
            "bordercolor": BORDER_COLOR,
            "steps": [
                {"range": [10, 18.5], "color": "rgba(96, 165, 250, 0.25)"},
                {"range": [18.5, 25], "color": "rgba(74, 222, 128, 0.25)"},
                {"range": [25, 30], "color": "rgba(245, 158, 11, 0.25)"},
                {"range": [30, 45], "color": "rgba(239, 68, 68, 0.25)"},
            ],
            "threshold": {
                "line": {"color": dominant_color, "width": 3},
                "thickness": 0.7, "value": bmi,
            },
        },
    ))

    fig.update_layout(
        **_theme_layout("Body Mass Index (BMI)", height=260, show_legend=False,
                        margin=dict(l=20, r=20, t=50, b=20)),
    )
    return fig.to_dict()


# ═══════════════════════════════════════════════════════════════════════
# 5. Calorie Progress Gauge
# ═══════════════════════════════════════════════════════════════════════

def create_calorie_gauge(
    current_calories: float,
    target_calories: float,
) -> Dict[str, Any]:
    """
    Plotly Indicator Gauge showing consumed vs target.
    Green if within target, Orange close, Red if exceeded.
    """
    remaining = max(0, target_calories - current_calories)
    pct = min(100, (current_calories / max(target_calories, 1)) * 100)

    # Bar colour based on progress
    if pct <= 85:
        bar_color = GREEN_PRIMARY
    elif pct <= 100:
        bar_color = YELLOW_WARN
    else:
        bar_color = RED_DANGER

    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=current_calories,
        number={
            "suffix": " kcal",
            "font": {"color": TEXT_LIGHT, "size": 26, "family": FONT_FAMILY},
            "valueformat": ".0f",
        },
        delta={
            "reference": target_calories,
            "position": "top",
            "relative": False,
            "valueformat": ".0f",
            "font": {"color": TEXT_MUTED, "size": 10, "family": FONT_FAMILY},
        },
        gauge={
            "axis": {
                "range": [0, max(target_calories * 1.2, 100)],
                "tickwidth": 1, "tickcolor": TEXT_MUTED,
                "tickfont": {"color": TEXT_MUTED, "size": 8, "family": FONT_FAMILY},
                "dtick": max(200, round(target_calories / 4, -2)),
            },
            "bar": {"color": bar_color, "thickness": 0.4,
                    "line": {"color": bar_color, "width": 2}},
            "bgcolor": PLOT_BG,
            "borderwidth": 0,
            "bordercolor": BORDER_COLOR,
            "steps": [
                {"range": [0, target_calories * 0.5],
                 "color": "rgba(74, 222, 128, 0.15)"},
                {"range": [target_calories * 0.5, target_calories * 0.85],
                 "color": "rgba(245, 158, 11, 0.15)"},
                {"range": [target_calories * 0.85, target_calories * 1.2],
                 "color": "rgba(239, 68, 68, 0.15)"},
            ],
            "threshold": {
                "line": {"color": bar_color, "width": 3},
                "thickness": 0.6, "value": current_calories,
            },
        },
    ))

    fig.add_annotation(
        text=f"Remaining: {remaining:.0f} kcal  |  {pct:.1f}%",
        x=0.5, y=-0.15, xref="paper", yref="paper",
        showarrow=False,
        font=dict(color=TEXT_MUTED, size=11, family=FONT_FAMILY),
    )

    fig.update_layout(
        **_theme_layout("Calorie Progress", height=280, show_legend=False,
                        margin=dict(l=20, r=20, t=50, b=40)),
    )
    return fig.to_dict()


# ═══════════════════════════════════════════════════════════════════════
# 6. Water Intake Gauge
# ═══════════════════════════════════════════════════════════════════════

def create_water_gauge(
    water_liters: float,
    target_liters: float = 2.5,
) -> Dict[str, Any]:
    """
    Plotly Indicator showing water intake as a circular progress gauge.
    """
    pct = min(100, (water_liters / max(target_liters, 0.1)) * 100)

    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=water_liters,
        number={
            "suffix": "L",
            "font": {"color": BLUE_INFO, "size": 24, "family": FONT_FAMILY},
            "valueformat": ".1f",
        },
        gauge={
            "axis": {
                "range": [0, max(target_liters * 1.3, 3.0)],
                "tickwidth": 1, "tickcolor": TEXT_MUTED,
                "tickfont": {"color": TEXT_MUTED, "size": 8, "family": FONT_FAMILY},
                "dtick": 0.5,
            },
            "bar": {"color": BLUE_INFO, "thickness": 0.4,
                    "line": {"color": BLUE_INFO, "width": 2}},
            "bgcolor": PLOT_BG,
            "borderwidth": 0,
            "bordercolor": BORDER_COLOR,
            "steps": [
                {"range": [0, target_liters], "color": "rgba(96, 165, 250, 0.15)"},
                {"range": [target_liters, target_liters * 1.3],
                 "color": "rgba(96, 165, 250, 0.05)"},
            ],
            "threshold": {
                "line": {"color": BLUE_LIGHT, "width": 3},
                "thickness": 0.7, "value": water_liters,
            },
        },
    ))

    fig.add_annotation(
        text=f"Target: {target_liters:.1f}L",
        x=0.5, y=-0.12, xref="paper", yref="paper",
        showarrow=False,
        font=dict(color=TEXT_MUTED, size=10, family=FONT_FAMILY),
    )

    fig.update_layout(
        **_theme_layout("Water Intake", height=240, show_legend=False,
                        margin=dict(l=20, r=20, t=50, b=30)),
    )
    return fig.to_dict()


# ═══════════════════════════════════════════════════════════════════════
# 7. Meal Nutrition Stacked Bar Chart
# ═══════════════════════════════════════════════════════════════════════

def create_stacked_bar(
    breakfast_protein: float, breakfast_carbs: float, breakfast_fat: float,
    lunch_protein: float, lunch_carbs: float, lunch_fat: float,
    snack_protein: float, snack_carbs: float, snack_fat: float,
    dinner_protein: float, dinner_carbs: float, dinner_fat: float,
) -> Dict[str, Any]:
    """
    Plotly Stacked Bar Chart showing Protein / Carbs / Fat per meal.
    """
    meals = ["Breakfast", "Lunch", "Snack", "Dinner"]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Protein", x=meals,
        y=[breakfast_protein, lunch_protein, snack_protein, dinner_protein],
        marker=dict(color=BLUE_INFO, line=dict(color=CARD_BG, width=1)),
        hovertemplate="<b>%{x}</b><br>Protein: %{y:.1f}g<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Carbs", x=meals,
        y=[breakfast_carbs, lunch_carbs, snack_carbs, dinner_carbs],
        marker=dict(color=YELLOW_WARN, line=dict(color=CARD_BG, width=1)),
        hovertemplate="<b>%{x}</b><br>Carbs: %{y:.1f}g<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Fat", x=meals,
        y=[breakfast_fat, lunch_fat, snack_fat, dinner_fat],
        marker=dict(color=RED_DANGER, line=dict(color=CARD_BG, width=1)),
        hovertemplate="<b>%{x}</b><br>Fat: %{y:.1f}g<extra></extra>",
    ))

    fig.update_layout(
        barmode="stack",
        **_theme_layout("Meal Nutrition Breakdown", height=300, show_legend=True,
                        margin=dict(l=40, r=40, t=50, b=40)),
        legend=dict(
            font=dict(color=TEXT_MUTED, size=9, family=FONT_FAMILY),
            orientation="h", yanchor="bottom", y=-0.25,
            xanchor="center", x=0.5,
        ),
        yaxis=dict(
            title=dict(text="Grams (g)", font=dict(color=TEXT_MUTED, size=11, family=FONT_FAMILY)),
            gridcolor=BORDER_COLOR, color=TEXT_MUTED,
        ),
        xaxis=dict(title=dict(text=""), color=TEXT_MUTED),
        bargap=0.3,
    )
    return fig.to_dict()


# ═══════════════════════════════════════════════════════════════════════
# 8. Meal Timeline Chart
# ═══════════════════════════════════════════════════════════════════════

def create_timeline(
    breakfast_kcal: float = 0, breakfast_items: int = 0,
    lunch_kcal: float = 0, lunch_items: int = 0,
    snack_kcal: float = 0, snack_items: int = 0,
    dinner_kcal: float = 0, dinner_items: int = 0,
) -> Dict[str, Any]:
    """
    Plotly Timeline (horizontal bar) showing meal schedule with calories.
    """
    meals = ["Breakfast", "Lunch", "Snack", "Dinner"]
    cals = [breakfast_kcal, lunch_kcal, snack_kcal, dinner_kcal]
    items_counts = [breakfast_items, lunch_items, snack_items, dinner_items]
    colors = [YELLOW_WARN, BLUE_INFO, GREEN_PRIMARY, RED_DANGER]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=cals,
        y=meals,
        orientation="h",
        cliponaxis=False,
        marker=dict(
            color=colors,
            line=dict(color=CARD_BG, width=2),
            cornerradius=6,
        ),
        text=[f"{c:.0f} kcal ({i} items)" for c, i in zip(cals, items_counts)],
        textposition="outside",
        textfont=dict(color=TEXT_LIGHT, size=10, family=FONT_FAMILY),
        hovertemplate="<b>%{y}</b><br>Calories: %{x:.0f} kcal<br>Items: %{customdata}<extra></extra>",
        customdata=items_counts,
    ))

    layout = _theme_layout("Meal Timeline", height=280, show_legend=False,
                           margin=dict(l=80, r=80, t=50, b=20))
    layout["xaxis"] = dict(
        title=dict(text="Calories (kcal)", font=dict(color=TEXT_MUTED, size=11)),
        gridcolor=BORDER_COLOR, color=TEXT_MUTED,
        zerolinecolor=BORDER_COLOR,
    )
    layout["yaxis"] = dict(
        title=dict(text="", font=dict(color=TEXT_MUTED)),
        color=TEXT_LIGHT,
        autorange="reversed",
    )
    fig.update_layout(**layout)
    return fig.to_dict()


# ═══════════════════════════════════════════════════════════════════════
# 9. Calories vs Goal Bullet Chart
# ═══════════════════════════════════════════════════════════════════════

def create_bullet_chart(
    current_calories: float,
    target_calories: float,
    tdee: float,
) -> Dict[str, Any]:
    """
    Plotly Bullet-style chart comparing target, recommended, and current calories.
    Uses an indicator with gauge mode styled as a bullet.
    """
    max_val = max(target_calories, tdee, current_calories) * 1.2

    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number+gauge+delta",
        value=current_calories,
        number={
            "suffix": " kcal",
            "font": {"color": TEXT_LIGHT, "size": 24, "family": FONT_FAMILY},
            "valueformat": ".0f",
        },
        delta={
            "reference": target_calories,
            "position": "top",
            "relative": False,
            "valueformat": ".0f",
            "font": {"color": TEXT_MUTED, "size": 10, "family": FONT_FAMILY},
        },
        gauge={
            "axis": {
                "range": [0, max_val],
                "tickwidth": 1, "tickcolor": TEXT_MUTED,
                "tickfont": {"color": TEXT_MUTED, "size": 8, "family": FONT_FAMILY},
            },
            "bar": {"color": GREEN_PRIMARY, "thickness": 0.3},
            "bgcolor": PLOT_BG,
            "borderwidth": 0,
            "steps": [
                {"range": [0, target_calories],
                 "color": "rgba(74, 222, 128, 0.12)"},
                {"range": [target_calories, tdee],
                 "color": "rgba(245, 158, 11, 0.12)"},
                {"range": [tdee, max_val],
                 "color": "rgba(239, 68, 68, 0.12)"},
            ],
            "threshold": {
                "line": {"color": GREEN_PRIMARY, "width": 3},
                "thickness": 0.6, "value": current_calories,
            },
        },
    ))

    # Annotations
    fig.add_annotation(
        text=f"Target: {target_calories:,.0f} kcal",
        x=0, y=-0.15, xref="paper", yref="paper",
        showarrow=False, xanchor="left",
        font=dict(color=TEXT_MUTED, size=10, family=FONT_FAMILY),
    )
    fig.add_annotation(
        text=f"TDEE: {tdee:,.0f} kcal",
        x=1, y=-0.15, xref="paper", yref="paper",
        showarrow=False, xanchor="right",
        font=dict(color=TEXT_MUTED, size=10, family=FONT_FAMILY),
    )

    fig.update_layout(
        **_theme_layout("Calories vs Goal", height=240, show_legend=False,
                        margin=dict(l=20, r=20, t=50, b=40)),
    )
    return fig.to_dict()


# ═══════════════════════════════════════════════════════════════════════
# 10. Nutrient Summary Sunburst Chart
# ═══════════════════════════════════════════════════════════════════════

def create_sunburst(
    protein_g: float,
    carbs_g: float,
    fat_g: float,
    fiber_g: float,
    sugar_g: float = 0,
    sodium_mg: float = 0,
) -> Dict[str, Any]:
    """
    Plotly Sunburst Chart showing nutrient hierarchy.
    Root: Nutrition → Children: Protein, Carbs, Fat, Fiber, Sugar, Sodium.
    """
    # Map g to kcal for visual proportion
    protein_kcal = protein_g * 4
    carbs_kcal = carbs_g * 4
    fat_kcal = fat_g * 9
    fiber_kcal = fiber_g * 2
    sugar_kcal = sugar_g * 4
    # Sodium doesn't contribute calories but we show it as a leaf
    total_kcal = max(protein_kcal + carbs_kcal + fat_kcal + fiber_kcal + sugar_kcal, 1)

    labels = [
        "Nutrition",
        "Protein", "Carbohydrates", "Fat", "Fiber", "Sugar", "Sodium",
    ]
    parents = [
        "",
        "Nutrition", "Nutrition", "Nutrition", "Nutrition", "Nutrition", "Nutrition",
    ]
    values = [
        total_kcal,
        protein_kcal, carbs_kcal, fat_kcal, fiber_kcal, sugar_kcal,
        max(sodium_mg * 0.001, 10),  # minimal visual presence
    ]
    colors = [
        TEXT_MUTED,
        BLUE_INFO, YELLOW_WARN, RED_DANGER, GREEN_PRIMARY, PINK, ORANGE,
    ]

    # Hover text
    hover_text = [
        f"Total: {total_kcal:,.0f} kcal",
        f"Protein: {protein_g:.1f}g ({protein_kcal:.0f} kcal)",
        f"Carbs: {carbs_g:.1f}g ({carbs_kcal:.0f} kcal)",
        f"Fat: {fat_g:.1f}g ({fat_kcal:.0f} kcal)",
        f"Fiber: {fiber_g:.1f}g ({fiber_kcal:.0f} kcal)",
        f"Sugar: {sugar_g:.1f}g ({sugar_kcal:.0f} kcal)",
        f"Sodium: {sodium_mg:.1f}mg",
    ]

    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(colors=colors, line=dict(color=CARD_BG, width=2)),
        textinfo="label+percent entry",
        textfont=dict(color=TEXT_LIGHT, size=10, family=FONT_FAMILY),
        hovertext=hover_text,
        hovertemplate="<b>%{label}</b><br>%{customdata}<extra></extra>",
        customdata=hover_text,
        branchvalues="total",
        maxdepth=2,
    ))

    fig.update_layout(
        **_theme_layout("Nutrient Summary", height=340, show_legend=False,
                        margin=dict(l=10, r=10, t=50, b=10)),
    )
    return fig.to_dict()


# ═══════════════════════════════════════════════════════════════════════
# Full Dashboard Charts Bundle
# ═══════════════════════════════════════════════════════════════════════

def generate_dashboard_charts(
    bmi: float,
    protein_g: float,
    carbs_g: float,
    fat_g: float,
    fiber_g: float,
    breakfast_kcal: float,
    lunch_kcal: float,
    snack_kcal: float,
    dinner_kcal: float,
    current_calories: float,
    target_calories: float,
    tdee: float = 2200.0,
    water_liters: float = 2.0,
    breakfast_protein: float = 0,
    breakfast_carbs: float = 0,
    breakfast_fat: float = 0,
    lunch_protein: float = 0,
    lunch_carbs: float = 0,
    lunch_fat: float = 0,
    snack_protein: float = 0,
    snack_carbs: float = 0,
    snack_fat: float = 0,
    dinner_protein: float = 0,
    dinner_carbs: float = 0,
    dinner_fat: float = 0,
    breakfast_items: int = 0,
    lunch_items: int = 0,
    snack_items: int = 0,
    dinner_items: int = 0,
    sugar_g: float = 0,
    sodium_mg: float = 0,
) -> Dict[str, Any]:
    """
    Generate all 10 Plotly charts for the diet recommendation dashboard.

    Returns a dict with keys:
        macronutrient_doughnut, meal_calorie_distribution,
        nutrition_balance_radar, bmi_gauge, calorie_progress_gauge,
        water_gauge, stacked_bar, timeline, bullet_chart, sunburst
    """
    return {
        "macronutrient_doughnut": create_macro_chart(protein_g, carbs_g, fat_g),
        "meal_calorie_distribution": create_calorie_chart(
            breakfast_kcal, lunch_kcal, snack_kcal, dinner_kcal
        ),
        "nutrition_balance_radar": create_radar_chart(
            protein_g, carbs_g, fat_g, fiber_g
        ),
        "bmi_gauge": create_bmi_gauge(bmi),
        "calorie_progress_gauge": create_calorie_gauge(current_calories, target_calories),
        "water_gauge": create_water_gauge(water_liters),
        "stacked_bar": create_stacked_bar(
            breakfast_protein, breakfast_carbs, breakfast_fat,
            lunch_protein, lunch_carbs, lunch_fat,
            snack_protein, snack_carbs, snack_fat,
            dinner_protein, dinner_carbs, dinner_fat,
        ),
        "timeline": create_timeline(
            breakfast_kcal, breakfast_items,
            lunch_kcal, lunch_items,
            snack_kcal, snack_items,
            dinner_kcal, dinner_items,
        ),
        "bullet_chart": create_bullet_chart(current_calories, target_calories, tdee),
        "sunburst": create_sunburst(protein_g, carbs_g, fat_g, fiber_g, sugar_g, sodium_mg),
    }