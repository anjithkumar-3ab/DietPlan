import { useEffect, useState } from 'react'
import { Navigate, Route, Routes, useLocation, useNavigate } from 'react-router-dom'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts'
import './App.css'

const API = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const DEMO_MODE = true

function getStoredAdmin() {
  try {
    return JSON.parse(localStorage.getItem('dietplan_admin_user') || '{}')
  } catch {
    localStorage.removeItem('dietplan_admin_user')
    return {}
  }
}

async function api(path, options = {}) {
  const token = localStorage.getItem('dietplan_admin_token')
  const request = (baseUrl) => fetch(`${baseUrl}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  })
  let response
  try {
    response = await request(API)
  } catch {
    response = await request('http://127.0.0.1:8001')
  }
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.detail || data.message || 'Request failed')
  return data
}

function AdminLogin() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')

  const submit = async (event) => {
    event.preventEvent?.()
    event.preventDefault()
    setError('')
    try {
      const data = await api('/auth/login', { method: 'POST', body: JSON.stringify(form) })
      if (data.user.role !== 'admin') throw new Error('This account is not an administrator.')
      localStorage.setItem('dietplan_admin_token', data.access_token)
      localStorage.setItem('dietplan_admin_user', JSON.stringify(data.user))
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <main className="admin-login">
      <section className="login-card">
        <img className="admin-logo" src="/logo.png" alt="NutriAI" />
        <h1>DietPlan Admin</h1>
        <p>Secure administration portal</p>
        {error && <div className="error-box">{error}</div>}
        <form onSubmit={submit}>
          <label>Email<input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required /></label>
          <label>Password<input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required /></label>
          <button className="admin-button">Sign in as admin</button>
        </form>
      </section>
    </main>
  )
}

function ProtectedAdmin({ children }) {
  if (DEMO_MODE) return children
  const token = localStorage.getItem('dietplan_admin_token')
  const user = getStoredAdmin()
  if (!token) return <Navigate to="/login" replace />
  if (user.role !== 'admin') return <Navigate to="/login" replace />
  return children
}

function AdminLayout() {
  const navigate = useNavigate()
  const location = useLocation()
  const [user] = useState(() => getStoredAdmin())
  const logout = () => {
    localStorage.removeItem('dietplan_admin_token')
    localStorage.removeItem('dietplan_admin_user')
    navigate(DEMO_MODE ? '/dashboard' : '/login')
  }
  const active = (path) => location.pathname === path

  return (
    <div className="admin-shell">
      <aside className="admin-sidebar">
        <div className="admin-brand"><img className="admin-logo small" src="/logo.png" alt="NutriAI" /><span>DietPlan Admin</span></div>
        <nav>
          <button className={active('/dashboard') ? 'active' : ''} onClick={() => navigate('/dashboard')}>Dashboard</button>
          <button className={active('/users') ? 'active' : ''} onClick={() => navigate('/users')}>Users</button>
          <button className={active('/foods') ? 'active' : ''} onClick={() => navigate('/foods')}>Foods</button>
          <button className={active('/plans') ? 'active' : ''} onClick={() => navigate('/plans')}>Diet Plans</button>
          <button className={active('/calendar') ? 'active' : ''} onClick={() => navigate('/calendar')}>Calendar</button>
          <button className={active('/reports') ? 'active' : ''} onClick={() => navigate('/reports')}>Reports</button>
        </nav>
        <div className="admin-sidebar-user"><strong>{user.name || 'Admin'}</strong><button onClick={logout}>Dashboard</button></div>
      </aside>
      <main className="admin-content">
        <Routes>
          <Route path="/dashboard" element={<AdminDashboard />} />
          <Route path="/users" element={<UsersPage />} />
          <Route path="/foods" element={<FoodsPage />} />
          <Route path="/plans" element={<PlansPage />} />
          <Route path="/calendar" element={<CalendarPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </div>
  )
}

function AdminDashboard() {
  const [stats, setStats] = useState(null)
  const [error, setError] = useState('')
  useEffect(() => {
    api('/admin/dashboard').then((data) => setStats(data.stats)).catch((err) => setError(err.message))
  }, [])

  const cards = stats ? [
    ['Registered users', stats.total_users],
    ['Active users', stats.active_users],
    ['Food records', stats.food_count],
    ['Diet plans', stats.recommendation_count],
    ['Finalized plans', stats.finalized_plan_count || 0],
    ['Accepted plans', stats.accepted_plan_count || 0],
    ['Draft plans', stats.draft_plan_count || 0],
    ['Today plans', stats.today_plan_count || 0],
    ['Completed today', stats.completed_today_count || 0],
    ['Health profiles', stats.profile_count],
    ['Administrators', stats.admin_count],
  ] : []

  const registeredUsers = Number(stats?.total_users || 0)
  const activeUsers = Number(stats?.active_users || 0)
  const userActivityData = [
    { name: 'Active users', value: activeUsers },
    { name: 'Inactive users', value: Math.max(registeredUsers - activeUsers, 0) },
  ]

  return (
    <div>
      <header className="admin-header"><div><p>Administration</p><h1>System Dashboard</h1></div></header>
      {error && <div className="error-box">{error}</div>}
      <div className="stat-grid">
        {cards.map(([label, value]) => <article key={label}><span>{label}</span><strong>{value ?? 0}</strong></article>)}
      </div>
      <section className="admin-panel chart-panel">
        <h2>User activity</h2>
        <div className="chart-wrap">
          {stats ? (
            registeredUsers > 0 ? (
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie data={userActivityData} dataKey="value" nameKey="name" innerRadius={68} outerRadius={100} paddingAngle={3}>
                    <Cell fill="#2f7d67" />
                    <Cell fill="#d7e1da" />
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            ) : <div className="empty-chart">No users to show yet.</div>
          ) : <div className="empty-chart">Loading analytics...</div>}
        </div>
      </section>
    </div>
  )
}

function UsersPage() {
  const [users, setUsers] = useState([])
  const [search, setSearch] = useState('')
  const [message, setMessage] = useState('')

  const load = async () => {
    try {
      const data = await api(`/admin/users?limit=100&search=${encodeURIComponent(search)}`)
      setUsers(data.users)
    } catch (err) {
      setMessage(err.message)
    }
  }
  useEffect(() => {
    load()
  }, [])

  const toggle = async (user) => {
    try {
      await api(`/admin/users/${user._id}`, { method: 'PUT', body: JSON.stringify({ is_active: !user.is_active }) })
      setMessage('User status updated.')
      load()
    } catch (err) {
      setMessage(err.message)
    }
  }

  const remove = async (user) => {
    if (!window.confirm(`Delete ${user.name}?`)) return
    try {
      await api(`/admin/users/${user._id}`, { method: 'DELETE' })
      setMessage('User deleted.')
      load()
    } catch (err) {
      setMessage(err.message)
    }
  }

  return (
    <div>
      <header className="admin-header"><div><p>User management</p><h1>Registered Users</h1></div></header>
      {message && <div className="success-box">{message}</div>}
      <div className="toolbar"><input placeholder="Search name or email" value={search} onChange={(e) => setSearch(e.target.value)} /><button onClick={load}>Search</button></div>
      <section className="admin-panel table-panel">
        <table><thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody>{users.map((user) => <tr key={user._id}><td>{user.name}</td><td>{user.email}</td><td><span className={`role ${user.role}`}>{user.role}</span></td><td>{user.is_active === false ? 'Inactive' : 'Active'}</td><td><button className="table-action" onClick={() => toggle(user)}>{user.is_active === false ? 'Activate' : 'Deactivate'}</button><button className="table-action danger" onClick={() => remove(user)}>Delete</button></td></tr>)}</tbody>
        </table>
      </section>
    </div>
  )
}

function FoodsPage() {
  const blank = { food_name: '', meal_type: 'Breakfast', food_preference: 'Veg', calories: 0, protein: 0, carbohydrates: 0, fat: 0, fiber: 0, sugar: 0, sodium: 0, allergens: 'None', category: 'General' }
  const [foods, setFoods] = useState([])
  const [form, setForm] = useState(blank)
  const [editing, setEditing] = useState(null)
  const [search, setSearch] = useState('')
  const [message, setMessage] = useState('')

  const load = async () => {
    try {
      const data = await api(`/admin/foods?limit=100&search=${encodeURIComponent(search)}`)
      setFoods(data.foods)
    } catch (err) {
      setMessage(err.message)
    }
  }
  useEffect(() => {
    load()
  }, [])

  const submit = async (event) => {
    event.preventDefault()
    const payload = { ...form, calories: Number(form.calories), protein: Number(form.protein), carbohydrates: Number(form.carbohydrates), fat: Number(form.fat), fiber: Number(form.fiber), sugar: Number(form.sugar), sodium: Number(form.sodium) }
    try {
      await api(editing ? `/admin/foods/${editing}` : '/admin/foods', { method: editing ? 'PUT' : 'POST', body: JSON.stringify(payload) })
      setMessage(editing ? 'Food updated.' : 'Food added.')
      setForm(blank)
      setEditing(null)
      load()
    } catch (err) {
      setMessage(err.message)
    }
  }

  const edit = (food) => {
    setEditing(food._id)
    setForm({ ...blank, ...food })
  }

  const remove = async (food) => {
    if (!window.confirm(`Delete ${food.food_name || food.name}?`)) return
    try {
      await api(`/admin/foods/${food._id}`, { method: 'DELETE' })
      setMessage('Food deleted.')
      load()
    } catch (err) {
      setMessage(err.message)
    }
  }

  return (
    <div>
      <header className="admin-header"><div><p>Food database</p><h1>Manage Foods</h1></div></header>
      {message && <div className="success-box">{message}</div>}
      <section className="admin-panel food-editor">
        <h2>{editing ? 'Edit food' : 'Add new food'}</h2>
        <form onSubmit={submit}>
          <div className="form-grid">
            <label>Food name<input value={form.food_name || form.name || ''} onChange={(e) => setForm({ ...form, food_name: e.target.value })} required /></label>
            <label>Meal type<select value={form.meal_type} onChange={(e) => setForm({ ...form, meal_type: e.target.value })}><option>Breakfast</option><option>Lunch</option><option>Dinner</option><option>Snack</option></select></label>
            <label>Preference<select value={form.food_preference} onChange={(e) => setForm({ ...form, food_preference: e.target.value })}><option>Veg</option><option>Non-Veg</option><option>Any</option></select></label>
            <label>Calories<input type="number" min="0" value={form.calories} onChange={(e) => setForm({ ...form, calories: e.target.value })} required /></label>
            <label>Protein (g)<input type="number" min="0" value={form.protein} onChange={(e) => setForm({ ...form, protein: e.target.value })} required /></label>
            <label>Carbs (g)<input type="number" min="0" value={form.carbohydrates} onChange={(e) => setForm({ ...form, carbohydrates: e.target.value })} required /></label>
            <label>Fat (g)<input type="number" min="0" value={form.fat} onChange={(e) => setForm({ ...form, fat: e.target.value })} required /></label>
            <label>Fiber (g)<input type="number" min="0" value={form.fiber} onChange={(e) => setForm({ ...form, fiber: e.target.value })} /></label>
          </div>
          <div className="form-actions"><button className="admin-button compact" type="submit">{editing ? 'Update food' : 'Add food'}</button>{editing && <button type="button" className="secondary-button" onClick={() => { setEditing(null); setForm(blank) }}>Cancel</button>}</div>
        </form>
      </section>
      <div className="toolbar"><input placeholder="Search food" value={search} onChange={(e) => setSearch(e.target.value)} /><button onClick={load}>Search</button></div>
      <section className="admin-panel table-panel">
        <table><thead><tr><th>Food</th><th>Meal</th><th>Calories</th><th>Protein</th><th>Carbs</th><th>Fat</th><th>Actions</th></tr></thead>
          <tbody>{foods.map((food) => <tr key={food._id}><td>{food.food_name || food.name}</td><td>{food.meal_type}</td><td>{food.calories}</td><td>{food.protein}</td><td>{food.carbohydrates}</td><td>{food.fat}</td><td><button className="table-action" onClick={() => edit(food)}>Edit</button><button className="table-action danger" onClick={() => remove(food)}>Delete</button></td></tr>)}</tbody>
        </table>
      </section>
    </div>
  )
}

function PlansPage() {
  const [plans, setPlans] = useState([])
  const [error, setError] = useState('')
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [selectedPlan, setSelectedPlan] = useState(null)

  useEffect(() => {
    api('/admin/recommendations?limit=100')
      .then((data) => setPlans((data.recommendations || []).map((plan) => ({
        ...plan,
        created_at: plan.created_at ? new Date(plan.created_at) : null,
      }))))
      .catch((err) => setError(err.message))
  }, [])

  const visiblePlans = plans.filter((plan) => {
    const name = (plan.user_name || plan.request_params?.name || '').toLowerCase()
    const matchesSearch = !search.trim() || name.includes(search.trim().toLower())
    const status = plan.status || (plan.is_accepted ? 'accepted' : plan.is_finalized ? 'finalized' : 'draft')
    const matchesStatus = statusFilter === 'all' || status === statusFilter
    return matchesSearch && matchesStatus
  })

  const closeDetails = () => setSelectedPlan(null)
  const selectedDiet = selectedPlan?.daily_plan
  const mealDetails = [
    ['breakfast', 'Breakfast'],
    ['lunch', 'Lunch'],
    ['dinner', 'Dinner'],
    ['snacks', 'Snacks'],
  ]

  return (
    <div>
      <header className="admin-header"><div><p>Recommendation management</p><h1>Diet Plans</h1></div></header>
      {error && <div className="error-box">{error}</div>}
      <div className="toolbar plan-toolbar">
        <input placeholder="Search by user name" value={search} onChange={(event) => setSearch(event.target.value)} />
        <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>
          <option value="all">All statuses</option>
          <option value="draft">Draft</option>
          <option value="accepted">Accepted</option>
          <option value="finalized">Finalized</option>
        </select>
      </div>
      <section className="admin-panel table-panel">
        <table><thead><tr><th>User</th><th>Plan Date</th><th>Calories</th><th>BMI</th><th>Preference</th><th>Status</th><th>Meals Taken</th><th>Completion</th></tr></thead>
          <tbody>{visiblePlans.map((plan) => {
            const checklist = plan.meal_checklist || {}
            const taken = Object.values(checklist).filter(Boolean).length
            const status = plan.status || (plan.is_accepted ? 'accepted' : plan.is_finalized ? 'finalized' : 'draft')
            const userName = plan.user_name || plan.request_params?.name || 'Unowned'
            return (
              <tr
                key={plan._id}
                className="plan-row"
                role="button"
                tabIndex={0}
                aria-label={`View diet details for ${userName}`}
                onClick={() => setSelectedPlan(plan)}
                onKeyDown={(event) => {
                  if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault()
                    setSelectedPlan(plan)
                  }
                }}
              >
                <td>{userName}</td>
                <td>{plan.plan_date || (plan.created_at instanceof Date && !Number.isNaN(plan.created_at) ? plan.created_at.toISOString().slice(0, 10) : '—')}</td>
                <td>{Number(plan.daily_calories || 0).toFixed(0)} kcal</td>
                <td>{Number(plan.bmi || 0).toFixed(1)}</td>
                <td>{plan.food_preference}</td>
                <td><span className={`role ${status}`}>{status}</span></td>
                <td>{taken} / 4</td>
                <td>{plan.completion_percentage || 0}%</td>
              </tr>
            )
          })}</tbody>
        </table>
      </section>
      {selectedPlan && (
        <div
          className="plan-modal-backdrop"
          onClick={(event) => {
            if (event.target === event.currentTarget) closeDetails()
          }}
        >
          <section className="plan-modal" role="dialog" aria-modal="true" aria-labelledby="plan-modal-title">
            <header className="plan-modal-header">
              <div>
                <p>Diet plan details</p>
                <h2 id="plan-modal-title">{selectedPlan.user_name || selectedPlan.request_params?.name || 'Personalized diet plan'}</h2>
              </div>
              <button type="button" className="plan-modal-close" onClick={closeDetails} aria-label="Close diet details">×</button>
            </header>
            <div className="plan-detail-grid">
              <article><span>Plan date</span><strong>{selectedPlan.plan_date || '—'}</strong></article>
              <article><span>Status</span><strong>{selectedPlan.status || (selectedPlan.is_accepted ? 'accepted' : selectedPlan.is_finalized ? 'finalized' : 'draft')}</strong></article>
              <article><span>Daily calories</span><strong>{Number(selectedPlan.daily_calories || selectedDiet?.target_daily_calories || 0).toFixed(0)} kcal</strong></article>
              <article><span>BMI</span><strong>{Number(selectedPlan.bmi || 0).toFixed(1)}{selectedPlan.bmi_category ? ` · ${selectedPlan.bmi_category}` : ''}</strong></article>
              <article><span>Preference</span><strong>{selectedPlan.food_preference || '—'}</strong></article>
              <article><span>Goal</span><strong>{selectedPlan.request_params?.goal || '—'}</strong></article>
            </div>
            {selectedDiet ? (
              <>
                <div className="plan-detail-macros">
                  <span>Protein <strong>{Number(selectedDiet.total_protein || 0).toFixed(1)} / {Number(selectedDiet.target_protein || selectedPlan.target_protein || 0).toFixed(1)} g</strong></span>
                  <span>Carbs <strong>{Number(selectedDiet.total_carbohydrates || 0).toFixed(1)} / {Number(selectedDiet.target_carbohydrates || selectedPlan.target_carbohydrates || 0).toFixed(1)} g</strong></span>
                  <span>Fat <strong>{Number(selectedDiet.total_fat || 0).toFixed(1)} / {Number(selectedDiet.target_fat || selectedPlan.target_fat || 0).toFixed(1)} g</strong></span>
                  <span>Water <strong>{Number(selectedDiet.recommended_water_liters || 0).toFixed(1)} L</strong></span>
                </div>
                <div className="plan-meal-list">
                  {mealDetails.map(([key, label]) => {
                    const meal = selectedDiet[key]
                    return (
                      <article className="plan-meal-card" key={key}>
                        <div className="plan-meal-heading">
                          <h3>{label}</h3>
                          <strong>{Number(meal?.total_calories || 0).toFixed(0)} kcal</strong>
                        </div>
                        {meal?.items?.length ? (
                          <ul>
                            {meal.items.map((item, index) => (
                              <li key={`${item.food_id || item.name}-${index}`}>
                                <span><strong>{item.name}</strong>{item.quantity && <small>{item.quantity}</small>}</span>
                                <span>{Number(item.calories || 0).toFixed(0)} kcal · P {Number(item.protein || 0).toFixed(1)}g · C {Number(item.carbohydrates || 0).toFixed(1)}g · F {Number(item.fat || 0).toFixed(1)}g</span>
                              </li>
                            ))}
                          </ul>
                        ) : <p className="plan-meal-empty">No food items listed.</p>}
                      </article>
                    )
                  })}
                </div>
              </>
            ) : <p className="plan-meal-empty">Detailed meals are not available for this plan.</p>}
          </section>
        </div>
      )}
    </div>
  )
}

function formatDateKey(date) {
  const year = date.getFullYear()
  const monthNumber = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${monthNumber}-${day}`
}

function CalendarPage() {
  const [today, setToday] = useState(() => new Date())
  const [month, setMonth] = useState(new Date(today.getFullYear(), today.getMonth(), 1))
  const [events, setEvents] = useState([])
  const [users, setUsers] = useState([])
  const [selectedDate, setSelectedDate] = useState(today)
  const [statusFilter, setStatusFilter] = useState('all')
  const [message, setMessage] = useState('')
  const [form, setForm] = useState({
    title: '',
    description: '',
    event_type: 'reminder',
    status: 'scheduled',
    start_at: `${formatDateKey(today)}T09:00`,
    end_at: `${formatDateKey(today)}T09:30`,
    all_day: true,
    timezone: 'Asia/Kolkata',
    user_id: '',
  })

  const dateKey = (date) => {
    return formatDateKey(date)
  }

  const load = async () => {
    const start = new Date(month.getFullYear(), month.getMonth(), 1)
    const end = new Date(month.getFullYear(), month.getMonth() + 1, 0, 23, 59, 59)
    try {
      const [calendarData, usersData] = await Promise.all([
        api(`/admin/calendar?start=${encodeURIComponent(start.toISOString())}&end=${encodeURIComponent(end.toISOString())}&status=${statusFilter === 'all' ? '' : statusFilter}`),
        api('/admin/users?limit=100'),
      ])
      setEvents(calendarData.events || [])
      setUsers(usersData.users || [])
    } catch (err) {
      setMessage(err.message)
    }
  }

  useEffect(() => {
    load()
  }, [month, statusFilter])

  useEffect(() => {
    const refreshToday = () => {
      const currentDate = new Date()
      if (formatDateKey(currentDate) !== formatDateKey(today)) {
        setToday(currentDate)
        setMonth(new Date(currentDate.getFullYear(), currentDate.getMonth(), 1))
        setSelectedDate(currentDate)
        setForm((currentForm) => ({
          ...currentForm,
          start_at: `${formatDateKey(currentDate)}T09:00`,
          end_at: `${formatDateKey(currentDate)}T09:30`,
        }))
      }
    }

    const intervalId = window.setInterval(refreshToday, 60_000)
    document.addEventListener('visibilitychange', refreshToday)
    return () => {
      window.clearInterval(intervalId)
      document.removeEventListener('visibilitychange', refreshToday)
    }
  }, [today])

  const moveMonth = (offset) => setMonth(new Date(month.getFullYear(), month.getMonth() + offset, 1))

  const firstCell = new Date(month.getFullYear(), month.getMonth(), 1)
  firstCell.setDate(1 - firstCell.getDay())
  const days = Array.from({ length: 42 }, (_, index) => {
    const date = new Date(firstCell)
    date.setDate(firstCell.getDate() + index)
    return date
  })

  const eventDateKey = (value) => {
    if (!value) return ''
    const date = new Date(value)
    return Number.isNaN(date.getTime()) ? String(value).slice(0, 10) : dateKey(date)
  }

  const submit = async (event) => {
    event.preventDefault()
    setMessage('')
    try {
      await api('/admin/calendar', {
        method: 'POST',
        body: JSON.stringify({
          ...form,
          start_at: form.all_day ? `${dateKey(selectedDate)}T00:00:00Z` : new Date(form.start_at).toISOString(),
          end_at: form.all_day ? `${dateKey(selectedDate)}T23:59:59Z` : new Date(form.end_at).toISOString(),
          user_id: form.user_id || null,
        }),
      })
      setMessage('Calendar event saved.')
      setForm({ ...form, title: '', description: '' })
      load()
    } catch (err) {
      setMessage(err.message)
    }
  }

  const remove = async (calendarEvent) => {
    if (String(calendarEvent._id).startsWith('plan-')) {
      setMessage('Diet plan events are managed from Diet Plans.')
      return
    }
    if (!window.confirm(`Cancel "${calendarEvent.title}"?`)) return
    try {
      await api(`/admin/calendar/${calendarEvent._id}`, { method: 'DELETE' })
      setMessage('Calendar event cancelled.')
      load()
    } catch (err) {
      setMessage(err.message)
    }
  }

  const selectedKey = dateKey(selectedDate)
  const selectedEvents = events.filter((item) => eventDateKey(item.start_at) === selectedKey)

  return (
    <div>
      <header className="admin-header">
        <div><p>Schedule</p><h1>Calendar</h1></div>
        <button className="admin-button compact" onClick={() => {
          setSelectedDate(today)
          setForm({ ...form, start_at: `${dateKey(today)}T09:00`, end_at: `${dateKey(today)}T09:30` })
        }}>Today</button>
      </header>
      {message && <div className={message.includes('saved') || message.includes('cancelled') ? 'success-box' : 'error-box'}>{message}</div>}

      <div className="calendar-layout">
        <section className="admin-panel calendar-main">
          <div className="calendar-toolbar">
            <div>
              <button className="calendar-nav" onClick={() => moveMonth(-1)} aria-label="Previous month">‹</button>
              <button className="calendar-nav" onClick={() => moveMonth(1)} aria-label="Next month">›</button>
            </div>
            <h2>{month.toLocaleDateString(undefined, { month: 'long', year: 'numeric' })}</h2>
            <select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}>
              <option value="all">All events</option>
              <option value="scheduled">Scheduled</option>
              <option value="in_progress">In progress</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>

          <div className="calendar-weekdays">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => <span key={day}>{day}</span>)}
          </div>
          <div className="calendar-grid">
            {days.map((day) => {
              const key = dateKey(day)
              const dayEvents = events.filter((item) => eventDateKey(item.start_at) === key)
              const outside = day.getMonth() !== month.getMonth()
              const isToday = key === dateKey(today)
              const isSelected = key === selectedKey
              return (
                <button
                  type="button"
                  key={key}
                  className={`calendar-day ${outside ? 'outside' : ''} ${isToday ? 'today' : ''} ${isSelected ? 'selected' : ''}`}
                  onClick={() => setSelectedDate(day)}
                >
                  <span className="calendar-date">{day.getDate()}</span>
                  <div className="calendar-events">
                    {dayEvents.slice(0, 3).map((item) => (
                      <span key={item._id} className={`calendar-event ${item.event_type}`}>
                        {item.title}
                      </span>
                    ))}
                    {dayEvents.length > 3 && <span className="calendar-more">+{dayEvents.length - 3} more</span>}
                  </div>
                </button>
              )
            })}
          </div>
        </section>

        <aside className="calendar-side">
          <section className="admin-panel">
            <h2>{selectedDate.toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' })}</h2>
            <div className="selected-events">
              {selectedEvents.length ? selectedEvents.map((item) => (
                <article key={item._id} className={`selected-event ${item.event_type}`}>
                  <div>
                    <span className={`calendar-status ${item.status}`}>{item.status}</span>
                    <strong>{item.title}</strong>
                    {item.description && <p>{item.description}</p>}
                    {item.completion && <div className="completion-line"><span style={{ width: `${item.completion.percentage || 0}%` }} /></div>}
                  </div>
                  {!String(item._id).startsWith('plan-') && <button className="table-action danger" onClick={() => remove(item)}>Cancel</button>}
                </article>
              )) : <div className="empty-day">No events scheduled</div>}
            </div>
          </section>

          <section className="admin-panel calendar-form">
            <h2>Add event</h2>
            <form onSubmit={submit}>
              <label>Title<input value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} required /></label>
              <label>Description<textarea value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} /></label>
              <div className="calendar-form-grid">
                <label>Type<select value={form.event_type} onChange={(event) => setForm({ ...form, event_type: event.target.value })}>
                  <option value="reminder">Reminder</option>
                  <option value="consultation">Consultation</option>
                  <option value="follow_up">Follow-up</option>
                  <option value="diet_plan">Diet plan</option>
                </select></label>
                <label>Status<select value={form.status} onChange={(event) => setForm({ ...form, status: event.target.value })}>
                  <option value="scheduled">Scheduled</option>
                  <option value="in_progress">In progress</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select></label>
              </div>
              <label>User<select value={form.user_id} onChange={(event) => setForm({ ...form, user_id: event.target.value })}>
                <option value="">All users / no user</option>
                {users.map((user) => <option key={user._id} value={user._id}>{user.name}</option>)}
              </select></label>
              <label className="calendar-check"><input type="checkbox" checked={form.all_day} onChange={(event) => setForm({ ...form, all_day: event.target.checked })} /> All day</label>
              {!form.all_day && <div className="calendar-form-grid">
                <label>Starts<input type="datetime-local" value={form.start_at} onChange={(event) => setForm({ ...form, start_at: event.target.value })} required /></label>
                <label>Ends<input type="datetime-local" value={form.end_at} onChange={(event) => setForm({ ...form, end_at: event.target.value })} required /></label>
              </div>}
              <button className="admin-button" type="submit">Save event</button>
            </form>
          </section>
        </aside>
      </div>
    </div>
  )
}

