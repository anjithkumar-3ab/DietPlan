/**
 * NutriAI – Main Application Router
 * Handles SPA navigation, sidebar state, toast notifications, and page lifecycle.
 */

// ── State ──

let currentPage = 'dashboard';
let sidebarOpen = false;

// ── Navigation ──

function navigate(page) {
  if (currentPage === page) return;

  currentPage = page;
  highlightNav(page);
  renderPage(page);
  closeSidebar();
}

function highlightNav(page) {
  document.querySelectorAll('.nav-item').forEach((item) => {
    item.classList.toggle('active', item.dataset.page === page);
  });
}

async function renderPage(page) {
  const container = document.getElementById('mainContent');
  if (!container) return;

  // Show loading state
  container.innerHTML = '<div class="spinner"></div>';

  // Each page has a render function: renderDashboard(), renderProfile(), etc.
  const renderFn = window[`render${camelCase(page)}`];

  if (typeof renderFn === 'function') {
    try {
      await renderFn(container);
    } catch (error) {
      console.error(`Error rendering page "${page}":`, error);
      container.innerHTML = `
        <div class="empty-state">
          <h3>Failed to load page</h3>
          <p>${error.message}</p>
          <button class="btn btn-primary" onclick="navigate('dashboard')">Back to Dashboard</button>
        </div>`;
    }
  } else {
    container.innerHTML = `
      <div class="empty-state">
        <h3>Page Not Found</h3>
        <p>The page "${page}" does not exist.</p>
        <button class="btn btn-primary" onclick="navigate('dashboard')">Go to Dashboard</button>
      </div>`;
  }
}

function camelCase(str) {
  return str.replace(/_([a-z])/g, (_, c) => c.toUpperCase()).replace(/^[a-z]/, (c) => c.toUpperCase());
}

// ── Sidebar Toggle (Mobile) ──

function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  sidebarOpen = !sidebarOpen;
  sidebar.classList.toggle('open', sidebarOpen);
  if (overlay) overlay.style.display = sidebarOpen ? 'block' : 'none';
}

function closeSidebar() {
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  sidebarOpen = false;
  sidebar.classList.remove('open');
  if (overlay) overlay.style.display = 'none';
}

// ── Toast Notifications ──

function showToast(message, type = 'info', duration = 3500) {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const id = `toast-${Date.now()}`;
  const toast = document.createElement('div');
  toast.id = id;
  toast.style.cssText = `
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 18px;
    font-size: 0.88rem;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 280px;
    max-width: 420px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    animation: slideInRight 0.3s ease;
    cursor: pointer;
  `;

  const colors = {
    success: '#4ade80',
    error: '#ef4444',
    info: '#60a5fa',
    warning: '#f59e0b',
  };

  const icons = {
    success: '✓',
    error: '✕',
    info: 'ℹ',
    warning: '⚠',
  };

  toast.innerHTML = `
    <span style="color:${colors[type]};font-weight:700;font-size:1rem;">${icons[type]}</span>
    <span style="flex:1;">${message}</span>
  `;

  toast.addEventListener('click', () => dismissToast(id));

  container.appendChild(toast);

  setTimeout(() => dismissToast(id), duration);
}

function dismissToast(id) {
  const toast = document.getElementById(id);
  if (toast) {
    toast.style.animation = 'slideOutRight 0.25s ease forwards';
    setTimeout(() => toast.remove(), 300);
  }
}

// ── Utility: Format number ──

function formatNum(n, decimals = 1) {
  if (n == null || isNaN(n)) return '—';
  return Number(n).toFixed(decimals);
}

// ── Utility: Format date ──

function formatDate(dateStr) {
  if (!dateStr) return '—';
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

// ── Utility: HTML escape ──

function escHtml(str) {
  if (!str) return '';
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}

// ── Animation keyframes for toasts (injected once) ──

(function injectKeyframes() {
  if (document.getElementById('nutriai-keyframes')) return;
  const style = document.createElement('style');
  style.id = 'nutriai-keyframes';
  style.textContent = `
    @keyframes slideInRight {
      from { transform: translateX(120%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOutRight {
      from { transform: translateX(0); opacity: 1; }
      to { transform: translateX(120%); opacity: 0; }
    }
  `;
  document.head.appendChild(style);
})();

// ── Initialize ──

document.addEventListener('DOMContentLoaded', () => {
  renderPage('dashboard');
  highlightNav('dashboard');
});

// ── Handle browser back/forward ──

window.addEventListener('popstate', (e) => {
  const page = e.state?.page || 'dashboard';
  renderPage(page);
  highlightNav(page);
});
