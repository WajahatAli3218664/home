@echo off
echo Starting RAG Chatbot Application...

REM Start the backend server in the background
start "Backend Server" cmd /c "cd backend && python -m uvicorn src.main:app --reload --port 8000"

REM Wait a bit for the backend to start
timeout /t 3 /nobreak >nul

REM Start the frontend server in the background
start "Frontend Server" cmd /c "cd frontend && npm run dev"

echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000 (or next available port)
echo.
echo Press Ctrl+C to stop both servers
pause