@echo off
setlocal
title DietPlan Launcher

echo ===================================================
echo                Starting DietPlan
echo ===================================================
echo.

if not exist "%~dp0backend\.env" (
    echo [WARNING] backend\.env was not found.
    echo Copy backend\.env.example to backend\.env and configure MongoDB.
)

echo [1/3] Starting FastAPI backend on port 8000...
start "DietPlan Backend" cmd /k "cd /d "%~dp0backend" && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

timeout /t 5 /nobreak >nul

if exist "%~dp0user-frontend\node_modules" (
    echo [2/3] Starting User Website on port 5173...
) else (
    echo [2/3] Installing User Website dependencies...
    cd /d "%~dp0user-frontend"
    call npm install
)
start "DietPlan User Website" cmd /k "cd /d "%~dp0user-frontend" && npm run dev -- --host 127.0.0.1 --port 5173"

if exist "%~dp0admin-frontend\node_modules" (
    echo [3/3] Starting Admin Website on port 5174...
) else (
    echo [3/3] Installing Admin Website dependencies...
    cd /d "%~dp0admin-frontend"
    call npm install
)
start "DietPlan Admin Website" cmd /k "cd /d "%~dp0admin-frontend" && npm run dev -- --host 127.0.0.1 --port 5174"

timeout /t 4 /nobreak >nul
start http://127.0.0.1:5173
start http://127.0.0.1:5174

echo.
echo ===================================================
echo User Website  : http://127.0.0.1:5173
echo Admin Website : http://127.0.0.1:5174
echo Backend API   : http://127.0.0.1:8000
echo API Docs      : http://127.0.0.1:8000/docs
echo ===================================================
pause
