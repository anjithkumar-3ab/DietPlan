@echo off
title NutriAI Setup

echo =====================================
echo        NutriAI Project Setup
echo =====================================
echo.

python -m pip install --upgrade pip

echo.
echo Installing project dependencies...
pip install -r requirements.txt
pip install -r backend\requirements.txt

echo.
echo =====================================
echo Setup completed successfully.
echo =====================================
pause