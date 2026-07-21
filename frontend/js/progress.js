/**
 * NutriAI – Progress Page
 * Shows weight and BMI progress from meal plan history.
 */

async function renderProgress(container) {
  container.innerHTML = `
    <!-- Top Bar -->
    <div class="topbar">
      <div class="flex gap-2" style="align-items:center;">
        <button class="mobile-menu-btn" onclick="toggleSidebar()" aria-label="Menu">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <h1>Progress</h1>
      </div>
    </div>

    <div id="progressContent">
      <div class="spinner"></div>
    </div>
  `;

  await loadProgress();
}

async function loadProgress() {
  const content = document.getElementById('progressContent');

  try {
    const api = await NutriAPI.recommendation;
    const data = await api.history(50, 0);

    if (!data?.recommendations || data.recommendations.length < 2) {
      content.innerHTML = `
        <div class="empty-state">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          <h3>Not enough data yet</h3>
          <p>Generate at least 2 meal plans to see your BMI and calorie progress over time.</p>
          <button class="btn btn-primary" onclick="navigate('diet_planner')">Generate Plans</button>
        </div>
      `;
      return;
    }

    // Sort by date ascending for charts
    const sorted = [...data.recommendations].sort(
      (a, b) => new Date(a.created_at) - new Date(b.created_at)
    );

    renderProgressCharts(content, sorted);
  } catch (error) {
    content.innerHTML = `
      <div class="alert alert-error">
        <span>Failed to load data: ${error.message}</span>
        <button class="btn btn-sm btn-secondary" onclick="loadProgress()" style="margin-left:auto;">Retry</button>
      </div>
    `;
  }
}

function renderProgressCharts(container, plans) {
  const bmiValues = plans.map((p) => p.bmi).filter((v) => v != null);
  const calorieValues = plans.map((p) => p.daily_calories).filter((v) => v != null);
  const dates = plans.map((p) => formatDateShort(p.created_at));

  const bmiMin = Math.floor(Math.min(...bmiValues) - 2);
  const bmiMax = Math.ceil(Math.max(...bmiValues) + 2);
  const bmiRange = bmiMax - bmiMin || 1;

  const calMin = Math.floor(Math.min(...calorieValues) - 200);
  const calMax = Math.ceil(Math.max(...calorieValues) + 200);
  const calRange = calMax - calMin || 1;

  // Latest stats
  const latest = plans[plans.length - 1];
  const first = plans[0];
  const bmiChange = (latest.bmi - first.bmi).toFixed(1);
  const bmiTrend = latest.bmi > first.bmi ? '↑' : latest.bmi < first.bmi ? '↓' : '→';

  container.innerHTML = `
    <!-- Summary Stats -->
    <div class="stats-grid mb-3">
      <div class="stat-card">
        <div class="stat-icon green">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="20" x2="12" y2="10"/></svg>
        </div>
        <div class="stat-info">
          <h3>${formatNum(latest.bmi)}</h3>
          <p>Current BMI · ${latest.bmi_category || '—'}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon blue">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
        </div>
        <div class="stat-info">
          <h3>${bmiTrend} ${bmiChange}</h3>
          <p>BMI Change</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon yellow">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
        </div>
        <div class="stat-info">
          <h3>${formatNum(latest.daily_calories, 0)}</h3>
          <p>Latest Daily Calories</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon red">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20V10"/><path d="M18 20V4"/><path d="M6 20v-4"/></svg>
        </div>
        <div class="stat-info">
          <h3>${plans.length}</h3>
          <p>Total Plans</p>
        </div>
      </div>
    </div>

    <!-- BMI Chart -->
    <div class="card mb-3">
      <div class="card-header">
        <span class="card-title">BMI Progress</span>
        <span class="card-subtitle">Trend across ${plans.length} plans</span>
      </div>
      <div style="padding:8px 0;">
        ${renderBarChart(bmiValues, dates, bmiMin, bmiRange, 'BMI', 'var(--accent)')}
      </div>
    </div>

    <!-- Calories Chart -->
    <div class="card mb-3">
      <div class="card-header">
        <span class="card-title">Calorie Targets</span>
        <span class="card-subtitle">Daily calorie targets across plans</span>
      </div>
      <div style="padding:8px 0;">
        ${renderBarChart(calorieValues, dates, calMin, calRange, 'kcal', 'var(--info)')}
      </div>
    </div>

    <!-- History Table -->
    <div class="card">
      <div class="card-header">
        <span class="card-title">Plan History Log</span>
      </div>
      <div class="table-container mt-2">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>BMI</th>
              <th>Category</th>
              <th>BMR</th>
              <th>TDEE</th>
              <th>Calories</th>
              <th>Preference</th>
            </tr>
          </thead>
          <tbody>
            ${plans
              .slice()
              .reverse()
              .map(
                (p) => `
              <tr>
                <td>${formatDate(p.created_at)}</td>
                <td style="font-weight:600;color:var(--accent);">${formatNum(p.bmi)}</td>
                <td><span class="badge badge-info">${p.bmi_category || '—'}</span></td>
                <td>${formatNum(p.bmr, 0)}</td>
                <td>${formatNum(p.tdee, 0)}</td>
                <td><strong>${formatNum(p.daily_calories, 0)}</strong></td>
                <td><span class="badge badge-success">${p.food_preference || '—'}</span></td>
              </tr>
            `
              )
              .join('')}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

function renderBarChart(values, labels, min, range, unit, color) {
  if (!values.length) return '<p style="color:var(--text-muted);text-align:center;padding:20px;">No data</p>';

  const maxBarHeight = 200;

  return `
    <div style="display:flex;align-items:flex-end;gap:8px;height:${maxBarHeight + 40}px;padding:0 8px;position:relative;">
      ${values
        .map(
          (val, i) => {
            const height = ((val - min) / range) * maxBarHeight;
            const hue = 140 - (i / Math.max(values.length - 1, 1)) * 60;
            return `
            <div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;">
              <span style="font-size:0.68rem;color:var(--text-secondary);margin-bottom:4px;">${formatNum(val, 1)}</span>
              <div style="width:100%;max-width:60px;height:${height}px;background:${color};border-radius:6px 6px 0 0;opacity:0.85;transition:height 0.5s ease;min-height:4px;position:relative;"
                   title="${labels[i]}: ${formatNum(val, 1)} ${unit}">
              </div>
              <span style="font-size:0.6rem;color:var(--text-muted);margin-top:6px;writing-mode:vertical-lr;text-orientation:mixed;height:60px;text-align:left;"
                    title="${labels[i]}">${labels[i]}</span>
            </div>
          `;
          }
        )
        .join('')}
    </div>
  `;
}

function formatDateShort(dateStr) {
  if (!dateStr) return '—';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });
}
