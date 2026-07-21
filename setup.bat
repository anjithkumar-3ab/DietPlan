@echo off
echo "Setting up the environment..."

REM Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
pip install -r backend/requirements.txt

echo "Setup complete."
pause
