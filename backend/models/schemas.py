"""
Pydantic models for request/response validation and state management
"""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime


# API Request/Response Models

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User message content")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    message: str = Field(..., description="AI assistant response")
    agent_type: str = Field(..., description="Type of agent that handled the query (billing, technical, policy)")
    session_id: str = Field(..., description="Session ID for tracking conversation")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


# LangGraph State Models

class Message(BaseModel):
    """Individual message in conversation."""
    role: Literal["user", "assistant", "system"] = Field(..., description="Message role")
    content: str = Field(..., description="Message content")
    agent_type: Optional[str] = Field(None, description="Agent that generated the message (for assistant role)")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")


class AgentState(BaseModel):
    """
    State management for LangGraph multi-agent workflow.
    Maintains conversation history, routing decisions, and session context.
    """
    # Conversation messages
    messages: List[Message] = Field(default_factory=list, description="Complete conversation history")
    
    # Current processing state
    current_message: Optional[str] = Field(None, description="Current user message being processed")
    current_agent: Optional[Literal["billing", "technical", "policy"]] = Field(
        None, 
        description="Agent selected to handle current query"
    )
    
    # Generated response
    response: Optional[str] = Field(None, description="Generated response from agent")
    
    # Session context
    session_id: str = Field(..., description="Unique session identifier")
    
    # Billing agent cache (Hybrid RAG/CAG)
    cached_billing_info: Optional[str] = Field(
        None, 
        description="Cached billing information for Hybrid RAG/CAG strategy"
    )
    
    # Additional context
    metadata: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Additional metadata (timestamps, retrieval info, etc.)"
    )
    
    class Config:
        arbitrary_types_allowed = True


class RoutingDecision(BaseModel):
    """Model for orchestrator routing decision."""
    agent: Literal["billing", "technical", "policy"] = Field(..., description="Selected agent")
    confidence: Optional[float] = Field(None, description="Confidence score (0-1)")
    reasoning: Optional[str] = Field(None, description="Explanation of routing decision")


class AgentResponse(BaseModel):
    """Model for agent response."""
    content: str = Field(..., description="Response content")
    agent_type: str = Field(..., description="Type of agent (billing, technical, policy)")
    sources: Optional[List[str]] = Field(None, description="Source documents used")
    cache_update: Optional[str] = Field(None, description="Updated cache for Hybrid RAG/CAG")


# Utility models

class StreamChunk(BaseModel):
    """Model for streaming response chunks."""
    content: str = Field(..., description="Chunk content")
    is_complete: bool = Field(False, description="Whether this is the final chunk")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

