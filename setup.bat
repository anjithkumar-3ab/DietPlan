@echo off
setlocal
title DietPlan Setup

echo ===================================================
echo                DietPlan Setup
echo ===================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or unavailable in PATH.
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or unavailable in PATH.
    pause
    exit /b 1
)

echo [1/5] Upgrading pip...
python -m pip install --upgrade pip

echo [2/5] Installing backend dependencies...
python -m pip install -r "%~dp0backend\requirements.txt"

echo [3/5] Installing root dependencies...
python -m pip install -r "%~dp0requirements.txt"

echo [4/5] Installing User Website dependencies...
cd /d "%~dp0user-frontend"
call npm install
if not exist ".env" copy ".env.example" ".env"

echo [5/5] Installing Admin Website dependencies...
cd /d "%~dp0admin-frontend"
call npm install
if not exist ".env" copy ".env.example" ".env"

cd /d "%~dp0"
if not exist "backend\.env" copy "backend\.env.example" "backend\.env"

echo.
echo ===================================================
echo Setup completed.
echo 1. Configure backend\.env with MongoDB.
echo 2. Run start.bat to launch both websites.
echo ===================================================
pause
