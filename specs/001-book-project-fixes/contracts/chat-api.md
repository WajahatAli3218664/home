# Chat API Contract

## POST /api/v1/chat/
**Description**: Process user query using RAG functionality and return AI response based on book content

### Request
- **Content-Type**: `application/json`
- **Headers**:
  - `Authorization: Bearer <jwt_token>` (optional for non-registered users)
- **Body**:
  ```json
  {
    "message": "What are the key concepts of Physical AI?",
    "context": {
      "chapter_id": "chapter-001",
      "selected_text": "Physical AI combines robotics, machine learning, and embodied intelligence."
    },
    "user_preferences": {
      "programming_level": "intermediate",
      "hardware_background": "beginner"
    }
  }
  ```

### Response
- **200 OK**:
  ```json
  {
    "success": true,
    "response": "Physical AI is an interdisciplinary field that combines robotics with artificial intelligence...",
    "sources": [
      {
        "chapter_id": "chapter-001",
        "title": "Introduction to Physical AI",
        "relevance_score": 0.92
      }
    ],
    "session_id": "session-123"
  }
  ```

- **400 Bad Request**: Malformed request or missing required fields
- **500 Internal Server Error**: AI service unavailable
- **429 Too Many Requests**: Rate limit exceeded

## GET /api/v1/chat/history/{session_id}
**Description**: Retrieve chat history for a specific session

### Request
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Path Parameters**:
  - `session_id`: The ID of the chat session to retrieve

### Response
- **200 OK**:
  ```json
  {
    "session_id": "session-123",
    "title": "Physical AI Concepts",
    "messages": [
      {
        "id": "msg-001",
        "role": "user",
        "content": "What are the key concepts of Physical AI?",
        "timestamp": "2025-12-18T10:00:00Z"
      },
      {
        "id": "msg-002",
        "role": "assistant",
        "content": "Physical AI is an interdisciplinary field that combines robotics with artificial intelligence...",
        "sources": [
          {
            "chapter_id": "chapter-001",
            "title": "Introduction to Physical AI",
            "relevance_score": 0.92
          }
        ],
        "timestamp": "2025-12-18T10:00:05Z"
      }
    ]
  }
  ```

- **401 Unauthorized**: Invalid or missing token
- **404 Not Found**: Session does not exist