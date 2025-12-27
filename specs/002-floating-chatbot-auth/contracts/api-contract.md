# API Contract: Floating Chatbot with Authentication

## Overview
This document specifies the API contracts between the frontend chatbot components and the backend services.

## Endpoint: Authenticate User

### Request
- **URL**: `/auth/login`
- **Method**: POST
- **Headers**:
  - `Content-Type`: `application/json`
- **Body**:
```json
{
  "provider": "string (required) - Authentication provider (google|facebook|email)",
  "credentials": "object (required) - Provider-specific credentials"
}
```

### Successful Response (200 OK)
- **Headers**:
  - `Content-Type`: `application/json`
- **Body**:
```json
{
  "isAuthenticated": true,
  "userId": "string - Unique identifier for the authenticated user",
  "authToken": "string - Authentication token for subsequent requests",
  "expiresAt": "string (ISO 8601 date) - Token expiration timestamp",
  "profile": {
    "name": "string - User's display name",
    "email": "string - User's email address",
    "image": "string (optional) - URL to user's profile image"
  }
}
```

### Error Response (4xx/5xx)
- **Headers**:
  - `Content-Type`: `application/json`
- **Body**:
```json
{
  "error": "string - Error message explaining the failure",
  "code": "string - Error code for client handling"
}
```

## Endpoint: Send Chat Message

### Request
- **URL**: `/chat/send`
- **Method**: POST
- **Headers**:
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer {authToken}`
- **Body**:
```json
{
  "message": "string (required) - The user's message/query",
  "conversationId": "string (optional) - ID of the current conversation"
}
```

### Successful Response (200 OK)
- **Headers**:
  - `Content-Type`: `application/json`
- **Body**:
```json
{
  "response": "string - The AI-generated response",
  "conversationId": "string - ID of the conversation",
  "citations": [
    {
      "sourceUrl": "string - URL of the referenced content",
      "sourceTitle": "string - Title of the referenced content",
      "textExcerpt": "string - Relevant text excerpt from the source"
    }
  ],
  "timestamp": "string (ISO 8601 date) - When the response was generated"
}
```

### Error Response (4xx/5xx)
- **Headers**:
  - `Content-Type`: `application/json`
- **Body**:
```json
{
  "error": "string - Error message explaining the failure",
  "code": "string - Error code for client handling"
}
```

## Endpoint: Start New Conversation

### Request
- **URL**: `/chat/new`
- **Method**: POST
- **Headers**:
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer {authToken}`
- **Body**: `{}`

### Successful Response (200 OK)
- **Headers**:
  - `Content-Type`: `application/json`
- **Body**:
```json
{
  "conversationId": "string - New unique conversation ID",
  "timestamp": "string (ISO 8601 date) - When the conversation was started"
}
```

## Endpoint: Get Conversation History

### Request
- **URL**: `/chat/history/{conversationId}`
- **Method**: GET
- **Headers**:
  - `Authorization`: `Bearer {authToken}`

### Successful Response (200 OK)
- **Headers**:
  - `Content-Type`: `application/json`
- **Body**:
```json
{
  "conversationId": "string - Unique conversation ID",
  "messages": [
    {
      "id": "string - Unique message ID",
      "content": "string - Message content",
      "sender": "string - Either 'user' or 'ai'",
      "timestamp": "string (ISO 8601 date) - When the message was created",
      "citations": [
        {
          "sourceUrl": "string - URL of the referenced content",
          "sourceTitle": "string - Title of the referenced content",
          "textExcerpt": "string - Relevant text excerpt from the source"
        }
      ]
    }
  ]
}
```

## Validation Rules
- All authenticated endpoints require a valid auth token in the Authorization header
- Message content should be between 1 and 1000 characters
- Conversations are tied to authenticated users
- Citations are optional for user messages, required for AI responses when sources exist

## Error Scenarios
- 400 Bad Request: Invalid request format or missing required fields
- 401 Unauthorized: Missing or invalid authentication token
- 403 Forbidden: User doesn't have permission to access the resource
- 404 Not Found: Conversation ID doesn't exist
- 429 Too Many Requests: Rate limit exceeded
- 500 Internal Server Error: Backend error processing the request
- 503 Service Unavailable: RAG system is temporarily unavailable