/**
 * DietPlan – Diet Planner Page
 * Collect user parameters, call recommendation API, and display the meal plan.
 */

async function renderDietPlanner(container) {
  container.innerHTML = `
    <!-- Top Bar -->
    <div class="topbar">
      <div class="flex gap-2" style="align-items:center;">
        <button class="mobile-menu-btn" onclick="toggleSidebar()" aria-label="Menu">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <h1>Diet Planner</h1>
      </div>
      <div class="topbar-actions">
        <button class="btn btn-sm btn-secondary" onclick="navigate('meal_history')">View History</button>
      </div>
    </div>

    <!-- Plan Form -->
    <div class="card mb-3" id="planFormCard">
      <div class="card-header">
        <span class="card-title">Generate Your Personalized Diet Plan</span>
      </div>

      <form id="dietPlanForm" onsubmit="generatePlan(event)">
        <div class="form-group">
          <label for="dp_name">Name *</label>
          <input type="text" id="dp_name" minlength="1" maxlength="100" placeholder="Enter your name" autocomplete="name" required />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="dp_age">Age *</label>
            <input type="number" id="dp_age" min="1" max="120" placeholder="25" required />
          </div>
          <div class="form-group">
            <label for="dp_gender">Gender *</label>
            <select id="dp_gender" required>
              <option value="">Select</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="dp_height">Height (cm) *</label>
            <input type="number" id="dp_height" min="50" max="250" step="0.1" placeholder="170" required />
          </div>
          <div class="form-group">
            <label for="dp_weight">Weight (kg) *</label>
            <input type="number" id="dp_weight" min="10" max="300" step="0.1" placeholder="70" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="dp_activity">Activity Level *</label>
            <select id="dp_activity" required>
              <option value="">Select</option>
              <option value="Sedentary">Sedentary</option>
              <option value="Light">Light</option>
              <option value="Moderate">Moderate</option>
              <option value="Active">Active</option>
              <option value="Very Active">Very Active</option>
            </select>
          </div>
          <div class="form-group">
            <label for="dp_goal">Goal *</label>
            <select id="dp_goal" required>
              <option value="">Select</option>
              <option value="Weight Loss">Weight Loss</option>
              <option value="Maintenance">Maintenance</option>
              <option value="Weight Gain">Weight Gain</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="dp_food_pref">Food Preference *</label>
            <select id="dp_food_pref" required>
              <option value="">Select</option>
              <option value="Veg">Veg</option>
              <option value="Non-Veg">Non-Veg</option>
              <option value="Any">Any</option>
            </select>
          </div>
          <div class="form-group">
            <label for="dp_meals">Meals Per Day</label>
            <select id="dp_meals">
              <option value="3">3 Meals</option>
              <option value="4" selected>4 Meals</option>
              <option value="5">5 Meals</option>
              <option value="6">6 Meals</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label>Allergies</label>
          <div class="checkbox-group" id="dpAllergyGroup">
            ${buildPlanPills(['Dairy', 'Eggs', 'Gluten', 'Peanuts', 'Tree Nuts', 'Soy', 'Shellfish', 'Fish', 'Wheat', 'Corn'])}
          </div>
        </div>

        <div class="form-group">
          <label>Medical Conditions</label>
          <div class="checkbox-group" id="dpMedicalGroup">
            ${buildPlanPills(['Diabetes', 'Hypertension', 'High Cholesterol', 'Thyroid', 'PCOS', 'Heart Disease', 'Kidney Disease', 'Gout', 'Anemia', 'None'])}
          </div>
        </div>

        <div id="planError" class="hidden"></div>

        <button type="submit" class="btn btn-primary btn-lg mt-2" id="planBtn" style="width:100%;justify-content:center;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          Generate Diet Plan
        </button>
      </form>
    </div>
  `;

  initPills('dpAllergyGroup');
  initPills('dpMedicalGroup');
}

function buildPlanPills(items) {
  return items
    .map((item) => `<span class="checkbox-pill" data-value="${item}">${item}</span>`)
    .join('');
}

function getSelectedPlanPills(groupId) {
  const container = document.getElementById(groupId);
  if (!container) return [];
  const selected = container.querySelectorAll('.checkbox-pill.selected');
  return Array.from(selected).map((p) => p.dataset.value);
}

