import { useEffect, useState } from 'react'
import { Navigate, Route, Routes, useLocation, useNavigate } from 'react-router-dom'
import './App.css'

const API = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

async function api(path, options = {}) {
  const response = await fetch(`${API}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.detail || data.message || 'Request failed')
  return data
}

const ACCOUNT_KEY = 'dietplan_account'

function getAccount() {
  try {
    return JSON.parse(localStorage.getItem(ACCOUNT_KEY) || '{}')
  } catch {
    return {}
  }
}

function saveAccount(account) {
  localStorage.setItem(ACCOUNT_KEY, JSON.stringify(account))
}

function Sidebar() {
  const navigate = useNavigate()
  const location = useLocation()
  const [open, setOpen] = useState(false)
  const isActive = (path) => location.pathname === path

  return (
    <>
      <aside className={`dp-sidebar ${open ? 'open' : ''}`}>
        <div className="dp-brand">
          <span className="dp-cup">☕</span>
          <span>DietPlan</span>
        </div>
        <div className="dp-nav-section">MAIN MENU</div>
        <button className={`dp-nav ${isActive('/dashboard') ? 'active' : ''}`} onClick={() => navigate('/dashboard')}><span>▦</span> Dashboard</button>
        <button className={`dp-nav ${isActive('/planner') ? 'active' : ''}`} onClick={() => navigate('/planner')}><span>🥗</span> Diet Plan</button>
        <button className={`dp-nav ${isActive('/today') ? 'active' : ''}`} onClick={() => navigate('/today')}><span>✓</span> Today's Diet</button>
        <button className={`dp-nav ${isActive('/history') ? 'active' : ''}`} onClick={() => navigate('/history')}><span>◷</span> Meal History</button>
        <div className="dp-nav-section settings-label">SETTINGS</div>
        <button className={`dp-nav ${isActive('/profile') ? 'active' : ''}`} onClick={() => navigate('/profile')}><span>⚙</span> Settings</button>
        <div className="dp-version">DietPlan v1.0.0</div>
      </aside>
      {open && <button className="dp-overlay" aria-label="Close menu" onClick={() => setOpen(false)} />}
      <button className="dp-mobile-menu" aria-label="Open menu" onClick={() => setOpen(!open)}>☰</button>
    </>
  )
}

function Topbar({ title, right }) {
  return (
    <header className="dp-topbar">
      <h1>{title}</h1>
      {right}
    </header>
  )
}

function PlannerPage() {
  const navigate = useNavigate()
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const account = getAccount()
  const [selectedAllergies, setSelectedAllergies] = useState([])
  const [selectedConditions, setSelectedConditions] = useState([])
  const [form, setForm] = useState({
    age: 25, gender: '', height: 170, weight: 70,
    activity_level: '', goal: '', food_preference: '', meals_per_day: 4,
  })

  const toggle = (value, list, setList) => setList(list.includes(value) ? list.filter((item) => item !== value) : [...list, value])
  const set = (key, value) => setForm((current) => ({ ...current, [key]: value }))

  const submit = async (event) => {
    event.preventEvent?.()
    event.preventDefault()
    if (!account.name) {
      setError('Please set your name once in General Settings.')
      navigate('/profile')
      return
    }
    setBusy(true)
    setError('')
    try {
      const activityMap = {
        Sedentary: 'Sedentary',
        Light: 'Light',
        Moderate: 'Moderate',
        Active: 'Active',
        'Very Active': 'Very Active',
      }
      const goalMap = {
        'Weight Loss': 'Weight Loss',
        Maintenance: 'Maintenance',
        'Weight Gain': 'Weight Gain',
      }
      const data = await api('/users/diet-plan', {
        method: 'POST',
        body: JSON.stringify({
          name: account.name || '',
          age: Number(form.age),
          gender: form.gender,
          height: Number(form.height),
          weight: Number(form.weight),
          activity_level: activityMap[form.activity_level],
          goal: goalMap[form.goal],
          food_preference: form.food_preference,
          allergies: selectedAllergies,
          medical_conditions: selectedConditions,
          meals_per_day: Number(form.meals_per_day),
        }),
      })
      if (data.success === false) {
        sessionStorage.setItem('latestDietPlan', JSON.stringify(data.recommendation))
        navigate('/today')
        setError(data.message)
        return
      }
      sessionStorage.setItem('latestDietPlan', JSON.stringify(data))
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  const allergyOptions = ['Dairy', 'Eggs', 'Gluten', 'Peanuts', 'Tree Nuts', 'Soy', 'Shellfish', 'Fish', 'Wheat', 'Corn']
  const conditionOptions = ['Diabetes', 'Hypertension', 'High Cholesterol', 'Thyroid', 'PCOS', 'Heart Disease', 'Kidney Disease', 'Gout', 'Anemia', 'None']

  return (
    <div className="dp-page">
      <Topbar title="Diet Planner" right={<button className="dp-history-button" onClick={() => navigate('/history')}>View History</button>} />
      <main className="dp-content">
        <section className="dp-card">
          <h2>Generate Your Personalized Diet Plan</h2>
          {error && <div className="dp-error">{error}</div>}
          <form onSubmit={submit}>
            <div className="dp-form-grid">
              <label>Age *<input type="number" min="1" max="120" value={form.age} onChange={(e) => set('age', e.target.value)} required /></label>
              <label>Gender *<select value={form.gender} onChange={(e) => set('gender', e.target.value)} required><option value="">Select</option><option>Male</option><option>Female</option></select></label>
              <label>Height (cm) *<input type="number" min="50" max="249" value={form.height} onChange={(e) => set('height', e.target.value)} required /></label>
              <label>Weight (kg) *<input type="number" min="10" max="299" value={form.weight} onChange={(e) => set('weight', e.target.value)} required /></label>
              <label>Activity Level *<select value={form.activity_level} onChange={(e) => set('activity_level', e.target.value)} required><option value="">Select</option><option>Sedentary</option><option>Light</option><option>Moderate</option><option>Active</option><option>Very Active</option></select></label>
              <label>Goal *<select value={form.goal} onChange={(e) => set('goal', e.target.value)} required><option value="">Select</option><option>Weight Loss</option><option>Maintenance</option><option>Weight Gain</option></select></label>
              <label>Food Preference *<select value={form.food_preference} onChange={(e) => set('food_preference', e.target.value)} required><option value="">Select</option><option>Veg</option><option>Non-Veg</option><option>Any</option></select></label>
              <label>Meals Per Day<select value={form.meals_per_day} onChange={(e) => set('meals_per_day', e.target.value)}><option value="3">3 Meals</option><option value="4">4 Meals</option><option value="5">5 Meals</option><option value="6">6 Meals</option></select></label>
            </div>
            <div className="dp-option-block">
              <span>Allergies</span>
              <div className="dp-pills">{allergyOptions.map((item) => <button type="button" key={item} className={selectedAllergies.includes(item) ? 'selected' : ''} onClick={() => toggle(item, selectedAllergies, setSelectedAllergies)}>{item}</button>)}</div>
            </div>
            <div className="dp-option-block">
              <span>Medical Conditions</span>
              <div className="dp-pills">{conditionOptions.map((item) => <button type="button" key={item} className={selectedConditions.includes(item) ? 'selected' : ''} onClick={() => toggle(item, selectedConditions, setSelectedConditions)}>{item}</button>)}</div>
            </div>
            <button className="dp-submit" disabled={busy}>ϟ {busy ? 'Generating...' : 'Generate Diet Plan'}</button>
          </form>
        </section>
      </main>
    </div>
  )
}

function formatNumber(value, digits = 0) {
  if (value == null || Number.isNaN(Number(value))) return '—'
  return Number(value).toFixed(digits)
}

function GaugeChart({ value, max, ticks, suffix = '', color = '#10b981' }) {
  const safeValue = Math.max(0, Math.min(Number(value) || 0, max))
  const percentage = safeValue / max
  const cx = 150
  const cy = 118
  const radius = 112

  const pointAt = (degrees) => {
    const radians = (degrees * Math.PI) / 180
    return {
      x: cx + radius * Math.cos(radians),
      y: cy - radius * Math.sin(radians),
    }
  }

  const arcPath = (start, end) => {
    const startPoint = pointAt(start)
    const endPoint = pointAt(end)
    return `M ${startPoint.x} ${startPoint.y} A ${radius} ${radius} 0 0 1 ${endPoint.x} ${endPoint.y}`
  }

  return (
    <div className="gauge-chart">
      <svg viewBox="0 0 300 150" role="img" aria-label={`Gauge value ${safeValue}${suffix}`}>
        <path d={arcPath(180, 0)} fill="none" stroke="#263449" strokeWidth="18" strokeLinecap="butt" />
        <path d={arcPath(180, 108)} fill="none" stroke="#3b82f6" strokeWidth="18" />
        <path d={arcPath(108, 72)} fill="none" stroke="#10b981" strokeWidth="18" />
        <path d={arcPath(72, 36)} fill="none" stroke="#f59e0b" strokeWidth="18" />
        <path d={arcPath(36, 0)} fill="none" stroke="#ef4444" strokeWidth="18" />

        {ticks.map((tick) => {
          const angle = 180 - (tick / max) * 180
          const outer = pointAt(angle)
          const inner = (() => {
            const radians = (angle * Math.PI) / 180
            return { x: cx + (radius - 24) * Math.cos(radians), y: cy - (radius - 24) * Math.sin(radians) }
          })()
          const label = (() => {
            const radians = (angle * Math.PI) / 180
            return { x: cx + (radius - 40) * Math.cos(radians), y: cy - (radius - 40) * Math.sin(radians) + 4 }
          })()
          return (
            <g key={tick}>
              <line x1={inner.x} y1={inner.y} x2={outer.x} y2={outer.y} stroke="#94a3b8" strokeWidth="1" />
              <text x={label.x} y={label.y} textAnchor="middle" fill="#94a3b8" fontSize="10">{tick}</text>
            </g>
          )
        })}

        <line
          x1={cx}
          y1={cy}
          x2={pointAt(180 - percentage * 180).x}
          y2={pointAt(180 - percentage * 180).y}
          stroke={color}
          strokeWidth="3"
          strokeLinecap="round"
        />
        <circle cx={cx} cy={cy} r="5" fill={color} />
        <text x={cx} y={cy + 32} textAnchor="middle" fill="#f8fafc" fontSize="22" fontWeight="700">
          {formatNumber(safeValue, suffix === ' kcal' ? 0 : 1)}{suffix}
        </text>
      </svg>
    </div>
  )
}

function DashboardPage() {
  const [plan, setPlan] = useState(null)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    api('/users/today')
      .then((data) => setPlan(data.plan))
      .catch((err) => setError(err.message))
  }, [])

  const daily = plan?.daily_plan || {}
  const macroData = plan ? [
    { name: 'Protein', value: plan.target_protein || 0, color: '#3b82f6' },
    { name: 'Carbohydrates', value: plan.target_carbohydrates || 0, color: '#f59e0b' },
    { name: 'Fat', value: plan.target_fat || 0, color: '#ef4444' },
  ] : []
  const bmi = plan?.bmi || 0
  const calorieValue = daily.total_daily_calories || plan?.daily_calories || 0

  const checklist = plan?.meal_checklist || {
    breakfast: false,
    lunch: false,
    snacks: false,
    dinner: false,
  }
  const completedMeals = Object.values(checklist).filter(Boolean).length

  return (
    <div className="dp-page dashboard-page">
      <Topbar
        title="Personalized Diet Recommendation Dashboard"
        right={
          <div className="dashboard-header-info">
            <span>Name: <strong>{plan?.user_name || plan?.request_params?.name || 'User'}</strong></span>
            <span>Date: <strong>{new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</strong></span>
            <span>Goal: <strong className="goal-value">{plan?.request_params?.goal || 'Weight Loss'}</strong></span>
            <b className="dashboard-bmi-badge">{plan?.bmi_category || 'NORMAL WEIGHT'}</b>
            <button className="dashboard-export" onClick={() => window.print()}>▣ Export</button>
          </div>
        }
      />
      <main className="dashboard-content">
        {error && <div className="dp-error">{error}</div>}
        <section className="kpi-grid">
          <article><span>BMI</span><strong>{formatNumber(bmi, 1)}</strong><small>{plan?.bmi_category || 'Body Mass Index'}</small></article>
          <article><span>BMR</span><strong>{formatNumber(plan?.bmr, 0)} <i>kcal</i></strong><small>Basal Metabolic Rate</small></article>
          <article><span>TDEE</span><strong>{formatNumber(plan?.tdee, 0)} <i>kcal</i></strong><small>Total Daily Energy</small></article>
          <article><span>Daily Calories</span><strong>{formatNumber(plan?.daily_calories, 0)} <i>kcal</i></strong><small>Target Intake</small></article>
          <article><span>Water Rec.</span><strong>{formatNumber(daily.recommended_water_liters, 1)} <i>L</i></strong><small>Recommended Water</small></article>
          <article><span>Nutrition Score</span><strong>78/100</strong><small>Macro Balance Quality</small></article>
        </section>
        <section className="chart-grid">
          <article className="dashboard-panel macro-panel">
            <div className="panel-title"><span>Macronutrient Split</span><b>Plotly Doughnut</b></div>
            <div className="macro-chart">
              {macroData.length ? (
                <>
                  <div className="macro-doughnut">
                    <svg viewBox="0 0 120 120" role="img" aria-label="Macronutrient split">
                      {(() => {
                        const total = macroData.reduce((sum, item) => sum + item.value, 0) || 1
                        let offset = 0
                        return macroData.map((item) => {
                          const fraction = item.value / total
                          const dash = fraction * 314
                          const gap = 314 - dash
                          const segment = (
                            <circle
                              key={item.name}
                              cx="60"
                              cy="60"
                              r="50"
                              fill="none"
                              stroke={item.color}
                              strokeWidth="16"
                              strokeDasharray={`${dash} ${gap}`}
                              strokeDashoffset={-offset}
                              transform="rotate(-90 60 60)"
                            />
                          )
                          offset += dash
                          return segment
                        })
                      })()}
                      <circle cx="60" cy="60" r="35" fill="#182132" />
                    </svg>
                  </div>
                  <div className="macro-legend">
                    {macroData.map((item) => (
                      <div key={item.name}>
                        <span className="macro-color" style={{ background: item.color }} />
                        <span>{item.name}</span>
                        <strong>{formatNumber(item.value, 1)}g</strong>
                      </div>
                    ))}
                  </div>
                </>
              ) : <span>No macro data</span>}
            </div>
          </article>
          <article className="dashboard-panel gauge-panel">
            <div className="panel-title"><span>BMI Indicator</span><b>Plotly Gauge</b></div>
            <GaugeChart
              value={bmi}
              max={40}
              ticks={[10, 15, 20, 25, 30, 35, 40]}
            />
          </article>
          <article className="dashboard-panel gauge-panel">
            <div className="panel-title"><span>Daily Calorie Progress</span><b>Plotly Gauge</b></div>
            <GaugeChart
              value={calorieValue}
              max={Math.max(Number(plan?.daily_calories || 2400) * 1.25, 2500)}
              ticks={[0, 500, 1000, 1500, 2000, 2500]}
              suffix=" kcal"
            />
          </article>
        </section>
        <section className="dashboard-panel today-progress-panel">
          <div className="panel-title"><span>Today's Diet Progress</span><b>{plan?.completion_percentage || 0}% Complete</b></div>
          <div className="today-progress-grid">
            {[
              ['Breakfast', 'breakfast', '🥯'],
              ['Lunch', 'lunch', '🍲'],
              ['Snack', 'snacks', '🥜'],
              ['Dinner', 'dinner', '🍝'],
            ].map(([label, key, icon]) => (
              <button type="button" key={key} className={checklist[key] ? 'complete' : ''} onClick={() => navigate('/today')}>
                <span>{icon}</span>
                <strong>{label}</strong>
                <small>{checklist[key] ? 'Completed' : 'Pending'}</small>
              </button>
            ))}
          </div>
          <div className="today-progress-footer">
            <span>{completedMeals} of 4 meals checked</span>
            <button type="button" onClick={() => navigate('/today')}>Open Today's Diet</button>
          </div>
        </section>
      </main>
    </div>
  )
}

function HistoryPage() {
  const [plans, setPlans] = useState([])
  const [selectedDate, setSelectedDate] = useState(() => {
    const now = new Date()
    return [
      now.getFullYear(),
      String(now.getMonth() + 1).padStart(2, '0'),
      String(now.getDate()).padStart(2, '0'),
    ].join('-')
  })
  const [calendarMonth, setCalendarMonth] = useState(() => {
    const now = new Date()
    return new Date(now.getFullYear(), now.getMonth(), 1)
  })

  useEffect(() => {
    api('/users/diet-plan')
      .then((data) => {
        const records = data.recommendations || []
        setPlans(records)
        if (records.length > 0) {
          const latest = records[0]
          const latestDate = latest.plan_date
            || (latest.created_at ? String(latest.created_at).slice(0, 10) : '')
          if (latestDate) {
            setSelectedDate(latestDate)
            const [year, month] = latestDate.split('-').map(Number)
            if (year && month) setCalendarMonth(new Date(year, month - 1, 1))
          }
        }
      })
      .catch(() => setPlans([]))
  }, [])

  const dateKey = (date) => [
    date.getFullYear(),
    String(date.getMonth() + 1).padStart(2, '0'),
    String(date.getDate()).padStart(2, '0'),
  ].join('-')

  const planDates = new Set(
    plans
      .map((plan) => {
        if (plan.plan_date) return plan.plan_date
        if (!plan.created_at) return null
        const date = new Date(plan.created_at)
        return Number.isNaN(date.getTime()) ? null : dateKey(date)
      })
      .filter(Boolean)
  )

  const year = calendarMonth.getFullYear()
  const month = calendarMonth.getMonth()
  const firstDay = new Date(year, month, 1)
  const gridStart = new Date(year, month, 1 - firstDay.getDay())
  const calendarDays = Array.from({ length: 42 }, (_, index) => {
    const date = new Date(gridStart)
    date.setDate(gridStart.getDate() + index)
    return date
  })

  const changeMonth = (offset) => setCalendarMonth(new Date(year, month + offset, 1))

  const filteredPlans = selectedDate
    ? plans.filter((plan) => {
        if (plan.plan_date) return plan.plan_date === selectedDate
        if (!plan.created_at) return false
        const planDate = new Date(plan.created_at)
        if (Number.isNaN(planDate.getTime())) {
          return String(plan.created_at).slice(0, 10) === selectedDate
        }
        return dateKey(planDate) === selectedDate
      })
    : plans

  return (
    <div className="dp-page">
      <Topbar title="Meal History" />
      <main className="dp-content">
        <section className="history-calendar">
          <div className="history-calendar-header">
            <button type="button" aria-label="Previous month" onClick={() => changeMonth(-1)}>‹</button>
            <h2>{calendarMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}</h2>
            <button type="button" aria-label="Next month" onClick={() => changeMonth(1)}>›</button>
          </div>
          <div className="history-calendar-grid">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
              <div className="history-calendar-weekday" key={day}>{day}</div>
            ))}
            {calendarDays.map((date) => {
              const key = dateKey(date)
              const isSelected = selectedDate === key
              const hasPlan = planDates.has(key)
              const isOutside = date.getMonth() !== month
              return (
                <button
                  type="button"
                  key={key}
                  className={[
                    'history-calendar-day',
                    isOutside ? 'outside' : '',
                    isSelected ? 'selected' : '',
                    hasPlan ? 'has-plan' : '',
                  ].join(' ')}
                  onClick={() => setSelectedDate(isSelected ? '' : key)}
                  aria-label={date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}
                >
                  <span>{date.getDate()}</span>
                  {hasPlan && <i />}
                </button>
              )
            })}
          </div>
          {selectedDate && (
            <button className="history-calendar-clear" type="button" onClick={() => setSelectedDate('')}>Clear selected date</button>
          )}
        </section>

        <div className="history-summary">
          <span>{filteredPlans.length} meal plan{filteredPlans.length === 1 ? '' : 's'} found</span>
          {selectedDate && <span>{new Date(`${selectedDate}T00:00:00`).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</span>}
        </div>
        {selectedDate ? (
          filteredPlans.length ? filteredPlans.map((plan, index) => {
            const daily = plan.daily_plan || {}
            const checklist = plan.meal_checklist || {}
            const status = plan.status || (plan.is_accepted ? 'accepted' : plan.is_finalized ? 'finalized' : 'draft')
            const mealRows = [
              ['Breakfast', 'breakfast', '🥯', daily.breakfast],
              ['Lunch', 'lunch', '🍲', daily.lunch],
              ['Snack', 'snacks', '🥜', daily.snacks],
              ['Dinner', 'dinner', '🍝', daily.dinner],
            ]

            return (
              <section className="dashboard-panel history-diet-table" key={plan.recommendation_id || index}>
                <div className="panel-title">
                  <span>Diet Plan · {selectedDate}</span>
                  <b className={`history-status ${status}`}>{status}</b>
                </div>
                <div className="history-plan-meta">
                  <span><strong>Calories:</strong> {formatNumber(plan.daily_calories, 0)} kcal</span>
                  <span><strong>BMI:</strong> {formatNumber(plan.bmi, 1)}</span>
                  <span><strong>Preference:</strong> {plan.food_preference || '—'}</span>
                  <span><strong>Completed:</strong> {plan.completion_percentage || 0}%</span>
                </div>
                <table>
                  <thead>
                    <tr>
                      <th>TAKE</th>
                      <th>MEAL</th>
                      <th>FOODS</th>
                      <th>CALORIES</th>
                      <th>PROTEIN</th>
                      <th>CARBS</th>
                      <th>FAT</th>
                    </tr>
                  </thead>
                  <tbody>
                    {mealRows.map(([label, key, icon, meal]) => (
                      <tr key={key} className={checklist[key] ? 'meal-taken' : ''}>
                        <td>
                          <span className={`history-check ${checklist[key] ? 'checked' : ''}`}>
                            {checklist[key] ? '✓' : '—'}
                          </span>
                        </td>
                        <td className={`meal-name ${label.toLowerCase()}`}><span>{icon}</span>{label}</td>
                        <td>{meal?.items?.map((item) => item.name).join(', ') || 'No matching foods'}</td>
                        <td><strong>{formatNumber(meal?.total_calories, 0)} kcal</strong></td>
                        <td>{formatNumber(meal?.total_protein, 1)}g</td>
                        <td>{formatNumber(meal?.total_carbohydrates, 1)}g</td>
                        <td>{formatNumber(meal?.total_fat, 1)}g</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </section>
            )
          }) : <section className="dp-card"><h2>No meal plans found for this date</h2></section>
        ) : (
          <section className="dp-card history-select-prompt">
            <h2>Select a highlighted date</h2>
            <p>Choose a date in the calendar to view that day's diet table.</p>
          </section>
        )}
      </main>
    </div>
  )
}

function TodayDietPage() {
  const navigate = useNavigate()
  const [plan, setPlan] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api('/users/today')
      .then((data) => setPlan(data.plan))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  const toggleMeal = async (meal, checked) => {
    try {
      const data = await api('/users/today/checklist', {
        method: 'PUT',
        body: JSON.stringify({ meal, checked }),
      })
      setPlan(data.plan)
      sessionStorage.setItem('latestDietPlan', JSON.stringify(data.plan))
    } catch (err) {
      setError(err.message)
    }
  }

  const acceptDiet = async () => {
    try {
      const data = await api('/users/today/accept', { method: 'PUT' })
      setPlan(data.plan)
      setError('')
      sessionStorage.setItem('latestDietPlan', JSON.stringify(data.plan))
    } catch (err) {
      setError(err.message)
    }
  }

  const regenerateDiet = async () => {
    if (!plan) return
    try {
      const params = plan.request_params || {}
      const data = await api('/users/today/regenerate', {
        method: 'POST',
        body: JSON.stringify({
          name: plan.user_name || params.name || getAccount().name || 'User',
          age: params.age,
          gender: params.gender,
          height: params.height,
          weight: params.weight,
          activity_level: params.activity_level,
          goal: params.goal,
          food_preference: params.food_preference,
          allergies: params.allergies || [],
          medical_conditions: params.medical_conditions || [],
          meals_per_day: params.meals_per_day || 4,
        }),
      })
      setPlan(data)
      setError('')
      sessionStorage.setItem('latestDietPlan', JSON.stringify(data))
    } catch (err) {
      setError(err.message)
    }
  }

  const daily = plan?.daily_plan || {}
  const checklist = plan?.meal_checklist || {
    breakfast: false,
    lunch: false,
    snacks: false,
    dinner: false,
  }
  const mealRows = [
    ['Breakfast', 'breakfast', '🥯', daily.breakfast],
    ['Lunch', 'lunch', '🍲', daily.lunch],
    ['Snack', 'snacks', '🥜', daily.snacks],
    ['Dinner', 'dinner', '🍝', daily.dinner],
  ]

  return (
    <div className="dp-page">
      <Topbar title="Today's Diet" />
      <main className="dp-content">
        {loading ? (
          <section className="dp-card"><h2>Loading today's diet plan...</h2></section>
        ) : !plan ? (
          <section className="dp-card today-empty">
            <h2>No finalized diet plan for today</h2>
            <p>Generate and finalize one diet plan for today in Diet Plan.</p>
            <button type="button" className="dp-submit" onClick={() => navigate('/planner')}>Go to Diet Plan</button>
          </section>
        ) : (
          <>
            {error && <div className="dp-error">{error}</div>}
            <section className="today-progress-summary">
              <div>
                <span>Today's Plan</span>
                <strong>{plan.status === 'accepted' || plan.is_accepted ? 'Accepted' : 'Review Draft'} · {plan.completion_percentage || 0}% completed</strong>
              </div>
              <div className="today-progress-track"><i style={{ width: `${plan.completion_percentage || 0}%` }} /></div>
              <div className="today-diet-actions">
                <button
                  type="button"
                  className="accept-diet-button"
                  onClick={acceptDiet}
                  disabled={Boolean(plan.is_accepted)}
                >
                  {plan.is_accepted ? '✓ Diet Accepted' : 'Accept Diet'}
                </button>
                <button
                  type="button"
                  className="regenerate-diet-button"
                  onClick={regenerateDiet}
                  disabled={Boolean(plan.is_accepted)}
                >
                  ↻ Regenerate Diet
                </button>
              </div>
            </section>
            <section className="dashboard-panel meal-table-panel today-table">
              <div className="panel-title"><span>Today's Diet Table</span><b>Check completed meals</b></div>
              <table>
                <thead><tr><th>TAKE</th><th>MEAL</th><th>FOODS</th><th>CALORIES</th><th>PROTEIN</th><th>CARBS</th><th>FAT</th></tr></thead>
                <tbody>
                  {mealRows.map(([label, key, icon, meal]) => (
                    <tr key={key} className={checklist[key] ? 'meal-taken' : ''}>
                      <td>
                        <label className="meal-checkbox">
                          <input
                            type="checkbox"
                            checked={Boolean(checklist[key])}
                            onChange={(event) => toggleMeal(key, event.target.checked)}
                          />
                          <span />
                        </label>
                      </td>
                      <td className={`meal-name ${label.toLowerCase()}`}><span>{icon}</span>{label}</td>
                      <td>{meal?.items?.map((item) => item.name).join(', ') || 'No matching foods'}</td>
                      <td><strong>{formatNumber(meal?.total_calories, 0)} kcal</strong></td>
                      <td>{formatNumber(meal?.total_protein, 1)}g</td>
                      <td>{formatNumber(meal?.total_carbohydrates, 1)}g</td>
                      <td>{formatNumber(meal?.total_fat, 1)}g</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          </>
        )}
      </main>
    </div>
  )
}

function ProfilePage() {
  const [account, setAccountState] = useState(() => getAccount())
  const [name, setName] = useState(account.name || '')
  const [saved, setSaved] = useState('')

  const saveName = (event) => {
    event.preventDefault()
    const cleanName = name.trim()
    if (!cleanName) return
    const next = { ...account, name: cleanName }
    saveAccount(next)
    setAccountState(next)
    setSaved('General settings saved.')
  }

  const switchAccount = () => {
    localStorage.removeItem(ACCOUNT_KEY)
    setAccountState({})
    setName('')
    setSaved('Account switched. Enter a new name in General Settings.')
  }

  return (
    <div className="dp-page">
      <Topbar title="Settings" />
      <main className="dp-content settings-layout">
        <section className="dp-card">
          <h2>General Settings</h2>
          {saved && <div className="settings-success">{saved}</div>}
          <form onSubmit={saveName}>
            <label className="dp-full">Account Name *
              <input value={name} onChange={(event) => setName(event.target.value)} placeholder="Enter your name" required />
            </label>
            <button className="dp-submit" type="submit">Save General Settings</button>
          </form>
        </section>
        <section className="dp-card account-settings">
          <h2>Switch Account</h2>
          <p>Clear the saved local account name and start as a different user.</p>
          <button type="button" className="switch-account-button" onClick={switchAccount}>Switch Account</button>
        </section>
      </main>
    </div>
  )
}

export default function App() {
  return (
    <div className="dp-app">
      <Sidebar />
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/planner" element={<PlannerPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/today" element={<TodayDietPage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="*" element={<Navigate to="/planner" replace />} />
      </Routes>
    </div>
  )
}
