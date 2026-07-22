/**
 * DietPlan – API Layer
 * Communicates with the FastAPI backend via Fetch API.
 */

const API_BASE = 'http://localhost:8000';

// ── Generic fetch wrapper ──

async function apiFetch(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const config = {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  };

  try {
    const response = await fetch(url, config);
    const data = await response.json();

    if (!response.ok) {
      const message = data.detail || data.message || `HTTP ${response.status}`;
      throw new Error(message);
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
      throw new Error('Unable to connect to the server. Please ensure the backend is running.');
    }
    throw error;
  }
}

// ── Profile API ──

async function profileAPI() {
  return {
    save: (profile) => apiFetch('/profile/', { method: 'POST', body: JSON.stringify(profile) }),
  };
}

// ── Recommendation API ──

async function recommendationAPI() {
  return {
    generate: (request) =>
      apiFetch('/recommendation/generate', { method: 'POST', body: JSON.stringify(request) }),

    history: (limit = 10, skip = 0) =>
      apiFetch(`/recommendation/history?limit=${limit}&skip=${skip}`),

    getById: (id) => apiFetch(`/recommendation/${id}`),

    delete: (id) => apiFetch(`/recommendation/${id}`, { method: 'DELETE' }),

    regenerate: (id) =>
      apiFetch(`/recommendation/${id}/regenerate`, { method: 'POST' }),

    health: () => apiFetch('/recommendation/health'),
  };
}

// ── Dashboard API ──

async function dashboardAPI() {
  return {
    getCharts: (recommendationId) =>
      apiFetch('/dashboard/charts', {
        method: 'POST',
        body: JSON.stringify({ recommendation_id: recommendationId }),
      }),
  };
}

// ── Food API ──

async function foodAPI() {
  return {
    all: (limit = 50) => apiFetch(`/foods/?limit=${limit}`),

    search: (query) => apiFetch(`/foods/search?query=${encodeURIComponent(query)}`),

    byCategory: (category) => apiFetch(`/foods/category/${encodeURIComponent(category)}`),

    getById: (id) => apiFetch(`/foods/${id}`),
  };
}

// ── Health API ──

async function healthAPI() {
  return {
    check: () => apiFetch('/health'),
  };
}

// ── Public API object (lazily initialized) ──

let _profile = null;
let _recommendation = null;
let _dashboard = null;
let _food = null;
let _health = null;

const DietPlanAPI = {
  get profile() {
    if (!_profile) _profile = profileAPI();
    return _profile;
  },
  get recommendation() {
    if (!_recommendation) _recommendation = recommendationAPI();
    return _recommendation;
  },
  get dashboard() {
    if (!_dashboard) _dashboard = dashboardAPI();
    return _dashboard;
  },
  get food() {
    if (!_food) _food = foodAPI();
    return _food;
  },
  get health() {
    if (!_health) _health = healthAPI();
    return _health;
  },
};

const NutriAPI = DietPlanAPI;
