# Translation API Contract

## POST /api/v1/translate/
**Description**: Translate book content from English to Urdu or other supported languages

### Request
- **Content-Type**: `application/json`
- **Headers**:
  - `Authorization: Bearer <jwt_token>` (optional)
- **Body**:
  ```json
  {
    "content_id": "chapter-001",
    "target_language": "ur",
    "text": "Physical AI combines robotics, machine learning, and embodied intelligence to create systems that can interact with the physical world."
  }
  ```

### Response
- **200 OK**:
  ```json
  {
    "success": true,
    "content_id": "chapter-001",
    "translated_text": "فزیکل ای آئی روبوٹکس، مشین لرننگ، اور امبدڈ انٹیلی جنس کو ملانے سے نظم کے ساتھ جسمانی دنیا کے ساتھ بات چیت کر سکتی ہے۔",
    "target_language": "ur",
    "status": "completed"
  }
  ```

- **400 Bad Request**: Missing required fields or unsupported language
- **500 Internal Server Error**: Translation service unavailable
- **429 Too Many Requests**: Rate limit exceeded

## GET /api/v1/translate/{content_id}/{language}
**Description**: Retrieve previously translated content

### Request
- **Path Parameters**:
  - `content_id`: The ID of the original content
  - `language`: The target language code (e.g., "ur")

### Response
- **200 OK**:
  ```json
  {
    "content_id": "chapter-001",
    "original_text": "Physical AI combines robotics, machine learning, and embodied intelligence...",
    "translated_text": "فزیکل ای آئی روبوٹکس، مشین لرننگ، اور امبدڈ انٹیلی جنس کو ملانے سے نظم کے ساتھ جسمانی دنیا کے ساتھ بات چیت کر سکتی ہے...",
    "language": "ur",
    "created_at": "2025-12-18T10:00:00Z",
    "status": "completed"
  }
  ```

- **404 Not Found**: Translation does not exist
- **400 Bad Request**: Invalid language code

## POST /api/v1/translate/bulk
**Description**: Translate multiple chapters at once

### Request
- **Content-Type**: `application/json`
- **Headers**:
  - `Authorization: Bearer <jwt_token>` (optional)
- **Body**:
  ```json
  {
    "target_language": "ur",
    "items": [
      {
        "content_id": "chapter-001",
        "text": "Introduction to Physical AI..."
      },
      {
        "content_id": "chapter-002", 
        "text": "Robotics Fundamentals..."
      }
    ]
  }
  ```

### Response
- **200 OK**:
  ```json
  {
    "success": true,
    "results": [
      {
        "content_id": "chapter-001",
        "status": "completed",
        "translated_text": "فزیکل ای آئی کا تعارف..."
      },
      {
        "content_id": "chapter-002",
        "status": "completed", 
        "translated_text": "روبوٹکس کے بنیادیات..."
      }
    ]
  }
  ```

- **400 Bad Request**: Missing required fields or unsupported language
- **500 Internal Server Error**: Translation service unavailable
- **429 Too Many Requests**: Rate limit exceeded