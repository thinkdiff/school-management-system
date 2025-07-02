@echo off
REM Run Application Script (Windows)
echo 🏫 Starting School Management System...
echo ====================================

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo ❌ .env file not found. Please create .env file with your MongoDB connection.
    pause
    exit /b 1
)

echo 🚀 Starting Streamlit application...
echo 📱 Application will open in your browser at: http://localhost:8501
echo 🔑 Default login: admin / admin123
echo.
echo Press Ctrl+C to stop the application
echo =====================================

streamlit run app.py
pause