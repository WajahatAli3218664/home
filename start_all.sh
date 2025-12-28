#!/bin/bash

echo "🚀 Starting Physical AI Textbook Platform..."

# Kill any existing backend processes
pkill -f "python demo_main.py" 2>/dev/null

# Start backend
echo "📡 Starting backend server..."
cd backend
nohup python demo_main.py > backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "❌ Backend failed to start. Check backend/backend.log"
    exit 1
fi

# Start frontend
echo "🌐 Starting frontend server..."
cd frontend
npm start

# Cleanup on exit
trap "kill $BACKEND_PID 2>/dev/null" EXIT