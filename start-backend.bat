@echo off
echo ========================================
echo Email Productivity Agent - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install backend dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
echo.

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Please edit .env file and add your OpenAI API key!
    echo.
    pause
)

REM Initialize database
if not exist "email_agent.db" (
    echo Initializing database with sample data...
    cd backend
    python seed_data.py
    cd ..
    echo.
) else (
    echo Database already exists, skipping seed data...
    echo.
)

echo ========================================
echo Backend setup complete!
echo Starting backend server...
echo API will be available at http://localhost:8000
echo API docs at http://localhost:8000/docs
echo ========================================
echo.

cd backend
python main.py
