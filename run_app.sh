#!/bin/bash

# Run Application Script
echo "🏫 Starting School Management System..."
echo "===================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create .env file with your MongoDB connection."
    exit 1
fi

echo "🚀 Starting Streamlit application..."
echo "📱 Application will open in your browser at: http://localhost:8501"
echo "🔑 Default login: admin / admin123"
echo ""
echo "Press Ctrl+C to stop the application"
echo "====================================="

streamlit run app.py