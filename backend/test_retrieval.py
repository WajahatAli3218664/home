"""
Test retrieval functionality with various query types
"""
import sys
import os

# Add the backend/src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.embedding_pipeline.vector_store import QdrantStore
from src.embedding_pipeline.config import Config, validate_config


def test_retrieval():
    """Test retrieval with various query types"""
    if not validate_config():
        print("Configuration is not valid. Please check your environment variables.")
        return
    
    # Initialize Qdrant store
    qdrant_store = QdrantStore()
    
    # Test queries of different types
    test_queries = [
        "What is Physical AI?",
        "Explain robotics fundamentals",
        "How do humanoid robots work?",
        "What are the applications of AI in robotics?",
        "Simulation in robotics"
    ]
    
    print("Testing retrieval with various query types...")
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = qdrant_store.validate_retrieval(query, top_k=3)
        
        if results:
            print(f"Found {len(results)} results:")
            for i, result in enumerate(results):
                print(f"  {i+1}. Score: {result['score']:.4f}")
                print(f"     Content: {result['content'][:100]}...")
                print(f"     Source: {result['source_url']}")
                print()
        else:
            print("  No results found for this query.")
    
    print("\nRetrieval testing completed.")


if __name__ == "__main__":
    test_retrieval()