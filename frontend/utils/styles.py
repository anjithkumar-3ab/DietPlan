"""
NutriAI Frontend Global Styles.

Provides CSS injection for the dark healthcare theme with glassmorphism.
"""

from __future__ import annotations

import streamlit as st


def inject_global_css() -> None:
    """Inject global CSS for the NutriAI dark healthcare theme.

    Should be called once in app.py after set_page_config.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* ===== Global Reset ===== */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        html, body, .stApp {
            background-color: #0E1117 !important;
            color: #F5F5F5 !important;
        }

        /* Hide default Streamlit chrome */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        .stDeployButton { display: none !important; }

        /* ===== Typography ===== */
        h1, h2, h3, h4, h5, h6 {
            color: #F5F5F5 !important;
            font-weight: 600 !important;
        }
        h1 { font-size: 1.6rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }

        p, li, span, div {
            color: #D1D5DB;
        }

        a {
            color: #66BB6A !important;
            text-decoration: none;
        }
        a:hover {
            color: #81C784 !important;
            text-decoration: underline;
        }

        /* ===== Content Container ===== */
        .block-container {
            max-width: 1200px !important;
            padding: 1.5rem 2rem !important;
        }

        /* ===== Glassmorphism Cards ===== */
        .glass-card {
            background: rgba(22, 27, 34, 0.85) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(46, 125, 50, 0.2) !important;
            border-radius: 16px !important;
            padding: 1.25rem 1.5rem !important;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        .glass-card:hover {
            border-color: rgba(46, 125, 50, 0.4) !important;
            box-shadow: 0 6px 32px rgba(46, 125, 50, 0.15) !important;
        }

        .glass-card-accent {
            background: rgba(22, 27, 34, 0.85) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-left: 4px solid #2E7D32 !important;
            border-radius: 16px !important;
            padding: 1.25rem 1.5rem !important;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3) !important;
        }

        /* ===== Metric Cards ===== */
        [data-testid="stMetric"] {
            background: rgba(22, 27, 34, 0.85) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(46, 125, 50, 0.2) !important;
            border-radius: 16px !important;
            padding: 1rem 1.25rem !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
            transition: all 0.3s ease !important;
        }
        [data-testid="stMetric"]:hover {
            border-color: rgba(46, 125, 50, 0.4) !important;
            box-shadow: 0 6px 24px rgba(46, 125, 50, 0.15) !important;
        }
        [data-testid="stMetric"] label {
            color: #9CA3AF !important;
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #F5F5F5 !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetric"] [data-testid="stMetricDelta"] {
            font-size: 0.75rem !important;
        }
        [data-testid="metric-container"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
        }

        /* ===== Buttons ===== */
        .stButton > button {
            border-radius: 12px !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            padding: 0.5rem 1.25rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #2E7D32, #43A047) !important;
            color: white !important;
            border: 1px solid rgba(46, 125, 50, 0.3) !important;
        }
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, #1B5E20, #2E7D32) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(46, 125, 50, 0.4) !important;
        }
        .stButton > button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.08) !important;
            color: #D1D5DB !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        .stButton > button[kind="secondary"]:hover {
            background: rgba(255, 255, 255, 0.12) !important;
            border-color: rgba(255, 255, 255, 0.2) !important;
            transform: translateY(-1px) !important;
        }

        /* ===== Expanders ===== */
        .streamlit-expanderHeader {
            background: rgba(22, 27, 34, 0.85) !important;
            backdrop-filter: blur(8px) !important;
            border: 1px solid rgba(46, 125, 50, 0.15) !important;
            border-radius: 12px !important;
            padding: 0.75rem 1rem !important;
            font-weight: 600 !important;
            color: #F5F5F5 !important;
            transition: all 0.3s ease !important;
        }
        .streamlit-expanderHeader:hover {
            border-color: rgba(46, 125, 50, 0.3) !important;
        }
        .streamlit-expanderContent {
            background: rgba(22, 27, 34, 0.5) !important;
            border: 1px solid rgba(46, 125, 50, 0.1) !important;
            border-top: none !important;
            border-radius: 0 0 12px 12px !important;
            padding: 1rem !important;
        }

        /* ===== Input Fields ===== */
        .stTextInput > div > div,
        .stNumberInput > div > div,
        .stSelectbox > div > div,
        .stTextArea > div > div {
            background: rgba(22, 27, 34, 0.9) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: #F5F5F5 !important;
            transition: all 0.3s ease !important;
        }
        .stTextInput > div > div:focus-within,
        .stNumberInput > div > div:focus-within,
        .stSelectbox > div > div:focus-within {
            border-color: #2E7D32 !important;
            box-shadow: 0 0 0 2px rgba(46, 125, 50, 0.2) !important;
        }
        .stTextInput input, .stNumberInput input, .stTextArea textarea {
            color: #F5F5F5 !important;
        }

        .stSelectbox div[data-baseweb="select"] > div {
            background: rgba(22, 27, 34, 0.9) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
        }

        /* ===== Slider ===== */
        .stSlider div[data-baseweb="slider"] {
            color: #2E7D32 !important;
        }

        /* ===== Tabs ===== */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(22, 27, 34, 0.6) !important;
            border-radius: 12px !important;
            padding: 0.375rem !important;
            gap: 0.25rem !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
            color: #9CA3AF !important;
            transition: all 0.3s ease !important;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(46, 125, 50, 0.2) !important;
            color: #66BB6A !important;
            box-shadow: 0 2px 8px rgba(46, 125, 50, 0.1) !important;
        }

        /* ===== Radio Buttons ===== */
        .stRadio div[role="radiogroup"] {
            gap: 0.5rem !important;
        }
        .stRadio div[role="radio"] {
            background: rgba(22, 27, 34, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            padding: 0.375rem 0.75rem !important;
            transition: all 0.3s ease !important;
        }
        .stRadio div[role="radio"][aria-checked="true"] {
            background: rgba(46, 125, 50, 0.15) !important;
            border-color: #2E7D32 !important;
        }

        /* ===== Progress Bar ===== */
        .stProgress > div > div {
            background: linear-gradient(90deg, #2E7D32, #66BB6A) !important;
            border-radius: 8px !important;
        }

        /* ===== Animation ===== */
        .element-container {
            animation: fadeIn 0.3s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* ===== Alerts ===== */
        .stAlert {
            border-radius: 12px !important;
            border: none !important;
            background: rgba(22, 27, 34, 0.9) !important;
            backdrop-filter: blur(8px) !important;
        }
        div[data-testid="stNotification"] {
            border-radius: 12px !important;
        }

        /* ===== Divider ===== */
        hr {
            border-color: rgba(255, 255, 255, 0.08) !important;
            margin: 1.5rem 0 !important;
        }

        /* ===== Scrollbar ===== */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #0E1117; }
        ::-webkit-scrollbar-thumb {
            background: rgba(46, 125, 50, 0.4);
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(46, 125, 50, 0.6);
        }

        /* ===== Checkbox ===== */
        .stCheckbox label { color: #D1D5DB !important; }

        /* ===== MultiSelect ===== */
        .stMultiSelect div[data-baseweb="select"] > div {
            background: rgba(22, 27, 34, 0.9) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
        }

        /* ===== Spinner ===== */
        .stSpinner > div {
            border-color: #2E7D32 !important;
            border-top-color: transparent !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )