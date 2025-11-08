"""
Policy & Compliance Agent - Pure CAG Implementation
Uses pre-loaded static policy documents without vector database queries
"""

from langchain_core.messages import HumanMessage, SystemMessage
from models.schemas import AgentState, Message
from utils.llm_config import get_response_llm
from utils.retrieval import get_policy_context


POLICY_AGENT_PROMPT = """You are a policy specialist. Provide brief, clear policy answers.

CRITICAL: Keep your response under 100 words. Be extremely concise.

Policy Documents: {context}

Question: {question}

Instructions:
1. Answer the specific policy question
2. Use bullet points (max 3-4 points)
3. Cite key policy terms briefly
4. Maximum 100 words total

Your brief policy response:"""


def policy_agent_node(state: AgentState) -> AgentState:
    """
    Policy & Compliance Agent node implementing Pure CAG strategy.
    
    Strategy:
    - Uses pre-loaded static policy documents from memory
    - No vector database queries - fastest response time
    - Ensures consistent policy information
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with generated response
    """
    try:
        print(f"📋 Policy Agent processing query...")
        
        # Get relevant policy context (Pure CAG with smart selection)
        context = get_policy_context(query=state.current_message)
        
        # Note: Smart selection message is printed by get_policy_context()
        
        # Format prompt with context
        prompt = POLICY_AGENT_PROMPT.format(
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
            agent_type="policy"
        )
        state.messages.append(assistant_message)
        
        print(f"   ✓ Generated policy response ({len(response.content)} chars)")
        
        return state
        
    except Exception as e:
        print(f"❌ Error in policy agent: {str(e)}")
        # Fallback response
        state.response = "I apologize, but I'm having trouble accessing policy documents right now. You can find our complete policies at [website]/legal or contact our compliance team for assistance."
        
        assistant_message = Message(
            role="assistant",
            content=state.response,
            agent_type="policy"
        )
        state.messages.append(assistant_message)
        
        return state

