# Auth API Contract

## POST /api/v1/auth/signup
**Description**: Register a new user and collect their background information

### Request
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "username": "john_doe",
    "password": "securePassword123",
    "programming_level": "intermediate",
    "software_experience": "3-5 years",
    "hardware_background": "beginner"
  }
  ```

### Response
- **201 Created**:
  ```json
  {
    "success": true,
    "user": {
      "id": "user-123",
      "email": "user@example.com",
      "username": "john_doe",
      "programming_level": "intermediate",
      "software_experience": "3-5 years",
      "hardware_background": "beginner"
    },
    "token": "jwt_token_here"
  }
  ```

- **400 Bad Request**: Invalid input data
- **409 Conflict**: User already exists

## POST /api/v1/auth/signin
**Description**: Authenticate user and return session token

### Request
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123"
  }
  ```

### Response
- **200 OK**:
  ```json
  {
    "success": true,
    "user": {
      "id": "user-123",
      "email": "user@example.com",
      "username": "john_doe",
      "programming_level": "intermediate",
      "software_experience": "3-5 years",
      "hardware_background": "beginner"
    },
    "token": "jwt_token_here"
  }
  ```

- **401 Unauthorized**: Invalid credentials
- **400 Bad Request**: Missing required fields

## GET /api/v1/auth/me
**Description**: Get current user information

### Request
- **Headers**:
  - `Authorization: Bearer <jwt_token>`

### Response
- **200 OK**:
  ```json
  {
    "id": "user-123",
    "email": "user@example.com",
    "username": "john_doe",
    "programming_level": "intermediate",
    "software_experience": "3-5 years",
    "hardware_background": "beginner",
    "created_at": "2025-12-18T10:00:00Z"
  }
  ```

- **401 Unauthorized**: Invalid or missing token