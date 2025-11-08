"""
Retrieval utilities for RAG and CAG strategies
Handles ChromaDB queries and document caching
"""

import os
from typing import List, Dict, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# Configuration
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = "customer_service_docs"
TOP_K = 5  # Number of chunks to retrieve

# Initialize global instances
_embeddings = None
_chroma_client = None
_collection = None
_policy_cache = None


def get_embeddings() -> OpenAIEmbeddings:
    """Get or create OpenAI embeddings instance."""
    global _embeddings
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    return _embeddings


def get_chroma_client():
    """Get or create ChromaDB client."""
    global _chroma_client
    if _chroma_client is None:
        _chroma_client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
    return _chroma_client


def get_collection():
    """Get or create ChromaDB collection."""
    global _collection
    if _collection is None:
        client = get_chroma_client()
        _collection = client.get_collection(name=COLLECTION_NAME)
    return _collection


def query_rag(
    query: str,
    document_type: Optional[str] = None,
    top_k: int = TOP_K
) -> List[Dict]:
    """
    Query ChromaDB for relevant documents (Pure RAG).
    
    Args:
        query: User query text
        document_type: Filter by document type (billing, technical, policy)
        top_k: Number of results to return
        
    Returns:
        List of relevant document chunks with metadata
    """
    try:
        # Get embeddings and collection
        embeddings = get_embeddings()
        collection = get_collection()
        
        # Generate query embedding
        query_embedding = embeddings.embed_query(query)
        
        # Prepare filter if document type specified
        where_filter = None
        if document_type:
            where_filter = {"document_type": document_type}
        
        # Query ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        formatted_results = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i]
                })
        
        return formatted_results
        
    except Exception as e:
        print(f"Error querying RAG: {str(e)}")
        return []


