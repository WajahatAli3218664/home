# API Contract: Book RAG System

## 1. Book Processing Endpoints

### POST /api/v1/books/process
Process a book and create vector embeddings

**Request**:
```json
{
  "book_id": "string",
  "title": "string",
  "content": "string",
  "language": "string",
  "chunking_strategy": "intelligent|by_chapter|by_section"
}
```

**Response (200)**:
```json
{
  "status": "success",
  "message": "Book processed successfully",
  "embedding_count": "number",
  "processing_time": "number"
}
```

**Response (400)**:
```json
{
  "status": "error",
  "message": "Invalid input data"
}
```

## 2. RAG Query Endpoints

### POST /api/v1/rag/query
Ask a question about the book content

**Request**:
```json
{
  "query": "string",
  "book_id": "string",
  "session_id": "string",
  "language": "string"
}
```

**Response (200)**:
```json
{
  "query_id": "string",
  "response": "string",
  "confidence_score": "number",
  "citations": [
    {
      "chunk_id": "string",
      "content": "string",
      "page": "string",
      "chapter": "string"
    }
  ],
  "response_time": "number"
}
```

### POST /api/v1/rag/query-selected
Ask a question about selected text only

**Request**:
```json
{
  "query": "string",
  "selected_text": "string",
  "session_id": "string",
  "language": "string"
}
```

**Response (200)**:
```json
{
  "query_id": "string",
  "response": "string",
  "confidence_score": "number",
  "citations": [],
  "response_time": "number"
}
```

## 3. Translation Endpoints

### GET /api/v1/translation/toggle
Toggle language preference

**Query Parameters**:
- `target_language`: "ur|en"
- `session_id`: "string"

**Response (200)**:
```json
{
  "status": "success",
  "message": "Language preference updated",
  "current_language": "string"
}
```

### POST /api/v1/translation/translate
Translate book content to Urdu

**Request**:
```json
{
  "content": "string",
  "source_language": "string",
  "target_language": "string"
}
```

**Response (200)**:
```json
{
  "status": "success",
  "translated_content": "string",
  "processing_time": "number"
}
```

## 4. Vector Search Endpoints

### POST /api/v1/search/semantic
Perform semantic search within book content

**Request**:
```json
{
  "query": "string",
  "book_id": "string",
  "limit": "number",
  "filters": {
    "chapter": "string",
    "section": "string",
    "language": "string"
  }
}
```

**Response (200)**:
```json
{
  "results": [
    {
      "chunk_id": "string",
      "content": "string",
      "similarity_score": "number",
      "metadata": {
        "chapter": "string",
        "section": "string",
        "page": "string",
        "language": "string"
      }
    }
  ],
  "search_time": "number"
}
```