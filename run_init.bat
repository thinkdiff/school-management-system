@echo off
REM Initialize Database Script (Windows)
echo 🗄️ Initializing School Management System Database...
echo ================================================

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

echo 🚀 Initializing database with sample data...
python init_database.py

echo ✅ Database initialization completed!
echo 🎯 You can now start the application with: run_app.bat
pause