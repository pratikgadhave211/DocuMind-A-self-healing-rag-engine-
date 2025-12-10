#!/bin/bash

# Start Frontend Only
echo "🎨 Starting Self-Healing RAG Frontend..."

# Check if node_modules exist
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Start development server
cd frontend
echo "✅ Frontend starting on http://localhost:3000"
npm run dev
