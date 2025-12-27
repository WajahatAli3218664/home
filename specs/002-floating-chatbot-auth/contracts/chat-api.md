# Chat API Contract

## POST /api/v1/chat
Initiate a conversation with the RAG chatbot

### Headers
- `Authorization: Bearer <token>` (required)

### Request Body
```json
{
  "query": "string (user question)"
}
```

### Response (200 OK)
```json
{
  "response": "string (AI answer)",
  "timestamp": "ISO 8601 datetime",
  "sources": [
    {
      "title": "string (source title)",
      "url": "string (source URL)",
      "chapter": "string (textbook chapter)"
    }
  ]
}
```

### Error Responses
- `401 Unauthorized`: Invalid or missing authentication token
- `422 Validation Error`: Malformed request body
- `500 Internal Server Error`: Server error processing request

## GET /api/v1/chat/history/{user_id}
Retrieve chat history for a specific user

### Headers
- `Authorization: Bearer <token>` (required)

### Path Parameters
- `user_id: int` (the user ID whose history to retrieve)

### Response (200 OK)
```json
{
  "history": [
    {
      "id": "int",
      "user_id": "int",
      "query": "string (original user query)",
      "response": "string (AI response)",
      "timestamp": "ISO 8601 datetime"
    }
  ]
}
```

### Error Responses
- `401 Unauthorized`: Invalid or missing authentication token
- `403 Forbidden`: User requesting history for another user
- `500 Internal Server Error`: Server error retrieving history