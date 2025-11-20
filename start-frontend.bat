@echo off
echo ========================================
echo Email Productivity Agent - Frontend
echo ========================================
echo.

cd frontend

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Installing Node.js dependencies...
    call npm install
    echo.
)

echo ========================================
echo Frontend setup complete!
echo Starting React development server...
echo App will open at http://localhost:3000
echo ========================================
echo.

call npm start
