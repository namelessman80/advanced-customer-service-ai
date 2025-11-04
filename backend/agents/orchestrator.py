"""
LangGraph Orchestrator Agent
Routes user queries to specialized worker agents using AWS Bedrock
"""

from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from models.schemas import AgentState, Message
from utils.llm_config import get_orchestrator_llm
from agents.billing_agent import billing_agent_node
from agents.technical_agent import technical_agent_node
from agents.policy_agent import policy_agent_node


# Orchestrator routing prompt
ROUTING_PROMPT = """You are a customer service query router. Analyze the user's message and classify it into ONE of these categories:

1. BILLING - Questions about:
   - Pricing plans and costs
   - Invoices and charges  
   - Payment terms and methods
   - Refunds and cancellations
   - Subscription upgrades or downgrades

2. TECHNICAL - Questions about:
   - Login or access issues
   - Performance or speed problems
   - API integration errors
   - Mobile app problems
   - Bug reports or technical troubleshooting
   - How-to guides for technical features

3. POLICY - Questions about:
   - Terms of Service
   - Privacy Policy
   - Data protection and GDPR
   - Cookie policies
   - Acceptable use policies
   - Legal compliance

Respond with ONLY ONE WORD: billing, technical, or policy

User message: {message}

Category:"""


def route_query(state: AgentState) -> AgentState:
    """
    Orchestrator node: Routes query to appropriate agent using AWS Bedrock.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state with selected agent
    """
    try:
        # Get the orchestrator LLM (AWS Bedrock)
        llm = get_orchestrator_llm()
        
        # Format routing prompt
        prompt = ROUTING_PROMPT.format(message=state.current_message)
        
        # Get routing decision
        messages = [HumanMessage(content=prompt)]
        response = llm.invoke(messages)
        
        # Extract agent selection
        agent_selection = response.content.strip().lower()
        
        # Validate and set agent
        valid_agents = ["billing", "technical", "policy"]
        if agent_selection not in valid_agents:
            # Default to technical if unclear
            print(f"⚠️  Unclear routing decision: '{agent_selection}', defaulting to technical")
            agent_selection = "technical"
        
        # Update state
        state.current_agent = agent_selection
        print(f"🎯 Orchestrator routed query to: {agent_selection.upper()} agent")
        
        return state
        
    except Exception as e:
        print(f"❌ Error in orchestrator routing: {str(e)}")
        # Default to technical agent on error
        state.current_agent = "technical"
        return state


def route_to_agent(state: AgentState) -> Literal["billing_agent", "technical_agent", "policy_agent"]:
    """
    Conditional routing function for LangGraph.
    Determines which agent node to execute next based on orchestrator decision.
    
    Args:
        state: Current agent state
        
    Returns:
        Name of the next node to execute
    """
    agent_map = {
        "billing": "billing_agent",
        "technical": "technical_agent",
        "policy": "policy_agent"
    }
    
    next_node = agent_map.get(state.current_agent, "technical_agent")
    return next_node


def create_agent_graph() -> StateGraph:
    """
    Create the LangGraph StateGraph for multi-agent workflow.
    
    Flow: START → orchestrator → [billing_agent | technical_agent | policy_agent] → END
    
    Returns:
        Compiled StateGraph
    """
    # Create graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("orchestrator", route_query)
    workflow.add_node("billing_agent", billing_agent_node)
    workflow.add_node("technical_agent", technical_agent_node)
    workflow.add_node("policy_agent", policy_agent_node)
    
    # Set entry point
    workflow.set_entry_point("orchestrator")
    
    # Add conditional routing from orchestrator to agents
    workflow.add_conditional_edges(
        "orchestrator",
        route_to_agent,
        {
            "billing_agent": "billing_agent",
            "technical_agent": "technical_agent",
            "policy_agent": "policy_agent"
        }
    )
    
    # All agents route to END
    workflow.add_edge("billing_agent", END)
    workflow.add_edge("technical_agent", END)
    workflow.add_edge("policy_agent", END)
    
    # Compile graph
    graph = workflow.compile()
    
    print("✅ LangGraph multi-agent workflow created successfully")
    print("   Flow: START → orchestrator → [billing | technical | policy] → END")
    
    return graph


# BMAD-METHOD Integration Point: Architecture Review
# "BMAD Architect reviewed multi-agent flow: Orchestrator → [Billing | Technical | Policy] → Response"

