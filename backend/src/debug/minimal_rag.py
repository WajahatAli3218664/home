"""
Minimal working RAG implementation as a reference
This demonstrates the correct flow from context retrieval to LLM response
"""
import sys
import os
from typing import List, Dict, Any
from datetime import datetime

# Add the backend src directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.qdrant_service import QdrantRetrievalService
from src.services.llm_service import LLMService
from src.config.logging import log_context_flow


class MinimalRAG:
    """
    Minimal RAG implementation that demonstrates the correct flow
    from context retrieval to LLM response
    """
    
    def __init__(self):
        self.qdrant_service = QdrantRetrievalService()
        self.llm_service = LLMService()
    
    def retrieve_context(self, query: str, book_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context from Qdrant based on the query
        """
        log_context_flow(
            component="MinimalRAG",
            message=f"Retrieving context for query: {query}",
            context_data={"query": query, "book_id": book_id}
        )
        
        # Use the Qdrant service to search for relevant chunks
        retrieved_contexts = self.qdrant_service.search_relevant_chunks(query, book_id)
        
        # Convert to a simplified format
        context_list = []
        for ctx in retrieved_contexts:
            context_list.append({
                "chunk_id": ctx.context_id,
                "content": ctx.chunk_text,
                "source_document": ctx.source_document,
                "similarity_score": ctx.similarity_score
            })
        
        log_context_flow(
            component="MinimalRAG",
            message=f"Retrieved {len(context_list)} context chunks",
            context_data={
                "retrieved_count": len(context_list),
                "contexts": context_list
            }
        )
        
        return context_list
    
    def format_context_for_prompt(self, contexts: List[Dict[str, Any]]) -> str:
        """
        Format the retrieved contexts into a single string for the LLM prompt
        """
        if not contexts:
            return ""
        
        formatted_contexts = []
        for ctx in contexts:
            formatted_contexts.append(f"Source: {ctx['source_document']}\nContent: {ctx['content']}\n")
        
        return "\n".join(formatted_contexts)
    
    def generate_response(self, query: str, context: str) -> str:
        """
        Generate a response using the LLM with the provided context
        """
        log_context_flow(
            component="MinimalRAG",
            message="Generating response with LLM",
            context_data={
                "query": query,
                "context_length": len(context),
                "context_preview": context[:200] + "..." if len(context) > 200 else context
            }
        )
        
        # Generate response using the LLM service
        response = self.llm_service.generate_response(query, context)
        
        log_context_flow(
            component="MinimalRAG",
            message="Received response from LLM",
            context_data={
                "response_length": len(response),
                "response_preview": response[:200] + "..." if len(response) > 200 else response
            }
        )
        
        return response
    
    def query(self, query: str, book_id: str = "default_book") -> Dict[str, Any]:
        """
        Complete RAG query: retrieve context and generate response
        """
        log_context_flow(
            component="MinimalRAG",
            message="Starting complete RAG query",
            context_data={"query": query, "book_id": book_id}
        )
        
        # Step 1: Retrieve context
        contexts = self.retrieve_context(query, book_id)
        
        # Step 2: Format context for prompt
        if contexts:
            formatted_context = self.format_context_for_prompt(contexts)
        else:
            formatted_context = ""
            log_context_flow(
                component="MinimalRAG",
                message="No contexts retrieved, proceeding with empty context",
                level="warning"
            )
        
        # Step 3: Generate response with context
        response = self.generate_response(query, formatted_context)
        
        result = {
            "query": query,
            "response": response,
            "retrieved_context_count": len(contexts),
            "retrieved_contexts": contexts,
            "timestamp": datetime.now().isoformat()
        }
        
        log_context_flow(
            component="MinimalRAG",
            message="RAG query completed successfully",
            context_data=result
        )
        
        return result


def run_minimal_rag_example():
    """
    Run an example of the minimal RAG implementation
    """
    print("Running Minimal RAG Implementation Example")
    print("=" * 50)
    
    # Initialize the minimal RAG
    rag = MinimalRAG()
    
    # Example query
    query = "What are the principles of robot kinematics?"
    book_id = "default_book"  # In a real implementation, this would be a specific book ID
    
    print(f"Query: {query}")
    print("-" * 30)
    
    try:
        # Execute the RAG query
        result = rag.query(query, book_id)
        
        print(f"Response: {result['response']}")
        print(f"Retrieved Context Count: {result['retrieved_context_count']}")
        print(f"Timestamp: {result['timestamp']}")
        
        if result['retrieved_context_count'] > 0:
            print("\nRetrieved Contexts:")
            for i, ctx in enumerate(result['retrieved_contexts'][:2], 1):  # Show first 2 contexts
                print(f"  {i}. Source: {ctx['source_document']}")
                print(f"     Content Preview: {ctx['content'][:100]}...")
                print(f"     Similarity: {ctx['similarity_score']:.2f}")
        
    except Exception as e:
        print(f"Error during RAG query: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("Minimal RAG Example Completed")


if __name__ == "__main__":
    run_minimal_rag_example()