# RAG Chatbot API Documentation

## Overview
This API provides a RAG (Retrieval-Augmented Generation) chatbot that answers questions based only on the Physical AI & Humanoid Robotics textbook content.

## Base URL
`http://127.0.0.1:8000` (local) or your Hugging Face Space URL

## Authentication
All chat endpoints require a Bearer token obtained through the auth endpoints.

## Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token
- `POST /api/v1/auth/me` - Get current user info

### Chat
- `POST /api/v1/chat/` - Send a message to the chatbot
- `GET /api/v1/chat/history/{user_id}` - Get chat history for a user

### Health Check
- `GET /` - Root endpoint
- `GET /health` - Health check endpoint

## Request/Response Examples

### Chat Request
```json
{
  "query": "What are the principles of embodied cognition?"
}
```

### Chat Response
```json
{
  "response": "Based on the textbook content, embodied cognition principles include: [response from LLM with textbook content] [1] Chapter 1: Foundations of Physical AI"
}
```

### cURL Example
```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{
    "query": "What are the principles of embodied cognition?"
  }'
```

### Axios Example
```javascript
const response = await axios.post('http://127.0.0.1:8000/api/v1/chat/', {
  query: 'What are the principles of embodied cognition?'
}, {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});
```

## Environment Variables
- `OPENAI_API_KEY` or `COHERE_API_KEY` - AI service API key
- `QDRANT_URL` - Vector database URL
- `QDRANT_API_KEY` - Vector database API key
- `JWT_SECRET_KEY` - JWT secret key
- `DATABASE_URL` - Database connection string

## Error Handling
- 401: Unauthorized (invalid or missing token)
- 403: Forbidden (attempting to access another user's data)
- 404: Not Found (endpoint doesn't exist)
- 500: Internal Server Error (server-side error)

## Book-only Answering
The chatbot strictly answers only from the textbook content. If the information is not available in the book, it will respond with "This information is not available in the book."