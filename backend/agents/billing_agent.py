"""
Billing Support Agent - Hybrid RAG/CAG Implementation
Uses cached general billing info (CAG) + specific query RAG on subsequent requests
"""

from langchain_core.messages import HumanMessage, SystemMessage
from models.schemas import AgentState, Message
from utils.llm_config import get_response_llm
from utils.retrieval import get_billing_context


BILLING_AGENT_PROMPT = """You are a helpful billing support specialist. Answer briefly and directly.

CRITICAL: Keep your response under 100 words. Be extremely concise.

Context: {context}

Question: {question}

Instructions:
1. Answer the specific question only
2. Use bullet points (max 3-4 points)
3. Include only essential pricing/policy details
4. Maximum 100 words total

Your brief response:"""


def billing_agent_node(state: AgentState) -> AgentState:
    """
    Billing Support Agent node implementing Hybrid RAG/CAG strategy.
    
    Strategy:
    - First billing query in session: Perform RAG and cache general billing info
    - Subsequent queries: Use cached info (CAG) + RAG for specific details
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with generated response
    """
    try:
        print(f"💰 Billing Agent processing query...")
        
        # Get context using Hybrid RAG/CAG strategy
        context_result = get_billing_context(
            query=state.current_message,
            cached_info=state.cached_billing_info
        )
        
        context = context_result["context"]
        cache_update = context_result.get("cache_update")
        
        # Update cache if this is the first query
        if cache_update is not None:
            state.cached_billing_info = cache_update
            print(f"   ✓ Cached general billing information for future queries")
        else:
            print(f"   ✓ Using cached billing info + specific RAG retrieval")
        
        # Format prompt with context
        prompt = BILLING_AGENT_PROMPT.format(
            context=context,
            question=state.current_message
        )
        
        # Get response from OpenAI GPT-4 with strict token limit
        llm = get_response_llm()
        messages = [HumanMessage(content=prompt)]
        response = llm.invoke(messages, max_tokens=150)
        
        # Update state with response
        state.response = response.content
        
        # Add message to conversation history
        assistant_message = Message(
            role="assistant",
            content=response.content,
            agent_type="billing"
        )
        state.messages.append(assistant_message)
        
        print(f"   ✓ Generated response ({len(response.content)} chars)")
        
        return state
        
    except Exception as e:
        print(f"❌ Error in billing agent: {str(e)}")
        # Fallback response
        state.response = "I apologize, but I'm having trouble accessing billing information right now. Please try again or contact our support team for assistance."
        
        assistant_message = Message(
            role="assistant",
            content=state.response,
            agent_type="billing"
        )
        state.messages.append(assistant_message)
        
        return state

