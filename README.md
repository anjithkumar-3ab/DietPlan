# DietPlan – Personalized Diet Recommendation System

DietPlan is a FastAPI and MongoDB application with separate React/Vite portals for users and administrators.

## Features

### User Website
- Dashboard with BMI, BMR, TDEE, calories, and nutrition charts
- Name and profile settings
- Personalized diet generation
- One finalized diet plan per day
- Today's Diet checklist
- Calendar-based meal history
- Draft acceptance and diet regeneration

### Admin Website
- Dashboard analytics
- Registered user management
- Food database management
- Diet plan and completion monitoring
- Local reports and optional Power BI embed

## Project Structure

```text
DietPlan/
├── backend/
│   ├── app/
│   │   ├── database/
│   │   ├── dependencies/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── services/
│   └── scripts/
├── user-frontend/
├── admin-frontend/
├── frontend/             # Legacy static compatibility frontend
├── Dataset/
├── assets/
├── powerbi/
├── setup.bat
├── start.bat
└── README.md
```

## Requirements

- Python 3.10 or newer
- Node.js 18 or newer
- MongoDB Atlas or local MongoDB
- Microsoft Power BI Desktop, optional for the `.pbix` report

## Quick Setup

Run:

```bat
setup.bat
```

Configure `backend/.env`:

```env
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=nutriai
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DEMO_MODE=true
```

For local demonstration, keep `DEMO_MODE=true`. Set it to `false` to require JWT authentication and role authorization.

## Start the Application

Run:

```bat
start.bat
```

The launcher opens:

- User Website: http://127.0.0.1:5173
- Admin Website: http://127.0.0.1:5174
- Backend API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

## Manual Commands

Backend:

```powershell
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

User Website:

```powershell
cd user-frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

Admin Website:

```powershell
cd admin-frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5174
```

## Create an Admin Account

Set temporary environment variables and run:

```powershell
$env:ADMIN_NAME="DietPlan Admin"
$env:ADMIN_EMAIL="admin@example.com"
$env:ADMIN_PASSWORD="ChangeMe123!"
python backend\scripts\create_admin.py
```

Public registration creates only normal `user` accounts. Use the admin script or an existing secure process to create or promote administrators.

## Database Collections

Existing collections remain in use:

- `foods`
- `health_profiles`
- `recommendations`
- `users`

The application persists the following user data in MongoDB:

- Account name and general profile settings
- Health metrics and profile calculations
- Generated draft, accepted, and finalized diet plans
- Meal completion checklists and completion percentages
- Food records created or updated by administrators
- User status and role changes
- Diet plan history and plan dates

Recommendations include:

- `plan_date`
- `is_finalized`
- `is_accepted`
- `status`
- `meal_checklist`
- `completion_percentage`

## Power BI

The `powerbi/Nutri.pbix` report can be opened in Microsoft Power BI Desktop. The Admin Reports page also provides a download and live database-based charts.

For a published report, set `VITE_POWERBI_URL` in `admin-frontend/.env` to an approved public or secure embed URL. Do not place credentials or private embed secrets in frontend code.
