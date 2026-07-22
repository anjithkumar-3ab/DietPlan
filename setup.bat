@echo off
title NutriAI Project Setup

echo ===================================================
echo               NutriAI Project Setup
echo   AI-Based Personalized Diet Planning System
echo ===================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to system PATH.
    echo Please install Python 3.10 or higher and try again.
    pause
    exit /b 1
)

echo [1/4] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [2/4] Installing root project dependencies...
pip install -r requirements.txt

echo.
echo [3/4] Installing backend dependencies...
pip install -r backend\requirements.txt

echo.
echo [4/4] Checking environment configuration...
if not exist "backend\.env" (
    if exist "backend\.env.example" (
        echo Copying backend\.env.example to backend\.env...
        copy "backend\.env.example" "backend\.env"
        echo [NOTICE] Created backend\.env from template. Please update your MongoDB URI in backend\.env.
    ) else (
        echo [WARNING] backend\.env not found. Please set up your MONGODB_URI in backend\.env.
    )
) else (
    echo [OK] backend\.env file exists.
)

echo.
echo ===================================================
echo           Setup Completed Successfully!
echo ===================================================
echo Next steps:
echo 1. Verify your MongoDB connection string in backend\.env
echo 2. (Optional) Seed food database: python backend\scripts\import_foods.py
echo 3. Launch the application by running start.bat
echo ===================================================
pause