def load_policy_documents(query: Optional[str] = None) -> str:
    """
    Load policy documents into memory for CAG (Context-Augmented Generation).
    With smart selection: only loads relevant policies based on query keywords.
    
    Args:
        query: User query to determine relevant policies (optional)
    
    Returns:
        Combined text of relevant policy documents
    """
    global _policy_cache
    
    try:
        # Path to policy documents
        data_dir = Path(__file__).parent.parent / "data" / "policy"
        
        # If no query, load all documents (for initial cache)
        if query is None:
            # Return cached version if available
            if _policy_cache is not None:
                return _policy_cache
            
            # Load all policy documents
            policy_docs = []
            for policy_file in data_dir.glob("*.txt"):
                with open(policy_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    policy_docs.append(f"=== {policy_file.stem} ===\n{content}\n")
            
            # Combine all documents
            _policy_cache = "\n".join(policy_docs)
            print(f"✓ Loaded {len(policy_docs)} policy documents into CAG cache")
            
            return _policy_cache
        
        # Smart selection based on query keywords
        query_lower = query.lower()
        
        # Policy file mapping with keywords
        policy_keywords = {
            'privacy_policy.txt': ['privacy', 'personal data', 'personal information', 'data collection', 'private'],
            'gdpr_data_processing.txt': ['gdpr', 'processing', 'data processing', 'lawful basis', 'consent', 'legitimate interest'],
            'gdpr_data_rights.txt': ['gdpr', 'rights', 'data rights', 'access', 'deletion', 'portability', 'rectification', 'erasure'],
            'terms_of_service.txt': ['terms', 'service', 'agreement', 'use', 'account', 'termination', 'liability'],
            'cookie_policy.txt': ['cookie', 'cookies', 'tracking', 'analytics', 'browser'],
            'acceptable_use_policy.txt': ['acceptable', 'prohibited', 'restrictions', 'abuse', 'misuse', 'violation']
        }
        
        # Determine which policies are relevant
        relevant_policies = []
        match_scores = {}
        
        for policy_file, keywords in policy_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                match_scores[policy_file] = score
        
        # If we have matches, use top matches
        if match_scores:
            # Sort by score and take top matches
            sorted_matches = sorted(match_scores.items(), key=lambda x: x[1], reverse=True)
            
            # Take policies with highest scores (at least 2 policies, max 3)
            top_score = sorted_matches[0][1]
            for policy_file, score in sorted_matches:
                if score >= top_score or len(relevant_policies) < 2:
                    relevant_policies.append(policy_file)
                if len(relevant_policies) >= 3:
                    break
        else:
            # No clear matches - use all policies (fallback)
            relevant_policies = list(policy_keywords.keys())
        
        # Load selected policies
        policy_docs = []
        for policy_file in relevant_policies:
            policy_path = data_dir / policy_file
            if policy_path.exists():
                with open(policy_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    policy_docs.append(f"=== {policy_path.stem} ===\n{content}\n")
        
        # Combine selected documents
        result = "\n".join(policy_docs)
        print(f"   ✓ Selected {len(policy_docs)}/{len(policy_keywords)} relevant policies (Smart CAG)")
        
        return result
        
    except Exception as e:
        print(f"Error loading policy documents: {str(e)}")
        return ""


def format_rag_context(results: List[Dict]) -> str:
    """
    Format RAG results into context string for LLM.
    
    Args:
        results: List of document chunks from query_rag
        
    Returns:
        Formatted context string
    """
    if not results:
        return "No relevant information found in the knowledge base."
    
    context_parts = []
    for i, result in enumerate(results, 1):
        source = result['metadata'].get('source_document', 'Unknown')
        content = result['content']
        context_parts.append(f"[Source {i}: {source}]\n{content}\n")
    
    return "\n".join(context_parts)


def get_billing_context(query: str, cached_info: Optional[str] = None) -> Dict:
    """
    Get context for billing queries using Hybrid RAG/CAG strategy.
    
    On first query: Perform RAG and cache general billing info
    On subsequent queries: Use cached info (CAG) + RAG for specific details
    
    Args:
        query: User query
        cached_info: Previously cached billing information
        
    Returns:
        Dictionary with context and cache_update
    """
    try:
        # Always query for specific information
        rag_results = query_rag(query, document_type="billing", top_k=3)
        rag_context = format_rag_context(rag_results)
        
        if cached_info is None:
            # First query: Build cache from general billing documents
            general_query = "pricing plans billing policy payment subscription"
            cache_results = query_rag(general_query, document_type="billing", top_k=5)
            cache_context = format_rag_context(cache_results)
            
            # Combine for response and save cache
            combined_context = f"General Billing Information (Cached):\n{cache_context}\n\nSpecific Information:\n{rag_context}"
            
            return {
                "context": combined_context,
                "cache_update": cache_context
            }
        else:
            # Subsequent queries: Use cache + RAG
            combined_context = f"General Billing Information (Cached):\n{cached_info}\n\nSpecific Information:\n{rag_context}"
            
            return {
                "context": combined_context,
                "cache_update": None  # No update needed
            }
            
    except Exception as e:
        print(f"Error in hybrid RAG/CAG: {str(e)}")
        return {
            "context": "Error retrieving billing information.",
            "cache_update": None
        }


def get_technical_context(query: str) -> str:
    """
    Get context for technical queries using Pure RAG.
    Always queries the database for latest information.
    
    Args:
        query: User query
        
    Returns:
        Formatted context string
    """
    results = query_rag(query, document_type="technical", top_k=5)
    return format_rag_context(results)


def get_policy_context(query: Optional[str] = None) -> str:
    """
    Get context for policy queries using Pure CAG with smart selection.
    Returns relevant pre-loaded documents based on query keywords.
    
    Args:
        query: User query to determine relevant policies (optional)
    
    Returns:
        Relevant policy documents as context
    """
    if query is None:
        # No query provided, return all policies (fallback)
        return load_policy_documents()
    
    return load_policy_documents(query=query)


def verify_chromadb_connection() -> bool:
    """
    Verify ChromaDB connection and collection exists.
    Used during startup to validate the system.
    
    Returns:
        True if connection successful
        
    Raises:
        Exception if connection fails
    """
    try:
        client = get_chroma_client()
        collection = get_collection()
        
        # Try to get collection info
        count = collection.count()
        print(f"   ChromaDB collection '{COLLECTION_NAME}' contains {count} documents")
        
        if count == 0:
            raise Exception("ChromaDB collection is empty. Run ingest_data.py first.")
        
        return True
        
    except Exception as e:
        raise Exception(f"ChromaDB connection failed: {str(e)}")

