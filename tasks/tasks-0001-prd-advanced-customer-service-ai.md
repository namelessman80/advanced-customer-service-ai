# Task List: Advanced Customer Service AI

**Based on PRD:** `0001-prd-advanced-customer-service-ai.md`

**Current State Assessment:**
- Greenfield project with no existing backend or frontend code
- Starting from scratch with a clean repository
- API keys available in `keyinfo.md`
- Technology stack: Python/FastAPI (backend), Next.js/React (frontend), LangGraph, ChromaDB, OpenAI, AWS Bedrock

---

## Relevant Files

### Backend Files
- `backend/main.py` - FastAPI application entry point with /chat endpoint and CORS configuration
- `backend/requirements.txt` - Python dependencies (FastAPI, LangChain, LangGraph, ChromaDB, OpenAI, Boto3)
- `backend/.env` - Environment variables for API keys (git-ignored)
- `backend/agents/__init__.py` - Agent module initialization
- `backend/agents/orchestrator.py` - LangGraph orchestrator logic with AWS Bedrock for routing
- `backend/agents/billing_agent.py` - Billing support agent with Hybrid RAG/CAG implementation
- `backend/agents/technical_agent.py` - Technical support agent with Pure RAG implementation
- `backend/agents/policy_agent.py` - Policy & compliance agent with Pure CAG implementation
- `backend/models/__init__.py` - Models module initialization
- `backend/models/schemas.py` - Pydantic models for API request/response validation
- `backend/utils/__init__.py` - Utils module initialization
- `backend/utils/llm_config.py` - LLM provider configuration (OpenAI, AWS Bedrock)
- `backend/utils/retrieval.py` - RAG/CAG utilities and ChromaDB interaction logic
- `backend/ingest_data.py` - Data ingestion script for processing and embedding documents
- `backend/data/billing/*.txt` - Mock billing documents (8 files)
- `backend/data/technical/*.txt` - Mock technical documents (12 files)
- `backend/data/policy/*.txt` - Mock policy documents (6 files)

### Frontend Files
- `frontend/package.json` - Node.js dependencies and scripts
- `frontend/next.config.js` - Next.js configuration
- `frontend/tsconfig.json` - TypeScript configuration
- `frontend/tailwind.config.js` - Tailwind CSS configuration
- `frontend/src/app/layout.tsx` - Root layout component
- `frontend/src/app/page.tsx` - Main chat interface page
- `frontend/src/components/ChatInterface.tsx` - Main chat container component
- `frontend/src/components/MessageList.tsx` - Conversation history display component
- `frontend/src/components/Message.tsx` - Individual message bubble component
- `frontend/src/components/ChatInput.tsx` - Input field and send button component
- `frontend/src/components/AgentBadge.tsx` - Agent identification badge component
- `frontend/src/components/LoadingIndicator.tsx` - Typing/loading animation component
- `frontend/src/components/ErrorMessage.tsx` - Error display component
- `frontend/src/lib/api.ts` - Backend API client with streaming support
- `frontend/.env.local` - Frontend environment variables (git-ignored)

### Root Level Files
- `README.md` - Project documentation with setup and running instructions
- `.gitignore` - Git ignore configuration
- `.env.example` - Example environment variables template

### Notes
- ChromaDB will persist to `backend/chroma_db/` directory (git-ignored)
- Mock documents should contain realistic 1-2 paragraph content with relevant keywords
- Use Server-Sent Events (SSE) for streaming responses
- Session management will be in-memory (no database persistence for MVP)

---

## Tasks

