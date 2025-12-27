# Data Model: Debug RAG Context Flow

## Overview
This data model describes the key entities involved in debugging and fixing the RAG context flow issue.

## Key Entities

### Retrieved Context
- **Description**: Text data retrieved from Qdrant vector database that should be included in the LLM prompt
- **Fields**:
  - `id` (string): Unique identifier for the context chunk
  - `content` (string): The actual text content retrieved from the vector database
  - `source_document` (string): Reference to the original document/chapter
  - `similarity_score` (float): Score indicating relevance to the query
  - `metadata` (object): Additional information about the context chunk
- **Relationships**: Associated with a user query and LLM prompt

### LLM Prompt
- **Description**: The input sent to the Qwen LLM that should contain both user query and retrieved context
- **Fields**:
  - `id` (string): Unique identifier for the prompt
  - `user_query` (string): The original query from the user
  - `retrieved_context` (array): Array of retrieved context objects
  - `formatted_prompt` (string): The final prompt string sent to the LLM
  - `timestamp` (datetime): When the prompt was created
- **Relationships**: Associated with user query and retrieved context

### RAG Service
- **Description**: The component responsible for retrieving context from Qdrant and preparing the prompt for the LLM
- **Fields**:
  - `id` (string): Unique identifier for the service instance
  - `status` (string): Current status (active, error, debugging)
  - `last_query` (string): The most recent query processed
  - `context_retrieval_time` (float): Time taken to retrieve context
  - `debug_info` (object): Information for debugging context flow
- **Relationships**: Interacts with Qdrant and LLM components

### Debug Log
- **Description**: Log entries for debugging the context flow
- **Fields**:
  - `id` (string): Unique identifier for the log entry
  - `timestamp` (datetime): When the log was created
  - `component` (string): Which component generated the log (e.g., RAG Service, Context Retrieval)
  - `message` (string): The log message
  - `context_snapshot` (object): Snapshot of relevant context at the time of logging
  - `level` (string): Log level (info, warning, error)
- **Relationships**: Associated with specific query and response cycle

## Validation Rules
1. Retrieved Context content must not be empty when successfully retrieved from Qdrant
2. LLM Prompt must contain both user_query and retrieved_context before being sent to LLM
3. Debug Log entries must include timestamp and component information
4. Similarity scores for retrieved context must be within 0-1 range

## State Transitions
- RAG Service: initialized → active → (error/debugging) → active
- Retrieved Context: pending → retrieved → injected → processed
- Debug Log: created → stored → analyzed → resolved (optional)