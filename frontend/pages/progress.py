"""
NutriAI Progress Page.

Track your health metrics over time, including BMI trends,
calorie history, and weight progress.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import streamlit as st

from frontend.utils.helpers import (
    get,
    format_bmi_category,
    bmi_color,
    format_date,
)
from frontend.components.cards import glass_card, info_card, empty_state_card
from frontend.components.navbar import render_header
from frontend.components.metrics import render_bmi_gauge
from frontend.components.charts import calories_over_time
from frontend.services.api import get_history, get_cached_history, api_available


def show() -> None:
    """Render the progress tracking page."""
    render_header("Progress")

    if not api_available():
        st.warning(
            "⚠️ Backend API is not reachable. Progress data may not be available."
        )

    # Load history for charting
    with st.spinner("Loading progress data..."):
        try:
            history = get_history(limit=100)
        except Exception as exc:
            st.error(f"❌ Failed to load progress data: {exc}")
            history = None

    recommendations = []
    if history and history.get("recommendations"):
        recommendations = history["recommendations"]

    if not recommendations:
        empty_state_card(
            "No Progress Data",
            "Generate some diet plans first to see your progress tracked over time.",
            emoji="📈",
        )
        if st.button("🥗 Generate Diet Plan", type="primary", use_container_width=True):
            st.session_state["page"] = "🥗 Diet Planner"
            st.rerun()
        return

    # Summary stats
    _render_summary_stats(recommendations)

    # Charts
    st.markdown("### Trends Over Time")
    calories_over_time(recommendations)

    # Historical BMI table
    st.markdown("### Historical Records")
    _render_history_table(recommendations)


def _render_summary_stats(recommendations: List[Dict[str, Any]]) -> None:
    """Render summary statistics from history.

    Args:
        recommendations: List of recommendation records.
    """
    if not recommendations:
        return

    # Get latest and earliest
    latest = recommendations[0]
    earliest = recommendations[-1]

    latest_bmi = latest.get("bmi", 0)
    earliest_bmi = earliest.get("bmi", 0)
    bmi_change = latest_bmi - earliest_bmi

    latest_calories = latest.get("daily_calories", 0)
    earliest_calories = earliest.get("daily_calories", 0)
    cal_change = latest_calories - earliest_calories

    total_plans = len(recommendations)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Current BMI",
            f"{latest_bmi:.1f}",
            delta=f"{bmi_change:+.1f}",
            help=f"{format_bmi_category(latest_bmi)}",
        )
    with col2:
        st.metric(
            "Daily Calories",
            f"{latest_calories:,.0f} kcal",
            delta=f"{cal_change:+,.0f}",
            help="Latest vs earliest daily calorie target",
        )
    with col3:
        st.metric(
            "Total Plans",
            str(total_plans),
            help="Total number of diet plans generated",
        )
    with col4:
        latest_protein = latest.get("target_protein", 0)
        st.metric(
            "Protein Target",
            f"{latest_protein:.0f}g",
            help="Latest protein target",
        )


def _render_history_table(recommendations: List[Dict[str, Any]]) -> None:
    """Render a table of historical records.

    Args:
        recommendations: List of recommendation records.
    """
    table_data = []
    for rec in recommendations:
        created = rec.get("created_at", "")
        date_str = format_date(created) if created else "N/A"
        bmi = rec.get("bmi", 0)
        category = format_bmi_category(bmi)
        color = bmi_color(bmi)
        daily_cal = rec.get("daily_calories", 0)

        table_data.append(
            {
                "Date": date_str,
                "BMI": f"{bmi:.1f}",
                "Category": f'<span style="color: {color};">{category}</span>',
                "Calories": f"{daily_cal:,.0f} kcal",
            }
        )

    if table_data:
        st.markdown(
            "<div class='glass-card' style='padding: 1rem; overflow-x: auto;'>",
            unsafe_allow_html=True,
        )

        html_rows = ""
        for row in table_data:
            html_rows += (
                f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.04);'>"
                f"<td style='padding: 0.5rem; color: #D1D5DB;'>{row['Date']}</td>"
                f"<td style='padding: 0.5rem; color: #F5F5F5; font-weight: 500;'>{row['BMI']}</td>"
                f"<td style='padding: 0.5rem;'>{row['Category']}</td>"
                f"<td style='padding: 0.5rem; color: #F5F5F5;'>{row['Calories']}</td>"
                f"</tr>"
            )

        st.markdown(
            f"""
            <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem;">
                <thead>
                    <tr style="border-bottom: 2px solid rgba(255,255,255,0.08);">
                        <th style="padding: 0.5rem; text-align: left; color: #9CA3AF;">Date</th>
                        <th style="padding: 0.5rem; text-align: left; color: #9CA3AF;">BMI</th>
                        <th style="padding: 0.5rem; text-align: left; color: #9CA3AF;">Category</th>
                        <th style="padding: 0.5rem; text-align: left; color: #9CA3AF;">Calories</th>
                    </tr>
                </thead>
                <tbody>
                    {html_rows}
                </tbody>
            </table>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)