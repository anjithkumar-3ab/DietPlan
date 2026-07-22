# 🥗 NutriAI - AI-Based Personalized Diet Planning & Recommendation System

NutriAI is an intelligent, AI-powered health and nutrition management platform designed to deliver personalized daily diet recommendations based on individual biometric data, dietary preferences, health goals, allergens, and medical conditions.

---

## ✨ Key Features

- **Personalized Biometric Analysis**: Calculates BMR (Basal Metabolic Rate), TDEE (Total Daily Energy Expenditure), and BMI categories using standard health formulas (Harris-Benedict & Mifflin-St Jeor).
- **AI-Driven Meal Plan Recommendation**: Dynamically selects breakfast, lunch, dinner, and snack items to match daily target calories and macronutrient ratios (Protein, Carbs, Fats, Fiber).
- **Allergen & Medical Condition Filtering**: Excludes forbidden foods based on allergies (*Peanuts, Gluten, Dairy, Soy, Tree Nuts, Shellfish, etc.*) and medical conditions (*Diabetes, Hypertension, High Cholesterol, Gout, PCOS, etc.*).
- **Interactive Analytics Dashboard**: Renders 10 dynamic Plotly charts detailing calorie targets, macro ratios, nutrient timelines, micronutrient balance, and food group breakdowns.
- **Searchable Food Catalog**: Queryable MongoDB database of categorized foods enriched with caloric density, macro profiles, and serving sizes.
- **Plan Management & History**: Save, retrieve, delete, or regenerate diet plans at any time.
- **PowerBI Analytics Integration**: Includes a pre-built PowerBI dashboard (`powerbi/Nutri.pbix`) for population nutrition analysis and macro tracking.

---

## 🛠️ Tech Stack

### **Backend**
- **Framework**: Python 3.10+, FastAPI, Uvicorn
- **Database**: MongoDB Atlas via PyMongo
- **Data & Analytics**: Pandas, Scikit-Learn, Plotly
- **Validation**: Pydantic v2

### **Frontend**
- **Interface**: HTML5, Vanilla CSS3 (Glassmorphic Design System), JavaScript (ES6+)
- **Charts & Icons**: Chart.js, FontAwesome

### **Analytics & BI**
- **Business Intelligence**: Microsoft PowerBI (`Nutri.pbix`)

---

## 📂 Project Structure

```
NutriAI/
├── backend/
│   ├── app/
│   │   ├── database/        # MongoDB connection handler
│   │   ├── routes/          # API endpoints (recommendation, dashboard, food, profile)
│   │   ├── schemas/         # Pydantic schemas & request validation
│   │   ├── services/        # BMR/TDEE calculation, meal plan algorithm, Plotly charts
│   │   └── main.py          # FastAPI application entry point
│   ├── scripts/             # Food dataset cleaning & MongoDB seed scripts
│   ├── .env.example         # Template for environment configuration
│   └── requirements.txt     # Backend Python dependencies
├── frontend/
│   ├── assets/              # Images, icons, and static assets
│   ├── css/                 # CSS stylesheets & design system tokens
│   ├── js/                  # App components, API connectors, & chart handlers
│   └── index.html           # SPA frontend interface
├── powerbi/
│   └── Nutri.pbix           # PowerBI dashboard report
├── requirements.txt         # Root project dependencies
├── setup.bat                # Automated setup script (Windows)
└── start.bat                # Automated launcher script (Windows)
```

---

## 🚀 Quick Start (Windows)

The easiest way to get started is using the automated batch scripts:

1. **Run Setup**:
   Double-click `setup.bat` (or execute in terminal):
   ```cmd
   setup.bat
   ```
   *This upgrades pip, installs required packages, and creates `backend\.env` from `backend\.env.example`.*

2. **Configure Database**:
   Open `backend\.env` and insert your MongoDB Atlas URI:
   ```env
   MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=NutriAI
   DATABASE_NAME=nutriai
   ```

3. **(Optional) Seed Food Database**:
   Seed the food database into MongoDB:
   ```cmd
   python backend\scripts\import_foods.py
   ```

4. **Start Application**:
   Double-click `start.bat` (or execute in terminal):
   ```cmd
   start.bat
   ```
   *This automatically launches the FastAPI Backend (Port 8000), Frontend web server (Port 5500), and opens the web application in your default browser.*

---

## 💻 Manual Installation & Setup

If you prefer manual configuration or are on Linux/macOS:

### 1. Prerequisites
- Python 3.10 or higher
- MongoDB Atlas cluster or local MongoDB instance

### 2. Virtual Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r backend/requirements.txt
```

### 4. Environment Configuration
Create `backend/.env` (or copy from `backend/.env.example`):
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:
```env
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=nutriai
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 5. Dataset Preprocessing & Seed (Optional)
If you wish to process raw CSV food datasets and seed your MongoDB database:
```bash
# Step 1: Preprocess dataset (if CSV placed in backend/data/raw)
python backend/scripts/preprocess_food_dataset.py

# Step 2: Import clean dataset to MongoDB
python backend/scripts/import_foods.py
```

### 6. Run Application Servers
Run the backend and frontend in separate terminal windows:

**Backend Terminal**:
```bash
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Frontend Terminal**:
```bash
cd frontend
python -m http.server 5500
```

Open `http://127.0.0.1:5500` in your web browser.

---

## 📡 API Endpoints Summary

FastAPI automatically generates interactive documentation at `http://127.0.0.1:8000/docs` (Swagger) and `http://127.0.0.1:8000/redoc` (ReDoc).

| Category | Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **Health** | `GET` | `/health` | Application & MongoDB health check |
| **Recommendation** | `POST` | `/recommendation/generate` | Generate personalized daily diet plan |
| **Recommendation** | `GET` | `/recommendation/history` | List recommendation history (paginated) |
| **Recommendation** | `GET` | `/recommendation/{id}` | Retrieve specific recommendation by ID |
| **Recommendation** | `DELETE` | `/recommendation/{id}` | Delete a recommendation by ID |
| **Recommendation** | `POST` | `/recommendation/{id}/regenerate` | Regenerate new meal plan from existing profile |
| **Dashboard** | `POST` | `/dashboard/charts` | Retrieve dashboard data and 10 Plotly chart JSON objects |
| **Foods** | `GET` | `/foods/` | List food items (paginated) |
| **Foods** | `GET` | `/foods/search` | Search food items by query string |
| **Foods** | `GET` | `/foods/category/{category}` | Filter food items by category |
| **Profile** | `POST` | `/profile/` | Create or save user health profile |

---

## 📊 PowerBI Analytics

The repository includes a ready-to-use PowerBI report in the `powerbi/` directory:
- **File**: `powerbi/Nutri.pbix`
- **Features**: Visualizes macronutrient distribution across food categories, caloric density heatmaps, and target goal compliance.
- **Usage**: Open `Nutri.pbix` in Microsoft PowerBI Desktop and connect to your MongoDB Atlas instance or exported dataset.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request for bug fixes or new features.

---

## 📄 License

Distributed under the MIT License.