function ReportsPage() {
  const powerBiUrl = import.meta.env.VITE_POWERBI_URL
  const [stats, setStats] = useState(null)
  const [plans, setPlans] = useState([])
  const [foods, setFoods] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      api('/admin/dashboard'),
      api('/admin/recommendations?limit=100'),
      api('/admin/foods?limit=100'),
    ])
      .then(([dashboardData, planData, foodData]) => {
        setStats(dashboardData.stats)
        setPlans(planData.recommendations || [])
        setFoods(foodData.foods || [])
      })
      .catch((err) => setError(err.message))
  }, [])

  const statusData = ['accepted', 'draft', 'finalized'].map((status) => ({
    name: status[0].toUpperCase() + status.slice(1),
    value: plans.filter((plan) => {
      const actual = plan.status || (plan.is_accepted ? 'accepted' : plan.is_finalized ? 'finalized' : 'draft')
      return actual === status
    }).length,
  })).filter((item) => item.value > 0)

  const preferenceData = ['Veg', 'Non-Veg', 'Any'].map((preference) => ({
    name: preference,
    value: plans.filter((plan) => (plan.food_preference || 'Any') === preference).length,
  })).filter((item) => item.value > 0)

  const nutritionData = [
    { name: 'Protein', value: foods.reduce((total, food) => total + Number(food.protein || 0), 0) },
    { name: 'Carbs', value: foods.reduce((total, food) => total + Number(food.carbohydrates || 0), 0) },
    { name: 'Fat', value: foods.reduce((total, food) => total + Number(food.fat || 0), 0) },
  ].map((item) => ({
    ...item,
    value: foods.length ? item.value / foods.length : 0,
  }))

  const statusColors = ['#16a34a', '#f59e0b', '#2563eb']
  const preferenceColors = ['#16a34a', '#ef4444', '#64748b']

  return (
    <div>
      <header className="admin-header"><div><p>Analytics</p><h1>Reports</h1></div></header>
      {error && <div className="error-box">{error}</div>}

      {powerBiUrl && (
        <section className="admin-panel powerbi-panel">
          <iframe title="Power BI report" src={powerBiUrl} />
        </section>
      )}

      <div className="report-actions">
        <a className="report-download" href="/Nutri.pbix" download>
          Download Power BI Report (.pbix)
        </a>
      </div>

      <div className="report-grid">
        <section className="admin-panel report-card">
          <h2>Plan Status</h2>
          <div className="report-chart">
            {statusData.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={statusData} dataKey="value" nameKey="name" innerRadius="48%" outerRadius="72%" paddingAngle={2}>
                    {statusData.map((item, index) => <Cell key={item.name} fill={statusColors[index % statusColors.length]} />)}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            ) : <div className="empty-chart">No diet plan data</div>}
          </div>
        </section>

        <section className="admin-panel report-card">
          <h2>Food Preference Usage</h2>
          <div className="report-chart">
            {preferenceData.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={preferenceData} dataKey="value" nameKey="name" innerRadius="48%" outerRadius="72%" paddingAngle={2}>
                    {preferenceData.map((item, index) => <Cell key={item.name} fill={preferenceColors[index % preferenceColors.length]} />)}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            ) : <div className="empty-chart">No preference data</div>}
          </div>
        </section>

        <section className="admin-panel report-card wide">
          <h2>Average Nutrition per Food</h2>
          <div className="report-chart">
            {foods.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={nutritionData}>
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip formatter={(value) => [`${Number(value).toFixed(1)} g`, 'Average per item']} />
                  <Bar dataKey="value" name="Average per item" fill="#2f7d67" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : <div className="empty-chart">No food data available</div>}
          </div>
        </section>
      </div>

      <div className="report-summary-grid">
        <section className="admin-panel"><span>Registered Users</span><strong>{stats?.total_users || 0}</strong></section>
        <section className="admin-panel"><span>Food Records</span><strong>{stats?.food_count || 0}</strong></section>
        <section className="admin-panel"><span>Diet Plans</span><strong>{stats?.recommendation_count || 0}</strong></section>
        <section className="admin-panel"><span>Today's Completed</span><strong>{stats?.completed_today_count || 0}</strong></section>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <Routes>
      {DEMO_MODE ? (
        <Route path="/*" element={<AdminLayout />} />
      ) : (
        <>
          <Route path="/login" element={<AdminLogin />} />
          <Route path="/*" element={<ProtectedAdmin><AdminLayout /></ProtectedAdmin>} />
        </>
      )}
    </Routes>
  )
}
