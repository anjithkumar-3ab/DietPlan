@echo off
title NutriAI Launcher

echo ===================================================
echo               Starting NutriAI
echo   AI-Based Personalized Diet Planning System
echo ===================================================
echo.

REM Check if backend .env exists
if not exist "%~dp0backend\.env" (
    echo [WARNING] backend\.env file not found!
    echo Please run setup.bat or create backend\.env with your MONGODB_URI.
    echo.
)

REM Start FastAPI Backend
echo [1/2] Launching FastAPI Backend Server...
start "NutriAI Backend" cmd /k "cd /d %~dp0backend && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

REM Wait for backend to initialize
echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Start Frontend (HTML/CSS/JS)
echo [2/2] Launching Frontend Web Server...
start "NutriAI Frontend" cmd /k "cd /d %~dp0frontend && python -m http.server 5500"

REM Open browser
timeout /t 2 /nobreak >nul
echo Opening NutriAI in browser...
start http://127.0.0.1:5500

echo.
echo ===================================================
echo           NutriAI is up and running!
echo ===================================================
echo Frontend UI       : http://127.0.0.1:5500
echo Backend API       : http://127.0.0.1:8000
echo API Docs (Swagger): http://127.0.0.1:8000/docs
echo API Docs (ReDoc)  : http://127.0.0.1:8000/redoc
echo ===================================================
echo Press any key to exit this window. (Servers run in background)
pause >nul