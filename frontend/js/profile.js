/**
 * NutriAI – Health Profile Page
 * Form to capture user health metrics, preferences, allergies, and medical conditions.
 */

async function renderProfile(container) {
  container.innerHTML = `
    <!-- Top Bar -->
    <div class="topbar">
      <div class="flex gap-2" style="align-items:center;">
        <button class="mobile-menu-btn" onclick="toggleSidebar()" aria-label="Menu">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </button>
        <h1>Health Profile</h1>
      </div>
    </div>

    <div class="card" style="max-width:800px;">
      <div class="card-header mb-2">
        <span class="card-title">Personal Information</span>
        <span class="card-subtitle">Fill in your details for accurate recommendations</span>
      </div>

      <form id="profileForm" onsubmit="saveProfile(event)">
        <!-- Personal Info -->
        <div class="form-row">
          <div class="form-group">
            <label for="full_name">Full Name *</label>
            <input type="text" id="full_name" placeholder="John Doe" required />
          </div>
          <div class="form-group">
            <label for="age">Age *</label>
            <input type="number" id="age" min="1" max="120" placeholder="25" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="gender">Gender *</label>
            <select id="gender" required>
              <option value="">Select gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>
          <div class="form-group">
            <label for="date_of_birth">Date of Birth</label>
            <input type="date" id="date_of_birth" />
          </div>
        </div>

        <!-- Body Metrics -->
        <div class="form-row">
          <div class="form-group">
            <label for="height">Height (cm) *</label>
            <input type="number" id="height" min="1" step="0.1" placeholder="170" required />
          </div>
          <div class="form-group">
            <label for="weight">Weight (kg) *</label>
            <input type="number" id="weight" min="1" step="0.1" placeholder="70" required />
          </div>
        </div>

        <div class="form-group">
          <label for="target_weight">Target Weight (kg)</label>
          <input type="number" id="target_weight" min="1" step="0.1" placeholder="65" />
          <span class="form-hint">Leave empty if you're maintaining current weight</span>
        </div>

        <!-- Lifestyle -->
        <div class="form-row">
          <div class="form-group">
            <label for="activity_level">Activity Level *</label>
            <select id="activity_level" required>
              <option value="">Select activity level</option>
              <option value="Sedentary">Sedentary</option>
              <option value="Lightly Active">Lightly Active</option>
              <option value="Moderately Active">Moderately Active</option>
              <option value="Very Active">Very Active</option>
              <option value="Athlete">Athlete</option>
            </select>
          </div>
          <div class="form-group">
            <label for="goal">Fitness Goal *</label>
            <select id="goal" required>
              <option value="">Select goal</option>
              <option value="Lose Weight">Lose Weight</option>
              <option value="Maintain Weight">Maintain Weight</option>
              <option value="Gain Weight">Gain Weight</option>
              <option value="Muscle Gain">Muscle Gain</option>
              <option value="Healthy Lifestyle">Healthy Lifestyle</option>
            </select>
          </div>
        </div>

        <!-- Food Preference -->
        <div class="form-group">
          <label for="food_preference">Food Preference *</label>
          <select id="food_preference" required>
            <option value="">Select preference</option>
            <option value="Vegetarian">Vegetarian</option>
            <option value="Non Vegetarian">Non Vegetarian</option>
            <option value="Vegan">Vegan</option>
            <option value="Eggetarian">Eggetarian</option>
            <option value="Jain">Jain</option>
          </select>
        </div>

        <!-- Allergies (multi-select pills) -->
        <div class="form-group">
          <label>Allergies</label>
          <div class="checkbox-group" id="allergyGroup">
            ${buildPills(['Dairy', 'Eggs', 'Gluten', 'Peanuts', 'Tree Nuts', 'Soy', 'Shellfish', 'Fish', 'Wheat', 'Corn'], 'allergy')}
          </div>
        </div>

        <!-- Medical Conditions -->
        <div class="form-group">
          <label>Medical Conditions</label>
          <div class="checkbox-group" id="medicalGroup">
            ${buildPills(['Diabetes', 'Hypertension', 'High Cholesterol', 'Thyroid', 'PCOS', 'Heart Disease', 'Kidney Disease', 'Gout', 'Anemia', 'None'], 'medical')}
          </div>
        </div>

        <!-- Exclude Ingredients -->
        <div class="form-group">
          <label>Exclude Ingredients</label>
          <div class="checkbox-group" id="excludeGroup">
            ${buildPills(['Mushroom', 'Coconut', 'Garlic', 'Onion', 'Tomato', 'Brinjal', 'Cauliflower', 'Bottlegourd', 'Citrus Fruits', 'None'], 'exclude')}
          </div>
        </div>

        <!-- Daily Habits -->
        <div class="form-row">
          <div class="form-group">
            <label for="water_intake_goal">Water Intake Goal (glasses/day)</label>
            <input type="number" id="water_intake_goal" min="1" max="20" placeholder="8" />
          </div>
          <div class="form-group">
            <label for="meals_per_day">Meals Per Day</label>
            <input type="number" id="meals_per_day" min="1" max="10" placeholder="4" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="sleep_hours">Sleep Hours</label>
            <input type="number" id="sleep_hours" min="0" max="24" step="0.5" placeholder="7" />
          </div>
          <div class="form-group">
            <label for="wake_up_time">Wake Up Time</label>
            <input type="time" id="wake_up_time" value="07:00" />
          </div>
          <div class="form-group">
            <label for="bed_time">Bed Time</label>
            <input type="time" id="bed_time" value="22:00" />
          </div>
        </div>

        <div id="profileError" class="hidden"></div>

        <button type="submit" class="btn btn-primary btn-lg mt-2" id="profileSubmitBtn" style="width:100%;justify-content:center;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
          Save Profile
        </button>
      </form>
    </div>
  `;

  // Initialize pill click handlers
  initPills('allergyGroup');
  initPills('medicalGroup');
  initPills('excludeGroup');
}

