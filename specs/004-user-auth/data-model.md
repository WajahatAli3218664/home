# Data Model: Auth, Personalization, and Translation System

## Overview
This document defines the data models for the authentication, personalization, and translation system based on the feature specification and technical requirements.

## User Entity

### Schema
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the user |
| email | String (255) | Unique, Not Null | User's email address for authentication |
| programming_level | Enum | Not Null | User's programming level (beginner, intermediate, advanced) |
| ai_experience | Enum | Not Null | User's AI experience level (none, basic, intermediate, advanced) |
| gpu_available | Boolean | Not Null | Whether user has access to GPU |
| ram_size | String (50) | Not Null | Amount of RAM available (e.g., "8GB", "16GB") |
| created_at | Timestamp | Not Null | When the user account was created |

### Validation Rules
- Email must be a valid email format
- Programming level must be one of: "beginner", "intermediate", "advanced"
- AI experience must be one of: "none", "basic", "intermediate", "advanced"
- RAM size must follow format like "4GB", "8GB", "16GB", "32GB"

## Translation Entity

### Schema
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the translation |
| user_id | UUID | Foreign Key, Not Null | Reference to the user who requested the translation |
| chapter_id | String (100) | Not Null | Identifier for the chapter that was translated |
| language | String (10) | Not Null | Language code (e.g., "ur" for Urdu) |
| translated_content | Text | Not Null | The translated content |
| created_at | Timestamp | Not Null | When the translation was created |

### Validation Rules
- Language must be a valid language code
- Chapter ID must exist in the content management system
- There should be a unique constraint on user_id, chapter_id, and language to prevent duplicate translations

## Relationships
- A User can have 0 or more Translations (one-to-many relationship)
- Each Translation is associated with exactly one User

## State Transitions
The data model doesn't include specific state transitions beyond creation, as the entities are primarily storage-focused rather than workflow-driven.

## Additional Considerations
- Indexes should be created on frequently queried fields (user_id, chapter_id, language)
- Translation content should be efficiently stored to handle potential large volumes of text
- Created_at timestamps should be indexed for efficient query performance when retrieving recent translations