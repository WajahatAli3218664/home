# Data Model: Textbook Generation Feature

## Overview
This document defines the data models for the textbook generation feature, based on the key entities identified in the feature specification.

## Entity Models

### User Profile
Represents a user with attributes including background level, preferences, progress tracking, and authentication details.

**Fields:**
- `id` (string): Unique identifier for the user
- `email` (string): User's email address (unique)
- `name` (string): User's display name
- `background_level` (string): User's background level (enum: 'beginner', 'intermediate', 'advanced')
- `preferences` (json): User preferences including language settings and UI preferences
- `created_at` (datetime): Account creation timestamp
- `updated_at` (datetime): Last update timestamp
- `last_login` (datetime): Last login timestamp

**Validations:**
- Email must be valid and unique
- Background level must be one of the defined enum values
- Created_at and updated_at are automatically managed

### Textbook Chapter
Represents a single chapter with content, metadata, and relationships to quizzes and summaries.

**Fields:**
- `id` (string): Unique identifier for the chapter
- `title` (string): Title of the chapter
- `slug` (string): URL-friendly identifier for the chapter
- `content` (text): Main content of the chapter
- `version` (string): Version identifier for the chapter
- `position` (integer): Position of the chapter in the book sequence
- `word_count` (integer): Number of words in the chapter
- `estimated_reading_time` (integer): Estimated reading time in minutes
- `metadata` (json): Additional metadata about the chapter
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

**Validations:**
- Title and slug are required
- Position must be unique within the textbook
- Estimated reading time must be positive
- Version follows semantic versioning format

### AI Chat Interaction
Represents a conversation between a user and the RAG-powered chatbot.

**Fields:**
- `id` (string): Unique identifier for the chat interaction
- `user_id` (string): Reference to the user
- `session_id` (string): Identifier for the chat session
- `query` (text): The question asked by the user
- `response` (text): The response provided by the AI
- `context_used` (text): The textbook content used to generate the response
- `timestamp` (datetime): When the interaction occurred
- `feedback` (json): User feedback about the response quality

**Validations:**
- User_id must reference a valid user
- Query and response are required
- Timestamp is automatically set

### Learning Materials
Represents auto-generated content including summaries, quizzes, and learning boosters for each chapter.

**Fields:**
- `id` (string): Unique identifier for the learning material
- `chapter_id` (string): Reference to the associated chapter
- `material_type` (string): Type of material (enum: 'summary', 'quiz', 'learning_booster')
- `content` (text): The actual material content
- `version` (string): Version of the learning material
- `metadata` (json): Additional metadata about the material
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

**Validations:**
- Chapter_id must reference a valid chapter
- Material_type must be one of the defined enum values
- Content is required

### User Progress
Tracks a user's progress through the textbook content.

**Fields:**
- `id` (string): Unique identifier for the progress record
- `user_id` (string): Reference to the user
- `chapter_id` (string): Reference to the chapter
- `content_version` (string): Version of content when progress was recorded
- `progress_percentage` (float): Progress as percentage (0-100)
- `last_accessed` (datetime): When the content was last accessed
- `completed` (boolean): Whether the chapter is completed
- `quiz_score` (json): Scores for quizzes associated with this chapter
- `time_spent` (integer): Time spent on the chapter in seconds

**Validations:**
- User_id and chapter_id must form a unique combination
- Progress_percentage must be between 0 and 100
- Time_spent must be non-negative

### Content Version
Manages content versioning to handle updates to textbook chapters.

**Fields:**
- `id` (string): Unique identifier for the version record
- `chapter_id` (string): Reference to the chapter
- `version` (string): Version identifier (e.g., "1.0.0")
- `content_hash` (string): Hash of the content to detect changes
- `created_at` (datetime): When this version was created
- `is_active` (boolean): Whether this is the current active version

**Validations:**
- Chapter_id and version combination must be unique
- Only one version per chapter can be active at a time

### Translation Cache
Caches translated content to improve performance of Urdu translation feature.

**Fields:**
- `id` (string): Unique identifier for the cache record
- `chapter_id` (string): Reference to the chapter
- `content_version` (string): Version of the original content
- `target_language` (string): Target language code (e.g., "ur")
- `translated_content` (text): The translated content
- `created_at` (datetime): When this translation was cached
- `expires_at` (datetime): When this cache entry expires

**Validations:**
- Chapter_id and target_language combination must be unique per content_version
- Expires_at must be in the future

## Relationships

### User Profile → User Progress
- One-to-many relationship
- A user can have progress records for multiple chapters

### Textbook Chapter → User Progress
- One-to-many relationship
- A chapter can have progress records for multiple users

### Textbook Chapter → AI Chat Interaction
- One-to-many relationship
- A chapter's content can be referenced in multiple chat interactions

### Textbook Chapter → Learning Materials
- One-to-many relationship
- A chapter can have multiple learning materials (summary, quiz, booster)

### Textbook Chapter → Content Version
- One-to-many relationship
- A chapter can have multiple versions over time

### User Profile → AI Chat Interaction
- One-to-many relationship
- A user can have multiple chat interactions

## Indexes

For optimal performance, the following indexes should be created:

1. User Profile: Index on `email`
2. Textbook Chapter: Index on `slug`, `position`
3. User Progress: Composite index on `user_id`, `chapter_id`
4. AI Chat Interaction: Index on `user_id`, `session_id`, `timestamp`
5. Learning Materials: Index on `chapter_id`, `material_type`
6. Content Version: Index on `chapter_id`, `version`, `is_active`

## State Transitions

### User Progress States
- `not_started` → `in_progress` → `completed`
- Progress percentage increases as user engages with content
- Completed status is set when user finishes the chapter

### Content Version States
- New version created with `is_active=false`
- When published, current active version becomes inactive
- New version becomes active