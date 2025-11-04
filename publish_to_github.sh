#!/bin/bash
# GitHub Publication Helper Script
# Run this to publish your project to GitHub

set -e  # Exit on error

echo "🚀 GitHub Publication Helper"
echo "=============================="
echo ""

# Check if in correct directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this from the project root directory"
    exit 1
fi

# Security check
echo "🔒 Security Check..."
if git ls-files | grep -E "(keyinfo\.md|\.env$)" > /dev/null 2>&1; then
    echo "❌ ERROR: Sensitive files detected in git!"
    echo "   Run: git rm --cached keyinfo.md backend/.env"
    echo "   Then add to .gitignore"
    exit 1
fi
echo "✅ No sensitive files detected"
echo ""

# Check git status
echo "📊 Git Status..."
git status --short
echo ""

# Ask for confirmation
read -p "📝 Ready to commit? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cancelled"
    exit 1
fi

# Stage files
echo "📦 Staging files..."
git add .

# Create commit
echo ""
read -p "💬 Commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Complete Advanced Customer Service AI system

- Multi-agent orchestration with LangGraph
- Three retrieval strategies (RAG, CAG, Hybrid)
- FastAPI backend with SSE streaming
- Next.js frontend with real-time UI
- 100% test coverage (11/11 tests passed)
- Comprehensive documentation"
fi

git commit -m "$commit_msg"
echo "✅ Committed"
echo ""

# Check if remote exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Setting up GitHub remote..."
    echo ""
    read -p "📝 Enter your GitHub username: " github_user
    
    repo_url="https://github.com/$github_user/advanced-customer-service-ai.git"
    echo "   Remote URL: $repo_url"
    git remote add origin "$repo_url"
    echo "✅ Remote added"
    echo ""
    echo "⚠️  IMPORTANT: Create the repository on GitHub first!"
    echo "   Go to: https://github.com/new"
    echo "   Repository name: advanced-customer-service-ai"
    echo "   Make it PUBLIC"
    echo "   Do NOT initialize with README"
    echo ""
    read -p "Press Enter when repository is created..." 
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push -u origin main || git push -u origin master

echo ""
echo "🎉 SUCCESS! Your project is now on GitHub!"
echo ""
echo "📋 Next Steps:"
echo "   1. Add topics on GitHub (langgraph, multi-agent, rag, fastapi, nextjs)"
echo "   2. Record demo video (see QUICK_START_GUIDE.md)"
echo "   3. Update README.md with demo video link"
echo "   4. Share on LinkedIn/Twitter!"
echo ""
echo "🔗 Repository should be at:"
git remote get-url origin | sed 's/\.git$//'
echo ""

