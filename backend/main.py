"""
FastAPI Backend for Advanced Customer Service AI
Implements streaming SSE endpoint with multi-agent LangGraph orchestration
"""

import os
import uuid
import json
import time
import asyncio
from typing import Dict, Optional, AsyncIterator
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from dotenv import load_dotenv

from models.schemas import ChatRequest, AgentState, Message
from agents.orchestrator import create_agent_graph
from utils.retrieval import verify_chromadb_connection

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Advanced Customer Service AI",
    description="Multi-agent customer service system with RAG/CAG strategies",
    version="1.0.0"
)

# CORS Configuration - Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development server
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store
# Format: {session_id: AgentState}
SESSION_STORE: Dict[str, AgentState] = {}

# Global LangGraph instance
agent_graph = None


@app.on_event("startup")
async def startup_event():
    """
    Startup validation: verify ChromaDB connection and LLM credentials.
    """
    print("\n" + "="*60)
    print("🚀 Starting Advanced Customer Service AI Backend")
    print("="*60)
    
    # Verify environment variables
    required_env_vars = ["OPENAI_API_KEY"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️  Warning: Missing environment variables: {', '.join(missing_vars)}")
    else:
        print("✅ Environment variables loaded")
    
    # Verify ChromaDB connection
    try:
        verify_chromadb_connection()
        print("✅ ChromaDB connection verified")
    except Exception as e:
        print(f"⚠️  ChromaDB connection warning: {str(e)}")
    
    # Initialize LangGraph
    global agent_graph
    try:
        agent_graph = create_agent_graph()
        print("✅ LangGraph multi-agent system initialized")
    except Exception as e:
        print(f"❌ Failed to initialize LangGraph: {str(e)}")
        raise
    
    print("="*60)
    print("✅ Backend is ready to accept requests")
    print("   API Docs: http://localhost:8000/docs")
    print("   Health Check: http://localhost:8000/health")
    print("="*60 + "\n")


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify server is running.
    """
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "Advanced Customer Service AI",
        "agents": ["billing", "technical", "policy"],
        "sessions_active": len(SESSION_STORE)
    }


def get_or_create_session(session_id: Optional[str] = None) -> tuple[str, AgentState]:
    """
    Retrieve existing session or create a new one.
    
    Args:
        session_id: Optional session ID. If None, creates new session.
        
    Returns:
        Tuple of (session_id, agent_state)
    """
    if session_id and session_id in SESSION_STORE:
        return session_id, SESSION_STORE[session_id]
    
    # Create new session
    new_session_id = session_id or str(uuid.uuid4())
    new_state = AgentState(
        session_id=new_session_id,
        messages=[],
        metadata={"created_at": datetime.now().isoformat()}
    )
    SESSION_STORE[new_session_id] = new_state
    
    print(f"📝 Created new session: {new_session_id}")
    return new_session_id, new_state


async def stream_response_tokens(text: str, delay: float = 0.02) -> AsyncIterator[str]:
    """
    Stream text token-by-token to simulate real-time generation.
    
    Args:
        text: Complete text to stream
        delay: Delay between tokens in seconds
        
    Yields:
        Individual words/tokens
    """
    # Split into words for more natural streaming
    words = text.split()
    
    for i, word in enumerate(words):
        # Add space before word (except first word)
        if i > 0:
            yield " " + word
        else:
            yield word
        
        # Small delay to simulate streaming
        await asyncio.sleep(delay)


async def generate_sse_stream(
    session_id: str,
    state: AgentState,
    user_message: str
) -> AsyncIterator[str]:
    """
    Generate Server-Sent Events stream for chat response.
    
    Args:
        session_id: Session identifier
        state: Current agent state
        user_message: User's message
        
    Yields:
        SSE-formatted event strings
    """
    try:
        # Add user message to state
        user_msg = Message(role="user", content=user_message)
        state.messages.append(user_msg)
        state.current_message = user_message
        
        # Send initial event with metadata
        initial_event = {
            "type": "start",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
        yield f"data: {json.dumps(initial_event)}\n\n"
        
        # Invoke LangGraph with retry logic
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                # Invoke the agent graph (returns dict)
                result = agent_graph.invoke(state)
                
                # Extract response and agent type from dict
                response_text = result.get("response")
                agent_type = result.get("current_agent")
                
                # Update state with result
                state.response = response_text
                state.current_agent = agent_type
                state.cached_billing_info = result.get("cached_billing_info")
                
                # Send agent type event
                agent_event = {
                    "type": "agent",
                    "agent_type": agent_type
                }
                yield f"data: {json.dumps(agent_event)}\n\n"
                
                # Stream response tokens
                async for token in stream_response_tokens(response_text, delay=0.02):
                    token_event = {
                        "type": "token",
                        "content": token
                    }
                    yield f"data: {json.dumps(token_event)}\n\n"
                
                # Send completion event
                complete_event = {
                    "type": "complete",
                    "session_id": session_id,
                    "agent_type": agent_type,
                    "timestamp": datetime.now().isoformat()
                }
                yield f"data: {json.dumps(complete_event)}\n\n"
                
                # Update session store
                SESSION_STORE[session_id] = state
                
                # Success - break retry loop
                break
                
            except Exception as e:
                if "rate_limit" in str(e).lower() and attempt < max_retries - 1:
                    # Rate limit error - retry with exponential backoff
                    print(f"⚠️  Rate limit hit, retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    # Other error or max retries reached
                    raise
        
    except Exception as e:
        # Send error event
        print(f"❌ Error processing request: {str(e)}")
        error_event = {
            "type": "error",
            "message": "I apologize, but I'm having trouble processing your request. Please try again.",
            "timestamp": datetime.now().isoformat()
        }
        yield f"data: {json.dumps(error_event)}\n\n"


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint with Server-Sent Events streaming.
    
    Accepts user message and returns streaming response from appropriate agent.
    
    Args:
        request: ChatRequest with message and optional session_id
        
    Returns:
        StreamingResponse with SSE events
    """
    try:
        # Validate input
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Get or create session
        session_id, state = get_or_create_session(request.session_id)
        
        print(f"\n💬 New message in session {session_id[:8]}...")
        print(f"   User: {request.message[:100]}{'...' if len(request.message) > 100 else ''}")
        
        # Create SSE stream
        return StreamingResponse(
            generate_sse_stream(session_id, state, request.message),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Disable proxy buffering
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred processing your request. Please try again."
        )


@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """
    Retrieve session information (for debugging/monitoring).
    
    Args:
        session_id: Session identifier
        
    Returns:
        Session state information
    """
    if session_id not in SESSION_STORE:
        raise HTTPException(status_code=404, detail="Session not found")
    
    state = SESSION_STORE[session_id]
    
    return {
        "session_id": session_id,
        "message_count": len(state.messages),
        "current_agent": state.current_agent,
        "has_cached_billing": state.cached_billing_info is not None,
        "metadata": state.metadata
    }


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session (cleanup).
    
    Args:
        session_id: Session identifier
        
    Returns:
        Success message
    """
    if session_id in SESSION_STORE:
        del SESSION_STORE[session_id]
        return {"message": "Session deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Advanced Customer Service AI",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "chat": "/chat (POST)",
            "health": "/health (GET)",
            "sessions": "/sessions/{session_id} (GET)",
            "docs": "/docs (GET)"
        },
        "agents": [
            {"name": "billing", "type": "Hybrid RAG/CAG"},
            {"name": "technical", "type": "Pure RAG"},
            {"name": "policy", "type": "Pure CAG"}
        ]
    }


# BMAD-METHOD Integration Point: Requirements Validation
# "BMAD PM validation: Backend API meets REQ-BE-001 through REQ-BE-029"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

