/**
 * NutriAI – Settings Page
 * Theme toggle, about info, and backend status.
 */

let currentTheme = 'dark';

async function renderSettings(container) {
  container.innerHTML = `
    <!-- Top Bar -->
    <div class="topbar">
      <div class="flex gap-2" style="align-items:center;">
        <button class="mobile-menu-btn" onclick="toggleSidebar()" aria-label="Menu">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <h1>Settings</h1>
      </div>
    </div>

    <!-- Theme -->
    <div class="card mb-3">
      <div class="card-header">
        <span class="card-title">Appearance</span>
      </div>
      <div class="flex-between">
        <div>
          <p style="font-weight:600;">Theme</p>
          <p style="font-size:0.82rem;color:var(--text-muted);">Choose your preferred color theme</p>
        </div>
        <div class="flex gap-1">
          <button class="btn btn-sm ${currentTheme === 'dark' ? 'btn-primary' : 'btn-secondary'}" onclick="setTheme('dark')">🌙 Dark</button>
          <button class="btn btn-sm ${currentTheme === 'light' ? 'btn-primary' : 'btn-secondary'}" onclick="setTheme('light')">☀️ Light</button>
        </div>
      </div>
    </div>

    <!-- Backend Status -->
    <div class="card mb-3">
      <div class="card-header">
        <span class="card-title">Backend Status</span>
        <span id="backendStatusBadge" class="badge badge-warning">Checking...</span>
      </div>
      <div id="backendStatusDetails" style="font-size:0.88rem;color:var(--text-secondary);">
        Checking connection to FastAPI backend...
      </div>
    </div>

    <!-- About -->
    <div class="card mb-3">
      <div class="card-header">
        <span class="card-title">About NutriAI</span>
      </div>
      <div style="font-size:0.9rem;color:var(--text-secondary);line-height:1.8;">
        <p><strong style="color:var(--text-primary);">Version:</strong> 1.0.0</p>
        <p><strong style="color:var(--text-primary);">Backend:</strong> FastAPI + MongoDB Atlas</p>
        <p><strong style="color:var(--text-primary);">Frontend:</strong> Vanilla HTML/CSS/JS</p>
        <p style="margin-top:12px;">
          NutriAI is an AI-Based Personalized Diet Planning & Recommendation System.
          It generates intelligent daily meal plans from a curated food database,
          respecting dietary preferences, allergies, and medical conditions.
        </p>
        <div style="margin-top:16px;display:flex;gap:8px;flex-wrap:wrap;">
          <span class="badge badge-success">🥗 Personalized Plans</span>
          <span class="badge badge-info">📊 BMI & BMR Calculation</span>
          <span class="badge badge-warning">🍎 Food Database</span>
          <span class="badge badge-success">⚠️ Allergy Filters</span>
        </div>
      </div>
    </div>

    <!-- API Endpoints Info -->
    <div class="card">
      <div class="card-header">
        <span class="card-title">API Endpoints</span>
      </div>
      <div class="table-container mt-2">
        <table>
          <thead>
            <tr>
              <th>Method</th>
              <th>Endpoint</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><span class="badge badge-success">POST</span></td>
              <td style="font-family:monospace;font-size:0.82rem;">/profile/</td>
              <td>Save health profile</td>
            </tr>
            <tr>
              <td><span class="badge badge-success">POST</span></td>
              <td style="font-family:monospace;font-size:0.82rem;">/recommendation/generate</td>
              <td>Generate diet plan</td>
            </tr>
            <tr>
              <td><span class="badge badge-info">GET</span></td>
              <td style="font-family:monospace;font-size:0.82rem;">/recommendation/history</td>
              <td>Get plan history</td>
            </tr>
            <tr>
              <td><span class="badge badge-info">GET</span></td>
              <td style="font-family:monospace;font-size:0.82rem;">/recommendation/{id}</td>
              <td>Get plan by ID</td>
            </tr>
            <tr>
              <td><span class="badge badge-danger">DELETE</span></td>
              <td style="font-family:monospace;font-size:0.82rem;">/recommendation/{id}</td>
              <td>Delete a plan</td>
            </tr>
            <tr>
              <td><span class="badge badge-success">POST</span></td>
              <td style="font-family:monospace;font-size:0.82rem;">/recommendation/{id}/regenerate</td>
              <td>Regenerate plan</td>
            </tr>
            <tr>
              <td><span class="badge badge-info">GET</span></td>
              <td style="font-family:monospace;font-size:0.82rem;">/foods/</td>
              <td>List all foods</td>
            </tr>
            <tr>
              <td><span class="badge badge-info">GET</span></td>
              <td style="font-family:monospace;font-size:0.82rem;">/health</td>
              <td>Health check</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `;

  // Check backend status
  checkBackendStatus();
}

async function checkBackendStatus() {
  const badge = document.getElementById('backendStatusBadge');
  const details = document.getElementById('backendStatusDetails');

  try {
    const api = await NutriAPI.health;
    const data = await api.check();

    badge.textContent = 'Connected';
    badge.className = 'badge badge-success';
    details.innerHTML = `
      <div class="flex gap-2" style="margin-top:8px;">
        <span>✅ Backend: ${data.status || 'healthy'}</span>
        <span>🗄 Database: ${data.database || 'connected'}</span>
        <span>🔗 Service: ${data.service || 'NutriAI Backend'}</span>
      </div>
    `;
  } catch {
    badge.textContent = 'Disconnected';
    badge.className = 'badge badge-danger';
    details.innerHTML = `
      <p style="color:var(--danger);margin-top:8px;">
        ⚠️ Unable to connect to the backend at localhost:8000.
        Please ensure the FastAPI server is running.
      </p>
    `;
  }
}

function setTheme(theme) {
  currentTheme = theme;

  const root = document.documentElement;

  if (theme === 'light') {
    root.style.setProperty('--bg-primary', '#f5f5f9');
    root.style.setProperty('--bg-secondary', '#ffffff');
    root.style.setProperty('--bg-card', '#ffffff');
    root.style.setProperty('--bg-sidebar', '#f0f0f5');
    root.style.setProperty('--bg-hover', '#e8e8f0');
    root.style.setProperty('--text-primary', '#1a1a2e');
    root.style.setProperty('--text-secondary', '#4a4a6a');
    root.style.setProperty('--text-muted', '#8a8aa0');
    root.style.setProperty('--border', '#d4d4e0');
    root.style.setProperty('--border-light', '#c0c0d0');
    root.style.setProperty('--accent-glow', 'rgba(34, 197, 94, 0.12)');
  } else {
    root.style.setProperty('--bg-primary', '#0f0f1a');
    root.style.setProperty('--bg-secondary', '#1a1a2e');
    root.style.setProperty('--bg-card', '#1e1e32');
    root.style.setProperty('--bg-sidebar', '#13132b');
    root.style.setProperty('--bg-hover', '#25254a');
    root.style.setProperty('--text-primary', '#e8e8f0');
    root.style.setProperty('--text-secondary', '#a0a0b8');
    root.style.setProperty('--text-muted', '#6b6b80');
    root.style.setProperty('--border', '#2a2a45');
    root.style.setProperty('--border-light', '#35355a');
    root.style.setProperty('--accent-glow', 'rgba(74, 222, 128, 0.15)');
  }

  showToast(`Theme switched to ${theme} mode`, 'info', 2000);

  // Re-render settings to update buttons
  const container = document.getElementById('mainContent');
  renderSettings(container);
}
