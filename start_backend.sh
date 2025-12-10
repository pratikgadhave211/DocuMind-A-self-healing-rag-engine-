#!/bin/bash

# Start Backend Only
echo "🔧 Starting Self-Healing RAG Backend..."

# Check virtual environment
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv .venv && pip install -r requirements.txt"
    exit 1
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create .env with OPENAI_API_KEY"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Start server
cd backend
echo "✅ Backend starting on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
python api_server.py