function buildPills(items, prefix) {
  return items
    .map(
      (item) =>
        `<span class="checkbox-pill" data-value="${item}" data-group="${prefix}">${item}</span>`
    )
    .join('');
}

function initPills(groupId) {
  const container = document.getElementById(groupId);
  if (!container) return;

  container.querySelectorAll('.checkbox-pill').forEach((pill) => {
    pill.addEventListener('click', () => {
      pill.classList.toggle('selected');
    });
  });
}

function getSelectedPills(groupId) {
  const container = document.getElementById(groupId);
  if (!container) return [];
  const selected = container.querySelectorAll('.checkbox-pill.selected');
  return Array.from(selected).map((p) => p.dataset.value);
}

async function saveProfile(event) {
  event.preventDefault();

  const btn = document.getElementById('profileSubmitBtn');
  const errorDiv = document.getElementById('profileError');

  btn.disabled = true;
  btn.innerHTML = '<div class="spinner" style="width:20px;height:20px;margin:0;border-width:2px;"></div> Saving...';

  const profile = {
    full_name: document.getElementById('full_name').value.trim(),
    age: parseInt(document.getElementById('age').value),
    gender: document.getElementById('gender').value,
    date_of_birth: document.getElementById('date_of_birth').value || null,
    height: parseFloat(document.getElementById('height').value),
    weight: parseFloat(document.getElementById('weight').value),
    target_weight: parseFloat(document.getElementById('target_weight').value) || null,
    activity_level: document.getElementById('activity_level').value,
    goal: document.getElementById('goal').value,
    food_preference: document.getElementById('food_preference').value,
    allergies: getSelectedPills('allergyGroup'),
    medical_conditions: getSelectedPills('medicalGroup'),
    exclude_ingredients: getSelectedPills('excludeGroup'),
    water_intake_goal: parseInt(document.getElementById('water_intake_goal').value) || null,
    meals_per_day: parseInt(document.getElementById('meals_per_day').value) || null,
    sleep_hours: parseFloat(document.getElementById('sleep_hours').value) || null,
    wake_up_time: document.getElementById('wake_up_time').value || null,
    bed_time: document.getElementById('bed_time').value || null,
  };

  try {
    const api = await NutriAPI.profile;
    await api.save(profile);
    showToast('Profile saved successfully!', 'success');
    // Redirect to diet planner
    setTimeout(() => navigate('diet_planner'), 800);
  } catch (error) {
    errorDiv.className = 'alert alert-error mt-2';
    errorDiv.classList.remove('hidden');
    errorDiv.textContent = error.message;
  } finally {
    btn.disabled = false;
    btn.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
      Save Profile
    `;
  }
}
