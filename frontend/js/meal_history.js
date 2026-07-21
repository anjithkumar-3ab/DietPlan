/**
 * NutriAI – Meal History Page
 * Displays previously generated meal plans with pagination.
 */

let historyPage = 0;
const HISTORY_LIMIT = 10;

async function renderMealHistory(container) {
  historyPage = 0;

  container.innerHTML = `
    <!-- Top Bar -->
    <div class="topbar">
      <div class="flex gap-2" style="align-items:center;">
        <button class="mobile-menu-btn" onclick="toggleSidebar()" aria-label="Menu">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <h1>Meal History</h1>
      </div>
      <div class="topbar-actions">
        <button class="btn btn-sm btn-primary" onclick="navigate('diet_planner')">+ New Plan</button>
      </div>
    </div>

    <div id="historyList">
      <div class="spinner"></div>
    </div>

    <div id="historyPagination" class="flex gap-2 mt-3" style="justify-content:center;"></div>
  `;

  await loadHistory();
}

async function loadHistory() {
  const listContainer = document.getElementById('historyList');
  const paginationContainer = document.getElementById('historyPagination');

  try {
    const api = await NutriAPI.recommendation;
    const data = await api.history(HISTORY_LIMIT, historyPage * HISTORY_LIMIT);

    if (!data?.recommendations || data.recommendations.length === 0) {
      listContainer.innerHTML = `
        <div class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          <h3>No meal plans yet</h3>
          <p>Generate your first personalized diet plan to see it here.</p>
          <button class="btn btn-primary" onclick="navigate('diet_planner')">Generate Diet Plan</button>
        </div>
      `;
      return;
    }

    listContainer.innerHTML = data.recommendations
      .map((rec, index) => renderHistoryCard(rec, index))
      .join('');

    // Pagination
    const totalCount = data.count || data.recommendations.length;
    const totalPages = Math.ceil(totalCount / HISTORY_LIMIT);

    paginationContainer.innerHTML = `
      <button class="btn btn-sm btn-secondary" ${historyPage === 0 ? 'disabled' : ''} onclick="historyPage--; loadHistory();">
        ← Previous
      </button>
      <span style="display:flex;align-items:center;font-size:0.88rem;color:var(--text-secondary);">
        Page ${historyPage + 1} of ${totalPages || 1}
      </span>
      <button class="btn btn-sm btn-secondary" ${historyPage >= totalPages - 1 ? 'disabled' : ''} onclick="historyPage++; loadHistory();">
        Next →
      </button>
    `;
  } catch (error) {
    listContainer.innerHTML = `
      <div class="alert alert-error">
        <span>Failed to load history: ${error.message}</span>
        <button class="btn btn-sm btn-secondary" onclick="loadHistory()" style="margin-left:auto;">Retry</button>
      </div>
    `;
  }
}

