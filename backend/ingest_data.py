"""
Data Ingestion Script for Advanced Customer Service AI
Processes mock documents, creates embeddings, and stores in ChromaDB
"""

import os
import glob
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import chromadb
from chromadb.config import Settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
DATA_DIR = Path(__file__).parent / "data"
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = "customer_service_docs"

# Text splitting parameters
CHUNK_SIZE = 800  # tokens (approximate, ~600-1000 words)
CHUNK_OVERLAP = 100  # tokens overlap for context continuity


def get_document_files() -> Dict[str, List[Path]]:
    """
    Retrieve all document files organized by type.
    
    Returns:
        Dictionary mapping document type to list of file paths
    """
    doc_files = {
        "billing": list((DATA_DIR / "billing").glob("*.txt")),
        "technical": list((DATA_DIR / "technical").glob("*.txt")),
        "policy": list((DATA_DIR / "policy").glob("*.txt")),
    }
    
    total_files = sum(len(files) for files in doc_files.values())
    print(f"\n📁 Found {total_files} documents:")
    for doc_type, files in doc_files.items():
        print(f"   - {doc_type.capitalize()}: {len(files)} files")
    
    return doc_files


def load_document(file_path: Path) -> str:
    """
    Load document content from file.
    
    Args:
        file_path: Path to the document file
        
    Returns:
        Document content as string
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def chunk_document(content: str, source_file: str) -> List[Dict]:
    """
    Split document into chunks with metadata.
    
    Args:
        content: Document text content
        source_file: Source filename for metadata
        
    Returns:
        List of chunk dictionaries with text and metadata
    """
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    # Split text into chunks
    chunks = text_splitter.split_text(content)
    
    # Create chunk dictionaries with metadata
    chunk_dicts = []
    for idx, chunk in enumerate(chunks):
        chunk_dicts.append({
            "text": chunk,
            "chunk_index": idx,
            "source_file": source_file,
            "total_chunks": len(chunks)
        })
    
    return chunk_dicts


def ingest_documents():
    """
    Main ingestion function: loads documents, creates embeddings, stores in ChromaDB.
    """
    print("\n" + "="*70)
    print("🚀 Starting Data Ingestion Pipeline")
    print("="*70)
    
    # Initialize OpenAI embeddings
    print("\n🔑 Initializing OpenAI embeddings (text-embedding-3-small)...")
    embeddings_model = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Initialize ChromaDB client with persistence
    print(f"💾 Initializing ChromaDB (persist_directory: {CHROMA_PERSIST_DIR})...")
    chroma_client = chromadb.PersistentClient(
        path=CHROMA_PERSIST_DIR,
        settings=Settings(anonymized_telemetry=False)
    )
    
    # Get or create collection (delete existing for fresh start)
    try:
        chroma_client.delete_collection(name=COLLECTION_NAME)
        print(f"🗑️  Deleted existing collection: {COLLECTION_NAME}")
    except Exception:
        print(f"ℹ️  No existing collection to delete")
    
    collection = chroma_client.create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Customer service documents with billing, technical, and policy content"}
    )
    print(f"✅ Created collection: {COLLECTION_NAME}")
    
    # Get all document files
    doc_files = get_document_files()
    
    # Process each document type
    total_chunks = 0
    total_documents = 0
    
    for doc_type, files in doc_files.items():
        print(f"\n📚 Processing {doc_type.upper()} documents...")
        
        for file_path in files:
            try:
                # Load document content
                content = load_document(file_path)
                filename = file_path.name
                
                # Chunk the document
                chunks = chunk_document(content, filename)
                
                print(f"   ✓ {filename}: {len(chunks)} chunks")
                
                # Prepare data for ChromaDB
                chunk_ids = []
                chunk_texts = []
                chunk_metadatas = []
                
                for chunk in chunks:
                    # Generate unique ID for each chunk
                    chunk_id = f"{doc_type}_{filename}_{chunk['chunk_index']}"
                    
                    # Prepare metadata
                    metadata = {
                        "document_type": doc_type,
                        "source_document": filename,
                        "chunk_index": chunk["chunk_index"],
                        "total_chunks": chunk["total_chunks"],
                        "last_updated": datetime.now().isoformat()
                    }
                    
                    chunk_ids.append(chunk_id)
                    chunk_texts.append(chunk["text"])
                    chunk_metadatas.append(metadata)
                
                # Generate embeddings for all chunks
                embeddings = embeddings_model.embed_documents(chunk_texts)
                
                # Add to collection
                collection.add(
                    ids=chunk_ids,
                    embeddings=embeddings,
                    documents=chunk_texts,
                    metadatas=chunk_metadatas
                )
                
                total_chunks += len(chunks)
                total_documents += 1
                
            except Exception as e:
                print(f"   ✗ Error processing {filename}: {str(e)}")
                continue
    
    print("\n" + "="*70)
    print("✅ Data Ingestion Complete!")
    print("="*70)
    print(f"📊 Statistics:")
    print(f"   - Total documents processed: {total_documents}")
    print(f"   - Total chunks created: {total_chunks}")
    print(f"   - Average chunks per document: {total_chunks / total_documents:.1f}")
    print(f"   - ChromaDB collection: {COLLECTION_NAME}")
    print(f"   - Persist directory: {CHROMA_PERSIST_DIR}")
    
    # Verify data
    print(f"\n🔍 Verifying data in ChromaDB...")
    collection_count = collection.count()
    print(f"   - Total items in collection: {collection_count}")
    
    # Test query
    print(f"\n🧪 Testing retrieval (sample query)...")
    test_query = "What are your pricing plans?"
    test_embedding = embeddings_model.embed_query(test_query)
    results = collection.query(
        query_embeddings=[test_embedding],
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )
    
    if results['documents'] and len(results['documents'][0]) > 0:
        print(f"   ✓ Retrieved {len(results['documents'][0])} relevant chunks")
        print(f"   Sample result from: {results['metadatas'][0][0]['source_document']}")
        print(f"   Distance: {results['distances'][0][0]:.4f}")
    else:
        print(f"   ⚠️  No results found for test query")
    
    print("\n✨ Ingestion pipeline completed successfully!\n")


if __name__ == "__main__":
    try:
        ingest_documents()
    except KeyboardInterrupt:
        print("\n\n⚠️  Ingestion interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during ingestion: {str(e)}")
        import traceback
        traceback.print_exc()

