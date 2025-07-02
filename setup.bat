@echo off
REM School Management System - Windows Setup Script
echo 🏫 School Management System - Quick Setup (Windows)
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📚 Installing Python dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️ .env file not found. Creating from .env.example...
    copy .env.example .env
    echo 📝 Please edit .env file with your MongoDB Atlas connection string
)

echo.
echo 🚀 Setup completed successfully!
echo.
echo Next steps:
echo 1. Edit .env file with your MongoDB Atlas connection
echo 2. Run: python init_database.py (to initialize database)
echo 3. Run: streamlit run app.py (to start the application)
echo.
echo 📖 Or use the batch files:
echo    run_init.bat  (initialize database)
echo    run_app.bat   (start application)
pause