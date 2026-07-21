@echo off
echo "Starting the application..."

REM Start backend
echo "Starting backend server..."
start "Backend" cmd /k "cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000"

REM Start frontend
echo "Starting frontend server..."
start "Frontend" cmd /k "cd frontend && streamlit run app.py"

echo "Application started."
pause
