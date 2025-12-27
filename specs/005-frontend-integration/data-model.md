# Data Model: Frontend Authentication, Personalization, and Translation Integration

## Overview
This document defines the frontend data models for the authentication, personalization, and translation system. Since the backend handles the primary data storage, this focuses on frontend state and API response structures.

## Authentication Context State

### Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| user | Object or null | No | User object when authenticated, null when not |
| token | String | No | JWT token when authenticated, null when not |
| isAuthenticated | Boolean | Yes | Authentication status |
| loading | Boolean | Yes | Whether authentication operations are in progress |
| error | String or null | No | Error message if authentication failed |

### User Object Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | String | Yes | User ID from backend |
| email | String | Yes | User's email |
| programming_level | String | Yes | User's programming level (beginner/intermediate/advanced) |
| ai_experience | String | Yes | User's AI experience level |
| gpu_available | Boolean | Yes | Whether user has GPU available |
| ram_size | String | Yes | Amount of RAM user has |

## Chapter Content State

### Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| originalContent | String | Yes | The original chapter content |
| modifiedContent | String | No | Personalized or translated content |
| isModified | Boolean | Yes | Whether content has been modified |
| contentType | String | Yes | Either "original", "personalized", or "translated" |

## API Response Models

### Auth Response Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| access_token | String | Yes | JWT access token |
| token_type | String | Yes | Token type (typically "bearer") |

### Personalization Response Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| success | Boolean | Yes | Whether the operation was successful |
| personalized_content | String | Yes | The personalized content |
| processing_time | Number | No | Time taken for processing |

### Translation Response Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| success | Boolean | Yes | Whether the operation was successful |
| translated_content | String | Yes | The translated content |
| language | String | Yes | The target language code (e.g., "ur") |
| processing_time | Number | No | Time taken for processing |

## Validation Rules
- JWT tokens must be properly formatted and not expired
- Content length should be within reasonable limits to prevent performance issues
- User profile fields must match the expected format from the backend

## Frontend State Relationships
- Authentication context state is shared across the entire application
- Chapter content state is local to each chapter page/component
- Error and loading states are managed per component/api call