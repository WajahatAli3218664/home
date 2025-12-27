# Implementation Tasks: Debug RAG Context Flow

**Feature**: Debug RAG Context Flow
**Branch**: `001-debug-rag-context`
**Created**: 2025-12-24
**Input**: Feature specification from `/specs/001-debug-rag-context/spec.md`

## Dependencies

- User Story 2 (P2) depends on User Story 1 (P1) being completed first
- User Story 3 (P3) can be implemented in parallel with User Story 2 (P2) after User Story 1 (P1) is complete

## Parallel Execution Examples

- **User Story 2 (P2)**: [P] T012-T015 can be executed in parallel as they work on different components
- **User Story 3 (P3)**: [P] T016-T018 can be executed in parallel as they create separate debugging tools

## Implementation Strategy

1. **MVP Scope**: Complete User Story 1 (P1) to identify why retrieved context is not reaching the LLM and add logging mechanisms
2. **Incremental Delivery**: Each user story delivers an independently testable increment of functionality
3. **Risk Mitigation**: Focus on debugging and visibility first (P1), then implementation (P2), then reference examples (P3)

## Phase 1: Setup

### Goal
Initialize project structure and dependencies for the debugging effort.

- [X] T001 Set up Python 3.11 virtual environment for the debugging project
- [X] T002 Install required dependencies: FastAPI, Qdrant, Qwen SDK, Pydantic, Requests, pytest
- [X] T003 Configure environment variables for Qdrant and Qwen LLM access

## Phase 2: Foundational

### Goal
Establish foundational components needed across all user stories.

- [X] T004 Create DebugLog model in backend/src/models/debug_log.py based on data model
- [X] T005 Create LLM Prompt model in backend/src/models/llm_prompt.py based on data model
- [X] T006 Create RetrievedContext model in backend/src/models/retrieved_context.py based on data model
- [X] T007 Set up logging configuration in backend/src/config/logging.py for context flow tracking
- [X] T008 Create DebugService in backend/src/services/debug_service.py for logging context flow

## Phase 3: User Story 1 - Debug RAG Context Flow (Priority: P1)

### Goal
Identify why the retrieved context from Qdrant is not being passed to the LLM.

### Independent Test
Can be fully tested by running a query against the system and verifying that the retrieved context is included in the LLM prompt, resulting in responses that reference the textbook data.

- [X] T009 [US1] Analyze existing RAG service in backend/src/services/rag_service.py to identify context flow issues
- [X] T010 [US1] Add comprehensive logging to RAG service to track context flow before LLM call
- [X] T011 [US1] Create debug endpoint GET /debug/log-context in backend/src/api/debug.py to retrieve recent context
- [X] T012 [P] [US1] Create debug endpoint GET /debug/context-flow in backend/src/api/debug.py to test complete flow
- [X] T013 [P] [US1] Document all common RAG implementation mistakes identified during analysis
- [X] T014 [P] [US1] Create a debugging script in backend/src/debug/analyze_context_flow.py to trace context path

## Phase 4: User Story 2 - Implement Proper Context Injection (Priority: P2)

### Goal
Implement the correct mechanism to inject retrieved text into the LLM prompt.

### Independent Test
Can be tested by examining the prompt structure sent to the LLM and verifying that it contains the retrieved context in the expected format.

- [X] T015 [US2] Update RAG service to properly inject retrieved context into LLM prompt
- [X] T016 [P] [US2] Create prompt formatting utility in backend/src/utils/prompt_formatter.py
- [X] T017 [P] [US2] Update LLM service to use formatted prompts with context
- [X] T018 [P] [US2] Create validation function to ensure prompts contain both query and context

## Phase 5: User Story 3 - Create Minimal Working RAG Implementation (Priority: P3)

### Goal
Create a minimal working RAG implementation that demonstrates the correct flow.

### Independent Test
Can be tested by running the minimal implementation and verifying that it successfully retrieves context and generates responses based on that context.

- [X] T019 [US3] Create minimal RAG implementation in backend/src/debug/minimal_rag.py as reference
- [X] T020 [P] [US3] Create test script in backend/src/debug/test_minimal_rag.py to validate minimal implementation
- [X] T021 [P] [US3] Add debug endpoint POST /debug/test-prompt in backend/src/api/debug.py for prompt testing

## Phase 6: Polish & Cross-Cutting Concerns

### Goal
Finalize implementation with proper documentation, testing, and optimization.

- [X] T022 Add unit tests for all new services using pytest in backend/tests/test_debug_services.py
- [X] T023 Update API documentation with new debug endpoints
- [X] T024 Performance test the context flow to ensure <500ms response time
- [X] T025 Document the debugging findings and solutions in IMPLEMENTATION_SUMMARY.md
- [X] T026 Clean up temporary debugging code that is no longer needed