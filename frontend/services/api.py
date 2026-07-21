"""
NutriAI Frontend API Service.

Centralized HTTP client for communicating with the FastAPI backend.
All read-only API calls use Streamlit caching to avoid redundant network requests.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import requests
import streamlit as st

from frontend.utils.constants import (
    API_BASE_URL,
    API_TIMEOUT,
    API_HEALTH,
    API_PROFILE,
    API_RECOMMENDATION_GENERATE,
    API_RECOMMENDATION_HISTORY,
    CACHE_TTL_HEALTH,
    CACHE_TTL_HISTORY,
    CACHE_TTL_FOODS,
    MAX_HISTORY_LIMIT,
)


# ---------------------------------------------------------------------------
# Low-level HTTP helpers
# ---------------------------------------------------------------------------


def _url(path: str) -> str:
    """Build a full API URL from a relative path.

    Args:
        path: Relative API path (e.g. "/health").

    Returns:
        Full URL string.
    """
    return f"{API_BASE_URL.rstrip('/')}{path}"


def _get(
    path: str, params: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """Send a GET request and return parsed JSON.

    Args:
        path: Relative API path.
        params: Optional query parameters.

    Returns:
        Parsed JSON response dict or None on failure.
    """
    try:
        response = requests.get(
            _url(path), params=params, timeout=API_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.HTTPError as exc:
        st.error(f"API error: {exc}")
        return None
    except requests.exceptions.RequestException as exc:
        st.error(f"Request failed: {exc}")
        return None


def _post(
    path: str, json_data: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """Send a POST request and return parsed JSON.

    Args:
        path: Relative API path.
        json_data: JSON payload.

    Returns:
        Parsed JSON response dict or None on failure.
    """
    try:
        response = requests.post(
            _url(path), json=json_data, timeout=API_TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.HTTPError as exc:
        st.error(f"API error: {exc}")
        return None
    except requests.exceptions.RequestException as exc:
        st.error(f"Request failed: {exc}")
        return None


def _delete(path: str) -> Optional[Dict[str, Any]]:
    """Send a DELETE request and return parsed JSON.

    Args:
        path: Relative API path.

    Returns:
        Parsed JSON response dict or None on failure.
    """
    try:
        response = requests.delete(_url(path), timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.HTTPError as exc:
        st.error(f"API error: {exc}")
        return None
    except requests.exceptions.RequestException as exc:
        st.error(f"Request failed: {exc}")
        return None


# ---------------------------------------------------------------------------
# API Error Check
# ---------------------------------------------------------------------------


def api_available() -> bool:
    """Check if the backend API is reachable.

    Returns:
        True if the health endpoint responds successfully.
    """
    result = _get(API_HEALTH)
    if result is None:
        return False
    return result.get("status") in ("ok", "healthy", "running")


# ---------------------------------------------------------------------------
# Profile API
# ---------------------------------------------------------------------------


def save_profile(profile_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Create or update a health profile.

    Args:
        profile_data: Full HealthProfile payload matching backend schema.

    Returns:
        API response dict or None on failure.
    """
    result = _post(API_PROFILE, json_data=profile_data)
    if result is not None:
        st.cache_data.clear()
    return result


# ---------------------------------------------------------------------------
# Diet Plan / Recommendation API
# ---------------------------------------------------------------------------


def generate_diet_plan(
    request_data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Generate a personalized diet plan.

    Args:
        request_data: RecommendationRequest payload.

    Returns:
        RecommendationResponse dict or None on failure.
    """
    result = _post(
        API_RECOMMENDATION_GENERATE, json_data=request_data
    )
    if result is not None:
        st.cache_data.clear()
    return result


@st.cache_data(ttl=CACHE_TTL_HISTORY, show_spinner=False)
def get_cached_history(limit: int = MAX_HISTORY_LIMIT) -> Optional[Dict[str, Any]]:
    """Fetch paginated recommendation history (cached).

    Args:
        limit: Max records (1-100).

    Returns:
        HistoryResponse dict or None on failure.
    """
    return _get(
        API_RECOMMENDATION_HISTORY,
        params={"limit": limit, "skip": 0},
    )


def get_history(
    limit: int = 10, skip: int = 0
) -> Optional[Dict[str, Any]]:
    """Fetch paginated recommendation history (always fresh).

    Args:
        limit: Max records (1-100).
        skip: Records to skip.

    Returns:
        HistoryResponse dict or None on failure.
    """
    return _get(
        API_RECOMMENDATION_HISTORY,
        params={"limit": limit, "skip": skip},
    )


def get_recommendation_by_id(
    recommendation_id: str,
) -> Optional[Dict[str, Any]]:
    """Fetch a single recommendation by its MongoDB ObjectId.

    Args:
        recommendation_id: 24-character hex string.

    Returns:
        SingleRecommendationResponse dict or None on failure.
    """
    path = f"/recommendation/{recommendation_id}"
    return _get(path)


def delete_recommendation(recommendation_id: str) -> Optional[Dict[str, Any]]:
    """Permanently delete a recommendation.

    Args:
        recommendation_id: 24-character hex string.

    Returns:
        MessageResponse dict or None on failure.
    """
    path = f"/recommendation/{recommendation_id}"
    result = _delete(path)
    if result is not None:
        st.cache_data.clear()
    return result


def regenerate_diet_plan(
    recommendation_id: str,
) -> Optional[Dict[str, Any]]:
    """Regenerate a diet plan from an existing recommendation.

    Args:
        recommendation_id: Source recommendation ID.

    Returns:
        RecommendationResponse dict or None on failure.
    """
    path = f"/recommendation/{recommendation_id}/regenerate"
    result = _post(path)
    if result is not None:
        st.cache_data.clear()
    return result


# ---------------------------------------------------------------------------
# Foods API
# ---------------------------------------------------------------------------


@st.cache_data(ttl=CACHE_TTL_FOODS, show_spinner=False)
def get_all_foods(limit: int = 50) -> Optional[Dict[str, Any]]:
    """Fetch all foods from the database (cached).

    Args:
        limit: Max records.

    Returns:
        Foods response dict or None on failure.
    """
    return _get("/foods/", params={"limit": limit})


@st.cache_data(ttl=CACHE_TTL_FOODS, show_spinner=False)
def search_foods(query: str) -> Optional[Dict[str, Any]]:
    """Search foods by name (cached).

    Args:
        query: Search query string.

    Returns:
        Foods response dict or None on failure.
    """
    return _get("/foods/search", params={"query": query})


@st.cache_data(ttl=CACHE_TTL_FOODS, show_spinner=False)
def get_foods_by_category(category: str) -> Optional[Dict[str, Any]]:
    """Get foods filtered by category (cached).

    Args:
        category: Food category name.

    Returns:
        Foods response dict or None on failure.
    """
    return _get(f"/foods/category/{category}")


@st.cache_data(ttl=CACHE_TTL_FOODS, show_spinner=False)
def get_food_by_id(food_id: str) -> Optional[Dict[str, Any]]:
    """Get a single food by ID (cached).

    Args:
        food_id: Food document ID.

    Returns:
        Food response dict or None on failure.
    """
    return _get(f"/foods/{food_id}")