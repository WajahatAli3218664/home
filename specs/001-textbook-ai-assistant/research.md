# Research Summary: Textbook AI Assistant Implementation

## 1. Groq API Integration

**Decision**: Use the groq-sdk for Python to integrate with the Groq API

**Rationale**: The Groq API provides access to the llama3-8b-8192 model as required by the specification. The SDK offers a clean interface that can be integrated with the OpenAI Agents SDK.

**Implementation approach**:
- Install groq-sdk package
- Configure API key from environment variables
- Use the Groq client to make requests to the llama3-8b-8192 model
- Handle rate limiting and errors appropriately

**Alternatives considered**:
- Direct HTTP requests to Groq API (more complex, error-prone)
- Using different LLM providers (would not meet requirement for Groq)

## 2. OpenAI Agents SDK Usage

**Decision**: Implement the OpenAI Assistant API for LLM orchestration and tool-handling

**Rationale**: The OpenAI Agents SDK provides a structured way to orchestrate LLM interactions, manage conversations, and handle tools for retrieval-augmented generation.

**Implementation approach**:
- Create an assistant with specific instructions for textbook-only responses
- Implement a retrieval tool that fetches relevant textbook content from Qdrant
- Use thread management for conversation context
- Implement proper error handling and response validation

**Alternatives considered**:
- Using raw OpenAI API calls (less structured, more manual work)
- Custom orchestration framework (reinventing existing solutions)

## 3. Citation Generation

**Decision**: Implement automatic citation generation based on retrieved context metadata

**Rationale**: Every response must include citations indicating the source chapter and section. This requires tracking the source of retrieved content and formatting it appropriately.

**Implementation approach**:
- Store chapter, section, and page information in Qdrant metadata
- Retrieve this information along with the content chunks
- Format citations in the response using the specified format
- Include citations as part of the system prompt instructions

**Alternatives considered**:
- Manual citation by the LLM (less reliable, may not follow format)
- Separate citation service (adds complexity)

## 4. Selected Text Handling

**Decision**: Implement a bypass mechanism that uses selected text as the exclusive context

**Rationale**: When users select specific text, the system must respond only based on that text, bypassing the general retrieval process.

**Implementation approach**:
- Add a parameter to the API endpoint to accept selected text
- If selected text is provided, skip the Qdrant retrieval
- Use the selected text directly as the context for the LLM
- Apply the same grounding and citation rules to the selected text

**Alternatives considered**:
- Merging selected text with retrieved results (violates requirement for exclusive use)
- Using selected text as additional filter in Qdrant search (not directly supported)

## 5. Grounding Enforcement

**Decision**: Implement multi-layered validation to ensure responses only use textbook content

**Rationale**: The system must strictly adhere to textbook content with no hallucinations, which requires both LLM prompting and response validation.

**Implementation approach**:
- System prompt that explicitly forbids external knowledge
- Response validation using similarity checks against textbook content
- Fallback responses when content is not found in the textbook
- Clear messaging when information is not available

**Alternatives considered**:
- Relying solely on LLM training (not reliable enough for strict grounding)
- Complex semantic validation (too computationally expensive)

## 6. Frontend Integration

**Decision**: Integrate the AI assistant as a component within the Docusaurus textbook pages

**Rationale**: The assistant needs to be easily accessible to readers while maintaining the textbook's educational context.

**Implementation approach**:
- Create a React component for the AI assistant
- Add the component to textbook pages with appropriate styling
- Implement text selection capture functionality
- Ensure responsive design for mobile users
- Follow frontend minimalism principles from the constitution

**Alternatives considered**:
- Separate application interface (breaks textbook context)
- Floating chat widget (may be distracting)

## Best Practices for Technology Integration

### OpenAI Agents SDK Best Practices
- Use Assistant API for conversation state management
- Implement proper thread cleanup to manage state
- Use function calling for tool integration
- Implement error handling for API rate limits

### Groq API Best Practices
- Cache responses where appropriate to reduce API calls
- Implement proper error handling for API failures
- Monitor token usage to stay within limits
- Use appropriate temperature settings for factual responses

### Frontend Best Practices
- Maintain responsive design for mobile compatibility
- Implement proper loading states for AI interactions
- Ensure accessibility standards are met
- Optimize for 3G connections as per constitution