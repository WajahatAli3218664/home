# Research: Debug RAG Context Flow

## Overview
This research addresses the issue where the RAG chatbot's LLM replies with generic responses and ignores textbook data from the Qdrant vector database. The goal is to identify why retrieved context is not reaching the LLM and implement a proper solution.

## Decision: Identify Context Flow Issues
**Rationale**: The core issue is that retrieved context from Qdrant is not being passed to the LLM, resulting in generic responses instead of context-aware responses based on textbook data.

**Alternatives considered**:
1. Complete rewrite of the RAG system - Rejected as too time-consuming and risky
2. Add new context injection mechanism alongside existing one - Rejected as it would create complexity without fixing the root cause
3. Debug and fix existing context flow - Selected as it addresses the root cause directly

## Decision: Implement Logging for Debugging
**Rationale**: To observe the context being sent to the LLM before the call, we'll implement logging mechanisms that will help identify exactly where the context flow breaks down.

**Alternatives considered**:
1. Use external debugging tools - Rejected as it adds complexity and dependencies
2. Add temporary debug endpoints - Rejected as logging is simpler and more appropriate for this issue
3. Add comprehensive logging to track context flow - Selected as it provides visibility into the entire process

## Decision: Create Minimal Working RAG Implementation
**Rationale**: A minimal working implementation will serve as a reference for the correct implementation and help ensure the main application code follows the same pattern.

**Alternatives considered**:
1. Directly fix the existing implementation without reference - Rejected as it's risky without knowing the correct pattern
2. Create a test suite first - Rejected as the focus is on fixing the immediate issue
3. Create a minimal working example - Selected as it provides a clear reference implementation

## Common RAG Implementation Mistakes
Based on research, here are common mistakes that cause RAG systems to ignore retrieved context:

1. **Context not included in prompt template**: The retrieved context is retrieved but not included in the prompt sent to the LLM
2. **Prompt template formatting issues**: The context and query are not properly formatted in the prompt
3. **Variable scoping issues**: The retrieved context variable is out of scope when constructing the LLM call
4. **Overwriting context**: The context is retrieved but then overwritten by an empty value or default query
5. **Incorrect API call parameters**: The context is available but not passed as a parameter to the LLM API
6. **Timing issues**: The context is retrieved asynchronously but the LLM call happens before retrieval completes
7. **Size limitations**: The context is retrieved but exceeds token limits and gets truncated or skipped
8. **Pathway not executed**: The RAG pathway is not being executed at all, and the system defaults to a simple chat pathway

## Recommended Debugging Approach
1. Add logging before the LLM call to see what prompt is being sent
2. Trace through the code to identify where the retrieved context should be injected
3. Check if the context retrieval is happening at all
4. Verify the context is being properly formatted into the prompt
5. Confirm the prompt with context is being passed to the LLM

## Implementation Strategy
1. Identify the exact point in the code where retrieved context should be injected into the LLM prompt
2. Implement proper context injection mechanism
3. Add logging to observe the context flow
4. Create a minimal working RAG implementation as a reference
5. List common implementation mistakes to avoid in the future