function renderHistoryCard(rec, index) {
  const plan = rec.daily_plan;
  const mealCounts = [
    plan?.breakfast?.items?.length || 0,
    plan?.lunch?.items?.length || 0,
    plan?.dinner?.items?.length || 0,
    plan?.snacks?.items?.length || 0,
  ];
  const totalItems = mealCounts.reduce((a, b) => a + b, 0);

  return `
    <div class="card mb-2" style="animation: slideUp 0.3s ease ${index * 0.05}s both;">
      <div class="flex-between mb-2">
        <div>
          <h3 style="font-size:1.05rem;font-weight:600;">
            Meal Plan ${rec.recommendation_id ? `#${rec.recommendation_id.slice(-6)}` : ''}
          </h3>
          <p style="font-size:0.82rem;color:var(--text-muted);">${formatDate(rec.created_at)}</p>
        </div>
        <span class="badge badge-success">${formatNum(rec.daily_calories, 0)} kcal</span>
      </div>

      <div class="stats-grid" style="grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px;">
        <div style="text-align:center;">
          <div style="font-size:1.2rem;font-weight:700;color:var(--accent);">${formatNum(rec.bmi)}</div>
          <div style="font-size:0.7rem;color:var(--text-muted);">BMI</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:1.2rem;font-weight:700;">${formatNum(rec.daily_calories, 0)}</div>
          <div style="font-size:0.7rem;color:var(--text-muted);">Calories</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:1.2rem;font-weight:700;">${totalItems}</div>
          <div style="font-size:0.7rem;color:var(--text-muted);">Items</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:1.2rem;font-weight:700;color:var(--info);">${formatNum(rec.tdee, 0)}</div>
          <div style="font-size:0.7rem;color:var(--text-muted);">TDEE</div>
        </div>
      </div>

      <!-- Meals Preview -->
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-bottom:14px;">
        <div style="background:var(--bg-primary);border-radius:var(--radius-sm);padding:10px 12px;">
          <span class="badge badge-warning" style="font-size:0.7rem;">Breakfast</span>
          <div style="font-size:0.8rem;color:var(--text-secondary);margin-top:4px;">${mealCounts[0]} items</div>
          <div style="font-size:0.78rem;color:var(--accent);">${formatNum(plan?.breakfast?.total_calories, 0)} kcal</div>
        </div>
        <div style="background:var(--bg-primary);border-radius:var(--radius-sm);padding:10px 12px;">
          <span class="badge badge-info" style="font-size:0.7rem;">Lunch</span>
          <div style="font-size:0.8rem;color:var(--text-secondary);margin-top:4px;">${mealCounts[1]} items</div>
          <div style="font-size:0.78rem;color:var(--accent);">${formatNum(plan?.lunch?.total_calories, 0)} kcal</div>
        </div>
        <div style="background:var(--bg-primary);border-radius:var(--radius-sm);padding:10px 12px;">
          <span class="badge badge-danger" style="font-size:0.7rem;">Dinner</span>
          <div style="font-size:0.8rem;color:var(--text-secondary);margin-top:4px;">${mealCounts[2]} items</div>
          <div style="font-size:0.78rem;color:var(--accent);">${formatNum(plan?.dinner?.total_calories, 0)} kcal</div>
        </div>
        <div style="background:var(--bg-primary);border-radius:var(--radius-sm);padding:10px 12px;">
          <span class="badge badge-success" style="font-size:0.7rem;">Snacks</span>
          <div style="font-size:0.8rem;color:var(--text-secondary);margin-top:4px;">${mealCounts[3]} items</div>
          <div style="font-size:0.78rem;color:var(--accent);">${formatNum(plan?.snacks?.total_calories, 0)} kcal</div>
        </div>
      </div>

      <!-- Info badges -->
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">
        <span class="badge" style="background:rgba(255,255,255,0.05);">🍽 ${rec.food_preference || '—'}</span>
        <span class="badge" style="background:rgba(255,255,255,0.05);">${rec.bmi_category || '—'}</span>
      </div>

      <div class="flex gap-1">
        <button class="btn btn-sm btn-primary" onclick="viewPlanDetail('${rec.recommendation_id || ''}')">📋 View Details</button>
        <button class="btn btn-sm btn-secondary" onclick="regenerateFromHistory('${rec.recommendation_id || ''}')">🔄 Regenerate</button>
        <button class="btn btn-sm btn-danger" onclick="deletePlan('${rec.recommendation_id || ''}')" style="margin-left:auto;">🗑 Delete</button>
      </div>
    </div>
  `;
}

async function viewPlanDetail(id) {
  if (!id) return;
  try {
    const api = await NutriAPI.recommendation;
    const data = await api.getById(id);
    if (data?.recommendation) {
      // Show in a modal
      showPlanModal(data.recommendation);
    }
  } catch (error) {
    showToast(error.message, 'error');
  }
}

function showPlanModal(rec) {
  const plan = rec.daily_plan || rec;

  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = `
    <div class="modal" style="max-width:700px;width:95%;">
      <div class="flex-between mb-2">
        <h2>Meal Plan Details</h2>
        <button class="btn btn-sm btn-secondary" onclick="this.closest('.modal-overlay').remove()">✕</button>
      </div>

      <div class="stats-grid" style="grid-template-columns:repeat(4,1fr);gap:10px;">
        <div class="stat-card" style="padding:12px;">
          <div class="stat-icon green" style="width:36px;height:36px;font-size:0.9rem;">BMI</div>
          <div class="stat-info"><h3 style="font-size:1.2rem;">${formatNum(rec.bmi)}</h3><p>${rec.bmi_category || ''}</p></div>
        </div>
        <div class="stat-card" style="padding:12px;">
          <div class="stat-icon blue" style="width:36px;height:36px;font-size:0.9rem;">🔥</div>
          <div class="stat-info"><h3 style="font-size:1.2rem;">${formatNum(rec.daily_calories, 0)}</h3><p>kcal</p></div>
        </div>
        <div class="stat-card" style="padding:12px;">
          <div class="stat-icon yellow" style="width:36px;height:36px;font-size:0.9rem;">💪</div>
          <div class="stat-info"><h3 style="font-size:1.2rem;">${formatNum(rec.target_protein || plan?.target_protein, 0)}g</h3><p>Protein</p></div>
        </div>
        <div class="stat-card" style="padding:12px;">
          <div class="stat-icon green" style="width:36px;height:36px;font-size:0.9rem;">🍞</div>
          <div class="stat-info"><h3 style="font-size:1.2rem;">${formatNum(rec.target_carbohydrates || plan?.target_carbohydrates, 0)}g</h3><p>Carbs</p></div>
        </div>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px;">
        ${renderModalMeal('Breakfast', plan.breakfast, 'breakfast')}
        ${renderModalMeal('Lunch', plan.lunch, 'lunch')}
        ${renderModalMeal('Dinner', plan.dinner, 'dinner')}
        ${renderModalMeal('Snacks', plan.snacks, 'snack')}
      </div>
    </div>
  `;

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) overlay.remove();
  });

  document.body.appendChild(overlay);
}

function renderModalMeal(name, meal, type) {
  if (!meal || !meal.items || meal.items.length === 0) return '';

  const items = meal.items
    .map(
      (item) => `
      <div class="meal-item">
        <div class="meal-item-info">
          <h4 style="font-size:0.82rem;">${item.name}</h4>
          <span style="font-size:0.72rem;">${item.quantity || ''} · ${item.category || ''}</span>
        </div>
        <div class="meal-item-cal" style="font-size:0.8rem;">${formatNum(item.calories, 0)} kcal</div>
      </div>
    `
    )
    .join('');

  return `
    <div class="meal-card" style="border:1px solid var(--border);">
      <div class="meal-card-header" style="padding:10px 14px;">
        <h3 style="font-size:0.9rem;">${name}</h3>
        <span class="meal-badge ${type}" style="font-size:0.68rem;">${formatNum(meal.total_calories, 0)} kcal</span>
      </div>
      <div class="meal-card-body" style="padding:8px 14px;">
        ${items}
      </div>
    </div>
  `;
}

async function regenerateFromHistory(id) {
  if (!id) return;
  try {
    const api = await NutriAPI.recommendation;
    showToast('Regenerating plan...', 'info', 2000);
    const data = await api.regenerate(id);
    if (data?.success) {
      showToast('Plan regenerated!', 'success');
      await loadHistory();
    }
  } catch (error) {
    showToast(error.message, 'error');
  }
}

async function deletePlan(id) {
  if (!id) return;
  if (!confirm('Are you sure you want to delete this meal plan?')) return;

  try {
    const api = await NutriAPI.recommendation;
    await api.delete(id);
    showToast('Plan deleted', 'success');
    await loadHistory();
  } catch (error) {
    showToast(error.message, 'error');
  }
}
