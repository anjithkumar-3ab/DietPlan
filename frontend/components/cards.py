"""
NutriAI Card Components.

Reusable card elements for displaying metrics, summaries, and meal plans.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import streamlit as st


def glass_card(title: str, content: str, accent: bool = False) -> None:
    """Render a glassmorphism card with title and content.

    Args:
        title: Card title.
        content: HTML content for the card body.
        accent: If True, renders with green left border accent.
    """
    card_class = "glass-card-accent" if accent else "glass-card"
    st.markdown(
        f"""
        <div class="{card_class}">
            <h4 style="margin: 0 0 0.5rem 0;">{title}</h4>
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(
    label: str,
    value: str,
    delta: Optional[str] = None,
    help_text: Optional[str] = None,
) -> None:
    """Render a styled metric card.

    Args:
        label: Metric label.
        value: Metric value string.
        delta: Optional delta/change string.
        help_text: Optional tooltip text.
    """
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.metric(label=label, value=value, delta=delta, help=help_text)


def meal_card(
    meal_type: str,
    items: List[Dict[str, Any]],
    totals: Dict[str, float],
    emoji: str,
) -> None:
    """Render a meal card with food items and nutritional totals.

    Args:
        meal_type: Type of meal (Breakfast, Lunch, Dinner, Snack).
        items: List of food item dicts.
        totals: Dict with total_calories, total_protein, total_carbohydrates, total_fat.
        emoji: Emoji icon for the meal.
    """
    calories = totals.get("total_calories", 0)
    protein = totals.get("total_protein", 0)
    carbs = totals.get("total_carbohydrates", 0)
    fat = totals.get("total_fat", 0)

    items_html = "".join(
        f"""
        <div style="display: flex; justify-content: space-between;
                    padding: 0.3rem 0; border-bottom: 1px solid rgba(255,255,255,0.04);
                    font-size: 0.85rem;">
            <span style="color: #D1D5DB;">{item.get('name', 'Item')}
                <span style="color: #6B7280; font-size: 0.75rem;">
                    ({item.get('quantity', '')})
                </span>
            </span>
            <span style="color: #F5F5F5; font-weight: 500;">
                {item.get('calories', 0):.0f} kcal
            </span>
        </div>
        """
        for item in items
    )

    st.markdown(
        f"""
        <div class="glass-card" style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;
                        margin-bottom: 0.75rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.5rem;">{emoji}</span>
                    <h4 style="margin: 0; font-size: 1.05rem;">{meal_type}</h4>
                </div>
                <span style="color: #66BB6A; font-weight: 600; font-size: 1rem;">
                    {calories:,.0f} kcal
                </span>
            </div>
            {items_html}
            <div style="display: flex; gap: 1.5rem; margin-top: 0.75rem;
                        padding-top: 0.5rem; border-top: 1px solid rgba(255,255,255,0.08);
                        font-size: 0.75rem; color: #9CA3AF;">
                <span>Protein: {protein:.1f}g</span>
                <span>Carbs: {carbs:.1f}g</span>
                <span>Fat: {fat:.1f}g</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(title: str, description: str, emoji: str = "ℹ️") -> None:
    """Render an information card.

    Args:
        title: Card title.
        description: Card description text.
        emoji: Emoji icon.
    """
    st.markdown(
        f"""
        <div class="glass-card" style="text-align: center; padding: 2rem 1.5rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">{emoji}</div>
            <h3 style="margin: 0 0 0.5rem 0;">{title}</h3>
            <p style="color: #9CA3AF; font-size: 0.9rem; margin: 0;">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state_card(
    title: str,
    message: str,
    emoji: str = "📭",
    action_label: Optional[str] = None,
) -> None:
    """Render an empty state card with an optional call to action.

    Args:
        title: Empty state title.
        message: Descriptive message.
        emoji: Emoji icon.
        action_label: Optional button label (rendered below).
    """
    st.markdown(
        f"""
        <div style="text-align: center; padding: 3rem 1.5rem;
                    border: 2px dashed rgba(255,255,255,0.1);
                    border-radius: 16px; margin: 1rem 0;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{emoji}</div>
            <h3 style="margin: 0 0 0.5rem 0; color: #9CA3AF;">{title}</h3>
            <p style="color: #6B7280; font-size: 0.9rem; margin: 0;">{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if action_label:
        st.button(action_label, type="primary", use_container_width=True)