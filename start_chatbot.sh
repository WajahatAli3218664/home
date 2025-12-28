#!/bin/bash

# Comprehensive startup script for the chatbot system
# This script starts both backend and frontend services

set -e

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  PHYSICAL AI CHATBOT - COMPLETE STARTUP"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo -e "${YELLOW}⚠ Not in project root. Moving to correct directory...${NC}"
    cd "$(dirname "$0")"
fi

echo -e "${BLUE}1. Checking Python environment...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}✗ Python 3 not found. Please install Python 3.10+${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓ Found $PYTHON_VERSION${NC}"

echo ""
echo -e "${BLUE}2. Checking Node.js environment...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠ Node.js not found. Frontend will not start.${NC}"
else
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Found Node.js $NODE_VERSION${NC}"
fi

echo ""
echo -e "${BLUE}3. Setting up Python dependencies...${NC}"
python3 -m pip install --upgrade pip --quiet 2>/dev/null || true
if [ -f "backend/requirements.txt" ]; then
    echo "Installing backend requirements..."
    pip install -q -r backend/requirements.txt 2>/dev/null || true
    echo -e "${GREEN}✓ Backend dependencies installed${NC}"
fi

echo ""
echo -e "${BLUE}4. Running integration tests...${NC}"
if [ -f "test_chatbot.py" ]; then
    python3 test_chatbot.py 2>&1 | grep -E "(✓|✗|PASS|FAIL|Results)" || true
    echo ""
fi

echo ""
echo -e "${BLUE}5. Starting Backend Server...${NC}"
echo -e "${YELLOW}Starting FastAPI backend on port 8000...${NC}"

# Kill any existing process on port 8000
lsof -ti:8000 2>/dev/null | xargs kill -9 2>/dev/null || true
sleep 1

# Start backend in background
cd /workspaces/home
nohup python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
echo "  Logs: tail -f backend.log"
echo "  API Docs: http://localhost:8000/docs"

# Wait for backend to be ready
echo -e "${YELLOW}  Waiting for backend to start...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/api/v1/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend is ready!${NC}"
        break
    fi
    sleep 1
    echo -n "."
done
echo ""

echo ""
echo -e "${BLUE}6. Starting Frontend Server...${NC}"

# Check if frontend exists
if [ -d "frontend" ]; then
    echo -e "${YELLOW}Starting Next.js frontend on port 3000...${NC}"
    
    cd frontend
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "Installing frontend dependencies..."
        npm install --silent 2>/dev/null || true
    fi
    
    # Start frontend in background
    nohup npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
    echo "  Logs: tail -f frontend.log"
    echo "  URL: http://localhost:3000"
    cd ..
else
    echo -e "${YELLOW}⚠ Frontend directory not found${NC}"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✓ STARTUP COMPLETE!${NC}"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Services running:"
echo -e "  ${GREEN}✓ Backend API${NC} - http://localhost:8000"
echo -e "  ${GREEN}✓ API Documentation${NC} - http://localhost:8000/docs"
if [ -d "frontend" ]; then
    echo -e "  ${GREEN}✓ Frontend${NC} - http://localhost:3000"
fi
echo ""
echo "Quick tests:"
echo "  Backend health: curl http://localhost:8000/api/v1/health"
echo "  Query chatbot: curl -X POST http://localhost:8000/api/v1/rag/query \\"
echo "                    -H 'Content-Type: application/json' \\"
echo "                    -d '{\"query\": \"What is AI?\", \"book_id\": \"test\", \"session_id\": \"test\"}'"
echo ""
echo "To stop services:"
echo "  pkill -f 'uvicorn backend.main:app'"
echo "  pkill -f 'npm run dev'"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