- [ ] **1.0 Project Foundation & Setup**
  - [ ] 1.1 Create root directory structure: `backend/`, `frontend/`, `tasks/`
  - [ ] 1.2 Create backend directory structure: `backend/agents/`, `backend/models/`, `backend/utils/`, `backend/data/billing/`, `backend/data/technical/`, `backend/data/policy/`
  - [ ] 1.3 Initialize Python virtual environment in backend directory: `python -m venv venv`
  - [ ] 1.4 Create `backend/requirements.txt` with dependencies: fastapi, uvicorn, langchain, langgraph, langchain-openai, langchain-aws, chromadb, python-dotenv, pydantic, boto3
  - [ ] 1.5 Install backend dependencies: `pip install -r requirements.txt`
  - [ ] 1.6 Initialize Next.js frontend with TypeScript and Tailwind CSS: `npx create-next-app@latest frontend --typescript --tailwind --app`
  - [ ] 1.7 Create `.env.example` file at root with template for OPENAI_API_KEY, AWS credentials, and other config
  - [ ] 1.8 Create `backend/.env` file with actual API keys from `keyinfo.md` (OPENAI_API_KEY, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_DEFAULT_REGION=us-east-1, CHROMA_PERSIST_DIR=./chroma_db)
  - [ ] 1.9 Create `frontend/.env.local` with NEXT_PUBLIC_API_URL=http://localhost:8000
  - [ ] 1.10 Create comprehensive `.gitignore` file (include venv/, node_modules/, .env, .env.local, chroma_db/, __pycache__/)
  - [ ] 1.11 Initialize Git repository: `git init` and create initial commit
  - [ ] 1.12 Create empty `__init__.py` files in all backend Python module directories

- [ ] **2.0 Mock Data Creation & Ingestion Pipeline**
  - [ ] 2.1 Create 2 pricing tier comparison documents in `backend/data/billing/` (pricing_tiers_basic_premium.txt, pricing_tiers_enterprise.txt)
  - [ ] 2.2 Create 2 invoice template examples in `backend/data/billing/` (invoice_template_monthly.txt, invoice_template_annual.txt)
  - [ ] 2.3 Create 2 billing policy documents in `backend/data/billing/` (payment_terms.txt, refund_policy.txt)
  - [ ] 2.4 Create 2 subscription management guides in `backend/data/billing/` (subscription_upgrade.txt, subscription_cancellation.txt)
  - [ ] 2.5 Create 4 troubleshooting guides in `backend/data/technical/` (login_issues.txt, performance_problems.txt, integration_errors.txt, mobile_app_issues.txt)
  - [ ] 2.6 Create 3 bug report summaries in `backend/data/technical/` (bug_report_api_timeout.txt, bug_report_ui_glitch.txt, bug_report_data_sync.txt)
  - [ ] 2.7 Create 3 technical how-to guides in `backend/data/technical/` (api_setup_guide.txt, webhook_configuration.txt, data_export_guide.txt)
  - [ ] 2.8 Create 2 forum post compilations in `backend/data/technical/` (forum_common_questions.txt, forum_integration_tips.txt)
  - [ ] 2.9 Create 1 Terms of Service document in `backend/data/policy/` (terms_of_service.txt)
  - [ ] 2.10 Create 1 Privacy Policy document in `backend/data/policy/` (privacy_policy.txt)
  - [ ] 2.11 Create 2 GDPR compliance documents in `backend/data/policy/` (gdpr_data_rights.txt, gdpr_data_processing.txt)
  - [ ] 2.12 Create 1 Cookie Policy document in `backend/data/policy/` (cookie_policy.txt)
  - [ ] 2.13 Create 1 Acceptable Use Policy document in `backend/data/policy/` (acceptable_use_policy.txt)
  - [ ] 2.14 Implement `backend/ingest_data.py` with imports (chromadb, openai, os, glob, datetime)
  - [ ] 2.15 Add document loading logic to read all .txt files from data directories
  - [ ] 2.16 Implement text chunking function (500-1000 tokens per chunk, 100 token overlap using langchain.text_splitter)
  - [ ] 2.17 Implement embedding generation using OpenAI text-embedding-3-small model
  - [ ] 2.18 Create ChromaDB persistent client with path from environment variable
  - [ ] 2.19 Create/get collection in ChromaDB with metadata schema
  - [ ] 2.20 Add chunks to ChromaDB with metadata (document_type, source_document, chunk_index, last_updated timestamp)
  - [ ] 2.21 Implement idempotency check (clear collection if re-running or check for existing documents)
  - [ ] 2.22 Add progress logging to show which documents are being processed
  - [ ] 2.23 Test ingestion script: run `python backend/ingest_data.py` and verify ChromaDB created and populated
  - [ ] 2.24 Verify 26 documents processed and appropriate chunks created (~26-52 chunks)
  - [ ] 2.25 Query ChromaDB to validate metadata is correctly attached to all chunks

