#!/usr/bin/env python3
"""
Quick Reference - Chatbot API Usage Examples
"""

import requests
import json

# API Base URL
API_URL = "http://localhost:8000"

# Example 1: Health Check
print("=" * 60)
print("EXAMPLE 1: Health Check")
print("=" * 60)
print("""
curl -X GET http://localhost:8000/api/v1/health

Expected Response:
{
  "status": "healthy",
  "message": "RAG Chatbot API is running!"
}
""")

# Example 2: RAG Query
print("=" * 60)
print("EXAMPLE 2: Query the Chatbot (RAG)")
print("=" * 60)
print("""
curl -X POST http://localhost:8000/api/v1/rag/query \\
  -H "Content-Type: application/json" \\
  -d '{
    "query": "What is artificial intelligence?",
    "book_id": "physics_101",
    "session_id": "user_session_123"
  }'

Expected Response:
{
  "response": "Artificial intelligence is the simulation of human intelligence...",
  "confidence_level": "HIGH",
  "session_id": "user_session_123",
  "retrieved_context": [
    {
      "chunk_id": "chunk_1",
      "text": "AI enables computers to learn from experience...",
      "similarity_score": 0.92
    }
  ],
  "response_time": 3.45
}
""")

# Example 3: Chat with Selected Text
print("=" * 60)
print("EXAMPLE 3: Query with Selected Text Context")
print("=" * 60)
print("""
curl -X POST http://localhost:8000/api/v1/rag/query \\
  -H "Content-Type: application/json" \\
  -d '{
    "query": "Explain this in simpler terms",
    "book_id": "physics_101",
    "session_id": "user_session_123",
    "selected_text": "Quantum mechanics describes how particles behave at subatomic scales..."
  }'
""")

# Example 4: Python Client
print("=" * 60)
print("EXAMPLE 4: Python Client Usage")
print("=" * 60)
print("""
import requests

url = "http://localhost:8000/api/v1/rag/query"
payload = {
    "query": "What is machine learning?",
    "book_id": "ai_fundamentals",
    "session_id": "session_001"
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Response: {result['response']}")
print(f"Confidence: {result['confidence_level']}")
print(f"Sources: {len(result['retrieved_context'])} references")
""")

# Example 5: JavaScript/Fetch Client
print("=" * 60)
print("EXAMPLE 5: JavaScript Client Usage")
print("=" * 60)
print("""
const query = {
  query: "Explain quantum computing",
  book_id: "quantum_physics",
  session_id: "user_session_456"
};

fetch('http://localhost:8000/api/v1/rag/query', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(query)
})
.then(response => response.json())
.then(data => {
  console.log('Answer:', data.response);
  console.log('Confidence:', data.confidence_level);
  console.log('Sources:', data.retrieved_context);
})
.catch(error => console.error('Error:', error));
""")

# Example 6: Request Headers
print("=" * 60)
print("EXAMPLE 6: Request Headers Reference")
print("=" * 60)
print("""
Required Headers:
  - Content-Type: application/json

Optional Headers:
  - Authorization: Bearer <token> (if auth is enabled)
  - X-User-ID: <user_id> (for user tracking)
  - X-Session-ID: <session_id> (for session tracking)
""")

# Example 7: Response Status Codes
print("=" * 60)
print("EXAMPLE 7: Response Status Codes")
print("=" * 60)
print("""
200 OK - Query processed successfully
  {
    "response": "...",
    "confidence_level": "HIGH",
    ...
  }

400 Bad Request - Invalid query or missing parameters
  {
    "detail": "Invalid query provided"
  }

422 Unprocessable Entity - Validation error
  {
    "detail": [
      {
        "loc": ["body", "query"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }

500 Internal Server Error - Server error
  {
    "detail": "Error processing query"
  }
""")

# Example 8: Advanced Query Examples
print("=" * 60)
print("EXAMPLE 8: Advanced Query Examples")
print("=" * 60)
print("""
Example 1: Asking for comparison
"How does supervised learning differ from unsupervised learning?"

Example 2: Asking for step-by-step explanation
"Explain the process of training a neural network step by step"

Example 3: Asking for practical applications
"What are real-world applications of machine learning?"

Example 4: Follow-up question with context
Query 1: "What is deep learning?"
Query 2: "Can you provide examples?" (in same session)

Example 5: Asking with specific textbook reference
"According to chapter 3, how does backpropagation work?"
""")

# Example 9: Testing Script
print("=" * 60)
print("EXAMPLE 9: Complete Testing Script")
print("=" * 60)
print("""
#!/bin/bash

# Test health
echo "Testing health endpoint..."
curl -X GET http://localhost:8000/api/v1/health

echo ""

# Test query
echo "Testing query endpoint..."
curl -X POST http://localhost:8000/api/v1/rag/query \\
  -H "Content-Type: application/json" \\
  -d '{
    "query": "What is artificial intelligence?",
    "book_id": "test_book",
    "session_id": "test_session"
  }'

echo ""

# Check API documentation
echo "API documentation available at:"
echo "http://localhost:8000/docs"
""")

# Example 10: Docker Deployment
print("=" * 60)
print("EXAMPLE 10: Docker Deployment")
print("=" * 60)
print("""
# Build image
docker build -t chatbot-api:latest .

# Run container
docker run -p 8000:8000 \\
  -e GROQ_API_KEY=your_key_here \\
  -e QDRANT_URL=your_url \\
  -e QDRANT_API_KEY=your_key \\
  -e DATABASE_URL=your_db_url \\
  chatbot-api:latest

# Run with docker-compose
docker-compose up -d
""")

# Example 11: Performance Optimization Tips
print("=" * 60)
print("EXAMPLE 11: Performance Optimization Tips")
print("=" * 60)
print("""
1. Batch Requests:
   Instead of individual queries, batch multiple queries together

2. Caching:
   Cache frequently asked questions and their responses

3. Async Processing:
   Use async/await for concurrent requests

4. Vector Database Optimization:
   - Ensure Qdrant collection is properly indexed
   - Use appropriate vector dimensions
   - Regular cleanup of old vectors

5. Database Optimization:
   - Index frequently queried fields
   - Archive old chat sessions
   - Monitor connection pool

6. API Rate Limiting:
   - Implement rate limiting to prevent abuse
   - Use request queues for high traffic

7. Response Caching:
   - Cache identical queries within a time window
   - Use Redis for distributed caching
""")

# Example 12: Monitoring and Logging
print("=" * 60)
print("EXAMPLE 12: Monitoring and Logging")
print("=" * 60)
print("""
# View logs
tail -f backend.log

# Monitor specific API calls
grep "api/v1/rag" backend.log

# Check error frequency
grep "ERROR" backend.log | wc -l

# Monitor response times
grep "response_time" backend.log | awk '{print $NF}' | sort -n

# Check Groq API usage
grep "Groq" backend.log | wc -l

# Monitor database connections
grep "database" backend.log | tail -20

# Real-time monitoring
watch -n 1 'tail -10 backend.log'
""")

print("\n" + "=" * 60)
print("For more information, see:")
print("  - http://localhost:8000/docs (Swagger UI)")
print("  - http://localhost:8000/redoc (ReDoc)")
print("  - INTEGRATION_COMPLETE.md")
print("=" * 60 + "\n")
