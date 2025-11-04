"""
Policy & Compliance Agent - Pure CAG Implementation
Uses pre-loaded static policy documents without vector database queries
"""

from langchain_core.messages import HumanMessage, SystemMessage
from models.schemas import AgentState, Message
from utils.llm_config import get_response_llm
from utils.retrieval import get_policy_context


POLICY_AGENT_PROMPT = """You are a policy and compliance specialist for our customer service platform.
Your role is to answer questions about our Terms of Service, Privacy Policy, GDPR compliance, 
Cookie Policy, and Acceptable Use Policy.

Use the provided policy documents to answer the user's question accurately and clearly.
These are our official policies, so cite specific sections when relevant.

Key Guidelines:
- Be precise and quote specific policy language when needed
- For GDPR questions, reference specific articles and rights
- Explain legal/compliance terms in plain language
- If a policy doesn't cover the user's specific scenario, acknowledge that
- For complex legal matters, suggest contacting legal/compliance team
- Be reassuring about data protection and user rights

Policy Documents:
{context}

User Question: {question}

Provide a clear, compliant response:"""


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
        
        # Get pre-loaded policy context (Pure CAG - no database query)
        context = get_policy_context()
        
        print(f"   ✓ Using pre-loaded policy documents (Pure CAG)")
        
        # Format prompt with context
        prompt = POLICY_AGENT_PROMPT.format(
            context=context,
            question=state.current_message
        )
        
        # Get response from OpenAI GPT-4
        llm = get_response_llm()
        messages = [HumanMessage(content=prompt)]
        response = llm.invoke(messages)
        
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

