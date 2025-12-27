# Research Summary: RAG Chatbot Implementation

## 1. Qdrant Integration for Similarity Threshold

**Decision**: Implement similarity threshold using Qdrant's score-based filtering

**Rationale**: Qdrant provides built-in scoring for vector similarity searches. We can set a minimum threshold score (e.g., 0.7) below which results are considered insufficiently relevant.

**Implementation approach**:
- Use Qdrant's `score_threshold` parameter in search queries
- Default threshold of 0.7, adjustable based on testing
- If no results meet threshold, return "not enough information" response

**Alternatives considered**:
- Cosine similarity calculation on retrieved vectors (more complex, redundant with Qdrant's built-in feature)
- Fixed number of top results without scoring (less precise, doesn't account for varying relevance)

## 2. Selected Text Handling

**Decision**: Implement conditional retrieval logic that bypasses vector search when selected text is provided

**Rationale**: When users select specific text, they want answers only from that context. The system should skip the Qdrant retrieval process entirely and use the selected text as the exclusive context.

**Implementation approach**:
- Check if `selected_text` parameter is provided in the API request
- If provided, use only the selected text as context for the LLM
- If not provided, proceed with normal Qdrant retrieval
- Add validation to ensure selected text is not empty or too short

**Alternatives considered**:
- Merging selected text with retrieved results (complicates logic, may dilute focus)
- Using selected text as additional filter in Qdrant search (not directly supported, complex implementation)

## 3. Confidence Level Calculation

**Decision**: Calculate confidence based on similarity scores and context relevance

**Rationale**: Confidence levels help users understand the reliability of responses. High confidence indicates strong match between query and context, while low confidence suggests the answer may be uncertain.

**Implementation approach**:
- High (0.8-1.0): Multiple high-scoring chunks with strong semantic match to query
- Medium (0.6-0.79): Single high-scoring chunk or multiple medium-scoring chunks
- Low (0.0-0.59): No high-scoring chunks or very low similarity scores

**Alternatives considered**:
- Fixed confidence based on number of retrieved chunks (doesn't account for relevance)
- LLM-generated confidence scores (adds complexity, potential for hallucination)

## 4. FastAPI Endpoint Design

**Decision**: Create a flexible `/chat` endpoint that accepts all required parameters with proper validation

**Rationale**: The endpoint needs to handle both regular queries and those with selected text, while maintaining proper error handling and validation.

**Implementation approach**:
- Use Pydantic models for request/response validation
- Implement proper error handling with HTTP status codes (422 for validation errors)
- Include rate limiting to prevent abuse
- Add proper documentation with OpenAPI schema

**Request model**:
```python
class ChatRequest(BaseModel):
    query: str
    book_id: str
    session_id: str
    selected_text: Optional[str] = None
```

**Alternatives considered**:
- Separate endpoints for different query types (increases complexity, harder to maintain)
- Query parameters instead of request body (less structured, harder to validate)

## 5. Database Schema for Chat History

**Decision**: Extend existing models to include confidence levels and maintain session structure

**Rationale**: Need to store conversation history with all relevant metadata for user experience and potential analytics.

**Implementation approach**:
- Add confidence_level field to chat message model
- Use existing Neon Postgres models where possible
- Create proper indexes for efficient retrieval by session_id

**Schema additions**:
```sql
-- Add confidence_level column to existing chat messages table
ALTER TABLE chat_messages ADD COLUMN confidence_level VARCHAR(10);
-- Add indexes for efficient queries
CREATE INDEX idx_session_id ON chat_messages(session_id);
```

**Alternatives considered**:
- Separate table for confidence levels (adds complexity to queries)
- JSON field for all metadata (less structured, harder to query)

## 6. Frontend Integration

**Decision**: Implement text selection capture and confidence display using existing ChatKit framework

**Rationale**: Need to maintain consistency with existing frontend architecture while adding required functionality.

**Implementation approach**:
- Add text selection event listeners to book content
- Send selected text as part of chat requests
- Display confidence badges using CSS styling
- Implement clear error messages using existing UI components

**Alternatives considered**:
- Custom chat interface (requires more development, breaks consistency)
- Confidence display as text instead of badge (less visual impact, harder to scan)

## Best Practices for Technology Integration

### FastAPI Best Practices
- Use dependency injection for service layer
- Implement proper error handling with custom exceptions
- Use middleware for authentication and logging
- Apply validation at API boundaries

### Qdrant Best Practices
- Use batching for multiple queries when possible
- Implement proper indexing strategies
- Monitor and adjust similarity thresholds based on performance
- Implement fallback strategies when vector search fails

### Frontend Best Practices
- Maintain responsive design for mobile compatibility
- Implement proper loading states for chat interactions
- Ensure accessibility standards are met
- Optimize for 3G connections as per constitution