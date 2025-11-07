# 🚀 How to Start the Application

## Quick Start (One Command!)

```bash
cd /Users/keithshin/Github/asu/advanced_customer_service_ai
./start.sh
```

That's it! Both servers will start automatically. 🎉

---

## What the Start Script Does

1. ✅ Starts the **Backend** (FastAPI + uvicorn) on port 8000
2. ✅ Starts the **Frontend** (Next.js) on port 3000
3. ✅ Shows status and URLs
4. ✅ Streams logs from both servers
5. ✅ Press **Ctrl+C** to stop both servers at once

---

## URLs After Starting

Once started, you can access:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main chat interface |
| **Backend API** | http://localhost:8000 | API endpoint |
| **API Docs** | http://localhost:8000/docs | Interactive API documentation |
| **Health Check** | http://localhost:8000/health | System health status |

---

## Logs

Logs are saved to files so you can view them later:

```bash
# View backend logs
tail -f backend.log

# View frontend logs
tail -f frontend.log

# View both at once
tail -f backend.log frontend.log
```

---

## Stopping the Servers

### Option 1: Interactive Stop (Recommended)
```bash
# If servers are running in foreground, press:
Ctrl+C
```

### Option 2: Stop Script
```bash
./stop.sh
```

This will:
- ✅ Stop backend server
- ✅ Stop frontend server
- ✅ Optionally delete log files

---

## Manual Start (If You Prefer)

### Backend Only
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

### Frontend Only
```bash
cd frontend
npm run dev
```

---

## Troubleshooting

### "Port already in use" Error

**Backend (Port 8000):**
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

**Frontend (Port 3000):**
```bash
# Find and kill process using port 3000
lsof -ti:3000 | xargs kill -9
```

**Or use the stop script:**
```bash
./stop.sh
```

### "Permission denied" Error
```bash
# Make scripts executable
chmod +x start.sh stop.sh
```

### Backend fails to start
```bash
# Check backend.log
cat backend.log

# Common issues:
# 1. Virtual environment not activated
# 2. Dependencies not installed
# 3. .env file missing

# Fix:
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend fails to start
```bash
# Check frontend.log
cat frontend.log

# Common issues:
# 1. node_modules not installed
# 2. .env.local file missing

# Fix:
cd frontend
npm install
```

### ChromaDB error
```bash
# Re-run data ingestion
cd backend
source venv/bin/activate
python ingest_data.py
```

---

## Quick Commands Reference

| Command | Description |
|---------|-------------|
| `./start.sh` | Start both servers |
| `./stop.sh` | Stop both servers |
| `tail -f backend.log` | View backend logs |
| `tail -f frontend.log` | View frontend logs |
| `./publish_to_github.sh` | Publish to GitHub |
| `cd backend && python e2e_tests.py` | Run tests |

---

## First Time Setup

If this is your first time running the application:

1. **Install Backend Dependencies:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Set Up Environment Variables:**
```bash
# Make sure backend/.env exists with your API keys
# (It should already be set up from earlier)
```

3. **Ingest Data:**
```bash
cd backend
source venv/bin/activate
python ingest_data.py
```

4. **Install Frontend Dependencies:**
```bash
cd frontend
npm install
```

5. **Start Everything:**
```bash
cd ..  # Back to project root
./start.sh
```

---

## Development Tips

### Auto-Reload
- **Backend**: Uses `--reload` flag, automatically restarts on code changes
- **Frontend**: Next.js hot-reloads automatically on code changes

### View Real-Time Logs
```bash
# In a new terminal while servers are running
tail -f backend.log frontend.log
```

### Test Backend API
```bash
# Health check
curl http://localhost:8000/health

# Test chat (in another terminal)
cd backend
source venv/bin/activate
python e2e_tests.py
```

---

## Status Checking

### Check if servers are running
```bash
# Check backend
curl -s http://localhost:8000/health | python3 -m json.tool

# Check frontend
curl -s http://localhost:3000 | head -5
```

### Check process IDs
```bash
# Backend process
ps aux | grep uvicorn

# Frontend process
ps aux | grep "next dev"
```

---

## 🎉 Ready to Go!

Just run:
```bash
./start.sh
```

Then open your browser to: **http://localhost:3000**

Enjoy your Advanced Customer Service AI! 🤖💬


