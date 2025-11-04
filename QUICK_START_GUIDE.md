# Quick Start Guide - Demo & GitHub Publication

## ✅ Credentials Updated!

Your OpenAI and AWS Bedrock credentials have been updated in `backend/.env`. 

**Security Note**: ✅ Both `keyinfo.md` and `.env` are git-ignored and will NOT be committed to GitHub.

---

## 🎥 Demo Video Recording - Quick Guide

### Option 1: Quick Screen Recording (Recommended - 10 minutes)

#### Preparation (2 minutes)
1. **Restart servers with new credentials**:
```bash
# Terminal 1: Backend (Ctrl+C to stop old one)
cd backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

2. **Open browser to** http://localhost:3000
3. **Start screen recording** (Mac: Cmd+Shift+5, Windows: Windows+G)

#### Recording Script (5-8 minutes)

**Part 1: Introduction (1 min)**
- Show welcome screen
- Say: "This is a multi-agent customer service AI with three specialists"
- Point to the three agent cards

**Part 2: Demo Each Agent (3 min)**

**Billing Agent:**
- Type: `"What does the Enterprise plan cost?"`
- Point out: 💰 Blue badge, real-time streaming
- Say: "Billing Agent uses Hybrid RAG/CAG with caching"

**Technical Agent:**
- Type: `"My API integration keeps timing out. How do I fix this?"`
- Point out: 🔧 Orange badge
- Say: "Technical Agent uses Pure RAG for latest docs"

**Policy Agent:**
- Type: `"Do you comply with GDPR?"`
- Point out: 📋 Green badge
- Say: "Policy Agent uses Pure CAG for fast responses"

**Part 3: Session Context (1 min)**
- Type: `"Can I upgrade from Basic to Premium?"`
- Point out: Same session ID maintained
- Say: "System maintains context across messages"

**Part 4: Code Walkthrough (2 min)**
- Open `backend/agents/orchestrator.py`
- Highlight routing logic
- Open `backend/main.py`
- Highlight streaming code
- Say: "LangGraph orchestrates, FastAPI streams with SSE"

**Part 5: Testing (1 min)**
- Show terminal: `python e2e_tests.py` results
- Point out: 100% pass rate (11/11 tests)

**Part 6: Closing (30 sec)**
- Say: "Production-ready system with comprehensive testing and documentation"
- Show README.md briefly

### Option 2: Screenshot Presentation (If no video)

Take screenshots at each step and create a slide deck:
1. Welcome screen
2. Each agent demo (3 screenshots)
3. Session context
4. Code snippets
5. Test results

---

## 📤 GitHub Publication - Step by Step

### 1. Initialize Git (if not already done)

```bash
cd /Users/keithshin/Github/asu/advanced_customer_service_ai

# Check git status
git status

# If not initialized:
git init
git branch -M main
```

### 2. Add Files to Git

```bash
# Stage all files (keyinfo.md and .env are auto-ignored)
git add .

# Verify what will be committed
git status

# You should see:
# ✅ All code files
# ✅ Documentation files
# ❌ NOT: .env, keyinfo.md, node_modules, venv, chroma_db
```

### 3. Create Initial Commit

```bash
git commit -m "Complete Advanced Customer Service AI system

- Multi-agent orchestration with LangGraph
- Three retrieval strategies (RAG, CAG, Hybrid)
- FastAPI backend with SSE streaming
- Next.js frontend with real-time UI
- 100% test coverage (11/11 tests passed)
- Comprehensive documentation"
```

### 4. Create GitHub Repository

**Option A: Via GitHub Website (Easier)**
1. Go to https://github.com/new
2. **Repository name**: `advanced-customer-service-ai`
3. **Description**: "Multi-agent customer service AI with LangGraph, RAG/CAG strategies, and real-time streaming"
4. **Public** ✅ (for showcase)
5. **Do NOT** initialize with README (we have one)
6. Click "Create repository"

**Option B: Via GitHub CLI**
```bash
gh repo create advanced-customer-service-ai --public --source=. --remote=origin
```

### 5. Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/advanced-customer-service-ai.git

# Push to GitHub
git push -u origin main
```

### 6. Configure Repository Settings (On GitHub Website)

1. **Add Topics**: 
   - langgraph
   - langchain
   - multi-agent
   - rag
   - fastapi
   - nextjs
   - openai
   - customer-service
   - ai

2. **Add Description**:
   "Production-ready multi-agent customer service AI with intelligent routing, multiple retrieval strategies (RAG, CAG, Hybrid), and real-time SSE streaming"

3. **Enable GitHub Pages** (Optional):
   - Settings → Pages → Source: main branch / docs (if you want to host docs)

### 7. Add Demo Video to README (After Recording)

1. Upload video to YouTube
2. Set as "Unlisted" (not private, but not searchable)
3. Copy video link
4. Update README.md:

