#!/bin/bash
# Unified Start Script - Launches both Backend and Frontend

echo "🚀 Starting Advanced Customer Service AI"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this from the project root directory"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up trap to catch Ctrl+C
trap cleanup SIGINT SIGTERM

# Start Backend
echo "🔧 Starting Backend (FastAPI + uvicorn)..."
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Check if backend started successfully
if ! ps -p $BACKEND_PID > /dev/null; then
    echo "❌ Backend failed to start. Check backend.log for errors"
    cat backend.log
    exit 1
fi

echo "✅ Backend started (PID: $BACKEND_PID)"
echo "   URL: http://localhost:8000"
echo "   Logs: backend.log"
echo ""

# Start Frontend
echo "⚛️  Starting Frontend (Next.js)..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 3

# Check if frontend started successfully
if ! ps -p $FRONTEND_PID > /dev/null; then
    echo "❌ Frontend failed to start. Check frontend.log for errors"
    cat frontend.log
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo "   URL: http://localhost:3000"
echo "   Logs: frontend.log"
echo ""
echo "=========================================="
echo "🎉 Both servers are running!"
echo "=========================================="
echo ""
echo "📋 Quick Info:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo "   Health:    http://localhost:8000/health"
echo ""
echo "📝 View Logs:"
echo "   Backend:  tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "⚠️  Press Ctrl+C to stop both servers"
echo ""

# Keep script running and show combined logs
tail -f backend.log frontend.log 2>/dev/null &
TAIL_PID=$!

# Wait for user to press Ctrl+C
wait $BACKEND_PID $FRONTEND_PID

