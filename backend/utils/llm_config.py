"""
LLM Configuration for Multi-Provider Setup
OpenAI for response generation, AWS Bedrock for routing
"""

import os
from typing import Optional, Union
from langchain_openai import ChatOpenAI
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()


def get_openai_llm(
    model: str = "gpt-4-turbo-preview",
    temperature: float = 0.7,
    streaming: bool = True
) -> ChatOpenAI:
    """
    Get OpenAI LLM for response generation.
    
    Args:
        model: OpenAI model name (default: gpt-4-turbo-preview)
        temperature: Sampling temperature (0.7 for natural responses)
        streaming: Enable streaming responses
        
    Returns:
        Configured ChatOpenAI instance
    """
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        streaming=streaming,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )


def get_bedrock_llm(
    model: str = "anthropic.claude-3-haiku-20240307-v1:0",
    temperature: float = 0.0,
    max_tokens: int = 1000
) -> ChatBedrock:
    """
    Get AWS Bedrock LLM for routing/classification.
    
    Args:
        model: Bedrock model ID (default: Claude 3 Haiku)
                Options:
                - anthropic.claude-3-haiku-20240307-v1:0 (Claude 3 Haiku)
                - amazon.nova-lite-v1:0 (Nova Lite)
                - amazon.nova-micro-v1:0 (Nova Micro)
        temperature: Sampling temperature (0.0 for deterministic routing)
        max_tokens: Maximum tokens in response
        
    Returns:
        Configured ChatBedrock instance
    """
    return ChatBedrock(
        model_id=model,
        model_kwargs={
            "temperature": temperature,
            "max_tokens": max_tokens
        },
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        credentials_profile_name=None,  # Use environment variables
    )


# Pre-configured instances for common use cases
# Response Generator: Natural responses with OpenAI
response_llm = get_openai_llm(
    model="gpt-4-turbo-preview",
    temperature=0.7,  # Natural, conversational responses
    streaming=True
)

# Orchestrator LLM (lazy initialization)
_orchestrator_llm = None
_orchestrator_fallback = False


def get_orchestrator_llm():
    """
    Get the orchestrator LLM with automatic fallback.
    Try AWS Bedrock first (cost-effective), fall back to OpenAI if unavailable.
    """
    global _orchestrator_llm, _orchestrator_fallback
    
    if _orchestrator_llm is not None:
        return _orchestrator_llm
    
    # Try Bedrock first
    if not _orchestrator_fallback:
        try:
            _orchestrator_llm = get_bedrock_llm(
                model="anthropic.claude-3-haiku-20240307-v1:0",
                temperature=0.0,
                max_tokens=500
            )
            # Test the connection
            _orchestrator_llm.invoke([HumanMessage(content="test")])
            print("✓ Using AWS Bedrock for orchestrator")
            return _orchestrator_llm
        except Exception as e:
            print(f"⚠️  Bedrock unavailable, using OpenAI fallback")
            _orchestrator_fallback = True
    
    # Fallback to OpenAI
    _orchestrator_llm = get_openai_llm(
        model="gpt-3.5-turbo",
        temperature=0.0,
        streaming=False
    )
    print("✓ Using OpenAI GPT-3.5-turbo for orchestrator")
    return _orchestrator_llm


def get_response_llm() -> ChatOpenAI:
    """Get the response generation LLM (OpenAI GPT-4 for quality)."""
    return response_llm