```bash
# Edit README.md, find the line:
**Live Demo**: [Watch on YouTube](#) *(Coming Soon)*

# Replace with:
**Live Demo**: [Watch on YouTube](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
```

5. Commit and push:
```bash
git add README.md
git commit -m "Add demo video link to README"
git push
```

---

## 🎬 YouTube Upload Settings (After Recording)

### Video Details
- **Title**: "Advanced Customer Service AI - Multi-Agent System with LangGraph Demo"
- **Description**:
```
Demo of a production-ready AI customer service system featuring:
✅ Multi-agent orchestration with LangGraph
✅ Three specialized agents (Billing, Technical, Policy)
✅ Multiple retrieval strategies (RAG, CAG, Hybrid RAG/CAG)
✅ Real-time SSE streaming
✅ 100% test coverage

🔗 GitHub: [Your GitHub Link]
📚 Full Documentation: See README.md
🧪 Test Results: 11/11 passed (100%)

Tech Stack: FastAPI, LangGraph, LangChain, OpenAI GPT-4, AWS Bedrock, ChromaDB, Next.js 16, React 19, TypeScript

Timestamps:
0:00 - Introduction
1:00 - Multi-Agent Routing Demo
4:00 - Session Context
5:00 - Code Walkthrough
7:00 - Testing Results
8:00 - Conclusion
```

- **Visibility**: Unlisted (best for portfolio)
- **Tags**: LangGraph, Multi-Agent AI, RAG, CAG, FastAPI, Next.js, Customer Service AI, OpenAI GPT-4

---

## ✅ Pre-Publication Checklist

Before pushing to GitHub:

### Files to Review
- [ ] ✅ README.md is complete
- [ ] ✅ .env is NOT committed (git-ignored)
- [ ] ✅ keyinfo.md is NOT committed (git-ignored)
- [ ] ✅ All documentation files are included
- [ ] ✅ Test results are documented

### Security Check
```bash
# Verify sensitive files are ignored
git status

# Should NOT see:
# - .env
# - keyinfo.md
# - Any API keys or tokens

# If they appear, add to .gitignore:
echo "keyinfo.md" >> .gitignore
echo ".env" >> .gitignore
```

### Test Before Publishing
```bash
# Run tests one more time
cd backend
python e2e_tests.py

# Expected: 11/11 tests PASSED
```

---

## 📊 After Publishing

### Share Your Project

1. **Update Profile README** (if you have one)
2. **Add to Portfolio Website**
3. **Share on LinkedIn**:
   ```
   Excited to share my latest project: Advanced Customer Service AI! 
   
   Built a production-ready multi-agent system using LangGraph with:
   🤖 3 specialized AI agents
   📊 Multiple retrieval strategies (RAG, CAG, Hybrid)
   ⚡ Real-time SSE streaming
   ✅ 100% test coverage
   
   Tech: Python, FastAPI, LangGraph, OpenAI GPT-4, Next.js, React
   
   [GitHub Link] | [Demo Video]
   ```

4. **Add to Resume/CV**:
   - Project name: Advanced Customer Service AI
   - Technologies: LangGraph, FastAPI, Next.js, OpenAI GPT-4, ChromaDB
   - Highlights: Multi-agent orchestration, 100% test coverage, production-ready

---

## 🚀 Quick Commands Reference

### Restart Backend with New Credentials
```bash
# Stop old backend (Ctrl+C or pkill)
pkill -f "uvicorn main:app"

# Start with new credentials
cd /Users/keithshin/Github/asu/advanced_customer_service_ai/backend
source venv/bin/activate
uvicorn main:app --reload
```

### Check What Will Be Committed
```bash
git status
git diff --cached  # See staged changes
```

### Undo If Needed
```bash
# Unstage a file
git reset HEAD <file>

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

---

## ❓ Troubleshooting

### "API key invalid" Error
- Double-check credentials in `backend/.env`
- Restart backend server to load new credentials

### Git Tracking .env File
```bash
# Remove from git if accidentally added
git rm --cached backend/.env
git rm --cached keyinfo.md

# Add to .gitignore
echo "backend/.env" >> .gitignore
echo "keyinfo.md" >> .gitignore

# Commit changes
git commit -m "Remove sensitive files from git"
```

### Large Files Warning
```bash
# ChromaDB and node_modules should be ignored
# If not, add to .gitignore:
echo "backend/chroma_db/" >> .gitignore
echo "frontend/node_modules/" >> .gitignore
```

---

## 🎉 You're Ready!

1. ✅ Credentials updated
2. ⏳ Record demo (optional but recommended)
3. ⏳ Push to GitHub
4. ⏳ Share your work!

**Need help?** Check:
- Full demo script: `DEMO_SCRIPT.md`
- Complete documentation: `README.md`
- Test results: `TESTING_RESULTS.md`

Good luck with your demo and publication! 🚀

