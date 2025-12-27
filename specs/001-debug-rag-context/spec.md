# Feature Specification: Debug RAG Context Flow

**Feature Branch**: `001-debug-rag-context`
**Created**: 2025-12-24
**Status**: Draft
**Input**: User description: "You are debugging a RAG chatbot. Issue: LLM replies with a generic chat response and ignores my textbook data. Setup: - Vector DB: Qdrant (data ingested) - LLM: Qwen - Backend: Python - RAG based chatbot Task: 1. Find why retrieved context is not reaching the LLM. 2. List exact mistakes that cause chat-only responses. 3. Show how to inject retrieved text into the prompt. 4. Give a minimal working RAG prompt. 5. Show how to log/print context before LLM call. Be concise and practical."

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Debug RAG Context Flow (Priority: P1)

As a developer maintaining the RAG chatbot, I need to identify why the retrieved context from Qdrant is not being passed to the LLM so that the chatbot can generate responses based on the textbook data instead of generic responses.

**Why this priority**: This is the core issue preventing the RAG system from functioning as intended. Without fixing this, the entire RAG functionality is broken and users get no benefit from the textbook data.

**Independent Test**: Can be fully tested by running a query against the system and verifying that the retrieved context is included in the LLM prompt, resulting in responses that reference the textbook data.

**Acceptance Scenarios**:

1. **Given** a user query that should match textbook content in Qdrant, **When** the RAG service retrieves relevant context and sends it to the LLM, **Then** the LLM response contains information from the retrieved context
2. **Given** a user query that should match textbook content in Qdrant, **When** I examine the logs before the LLM call, **Then** I can see the retrieved context being passed to the LLM

---

### User Story 2 - Implement Proper Context Injection (Priority: P2)

As a developer, I need to implement the correct mechanism to inject retrieved text into the LLM prompt so that the LLM has access to the relevant textbook data when generating responses.

**Why this priority**: This is essential for the RAG system to work correctly. The retrieved context must be properly formatted and included in the prompt sent to the LLM.

**Independent Test**: Can be tested by examining the prompt structure sent to the LLM and verifying that it contains the retrieved context in the expected format.

**Acceptance Scenarios**:

1. **Given** a user query and retrieved context from Qdrant, **When** the system constructs the LLM prompt, **Then** the prompt contains both the user query and the retrieved context in the proper format

---

### User Story 3 - Create Minimal Working RAG Implementation (Priority: P3)

As a developer, I need to create a minimal working RAG implementation that demonstrates the correct flow from context retrieval to LLM response so that I have a reference for the proper implementation.

**Why this priority**: Having a working example will serve as a reference for the correct implementation and help ensure the main application code follows the same pattern.

**Independent Test**: Can be tested by running the minimal implementation and verifying that it successfully retrieves context and generates responses based on that context.

**Acceptance Scenarios**:

1. **Given** a minimal RAG implementation, **When** a query is submitted, **Then** the system retrieves relevant context and generates a response that incorporates the retrieved information

---

### Edge Cases

- What happens when the retrieval system returns no relevant context for a query?
- How does the system handle extremely long retrieved context that might exceed LLM token limits?
- What if the Qdrant vector database is temporarily unavailable during context retrieval?
- How does the system handle malformed or empty responses from the LLM?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST identify the exact point in the code where retrieved context is not being passed to the LLM
- **FR-002**: System MUST implement proper context injection into the LLM prompt so that retrieved text is included when generating responses
- **FR-003**: System MUST provide logging mechanism to print/observe the context being sent to the LLM before the call
- **FR-004**: System MUST create a minimal working RAG prompt that demonstrates the correct flow from context retrieval to LLM response
- **FR-005**: System MUST list common implementation mistakes that cause the RAG system to ignore retrieved context

### Key Entities

- **Retrieved Context**: Text data retrieved from Qdrant vector database that should be included in the LLM prompt
- **LLM Prompt**: The input sent to the Qwen LLM that should contain both user query and retrieved context
- **RAG Service**: The component responsible for retrieving context from Qdrant and preparing the prompt for the LLM

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The RAG chatbot generates responses that reference textbook data instead of generic responses, with at least 90% of responses containing information from retrieved context
- **SC-002**: Developers can observe the context being passed to the LLM through logging mechanism before each LLM call
- **SC-003**: A minimal working RAG implementation demonstrates the correct flow from context retrieval to LLM response
- **SC-004**: The debugging process identifies and documents all implementation mistakes that cause the RAG system to ignore retrieved context
- **SC-005**: The RAG system correctly injects retrieved text into the LLM prompt in 100% of test cases
