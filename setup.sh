#!/bin/bash

# School Management System - Quick Setup Script
echo "🏫 School Management System - Quick Setup"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✅ pip found: $(pip3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️ .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your MongoDB Atlas connection string"
fi

echo ""
echo "🚀 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your MongoDB Atlas connection"
echo "2. Run: python init_database.py (to initialize database)"
echo "3. Run: streamlit run app.py (to start the application)"
echo ""
echo "📖 Or use the quick commands:"
echo "   ./run_init.sh  (initialize database)"
echo "   ./run_app.sh   (start application)"