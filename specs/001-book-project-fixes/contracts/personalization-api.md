# Personalization API Contract

## POST /api/v1/personalize/{content_id}
**Description**: Adapt content based on user's background information

### Request
- **Content-Type**: `application/json`
- **Headers**:
  - `Authorization: Bearer <jwt_token>` (required)
- **Path Parameters**:
  - `content_id`: The ID of the content to personalize
- **Body**:
  ```json
  {
    "user_preferences": {
      "programming_level": "beginner",
      "software_experience": "0-1 years",
      "hardware_background": "none"
    },
    "personalization_level": "high"
  }
  ```

### Response
- **200 OK**:
  ```json
  {
    "success": true,
    "content_id": "chapter-001",
    "original_content": "Physical AI requires understanding of advanced robotics algorithms...",
    "personalized_content": "Physical AI means robots that can learn and adapt to their environment. Think of it like a child learning to walk and interact with objects around them...",
    "personalization_metadata": {
      "difficulty": "beginner",
      "examples_added": true,
      "technical_depth": "reduced"
    }
  }
  ```

- **400 Bad Request**: Missing required fields or unsupported personalization level
- **401 Unauthorized**: Invalid or missing token
- **404 Not Found**: Content does not exist
- **500 Internal Server Error**: Personalization service unavailable

## PUT /api/v1/user/preferences
**Description**: Update user's preferences that guide content personalization

### Request
- **Content-Type**: `application/json`
- **Headers**:
  - `Authorization: Bearer <jwt_token>`
- **Body**:
  ```json
  {
    "programming_level": "intermediate",
    "software_experience": "2-3 years",
    "hardware_background": "beginner",
    "learning_style": "visual",
    "interests": ["robotics", "ai"]
  }
  ```

### Response
- **200 OK**:
  ```json
  {
    "success": true,
    "message": "User preferences updated successfully"
  }
  ```

- **400 Bad Request**: Invalid preference values
- **401 Unauthorized**: Invalid or missing token

## GET /api/v1/user/preferences
**Description**: Retrieve user's preferences that guide content personalization

### Request
- **Headers**:
  - `Authorization: Bearer <jwt_token>`

### Response
- **200 OK**:
  ```json
  {
    "programming_level": "intermediate",
    "software_experience": "2-3 years",
    "hardware_background": "beginner",
    "learning_style": "visual",
    "interests": ["robotics", "ai"]
  }
  ```

- **401 Unauthorized**: Invalid or missing token