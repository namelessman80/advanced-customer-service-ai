#!/bin/bash
# Stop Script - Stops both Backend and Frontend servers

echo "🛑 Stopping Advanced Customer Service AI servers..."
echo ""

# Kill backend (uvicorn)
echo "Stopping Backend..."
pkill -f "uvicorn main:app" && echo "✅ Backend stopped" || echo "⚠️  Backend not running"

# Kill frontend (Next.js)
echo "Stopping Frontend..."
pkill -f "next dev" && echo "✅ Frontend stopped" || echo "⚠️  Frontend not running"

# Clean up log files
if [ -f backend.log ] || [ -f frontend.log ]; then
    echo ""
    read -p "Delete log files? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f backend.log frontend.log
        echo "✅ Log files deleted"
    fi
fi

echo ""
echo "✅ All servers stopped"

