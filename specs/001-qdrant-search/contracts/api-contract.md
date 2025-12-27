# API Contract: Qdrant Search Interface

## Overview
This document specifies the API contract between the Qdrant search frontend component and the backend service.

## Endpoint: Search Query

### Request
- **URL**: `/retrieve`
- **Method**: POST
- **Headers**:
  - `Content-Type`: `application/json`
  - `Accept`: `application/json`
- **Body**:
```json
{
  "query": "string (required) - The search query text from the user"
}
```

### Successful Response (200 OK)
- **Headers**:
  - `Content-Type`: `application/json`
- **Body**:
```json
{
  "results": [
    {
      "content": "string (required) - The content snippet returned from the search",
      "source": "string (required) - URL pointing to the source of the content",
      "score": "number (required) - Similarity score between 0 and 1, where 1 is highest similarity"
    }
  ]
}
```

### Error Response (4xx/5xx)
- **Headers**:
  - `Content-Type`: `application/json`
- **Body**:
```json
{
  "error": "string - Error message explaining the failure"
}
```

## Example Request
```
POST /retrieve
Content-Type: application/json

{
  "query": "How does semantic search work?"
}
```

## Example Response
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "results": [
    {
      "content": "Semantic search works by understanding the meaning and context of search queries rather than just matching keywords...",
      "source": "https://example.com/semantic-search-intro",
      "score": 0.95
    },
    {
      "content": "In semantic search, queries are converted to vector embeddings which are then compared to document embeddings in the vector database...",
      "source": "https://example.com/semantic-search-technical",
      "score": 0.87
    }
  ]
}
```

## Validation Rules
- Query text should be between 1 and 500 characters
- Results array can be empty if no matches found
- Each result must include content, source, and score fields
- Score value must be between 0 and 1 (inclusive)
- Source must be a valid URL format

## Error Scenarios
- 400 Bad Request: Query parameter missing or invalid
- 404 Not Found: Endpoint does not exist
- 422 Unprocessable Entity: Query format is invalid
- 500 Internal Server Error: Backend error processing the request
- 503 Service Unavailable: Backend service is temporarily unavailable