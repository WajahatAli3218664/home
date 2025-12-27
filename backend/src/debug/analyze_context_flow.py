"""
Debugging script to trace context flow in the RAG system
This script helps identify where the context flow breaks down in the RAG system
"""
import sys
import os
from datetime import datetime

# Add the backend src directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.rag_service import RAGService
from src.config.logging import log_context_flow


def analyze_context_flow(query: str, book_id: str = "default_book"):
    """
    Analyze the context flow for a given query
    """
    print(f"Starting context flow analysis for query: '{query}'")
    print("="*60)
    
    # Initialize the RAG service
    rag_service = RAGService()
    
    # Log the start of the analysis
    log_context_flow(
        component="DebugScript",
        message=f"Starting context flow analysis for query: {query}",
        context_data={"query": query, "book_id": book_id, "analysis_start_time": datetime.now().isoformat()}
    )
    
    try:
        # Execute the RAG service to get an answer
        result = rag_service.get_answer(
            query=query,
            book_id=book_id,
            session_id="debug_session"
        )
        
        print(f"Query: {query}")
        print(f"Response: {result.get('response', 'No response')}")
        print(f"Confidence Level: {result.get('confidence_level', 'N/A')}")
        print(f"Retrieved Context Count: {len(result.get('retrieved_context', []))}")
        
        # Log the results
        log_context_flow(
            component="DebugScript",
            message=f"Context flow analysis completed for query: {query}",
            context_data={
                "query": query,
                "response_preview": result.get('response', '')[:200],
                "confidence_level": result.get('confidence_level', 'N/A'),
                "retrieved_context_count": len(result.get('retrieved_context', [])),
                "analysis_end_time": datetime.now().isoformat()
            }
        )
        
        return result
        
    except Exception as e:
        print(f"Error during context flow analysis: {str(e)}")
        log_context_flow(
            component="DebugScript",
            message=f"Error during context flow analysis: {str(e)}",
            level="error"
        )
        raise e


def run_debugging_tests():
    """
    Run a series of debugging tests to analyze different aspects of the context flow
    """
    test_queries = [
        "What are the principles of robot kinematics?",
        "Explain the concept of forward kinematics",
        "How does inverse kinematics work?",
        "What is the Jacobian matrix in robotics?"
    ]
    
    print("Running RAG context flow debugging tests...")
    print("="*60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        print("-" * 40)
        try:
            result = analyze_context_flow(query)
            print(f"✓ Test {i} completed successfully")
        except Exception as e:
            print(f"✗ Test {i} failed: {str(e)}")
    
    print("\n" + "="*60)
    print("Debugging tests completed.")


if __name__ == "__main__":
    # Run the debugging tests
    run_debugging_tests()