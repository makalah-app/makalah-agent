#!/bin/bash

# Agent-Makalah Backend Development Server Startup Script

set -e  # Exit on any error

echo "🚀 Starting Agent-Makalah Backend Development Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run 'python -m venv venv' first."
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if FastAPI is installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install fastapi "uvicorn[standard]" pydantic pydantic-settings
fi

# Change to src directory
cd src

# Start the server
echo "🔥 Starting FastAPI server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "📊 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"

python main.py 