// Toggle checkbox-pill selection on click
function initPills(groupId) {
  const container = document.getElementById(groupId);
  if (!container) return;

  container.querySelectorAll('.checkbox-pill').forEach((pill) => {
    pill.addEventListener('click', () => {
      pill.classList.toggle('selected');
    });
  });
}

async function generatePlan(event) {
  event.preventDefault();

  const btn = document.getElementById('planBtn');
  const errorDiv = document.getElementById('planError');

  if (errorDiv) {
    errorDiv.className = 'hidden';
    errorDiv.textContent = '';
  }

  btn.disabled = true;
  btn.innerHTML = '<div class="spinner" style="width:22px;height:22px;margin:0;border-width:2px;"></div> Generating...';

  const request = {
    name: document.getElementById('dp_name').value.trim(),
    age: parseInt(document.getElementById('dp_age').value),
    gender: document.getElementById('dp_gender').value,
    height: parseFloat(document.getElementById('dp_height').value),
    weight: parseFloat(document.getElementById('dp_weight').value),
    activity_level: document.getElementById('dp_activity').value,
    goal: document.getElementById('dp_goal').value,
    food_preference: document.getElementById('dp_food_pref').value,
    allergies: getSelectedPlanPills('dpAllergyGroup'),
    medical_conditions: getSelectedPlanPills('dpMedicalGroup'),
    meals_per_day: parseInt(document.getElementById('dp_meals').value),
  };

  try {
    const api = await NutriAPI.recommendation;
    const data = await api.generate(request);

    if (data?.success) {
      showToast('Diet plan generated successfully!', 'success');

      // Preserve generated recommendation data for Dashboard
      window.latestRecommendationData = data;

      // Programmatically navigate to Dashboard using existing sidebar navigation router
      navigate('dashboard_page');
    } else {
      throw new Error(data?.message || 'Failed to generate plan');
    }
  } catch (error) {
    if (errorDiv) {
      errorDiv.className = 'alert alert-error';
      errorDiv.classList.remove('hidden');
      errorDiv.textContent = error.message;
    }
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = `
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        Generate Diet Plan
      `;
    }
  }
}