- [ ] **3.0 Backend Multi-Agent System Implementation**
  - [ ] 3.1 Create `backend/utils/llm_config.py` with OpenAI client configuration (GPT-4 for responses)
  - [ ] 3.2 Add AWS Bedrock client configuration in `llm_config.py` (Claude 3 Haiku, Nova Lite, or Nova Micro for routing - developer's choice)
  - [ ] 3.3 Set temperature configs: orchestrator temp=0 (deterministic), response generation temp=0.7 (natural)
  - [ ] 3.4 Create `backend/utils/retrieval.py` with ChromaDB client initialization
  - [ ] 3.5 Implement RAG query function in `retrieval.py` (query vector DB with metadata filtering, return top_k=3-5 chunks)
  - [ ] 3.6 Implement CAG cache management functions in `retrieval.py` (load documents into memory, retrieve from cache)
  - [ ] 3.7 Create `backend/models/schemas.py` with Pydantic models: ChatRequest (message: str, session_id: Optional[str]), ChatResponse, AgentState (messages, current_agent, session_context, cached_billing_info)
  - [ ] 3.8 Create `backend/agents/orchestrator.py` with LangGraph imports
  - [ ] 3.9 Define orchestrator node function that uses AWS Bedrock to classify queries into: billing, technical, or policy
  - [ ] 3.10 Implement routing logic that returns next agent node based on classification
  - [ ] 3.11 Add prompt for orchestrator: "Classify this customer service query into one of three categories: billing/pricing, technical support, or policy/compliance. Return only the category name."
  - [ ] 3.12 Create `backend/agents/billing_agent.py` with Hybrid RAG/CAG implementation
  - [ ] 3.13 Implement billing agent logic: check if cached_billing_info exists in state, if not perform RAG and cache results, if yes use CAG + RAG for specific queries
  - [ ] 3.14 Add billing agent prompt: "You are a billing support specialist. Answer questions about pricing, invoices, payment terms, and subscriptions using the provided context."
  - [ ] 3.15 Configure billing agent to use OpenAI GPT-4 for response generation
  - [ ] 3.16 Create `backend/agents/technical_agent.py` with Pure RAG implementation
  - [ ] 3.17 Implement technical agent to always query ChromaDB for latest technical documents (document_type="technical")
  - [ ] 3.18 Add technical agent prompt: "You are a technical support specialist. Provide troubleshooting steps and solutions based on our knowledge base. Be specific and actionable."
  - [ ] 3.19 Configure technical agent to use OpenAI GPT-4 for response generation
  - [ ] 3.20 Create `backend/agents/policy_agent.py` with Pure CAG implementation
  - [ ] 3.21 Load all policy documents into memory at initialization (read from data/policy/)
  - [ ] 3.22 Implement policy agent to use pre-loaded context without ChromaDB queries
  - [ ] 3.23 Add policy agent prompt: "You are a policy and compliance specialist. Answer questions about our Terms of Service, Privacy Policy, and compliance using the provided policy documents."
  - [ ] 3.24 Configure policy agent to use OpenAI GPT-4 for response generation
  - [ ] 3.25 Create LangGraph StateGraph in orchestrator.py connecting: START → orchestrator → [billing_agent | technical_agent | policy_agent] → END
  - [ ] 3.26 Add conditional edges from orchestrator based on routing decision
  - [ ] 3.27 Implement state management to maintain conversation history across nodes
  - [ ] 3.28 Test individual agent responses with sample queries in Python REPL

- [ ] **4.0 FastAPI Streaming API & Integration**
  - [ ] 4.1 Create `backend/main.py` with FastAPI app initialization
  - [ ] 4.2 Add CORS middleware configuration to allow frontend origin (localhost:3000)
  - [ ] 4.3 Import LangGraph orchestrator and agent modules
  - [ ] 4.4 Implement in-memory session store (dict) to maintain conversation state per session_id
  - [ ] 4.5 Create `/chat` POST endpoint with ChatRequest Pydantic model
  - [ ] 4.6 Generate session_id if not provided in request (use uuid)
  - [ ] 4.7 Retrieve or create session state from session store
  - [ ] 4.8 Add user message to conversation history in state
  - [ ] 4.9 Invoke LangGraph graph with current state and user message
  - [ ] 4.10 Implement Server-Sent Events (SSE) streaming using StreamingResponse from fastapi.responses
  - [ ] 4.11 Create async generator function to stream LLM tokens as they're generated
  - [ ] 4.12 Format SSE events with data: prefix and include agent type in metadata
  - [ ] 4.13 Send initial event with agent_type (billing, technical, or policy)
  - [ ] 4.14 Stream response tokens as individual SSE events
  - [ ] 4.15 Send final event with session_id and completion signal
  - [ ] 4.16 Update session state with complete response and save to session store
  - [ ] 4.17 Add error handling with try-except blocks around LLM calls
  - [ ] 4.18 Implement exponential backoff retry logic for rate limit errors (max 3 retries)
  - [ ] 4.19 Return user-friendly error messages without exposing internal errors
  - [ ] 4.20 Add health check endpoint GET `/health` that returns {status: "ok"}
  - [ ] 4.21 Add startup event to verify ChromaDB connection and LLM API credentials
  - [ ] 4.22 Test backend server: run `uvicorn backend.main:app --reload` and verify server starts on localhost:8000
  - [ ] 4.23 Test `/chat` endpoint with curl or Postman, verify streaming works and session maintained

- [ ] **5.0 Frontend Chat Interface Implementation**
  - [ ] 5.1 Install additional frontend dependencies if needed: `npm install` in frontend directory
  - [ ] 5.2 Update `frontend/src/app/layout.tsx` with proper metadata and font configuration
  - [ ] 5.3 Create `frontend/src/lib/api.ts` with API client functions
  - [ ] 5.4 Implement `sendMessage` function in api.ts that connects to backend /chat endpoint with SSE
  - [ ] 5.5 Add EventSource or fetch with streaming support to handle SSE responses
  - [ ] 5.6 Parse SSE events to extract agent_type, message tokens, and session_id
  - [ ] 5.7 Create `frontend/src/components/AgentBadge.tsx` component with props: agentType ("billing" | "technical" | "policy")
  - [ ] 5.8 Style AgentBadge with distinct colors/icons: 💰 Billing (blue), 🔧 Technical (orange), 📋 Policy (green)
  - [ ] 5.9 Create `frontend/src/components/Message.tsx` component with props: content, role ("user" | "assistant"), agentType (optional)
  - [ ] 5.10 Style Message component: user messages right-aligned (blue bg), assistant messages left-aligned (gray bg)
  - [ ] 5.11 Include AgentBadge in assistant messages to show which agent responded
  - [ ] 5.12 Create `frontend/src/components/LoadingIndicator.tsx` with typing animation (three dots bouncing)
  - [ ] 5.13 Create `frontend/src/components/ErrorMessage.tsx` with props: message, onRetry (optional callback)
  - [ ] 5.14 Style ErrorMessage with red background and clear error text
  - [ ] 5.15 Create `frontend/src/components/ChatInput.tsx` with textarea and send button
  - [ ] 5.16 Add state management in ChatInput: message text, disabled state
  - [ ] 5.17 Implement Enter key to submit (without Shift), clear input after send
  - [ ] 5.18 Disable input and button while waiting for response
  - [ ] 5.19 Create `frontend/src/components/MessageList.tsx` to display array of messages
  - [ ] 5.20 Implement auto-scroll to bottom when new messages added (useEffect with ref to scroll container)
  - [ ] 5.21 Create `frontend/src/components/ChatInterface.tsx` as main container component
  - [ ] 5.22 Add state management in ChatInterface: messages array, isLoading, error, sessionId, streamingMessage
  - [ ] 5.23 Generate sessionId on component mount (use crypto.randomUUID() or similar)
  - [ ] 5.24 Implement handleSendMessage function: add user message to array, call API, handle streaming response
  - [ ] 5.25 Update streamingMessage state token-by-token as SSE events arrive
  - [ ] 5.26 When stream completes, add complete assistant message to messages array and clear streamingMessage
  - [ ] 5.27 Handle errors from API and set error state with user-friendly message
  - [ ] 5.28 Implement retry functionality that resends the last message
  - [ ] 5.29 Update `frontend/src/app/page.tsx` to render ChatInterface component
  - [ ] 5.30 Style page.tsx with centered layout and appropriate padding
  - [ ] 5.31 Add header/title to page: "Advanced Customer Service AI"
  - [ ] 5.32 Test frontend: run `npm run dev` and verify UI loads on localhost:3000
  - [ ] 5.33 Test send message functionality with backend running, verify streaming works visually

- [ ] **6.0 End-to-End Testing & Validation**
  - [ ] 6.1 **Test 1: Orchestrator Routing - Billing** - Send query "What does the Enterprise plan cost?" and verify routed to Billing Agent with pricing info
  - [ ] 6.2 **Test 2: Orchestrator Routing - Technical** - Send query "My API integration keeps timing out, how do I fix this?" and verify routed to Technical Support Agent
  - [ ] 6.3 **Test 3: Orchestrator Routing - Policy** - Send query "Do you comply with GDPR?" and verify routed to Policy & Compliance Agent
  - [ ] 6.4 **Test 4: Hybrid RAG/CAG - Session Caching** - Send two billing queries in same session, verify second is faster (caching working)
  - [ ] 6.5 **Test 5: Pure RAG - Latest Information** - Send query "Are there any known issues with the mobile app?" and verify response references bug reports
  - [ ] 6.6 **Test 6: Pure CAG - No Retrieval** - Send query "What is your Privacy Policy?" and verify fast response (<2 sec) with policy content
  - [ ] 6.7 **Test 7: Context Maintenance** - Send follow-up query that references previous message, verify context maintained
  - [ ] 6.8 **Test 8: No Information Found** - Send irrelevant query like "What's the weather?" and verify graceful handling (no hallucination)
  - [ ] 6.9 **Test 9: API Streaming** - Verify response is streamed token-by-token, not returned as single block
  - [ ] 6.10 **Test 10: Multi-Provider LLM Usage** - Check logs to confirm orchestrator uses AWS Bedrock and agents use OpenAI
  - [ ] 6.11 **Test 11: Message Display** - Verify both user and assistant messages display correctly with proper alignment
  - [ ] 6.12 **Test 12: Agent Identification** - Send queries triggering all three agents and verify badges show correctly
  - [ ] 6.13 **Test 13: Real-Time Streaming Display** - Verify tokens appear smoothly in real-time on frontend
  - [ ] 6.14 **Test 14: Input State Management** - Verify input clears and disables after sending until response completes
  - [ ] 6.15 **Test 15: Auto-Scroll** - Send multiple messages and verify view scrolls to show latest automatically
  - [ ] 6.16 **Test 16: Error Display** - Stop backend server and send message, verify error message displays properly
  - [ ] 6.17 **Test 17: Session Persistence** - Send multiple messages and verify all remain in conversation history
  - [ ] 6.18 **Test 18: End-to-End Flow** - Run complete conversation with multiple agent switches, verify seamless experience
  - [ ] 6.19 **Test 19: Data Pipeline Validation** - Verify ChromaDB contains 26 documents with proper metadata and chunks
  - [ ] 6.20 **Test 20: Cold Start** - Restart backend and verify system loads ChromaDB from disk successfully
  - [ ] 6.21 Document any bugs or issues found during testing in a TESTING.md file
  - [ ] 6.22 Fix any critical bugs that prevent core functionality from working

- [ ] **7.0 Documentation & Demo Preparation**
  - [ ] 7.1 Create comprehensive `README.md` at project root with project title and overview
  - [ ] 7.2 Add "Features" section to README listing: multi-agent system, RAG/CAG/Hybrid retrieval, streaming responses, multi-provider LLMs
  - [ ] 7.3 Add "Architecture" section with high-level diagram or description of LangGraph orchestrator and three agents
  - [ ] 7.4 Add "Technology Stack" section listing all technologies used (Python, FastAPI, LangChain, LangGraph, ChromaDB, Next.js, OpenAI, AWS Bedrock)
  - [ ] 7.5 Add "Prerequisites" section: Python 3.10+, Node.js 18+, API keys for OpenAI and AWS Bedrock
  - [ ] 7.6 Add "Setup Instructions" section with step-by-step guide:
  - [ ] 7.7 Document: Clone repository command
  - [ ] 7.8 Document: Backend setup (create venv, install requirements, set up .env)
  - [ ] 7.9 Document: Run data ingestion script: `python backend/ingest_data.py`
  - [ ] 7.10 Document: Start backend server: `uvicorn backend.main:app --reload`
  - [ ] 7.11 Document: Frontend setup (npm install, set up .env.local)
  - [ ] 7.12 Document: Start frontend: `npm run dev`
  - [ ] 7.13 Document: Access application at http://localhost:3000
  - [ ] 7.14 Add "Environment Variables" section with .env.example reference and explanation of each variable
  - [ ] 7.15 Add "Usage" section with example queries for each agent type
  - [ ] 7.16 Add "Project Structure" section showing directory tree and key files
  - [ ] 7.17 Add "Retrieval Strategies" section explaining Pure RAG, Pure CAG, and Hybrid RAG/CAG implementations
  - [ ] 7.18 Add "Testing" section with instructions to run tests and validate functionality
  - [ ] 7.19 Add "Development Methodology" section noting Vibe Coding Strategy and BMAD-METHOD integration points
  - [ ] 7.20 Add "Demo Video" section with YouTube link (to be added after video creation)
  - [ ] 7.21 Add "License" and "Author" sections
  - [ ] 7.22 Review and polish README for clarity and completeness
  - [ ] 7.23 Prepare demo script covering: architecture overview, query routing demo for all 3 agents, code walkthrough of key components
  - [ ] 7.24 Record screen while demonstrating the application (5-10 minutes)
  - [ ] 7.25 Show: Sending billing query and showing Billing Agent response
  - [ ] 7.26 Show: Sending technical query and showing Technical Support Agent response
  - [ ] 7.27 Show: Sending policy query and showing Policy Agent response
  - [ ] 7.28 Show: Follow-up query demonstrating context maintenance
  - [ ] 7.29 Show code walkthrough: orchestrator.py (routing logic), billing_agent.py (Hybrid RAG/CAG), technical_agent.py (Pure RAG), policy_agent.py (Pure CAG)
  - [ ] 7.30 Show code walkthrough: main.py (FastAPI streaming), ChatInterface.tsx (frontend streaming)
  - [ ] 7.31 Edit video for clarity and proper length (5-10 minutes)
  - [ ] 7.32 Upload video to YouTube as unlisted
  - [ ] 7.33 Add YouTube link to README.md
  - [ ] 7.34 Create final Git commit with all completed work
  - [ ] 7.35 Push to GitHub public repository
  - [ ] 7.36 Verify repository is public and all files are accessible

---

## BMAD-METHOD Integration Checkpoints

As specified in the PRD (Section 7.7), document these checkpoints in code comments or commit messages:

1. **After Task 3.27** - Architecture Review: "BMAD Architect reviewed multi-agent flow: Orchestrator → [Billing | Technical | Policy] → Response"

2. **After Task 4.23** - Requirements Validation: "BMAD PM validation: Backend API meets REQ-BE-001 through REQ-BE-029"

3. **After Task 5.33** - Requirements Validation: "BMAD PM validation: Frontend meets REQ-FE-001 through REQ-FE-020"

4. **After Task 6.22** - Code Review: "BMAD Developer review: All components - code quality check passed"

---

**Status:** ✅ Complete task list generated with detailed sub-tasks and file mappings.

**Estimated Timeline:** 8-9 days (per PRD Section 11)

**Next Steps:** Begin with Task 1.0 (Project Foundation & Setup)

