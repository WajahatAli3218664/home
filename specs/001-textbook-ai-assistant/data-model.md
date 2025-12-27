# Data Model: Textbook AI Assistant for Physical AI & Humanoid Robotics

## Entities

### 1. TextbookContent
Represents the textbook content that the AI assistant queries

**Fields**:
- `content_id`: String (Primary Key) - Unique identifier for the content chunk
- `book_id`: String - Reference to the textbook
- `chapter`: String - Chapter number/name
- `section`: String - Section within the chapter
- `page_number`: Integer - Page number in the textbook
- `content_text`: String - The actual text content
- `embedding_id`: String - Reference to the vector embedding in Qdrant
- `metadata`: JSON - Additional metadata about the content

**Validation**:
- `content_id` must be unique
- `book_id` must reference an existing textbook
- `content_text` must not be empty
- `chapter` and `section` must be provided

### 2. UserQuery
Represents a question or input from the reader that triggers the AI process

**Fields**:
- `query_id`: String (Primary Key) - Unique identifier for the query
- `session_id`: String - Reference to the user session
- `query_text`: String - The actual question from the user
- `timestamp`: DateTime - When the query was submitted
- `selected_text`: String (Optional) - Text selected by the user (if any)
- `source_context`: String - Where the query originated (e.g., chapter name)

**Validation**:
- `query_text` must not be empty
- `query_id` must be unique
- `timestamp` is automatically set by the system

### 3. RetrievedContext
Represents a chunk of textbook content retrieved for answering a query

**Fields**:
- `context_id`: String (Primary Key) - Unique identifier for the context chunk
- `query_id`: String (Foreign Key) - Reference to the original query
- `content_id`: String (Foreign Key) - Reference to the textbook content
- `text_chunk`: String - The specific text chunk used
- `similarity_score`: Float - Similarity score from vector search (0.0 to 1.0)
- `chapter`: String - Chapter where the content is from
- `section`: String - Section where the content is from
- `page_number`: Integer - Page number where the content is from

**Validation**:
- `similarity_score` must be between 0.0 and 1.0
- `text_chunk` must not be empty
- `content_id` must reference an existing textbook content

### 4. AIResponse
Represents the generated answer from the AI assistant based on the retrieved context

**Fields**:
- `response_id`: String (Primary Key) - Unique identifier for the response
- `query_id`: String (Foreign Key) - Reference to the original query
- `response_text`: String - The generated response text
- `timestamp`: DateTime - When the response was generated
- `citations`: Array<String> - List of citations used in the response
- `confidence_level`: String - Confidence level of the response ("High", "Medium", "Low")
- `grounding_status`: String - Whether the response is grounded ("Valid", "Not Found", "External")

**Validation**:
- `response_text` must not be empty
- `confidence_level` must be one of "High", "Medium", or "Low"
- `grounding_status` must be one of "Valid", "Not Found", or "External"

### 5. Citation
Represents the reference information that indicates the source of the answer within the textbook

**Fields**:
- `citation_id`: String (Primary Key) - Unique identifier for the citation
- `response_id`: String (Foreign Key) - Reference to the AI response
- `content_id`: String (Foreign Key) - Reference to the textbook content
- `chapter`: String - Chapter reference
- `section`: String - Section reference
- `page_number`: Integer - Page number reference
- `citation_format`: String - The formatted citation string

**Validation**:
- `chapter` and `section` must be provided
- `content_id` must reference an existing textbook content
- `citation_format` must follow the required format

### 6. UserSession
Represents a user's interaction session with the AI assistant

**Fields**:
- `session_id`: String (Primary Key) - Unique identifier for the session
- `user_id`: String (Optional) - Reference to the user (if authenticated)
- `book_id`: String - Reference to the textbook being queried
- `created_at`: DateTime - When the session was created
- `updated_at`: DateTime - When the session was last updated
- `metadata`: JSON - Additional session information

**Validation**:
- `session_id` must be unique
- `book_id` must reference an existing textbook

## Relationships

1. **UserSession** (1) → (Many) **UserQuery**: A session contains multiple queries
2. **UserQuery** (1) → (Many) **RetrievedContext**: A query can retrieve multiple context chunks
3. **RetrievedContext** (Many) → (1) **TextbookContent**: Context chunks come from textbook content
4. **UserQuery** (1) → (1) **AIResponse**: Each query generates one response
5. **AIResponse** (1) → (Many) **Citation**: A response can have multiple citations

## State Transitions

### UserQuery States
- `PENDING`: Query is being processed
- `PROCESSED`: Query has been processed and response generated
- `ERROR`: Error occurred during processing

### AIResponse States
- `GENERATING`: Response is being generated by the LLM
- `VALIDATED`: Response has passed grounding validation
- `REJECTED`: Response failed grounding validation

## Validation Rules

1. **Grounding Validation**: Responses must only contain information from the textbook content
2. **Citation Requirement**: Every response must include at least one citation
3. **Content Completeness**: Each response must address the original query
4. **Source Tracking**: Retrieved context must accurately reference the original textbook content
5. **Session Continuity**: Sessions must maintain context for multi-turn conversations