function renderPlanResult(container, data) {
  const plan = data.daily_plan;

  container.innerHTML = `
    <!-- Health Metrics -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon green">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        </div>
        <div class="stat-info">
          <h3>${formatNum(data.bmi)}</h3>
          <p>BMI · ${data.bmi_category || '—'}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon blue">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
        </div>
        <div class="stat-info">
          <h3>${formatNum(data.daily_calories, 0)}</h3>
          <p>Daily Calories (kcal)</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon yellow">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
        </div>
        <div class="stat-info">
          <h3>${formatNum(data.bmr, 0)}</h3>
          <p>BMR (kcal)</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon green">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
        </div>
        <div class="stat-info">
          <h3>${formatNum(data.tdee, 0)}</h3>
          <p>TDEE (kcal)</p>
        </div>
      </div>
    </div>

    <!-- Meal Cards -->
    <div class="meal-grid">
      ${renderMealCard('Breakfast', plan.breakfast, 'breakfast')}
      ${renderMealCard('Lunch', plan.lunch, 'lunch')}
      ${renderMealCard('Dinner', plan.dinner, 'dinner')}
      ${renderMealCard('Snacks', plan.snacks, 'snack')}
    </div>

    <!-- Nutrition Summary -->
    <div class="nutrition-summary mt-3">
      <div class="card-header mb-2">
        <span class="card-title">Nutrition Summary</span>
        <span class="card-subtitle">Daily Totals vs Targets</span>
      </div>

      <div class="nutrition-bars">
        <div class="nutrition-bar-item">
          <span class="nutrition-bar-label">Calories</span>
          <div class="nutrition-bar-track">
            <div class="nutrition-bar-fill protein" style="width:${calcPct(plan.total_daily_calories, data.daily_calories)}%"></div>
          </div>
          <span class="nutrition-bar-value">${formatNum(plan.total_daily_calories, 0)} / ${formatNum(data.daily_calories, 0)}</span>
        </div>
        <div class="nutrition-bar-item">
          <span class="nutrition-bar-label">Protein</span>
          <div class="nutrition-bar-track">
            <div class="nutrition-bar-fill protein" style="width:${calcPct(plan.total_protein, data.target_protein)}%"></div>
          </div>
          <span class="nutrition-bar-value">${formatNum(plan.total_protein, 1)}g / ${formatNum(data.target_protein, 1)}g</span>
        </div>
        <div class="nutrition-bar-item">
          <span class="nutrition-bar-label">Carbs</span>
          <div class="nutrition-bar-track">
            <div class="nutrition-bar-fill carbs" style="width:${calcPct(plan.total_carbohydrates, data.target_carbohydrates)}%"></div>
          </div>
          <span class="nutrition-bar-value">${formatNum(plan.total_carbohydrates, 1)}g / ${formatNum(data.target_carbohydrates, 1)}g</span>
        </div>
        <div class="nutrition-bar-item">
          <span class="nutrition-bar-label">Fats</span>
          <div class="nutrition-bar-track">
            <div class="nutrition-bar-fill fat" style="width:${calcPct(plan.total_fat, data.target_fat)}%"></div>
          </div>
          <span class="nutrition-bar-value">${formatNum(plan.total_fat, 1)}g / ${formatNum(data.target_fat, 1)}g</span>
        </div>
        <div class="nutrition-bar-item">
          <span class="nutrition-bar-label">Fiber</span>
          <div class="nutrition-bar-track">
            <div class="nutrition-bar-fill fiber" style="width:${calcPct(plan.total_fiber || 0, 30)}%"></div>
          </div>
          <span class="nutrition-bar-value">${formatNum(plan.total_fiber || 0, 1)}g</span>
        </div>
      </div>

      <div style="margin-top:16px;padding-top:16px;border-top:1px solid var(--border);display:flex;gap:12px;flex-wrap:wrap;">
        <span class="badge badge-info">🥤 Water: ${plan.recommended_water_liters || '2.0'}L</span>
        <span class="badge badge-success">🍽 ${data.food_preference || '—'}</span>
      </div>
    </div>

    ${data.recommendation_id ? `
      <div class="mt-3 flex gap-2" style="justify-content:center;">
        <button class="btn btn-secondary" onclick="regeneratePlan('${data.recommendation_id}')">🔄 Regenerate</button>
      </div>
    ` : ''}
  `;
}

function renderMealCard(name, meal, type) {
  if (!meal || !meal.items || meal.items.length === 0) {
    return `
      <div class="meal-card">
        <div class="meal-card-header">
          <h3>${name}</h3>
          <span class="meal-badge ${type}">${type}</span>
        </div>
        <div class="meal-card-body">
          <p style="color:var(--text-muted);text-align:center;padding:20px;">No items for this meal</p>
        </div>
      </div>
    `;
  }

  const items = meal.items
    .map(
      (item) => `
      <div class="meal-item">
        <div class="meal-item-info">
          <h4>${item.name}</h4>
          <span>${item.category || ''} · ${item.quantity || ''}</span>
        </div>
        <div class="meal-item-cal">${formatNum(item.calories, 0)} kcal</div>
      </div>
    `
    )
    .join('');

  return `
    <div class="meal-card">
      <div class="meal-card-header">
        <h3>${name}</h3>
        <span class="meal-badge ${type}">${type}</span>
      </div>
      <div class="meal-card-body">
        ${items}
        <div class="meal-item" style="border-top:1px solid var(--accent);margin-top:4px;padding-top:12px;">
          <div class="meal-item-info"><h4 style="color:var(--accent);">Total</h4></div>
          <div class="meal-item-cal">${formatNum(meal.total_calories, 0)} kcal</div>
        </div>
      </div>
    </div>
  `;
}

function calcPct(value, target) {
  if (!value || !target || target === 0) return 0;
  return Math.min(100, (value / target) * 100);
}

async function regeneratePlan(recommendationId) {
  try {
    showToast('Regenerating plan...', 'info', 2000);
    const api = await NutriAPI.recommendation;
    const data = await api.regenerate(recommendationId);

    if (data?.success) {
      showToast('Plan regenerated!', 'success');
      const resultDiv = document.getElementById('planResult');
      renderPlanResult(resultDiv, data);
      resultDiv.scrollIntoView({ behavior: 'smooth' });
    }
  } catch (error) {
    showToast(error.message, 'error');
  }
}