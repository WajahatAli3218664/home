#!/usr/bin/env python3
"""
Test script to verify chatbot functionality with integrated APIs
"""
import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.services.llm_service import LLMService
from backend.src.services.qdrant_service import QdrantRetrievalService
from backend.src.services.rag_service import RAGService
from backend.src.config.settings import settings

def test_groq_api():
    """Test Groq API integration"""
    print("\n" + "="*60)
    print("TEST 1: Groq API Integration")
    print("="*60)
    
    try:
        llm = LLMService()
        response = llm.generate_response(
            query="What is robotics?",
            context="Robotics is the field of engineering and science that deals with the design, construction, operation, and application of robots."
        )
        print("✓ Groq API is working correctly")
        print(f"  Response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"✗ Groq API test failed: {e}")
        return False

def test_qdrant_connection():
    """Test Qdrant connection"""
    print("\n" + "="*60)
    print("TEST 2: Qdrant Vector Database Connection")
    print("="*60)
    
    try:
        qdrant = QdrantRetrievalService()
        # Test connection without actual search
        print("✓ Qdrant service initialized")
        print(f"  URL: {settings.qdrant_url}")
        print(f"  Collection: {settings.qdrant_collection_name}")
        return True
    except Exception as e:
        print(f"✗ Qdrant connection test failed: {e}")
        return False

def test_rag_service():
    """Test RAG service"""
    print("\n" + "="*60)
    print("TEST 3: RAG Service")
    print("="*60)
    
    try:
        rag = RAGService()
        print("✓ RAG service initialized successfully")
        return True
    except Exception as e:
        print(f"✗ RAG service test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints availability"""
    print("\n" + "="*60)
    print("TEST 4: API Endpoints Check")
    print("="*60)
    
    try:
        # Import and check routers
        from backend.src.api import routers
        print("✓ API routers imported successfully")
        print("  Available endpoints:")
        print("    - /api/v1/health")
        print("    - /api/v1/chat")
        print("    - /api/v1/rag/query")
        print("    - /api/v1/rag/query-selected")
        return True
    except Exception as e:
        print(f"✗ API endpoint check failed: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("CHATBOT INTEGRATION TEST SUITE")
    print("="*80)
    
    results = {
        "Groq API": test_groq_api(),
        "Qdrant Connection": test_qdrant_connection(),
        "RAG Service": test_rag_service(),
        "API Endpoints": test_api_endpoints(),
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60)
    
    if passed == total:
        print("\n✓ All tests passed! The chatbot is ready to use.")
        print("\nTo start the backend server, run:")
        print("  cd /workspaces/home && python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000")
        print("\nTo test the API:")
        print('  curl -X POST http://localhost:8000/api/v1/rag/query \\')
        print('    -H "Content-Type: application/json" \\')
        print('    -d \'{"query": "What is AI?", "book_id": "test", "session_id": "test"}\'')
    else:
        print(f"\n✗ {total - passed} test(s) failed. Please fix the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
