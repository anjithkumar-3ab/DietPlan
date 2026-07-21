/**
 * NutriAI – Dashboard Page
 * Displays welcome card, BMI, daily calories, nutrition summary, and quick actions.
 */

async function renderDashboard(container) {
  // Try to fetch the latest recommendation for stats
  let latestData = null;
  try {
    const api = await NutriAPI.recommendation;
    const history = await api.history(1, 0);
    if (history?.recommendations?.length > 0) {
      latestData = history.recommendations[0];
    }
  } catch {
    // Silently fail — dashboard still renders
  }

  const bmi = latestData?.bmi;
  const bmiCategory = latestData?.bmi_category || '—';
  const dailyCalories = latestData?.daily_calories;
  const tdee = latestData?.tdee;
  const targetProtein = latestData?.target_protein;
  const targetCarbs = latestData?.target_carbohydrates;
  const targetFat = latestData?.target_fat;

  container.innerHTML = `
    <!-- Top Bar -->
    <div class="topbar">
      <div class="flex gap-2" style="align-items:center;">
        <button class="mobile-menu-btn" onclick="toggleSidebar()" aria-label="Menu">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <h1>Dashboard</h1>
      </div>
      <div class="topbar-actions">
        <button class="btn btn-sm btn-secondary" onclick="navigate('diet_planner')">+ New Plan</button>
      </div>
    </div>

    <!-- Welcome Card -->
    <div class="welcome-card">
      <h2>Welcome to NutriAI 👋</h2>
      <p>Your AI-powered personalized diet planning assistant. Generate custom meal plans based on your health profile, preferences, and goals.</p>
    </div>

    <!-- Stats Grid -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon green">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        </div>
        <div class="stat-info">
          <h3>${formatNum(bmi)}</h3>
          <p>BMI ${bmiCategory ? `· ${bmiCategory}` : ''}</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon blue">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
        </div>
        <div class="stat-info">
          <h3>${formatNum(dailyCalories, 0)}</h3>
          <p>Daily Calories (kcal)</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon yellow">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>
        </div>
        <div class="stat-info">
          <h3>${formatNum(tdee, 0)}</h3>
          <p>TDEE (kcal)</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon red">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
        </div>
        <div class="stat-info">
          <h3>${latestData ? 'Active' : '—'}</h3>
          <p>Plan Status</p>
        </div>
      </div>
    </div>

    <!-- Nutrition & Quick Actions -->
    <div class="two-col">
      <!-- Today's Nutrition -->
      <div class="card">
        <div class="card-header">
          <span class="card-title">Today's Nutrition Targets</span>
          ${latestData ? '<span class="badge badge-success">Latest Plan</span>' : '<span class="badge badge-warning">No Plan Yet</span>'}
        </div>
        ${latestData ? `
          <div class="nutrition-bars">
            <div class="nutrition-bar-item">
              <span class="nutrition-bar-label">Protein</span>
              <div class="nutrition-bar-track"><div class="nutrition-bar-fill protein" style="width:${calcPercent(targetProtein, 100)}%"></div></div>
              <span class="nutrition-bar-value">${formatNum(targetProtein, 0)}g</span>
            </div>
            <div class="nutrition-bar-item">
              <span class="nutrition-bar-label">Carbs</span>
              <div class="nutrition-bar-track"><div class="nutrition-bar-fill carbs" style="width:${calcPercent(targetCarbs, 300)}%"></div></div>
              <span class="nutrition-bar-value">${formatNum(targetCarbs, 0)}g</span>
            </div>
            <div class="nutrition-bar-item">
              <span class="nutrition-bar-label">Fats</span>
              <div class="nutrition-bar-track"><div class="nutrition-bar-fill fat" style="width:${calcPercent(targetFat, 65)}%"></div></div>
              <span class="nutrition-bar-value">${formatNum(targetFat, 0)}g</span>
            </div>
          </div>
        ` : `
          <div class="empty-state" style="padding: 40px 20px;">
            <h3>No meal plan generated yet</h3>
            <p>Start by creating your health profile, then generate a personalized diet plan.</p>
            <button class="btn btn-primary" onclick="navigate('diet_planner')">Generate Diet Plan</button>
          </div>
        `}
      </div>

      <!-- Quick Actions -->
      <div class="card">
        <div class="card-header">
          <span class="card-title">Quick Actions</span>
        </div>
        <div style="display:flex;flex-direction:column;gap:12px;">
          <button class="btn btn-primary btn-lg" onclick="navigate('diet_planner')" style="justify-content:center;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            Generate Diet Plan
          </button>
          <button class="btn btn-secondary btn-lg" onclick="navigate('profile')" style="justify-content:center;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            Update Health Profile
          </button>
          <button class="btn btn-secondary btn-lg" onclick="navigate('meal_history')" style="justify-content:center;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            View Meal History
          </button>
          <button class="btn btn-secondary btn-lg" onclick="navigate('progress')" style="justify-content:center;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
            Track Progress
          </button>
        </div>
      </div>
    </div>

    ${latestData ? `
      <div class="mt-3">
        <div class="card" style="text-align:center;">
          <p style="color:var(--text-secondary);margin-bottom:12px;">Generated on ${formatDate(latestData.created_at)}</p>
          <button class="btn btn-sm btn-secondary" onclick="navigate('diet_planner')">View Full Plan →</button>
        </div>
      </div>
    ` : ''}
  `;
}

function calcPercent(value, max) {
  if (!value || !max) return 0;
  return Math.min(100, (value / max) * 100);
}
