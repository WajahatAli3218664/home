# Data Model: Physical AI & Humanoid Robotics Textbook

## Entities

### Chapter
Represents a single unit of instruction with defined structure (introduction, concepts, visuals, summaries, quizzes)

**Fields:**
- `id` (string): Unique identifier for the chapter
- `title` (string): Title of the chapter
- `slug` (string): URL-friendly identifier
- `content` (string): The main content of the chapter in MDX format
- `duration` (number): Estimated reading time in minutes
- `module_id` (string): Reference to the curriculum module this chapter belongs to
- `order` (number): The sequence number within the curriculum
- `learning_objectives` (string[]): List of learning objectives for this chapter
- `prerequisites` (string[]): List of prerequisite knowledge required
- `quiz_questions` (QuizQuestion[]): Array of quiz questions associated with this chapter

**Validation Rules:**
- `title` must be between 5-100 characters
- `duration` must be ≤ 4 minutes (to meet 45-min total requirement)
- `content` must be in valid MDX format
- `order` must be unique within the module
- `learning_objectives` must have 1-5 items

### Curriculum Module
Groups chapters by topic area (ROS 2, simulation, NVIDIA Isaac, VLA) with specific learning objectives

**Fields:**
- `id` (string): Unique identifier for the module
- `title` (string): Title of the module
- `slug` (string): URL-friendly identifier
- `description` (string): Brief description of the module
- `topic_area` (string): The topic area (ROS 2, Simulation, NVIDIA Isaac, VLA)
- `chapters` (string[]): Array of chapter IDs in this module
- `duration_range` (object): Min and max time range for the module (min, max in weeks)
- `learning_outcomes` (string[]): Learning outcomes expected from this module

**Validation Rules:**
- `title` must be between 5-80 characters
- `topic_area` must be one of the defined curriculum areas
- `chapters` must contain valid chapter IDs
- `duration_range.min` must be ≤ `duration_range.max`

### User Profile
Stores user background information for personalization and authentication

**Fields:**
- `id` (string): Unique identifier for the user
- `auth_id` (string): Authentication provider ID
- `email` (string): User's email address
- `name` (string): User's name
- `background` (string): User's background (e.g., Beginner, Intermediate, Advanced, Engineer, Student)
- `preferred_language` (string): Preferred language (default: English)
- `learning_preferences` (object): Preferences for content delivery
- `progress` (object[]): Track user progress through chapters
- `personalization_settings` (object): Settings for content adaptation

**Validation Rules:**
- `email` must be a valid email format
- `background` must be one of predefined values
- `preferred_language` must be supported by the system (English, Urdu initially)
- `progress` must contain valid chapter IDs

### Chat Query
Represents a user question to the RAG system with proper grounding and citation

**Fields:**
- `id` (string): Unique identifier for the query
- `user_id` (string): Reference to the user who made the query
- `question` (string): The original question text
- `context` (string): Additional context provided by the user
- `timestamp` (datetime): When the query was made
- `sources` (string[]): Array of source document IDs referenced in the response
- `response` (string): The RAG-generated response
- `is_ground_validated` (boolean): Whether the response was validated against book content
- `confidence_score` (number): Confidence score for the response (0-1)

**Validation Rules:**
- `question` must be between 5-500 characters
- `sources` must contain valid document IDs
- `confidence_score` must be between 0-1
- `is_ground_validated` must be true for all responses

### Translation Unit
Represents content that can be translated while preserving technical accuracy

**Fields:**
- `id` (string): Unique identifier for the translation unit
- `source_content_id` (string): ID of the original content
- `source_language` (string): Source language code (e.g., 'en')
- `target_language` (string): Target language code (e.g., 'ur')
- `content_type` (string): Type of content (chapter, quiz, term)
- `translations` (object): Map of content elements to translations
- `terminology_mapping` (object): Mapping of technical terms
- `review_status` (string): Status of translation review
- `last_updated` (datetime): When translation was last updated

**Validation Rules:**
- `source_language` and `target_language` must be valid language codes
- `content_type` must be one of predefined types
- `review_status` must be one of: 'pending', 'reviewed', 'approved'
- `terminology_mapping` must preserve technical meaning

### Quiz Question
Represents a question in the quiz section of a chapter

**Fields:**
- `id` (string): Unique identifier for the question
- `chapter_id` (string): Reference to the chapter this question belongs to
- `question_text` (string): The text of the question
- `options` (string[]): Array of possible answers
- `correct_answer` (string): The correct answer
- `explanation` (string): Explanation for the correct answer
- `difficulty` (string): Difficulty level (easy, medium, hard)
- `question_type` (string): Type of question (multiple-choice, true-false, short-answer)

**Validation Rules:**
- `question_text` must be between 10-500 characters
- `options` must have 2-6 items
- `correct_answer` must be one of the options
- `difficulty` must be one of the predefined values
- `question_type` must be one of the predefined values

## Relationships

- Curriculum Module (1) → (Many) Chapter
- User Profile (1) → (Many) Chat Query
- Chapter (1) → (Many) Quiz Question
- Translation Unit (1) → (Many) Chapter (or other content types)

## State Transitions

### Quiz Question
- Draft → Published (when added to a chapter)
- Published → Archived (when chapter is updated significantly)

### Translation Unit
- Pending → Reviewing (when initial translation is complete)
- Reviewing → Approved (when reviewed and confirmed accurate)
- Approved → Needs Update (when source content changes)

## Indexes

- User Profile: email (unique), auth_id (unique)
- Chapter: slug (unique), module_id
- Chat Query: user_id, timestamp
- Translation Unit: source_content_id, source_language, target_language (unique combination)