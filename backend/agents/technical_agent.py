"""
Technical Support Agent - Pure RAG Implementation
Always queries vector database for the most current technical information
"""

from langchain_core.messages import HumanMessage, SystemMessage
from models.schemas import AgentState, Message
from utils.llm_config import get_response_llm
from utils.retrieval import get_technical_context


TECHNICAL_AGENT_PROMPT = """You are an expert technical support specialist for our customer service platform.
Your role is to help users troubleshoot technical issues, resolve errors, and guide them through technical processes.

Use the provided context from our technical knowledge base to answer the user's question accurately.
This includes troubleshooting guides, bug reports, how-to documentation, and community forum discussions.

Key Guidelines:
- Provide clear, step-by-step solutions when appropriate
- Reference specific error messages or symptoms mentioned
- Mention if an issue is a known bug and its resolution status
- For API or integration issues, cite specific endpoints or parameters
- If troubleshooting requires account-specific information, guide them to support
- Be technical but accessible - explain technical terms when needed

Context from Technical Knowledge Base:
{context}

User Question: {question}

Provide a detailed, actionable response:"""


def technical_agent_node(state: AgentState) -> AgentState:
    """
    Technical Support Agent node implementing Pure RAG strategy.
    
    Strategy:
    - Always queries the vector database for latest technical information
    - No caching - ensures users get most current bug fixes and updates
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with generated response
    """
    try:
        print(f"🔧 Technical Agent processing query...")
        
        # Get context using Pure RAG (always query database)
        context = get_technical_context(query=state.current_message)
        
        print(f"   ✓ Retrieved latest technical documentation")
        
        # Format prompt with context
        prompt = TECHNICAL_AGENT_PROMPT.format(
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
            agent_type="technical"
        )
        state.messages.append(assistant_message)
        
        print(f"   ✓ Generated technical response ({len(response.content)} chars)")
        
        return state
        
    except Exception as e:
        print(f"❌ Error in technical agent: {str(e)}")
        # Fallback response
        state.response = "I apologize, but I'm having trouble accessing technical documentation right now. Please try again or contact our technical support team for immediate assistance."
        
        assistant_message = Message(
            role="assistant",
            content=state.response,
            agent_type="technical"
        )
        state.messages.append(assistant_message)
        
        return state

