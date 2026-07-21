@echo off
title NutriAI Launcher

echo =====================================
echo      Starting NutriAI Project
echo =====================================
echo.

REM Start FastAPI Backend
echo Starting Backend...
start "NutriAI Backend" cmd /k "cd /d %~dp0backend && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

REM Wait for backend to initialize
timeout /t 5 /nobreak >nul

REM Start Frontend (HTML/CSS/JS)
echo Starting Frontend...
start "NutriAI Frontend" cmd /k "cd /d %~dp0frontend && python -m http.server 5500"

REM Open browser
timeout /t 2 /nobreak >nul
start http://127.0.0.1:5500

echo.
echo =====================================
echo Backend  : http://127.0.0.1:8000
echo Swagger  : http://127.0.0.1:8000/docs
echo Frontend : http://127.0.0.1:5500
echo =====================================
pause