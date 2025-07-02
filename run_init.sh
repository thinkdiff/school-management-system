#!/bin/bash

# Initialize Database Script
echo "🗄️ Initializing School Management System Database..."
echo "================================================"

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

echo "🚀 Initializing database with sample data..."
python init_database.py

echo "✅ Database initialization completed!"
echo "🎯 You can now start the application with: ./run_app.sh"