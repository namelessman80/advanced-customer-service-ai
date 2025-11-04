# Demo Video Script - Advanced Customer Service AI

**Target Duration**: 5-10 minutes  
**Format**: Screen recording with voice-over  
**Audience**: Technical evaluators, potential users, stakeholders

---

## Pre-Recording Checklist

- [ ] Backend server running (`uvicorn main:app --reload`)
- [ ] Frontend server running (`npm run dev`)
- [ ] Browser open to `http://localhost:3000`
- [ ] Terminal windows arranged for showing logs
- [ ] Code editor open with key files
- [ ] Audio recording setup tested
- [ ] Screen recording software ready (OBS, QuickTime, etc.)

---

## Demo Structure

### Part 1: Introduction & System Overview (1-2 minutes)

**Talking Points:**
> "Welcome! Today I'm demonstrating an Advanced Customer Service AI system that uses multiple specialized agents to handle different types of customer queries."

**Show:**
1. **Welcome Screen** (http://localhost:3000)
   - Point out the clean UI
   - Highlight the three agent cards (Billing, Technical, Policy)
   - Explain the concept: "Instead of one generic AI, we have three specialists"

2. **Architecture Diagram** (show README.md section)
   - Explain the flow: User → Orchestrator → Specialized Agent → Response
   - Mention key technologies: LangGraph, OpenAI GPT-4, ChromaDB

**Script:**
> "The system uses LangGraph for multi-agent orchestration. When a user sends a query, an orchestrator analyzes it and routes it to the most appropriate specialist. We have three agents: Billing for pricing questions, Technical Support for API issues, and Policy for compliance questions."

---

### Part 2: Multi-Agent Routing Demo (3-4 minutes)

**Talking Points:**
> "Let's see the intelligent routing in action. I'll send three different types of queries and watch them get routed to the correct agent."

#### Demo 2.1: Billing Agent (💰 Hybrid RAG/CAG)

**Action:**
1. Type in chat: `"What does the Enterprise plan cost?"`
2. Click Send
3. Show real-time streaming

**Show:**
- Real-time token streaming
- 💰 Billing badge appears
- Response mentions pricing details

**Script:**
> "Notice how the system automatically identified this as a billing question and routed it to the Billing Agent, indicated by the blue dollar sign badge. The response streams in real-time, creating a natural conversation feel. The Billing Agent uses a Hybrid RAG/CAG strategy - it caches general billing information for faster responses while still querying specific details from the database."

#### Demo 2.2: Technical Support Agent (🔧 Pure RAG)

**Action:**
1. Type: `"My API integration keeps timing out. How do I fix this?"`
2. Click Send
3. Show response with technical details

**Show:**
- Real-time streaming
- 🔧 Technical Support badge (orange)
- Technical troubleshooting steps in response

**Script:**
> "This query is clearly technical, so it's routed to the Technical Support Agent, shown by the orange wrench badge. This agent uses Pure RAG - Retrieval-Augmented Generation - meaning it always queries our vector database for the latest documentation. This ensures users always get the most up-to-date troubleshooting information."

#### Demo 2.3: Policy & Compliance Agent (📋 Pure CAG)

**Action:**
1. Type: `"Do you comply with GDPR?"`
2. Click Send
3. Show policy response

**Show:**
- Real-time streaming
- 📋 Policy badge (green)
- Detailed GDPR compliance information

**Script:**
> "Policy questions are routed to the Policy & Compliance Agent, marked with the green clipboard badge. This agent uses Pure CAG - Context-Augmented Generation - meaning it works with pre-loaded policy documents rather than querying a database. This is perfect for static content like policies that rarely change, providing fast, consistent responses."

---

### Part 3: Advanced Features (2-3 minutes)

#### Demo 3.1: Session Context & Follow-up

**Action:**
1. Type: `"What are your pricing plans?"`
2. Wait for response
3. **Point out session ID in header**
4. Type follow-up: `"Can I upgrade from Basic to Premium?"`
5. Show contextual response

**Show:**
- Session ID maintained
- Follow-up understands context

**Script:**
> "The system maintains conversation context through sessions. See the session ID in the header? When I ask a follow-up question, the agent understands the context from our previous conversation about pricing plans. This creates a natural, multi-turn conversation experience."

#### Demo 3.2: Caching Performance

**Action:**
1. Refresh page (new session)
2. Type: `"Tell me about payment methods"`
3. Note response time
4. In same session, type: `"What about annual billing?"`
5. Note faster response

**Show:**
- Backend terminal showing cache messages
- Faster second response

**Script:**
> "Let me demonstrate the caching benefit. The first billing query takes about 13 seconds as it queries the database and creates a cache. But watch what happens with the second query in the same session - it's about 40% faster because it's using the cached information combined with specific retrieval. This Hybrid strategy balances performance with accuracy."

---

### Part 4: Code Walkthrough (2-3 minutes)

**Talking Points:**
> "Now let's look at how this works under the hood. I'll walk through the key components."

#### Show 4.1: Orchestrator Logic

**Show File:** `backend/agents/orchestrator.py`

**Highlight:**
```python
def route_query(state: AgentState) -> AgentState:
    """Routes query to appropriate agent using AWS Bedrock/OpenAI"""
    # Show routing logic
    llm = get_orchestrator_llm()
    response = llm.invoke(routing_prompt)
    agent_selection = response.content.strip().lower()
```

**Script:**
> "This is the orchestrator - the brain of our routing system. It uses an LLM with temperature set to 0 for deterministic classification. It analyzes the user's query and determines which specialized agent should handle it."

#### Show 4.2: Billing Agent (Hybrid RAG/CAG)

**Show File:** `backend/agents/billing_agent.py`

**Highlight:**
```python
def billing_agent_node(state: AgentState) -> AgentState:
    """Hybrid RAG/CAG strategy"""
    context_result = get_billing_context(
        query=state.current_message,
        cached_info=state.cached_billing_info  # Uses cache!
    )
```

**Script:**
> "The Billing Agent implements our Hybrid strategy. On the first query, it performs RAG and caches general billing information. On subsequent queries, it uses that cache plus specific RAG for the current question. This is why we see that 40% performance improvement."

#### Show 4.3: Streaming API

**Show File:** `backend/main.py`

**Highlight:**
```python
async def generate_sse_stream(...):
    """Generate Server-Sent Events stream"""
    # Show token streaming logic
    async for token in stream_response_tokens(response_text):
        yield f"data: {json.dumps(token_event)}\n\n"
```

**Script:**
> "The streaming is powered by Server-Sent Events. As the LLM generates tokens, we immediately send them to the client. This creates that real-time typing effect you saw in the UI."

#### Show 4.4: Frontend API Client

**Show File:** `frontend/lib/api.ts`

**Highlight:**
```typescript
export async function sendMessage(message, sessionId, callbacks) {
  // SSE stream reading logic
  const reader = response.body.getReader();
  // Process tokens as they arrive
}
```

**Script:**
> "On the frontend, we use the ReadableStream API to process SSE events as they arrive. Each token triggers a callback that updates the UI in real-time."

---

### Part 5: Testing & Quality (1 minute)

**Show:** Run automated tests

**Action:**
```bash
cd backend
python e2e_tests.py
```

**Show:**
- All 11 tests passing (green checkmarks)
- 100% success rate
- Performance metrics

**Script:**
> "Quality is crucial. I've implemented comprehensive end-to-end testing with 11 automated tests covering routing, retrieval strategies, streaming, context maintenance, and error handling. As you can see, all tests pass with a 100% success rate."

**Show:** `TESTING_RESULTS.md` briefly

---

### Part 6: Closing & Next Steps (30 seconds)

**Talking Points:**
> "In summary, we've built a production-ready, multi-agent customer service AI that intelligently routes queries, implements multiple retrieval strategies for optimal performance, and provides a smooth real-time user experience."

**Show:**
- README.md sections (Features, Architecture)
- GitHub repository (if published)

**Script:**
> "All code, documentation, and test results are available in the repository. The system is fully tested, documented, and ready for deployment. Thank you for watching!"

---

## Recording Tips

### Technical Setup
- **Resolution**: 1920x1080 minimum
- **Frame Rate**: 30 FPS
- **Audio**: Clear, no background noise
- **Cursor**: Enlarged for visibility

### Best Practices
1. **Speak clearly and at moderate pace**
2. **Pause between sections** (easier to edit)
3. **Point out key UI elements** with cursor
4. **Show, don't just tell** - demonstrate features
5. **Keep terminal output visible** when relevant
6. **Zoom in on code** when explaining specific lines

### Common Mistakes to Avoid
- ❌ Speaking too fast
- ❌ Not highlighting what you're talking about
- ❌ Skipping over errors without explanation
- ❌ Code font too small to read
- ❌ Background noise or interruptions

---

## Post-Recording

### Editing Checklist
- [ ] Cut out long pauses or mistakes
- [ ] Add title screen (0-3 seconds)
- [ ] Add chapter markers in YouTube
- [ ] Add background music (subtle, if desired)
- [ ] Add text overlays for key points
- [ ] Export in 1080p

### YouTube Upload
- [ ] Title: "Advanced Customer Service AI - Multi-Agent System with LangGraph"
- [ ] Description: Include GitHub link, tech stack, key features
- [ ] Tags: LangGraph, LangChain, Multi-agent AI, RAG, CAG, FastAPI, Next.js
- [ ] Thumbnail: Eye-catching with system architecture diagram
- [ ] Chapters: Add timestamps for each section

### YouTube Description Template

```
Advanced Customer Service AI - Multi-Agent System Demo

This video demonstrates a production-ready AI customer service system featuring:
✅ Multi-agent orchestration with LangGraph
✅ Three specialized agents (Billing, Technical, Policy)
✅ Multiple retrieval strategies (RAG, CAG, Hybrid)
✅ Real-time SSE streaming
✅ 100% test coverage

🔗 GitHub Repository: [Your GitHub Link]
📚 Documentation: [Link to README]
🧪 Test Results: [Link to TESTING_RESULTS.md]

Tech Stack:
- Backend: FastAPI, LangGraph, LangChain, ChromaDB
- LLMs: OpenAI GPT-4, AWS Bedrock Claude
- Frontend: Next.js 16, React 19, TypeScript
- Vector DB: ChromaDB

Timestamps:
0:00 - Introduction
1:00 - Multi-Agent Routing Demo
4:00 - Advanced Features
6:00 - Code Walkthrough
8:00 - Testing & Quality
9:00 - Conclusion

#LangGraph #MultiAgent #AI #CustomerService #RAG
```

---

## Alternative: Screenshot-Based Demo

If video recording isn't possible, create a screenshot-based demo:

1. **Capture key moments** as screenshots
2. **Add annotations** with arrows and text
3. **Create a slide deck** in PowerPoint/Google Slides
4. **Export as PDF** or upload to SlideShare

---

**Good luck with your demo! 🎥**


