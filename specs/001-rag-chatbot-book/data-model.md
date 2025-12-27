# Data Model: RAG Chatbot in Published Book

## Entities

### 1. ChatSession
Represents a conversation session between a user and the chatbot

**Fields**:
- `session_id`: String (Primary Key) - Unique identifier for the session
- `user_id`: String (Foreign Key) - Reference to the user (optional for anonymous sessions)
- `book_id`: String - Reference to the book being queried
- `created_at`: DateTime - When the session was created
- `updated_at`: DateTime - When the session was last updated
- `metadata`: JSON - Additional session information

**Validation**:
- `session_id` must be unique
- `book_id` must reference an existing book
- `created_at` and `updated_at` are automatically set by the system

### 2. ChatMessage
Represents a single message in the conversation (either user query or bot response)

**Fields**:
- `message_id`: String (Primary Key) - Unique identifier for the message
- `session_id`: String (Foreign Key) - Reference to the parent session
- `role`: String - Either "user" or "assistant"
- `content`: String - The actual message content
- `timestamp`: DateTime - When the message was created
- `confidence_level`: String - Confidence level of the response ("High", "Medium", "Low")
- `retrieved_context_ids`: Array<String> - IDs of the context chunks used for this response
- `query_type`: String - Either "general" or "selected_text" indicating the query type

**Validation**:
- `role` must be either "user" or "assistant"
- `confidence_level` must be one of "High", "Medium", or "Low"
- `query_type` must be either "general" or "selected_text"
- `content` must not be empty
- `session_id` must reference an existing session

### 3. RetrievedContext
Represents a chunk of book content retrieved for answering a query

**Fields**:
- `context_id`: String (Primary Key) - Unique identifier for the context chunk
- `book_id`: String - Reference to the book
- `chunk_text`: String - The actual text chunk
- `chunk_metadata`: JSON - Additional metadata about the chunk (page number, chapter, etc.)
- `similarity_score`: Float - Similarity score from vector search (0.0 to 1.0)
- `embedding_id`: String - Reference to the vector embedding in Qdrant

**Validation**:
- `similarity_score` must be between 0.0 and 1.0
- `chunk_text` must not be empty
- `book_id` must reference an existing book

### 4. BookContent
Represents the book content that the chatbot queries

**Fields**:
- `book_id`: String (Primary Key) - Unique identifier for the book
- `title`: String - Title of the book
- `author`: String - Author of the book
- `content_type`: String - Type of content (e.g., "textbook", "manual")
- `created_at`: DateTime - When the book content was added
- `updated_at`: DateTime - When the book content was last updated
- `metadata`: JSON - Additional book metadata

**Validation**:
- `book_id` must be unique
- `title` must not be empty
- `content_type` must be one of predefined values

### 5. UserSessionPreference
Stores user preferences for the chat session (optional, for personalization)

**Fields**:
- `preference_id`: String (Primary Key) - Unique identifier for the preference
- `session_id`: String (Foreign Key) - Reference to the session
- `language_preference`: String - Language for responses (default: "en")
- `response_style`: String - Style of responses (e.g., "formal", "casual", "technical")
- `last_selected_text`: String - Last selected text for context (for continuity)

**Validation**:
- `session_id` must reference an existing session
- `language_preference` must be one of supported languages
- `response_style` must be one of predefined values

## Relationships

1. **ChatSession** (1) → (Many) **ChatMessage**: A session contains multiple messages
2. **ChatMessage** (Many) → (Many) **RetrievedContext**: A message can reference multiple context chunks
3. **BookContent** (1) → (Many) **RetrievedContext**: A book contains multiple context chunks
4. **ChatSession** (1) → (0 or 1) **UserSessionPreference**: A session may have user preferences

## State Transitions

### ChatSession States
- `ACTIVE`: Session is currently active with recent messages
- `INACTIVE`: Session has no activity for a period (configurable)
- `ARCHIVED`: Session is closed and read-only

### ChatMessage States
- `PENDING`: Message is being processed
- `COMPLETE`: Message is fully processed and stored
- `ERROR`: Message processing failed

## Validation Rules

1. **Temporal Consistency**: Messages in a session must be ordered by timestamp
2. **Content Completeness**: Each user message must have a corresponding assistant response
3. **Confidence Validity**: Confidence level must be provided for all assistant messages
4. **Context Relevance**: Retrieved context must have a minimum similarity score (configurable)
5. **Session Integrity**: Sessions must have a valid book_id that exists in BookContent