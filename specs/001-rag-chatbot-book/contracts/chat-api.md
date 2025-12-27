# Chat API Contract

## Overview
This document defines the API contract for the RAG chatbot feature, specifying endpoints for interacting with the book content and chat functionality.

## Base URL
`/api/v1`

## Endpoints

### POST /chat
Initiate a conversation or continue an existing one with the RAG chatbot.

**Request Body**:
```json
{
  "session_id": "uuid",
  "book_id": "uuid",
  "query": "string (the user's question)",
  "selected_text": "string (optional, text the user highlighted)",
  "user_id": "uuid (optional)"
}
```

**Response** (200 OK):
```json
{
  "response_id": "uuid",
  "session_id": "uuid",
  "query": "string (echo of the user's question)",
  "answer": "string (the chatbot's response)",
  "confidence_level": "enum (high|medium|low)",
  "source_chunks_used": ["uuid"],
  "grounded_in_content": "boolean",
  "timestamp": "datetime"
}
```

**Error Responses**:
- 400: Invalid request format
- 404: Book ID not found
- 500: Internal server error during processing

### GET /chat/{session_id}/history
Retrieve the conversation history for a specific session.

**Path Parameters**:
- session_id: UUID of the session

**Response** (200 OK):
```json
{
  "session_id": "uuid",
  "history": [
    {
      "query": "string",
      "answer": "string",
      "timestamp": "datetime",
      "confidence_level": "enum (high|medium|low)"
    }
  ]
}
```

**Error Responses**:
- 404: Session ID not found
- 500: Internal server error

### POST /books
Upload a new book for the RAG system to use.

**Request Body**:
```json
{
  "title": "string",
  "author": "string",
  "content": "string (full text of the book)",
  "chunk_size": "integer (optional, default: 512)",
  "embedding_model": "string (optional, default: 'MiniLM')"
}
```

**Response** (201 Created):
```json
{
  "book_id": "uuid",
  "title": "string",
  "author": "string",
  "status": "processing|ready|error",
  "created_at": "datetime"
}
```

**Error Responses**:
- 400: Invalid request format
- 500: Internal server error during processing

### GET /books/{book_id}
Get information about a specific book.

**Path Parameters**:
- book_id: UUID of the book

**Response** (200 OK):
```json
{
  "book_id": "uuid",
  "title": "string",
  "author": "string",
  "status": "processing|ready|error",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### GET /books
List all available books.

**Response** (200 OK):
```json
[
  {
    "book_id": "uuid",
    "title": "string",
    "author": "string",
    "status": "processing|ready|error",
    "created_at": "datetime"
  }
]
```

### POST /auth/login
User authentication endpoint (using Better-Auth).

**Request Body**:
```json
{
  "email": "string",
  "password": "string"
}
```

**Response** (200 OK):
```json
{
  "user_id": "uuid",
  "email": "string",
  "name": "string (optional)",
  "access_token": "string"
}
```

### GET /health
Health check endpoint.

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "datetime"
}
```