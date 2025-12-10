#!/bin/bash

# Self-Healing RAG System Startup Script
# This script starts both backend and frontend servers

echo "🚀 Starting Self-Healing RAG System..."
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv .venv"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create .env with OPENAI_API_KEY"
    echo "Example: echo 'OPENAI_API_KEY=your-key-here' > .env"
    exit 1
fi

# Check if frontend node_modules exist
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend server
echo "🔧 Starting Backend API Server..."
source .venv/bin/activate
cd backend
python api_server.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 5

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ Backend failed to start. Check logs/backend.log"
    exit 1
fi

echo "✅ Backend running on http://localhost:8000"

# Start frontend server
echo "🎨 Starting Frontend Server..."
cd frontend
npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "⏳ Waiting for frontend to initialize..."
sleep 3

# Check if frontend is running
if ! ps -p $FRONTEND_PID > /dev/null; then
    echo "❌ Frontend failed to start. Check logs/frontend.log"
    kill $BACKEND_PID
    exit 1
fi

echo "✅ Frontend running on http://localhost:3000"
echo ""
echo "========================================"
echo "🎉 Self-Healing RAG System is ready!"
echo "========================================"
echo ""
echo "📍 Access points:"
echo "   Frontend:  http://localhost:3000"
echo "   API:       http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📊 Logs:"
echo "   Backend:   logs/backend.log"
echo "   Frontend:  logs/frontend.log"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Keep script running
wait $BACKEND_PID $FRONTEND_PID
