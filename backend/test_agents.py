"""
Test script for multi-agent system
Validates orchestrator routing and agent responses
"""

import uuid
from models.schemas import AgentState, Message
from agents.orchestrator import create_agent_graph


def test_agent_system():
    """Test the multi-agent system with sample queries."""
    
    print("\n" + "="*70)
    print("🧪 Testing Multi-Agent System")
    print("="*70)
    
    # Create the agent graph
    print("\n📊 Creating LangGraph workflow...")
    graph = create_agent_graph()
    
    # Test queries for each agent type
    test_queries = [
        {
            "message": "What are your pricing plans?",
            "expected_agent": "billing",
            "description": "Billing query - pricing"
        },
        {
            "message": "How do I troubleshoot login issues?",
            "expected_agent": "technical",
            "description": "Technical query - login issues"
        },
        {
            "message": "What is your privacy policy regarding my data?",
            "expected_agent": "policy",
            "description": "Policy query - privacy"
        },
        {
            "message": "Can I get a refund?",
            "expected_agent": "billing",
            "description": "Billing query - refund"
        }
    ]
    
    # Test each query
    for i, test in enumerate(test_queries, 1):
        print(f"\n{'─'*70}")
        print(f"Test {i}: {test['description']}")
        print(f"{'─'*70}")
        print(f"Query: \"{test['message']}\"")
        print(f"Expected Agent: {test['expected_agent'].upper()}")
        
        try:
            # Create initial state
            session_id = str(uuid.uuid4())
            initial_state = AgentState(
                messages=[],
                current_message=test['message'],
                session_id=session_id
            )
            
            # Add user message to history
            user_message = Message(
                role="user",
                content=test['message']
            )
            initial_state.messages.append(user_message)
            
            # Run the graph
            print(f"\n🚀 Executing workflow...")
            result = graph.invoke(initial_state)
            
            # Check results (LangGraph returns dict)
            actual_agent = result.get("current_agent")
            response = result.get("response")
            cached_info = result.get("cached_billing_info")
            
            print(f"\n📊 Results:")
            print(f"   Routed to: {actual_agent.upper() if actual_agent else 'UNKNOWN'} agent")
            print(f"   Match: {'✅ PASS' if actual_agent == test['expected_agent'] else '❌ FAIL'}")
            print(f"   Response length: {len(response) if response else 0} characters")
            if response:
                print(f"\n   Response preview:")
                print(f"   {response[:200]}...")
            
            # Check if cache was updated (for billing)
            if actual_agent == "billing" and cached_info:
                print(f"\n   💾 Billing cache initialized: {len(cached_info)} chars")
            
        except Exception as e:
            print(f"\n❌ Test failed with error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*70}")
    print("✅ Multi-Agent System Tests Complete")
    print("="*70)
    
    # Test conversation continuity (second billing query to test cache)
    print(f"\n{'='*70}")
    print("🧪 Testing Hybrid RAG/CAG Cache (Billing Agent)")
    print("="*70)
    
    try:
        session_id = str(uuid.uuid4())
        
        # First query
        print(f"\n📝 First billing query (should create cache)...")
        state1 = AgentState(
            messages=[],
            current_message="What payment methods do you accept?",
            session_id=session_id
        )
        result1 = graph.invoke(state1)
        cache_created = result1.get("cached_billing_info") is not None
        print(f"   Cache created: {'✅ YES' if cache_created else '❌ NO'}")
        
        # Second query with cache
        if cache_created:
            print(f"\n📝 Second billing query (should use cache)...")
            state2 = AgentState(
                messages=result1.get("messages", []),
                current_message="How much does the Enterprise plan cost?",
                session_id=session_id,
                cached_billing_info=result1.get("cached_billing_info")
            )
            result2 = graph.invoke(state2)
            cache_used = result2.get("cached_billing_info") == result1.get("cached_billing_info")
            print(f"   Cache used (unchanged): {'✅ YES' if cache_used else '❌ NO'}")
            print(f"   Response generated: {'✅ YES' if result2.get('response') else '❌ NO'}")
    
    except Exception as e:
        print(f"\n❌ Cache test failed: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n✨ All tests completed!\n")


if __name__ == "__main__":
    test_agent_system()

