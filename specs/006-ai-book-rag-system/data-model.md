# Data Model: AI-Powered Book RAG System

## Entities

### Book Content
- **Fields**:
  - id (string): Unique identifier for the book
  - title (string): Title of the book
  - author (string): Author of the book
  - content (string): Raw text content of the book
  - language (string): Primary language of the book (e.g., 'en', 'ur')
  - translated_content (string): Translated content (if applicable)
  - metadata (object): Additional metadata about the book
  - created_at (datetime): Timestamp when the book was added
  - updated_at (datetime): Timestamp when the book was last updated

### Vector Embedding
- **Fields**:
  - id (string): Unique identifier for the embedding
  - book_id (string): Reference to the book this embedding belongs to
  - content_chunk (string): The text chunk that was embedded
  - embedding_vector (array[float]): The actual embedding vector
  - chapter (string): Chapter identifier
  - section (string): Section identifier
  - page (string): Page identifier
  - language (string): Language of the chunk
  - source (string): Source identifier (e.g., 'book')
  - created_at (datetime): Timestamp when the embedding was created

### Chat Session
- **Fields**:
  - id (string): Unique identifier for the session
  - user_id (string): Reference to the user (optional for anonymous sessions)
  - created_at (datetime): Timestamp when the session was created
  - updated_at (datetime): Timestamp when the session was last updated
  - language_preference (string): Language preference for the session ('en' or 'ur')

### User Query
- **Fields**:
  - id (string): Unique identifier for the query
  - session_id (string): Reference to the chat session
  - query_text (string): The original query text
  - language (string): Language of the query
  - created_at (datetime): Timestamp when the query was made

### AI Response
- **Fields**:
  - id (string): Unique identifier for the response
  - query_id (string): Reference to the user query
  - response_text (string): The AI-generated response
  - confidence_score (float): Confidence score of the response (0-1)
  - citations (array[object]): List of citations used in the response
  - retrieved_chunks (array[string]): IDs of the retrieved content chunks
  - created_at (datetime): Timestamp when the response was generated

### Retrieved Context
- **Fields**:
  - id (string): Unique identifier for the context
  - query_id (string): Reference to the user query
  - content_chunk_id (string): Reference to the vector embedding used
  - similarity_score (float): Similarity score of the match (0-1)
  - content_text (string): The actual content text retrieved

## Relationships

- Book Content → Vector Embedding (1 to many): A book can have many vector embeddings
- Chat Session → User Query (1 to many): A session can have many user queries
- User Query → AI Response (1 to 1): Each query has one response
- User Query → Retrieved Context (1 to many): A query can retrieve multiple context chunks
- Vector Embedding → Retrieved Context (1 to many): An embedding can be used in multiple contexts

## Validation Rules

- Book Content: Title and content are required fields
- Vector Embedding: book_id, content_chunk, and embedding_vector are required
- Chat Session: Must have either a user_id or be anonymous
- User Query: query_text is required and must not be empty
- AI Response: Must reference a valid user query and include response_text
- Retrieved Context: Must reference both a query and a content chunk