# Data Model: Qdrant Search Interface

## Overview
This document defines the data structures used in the Qdrant search interface component.

## Query Model
Represents the user's search input

### Fields
- `text`: string (required) - The search query text entered by the user

### Validation Rules
- Must not be empty or whitespace-only
- Maximum length: 500 characters (prevents extremely long queries)

## Search Result Model
Represents a single search result from the backend

### Fields
- `content`: string (required) - The content snippet returned from the search
- `source`: string (required) - URL pointing to the source of the content
- `score`: number (required) - Similarity score between 0 and 1, where 1 is highest similarity

### Validation Rules
- `content` must be non-empty
- `source` must be a valid URL format
- `score` must be a number between 0 and 1 (inclusive)

## Search Results Collection
Represents the collection of results returned from a single search

### Structure
- Array of Search Result objects
- Ordered by score in descending order (highest scores first)

### Constraints
- May be empty if no results match the query
- Maximum of 20 results per query (configurable limit)

## Component State Model
Describes the internal state of the React component

### Fields
- `query`: string - Current user input in the search box
- `results`: Search Results Collection - Currently displayed results
- `loading`: boolean - Whether a search request is in progress
- `error`: string or null - Error message if a problem occurred
- `backendUrl`: string - The base URL for the backend API

### Transitions
1. Initial state: `query` is empty, `results` is empty, `loading` is false, `error` is null
2. Query submitted: `loading` becomes true, `error` becomes null
3. Results received: `results` is updated with data, `loading` becomes false
4. Error occurs: `error` is set to error message, `loading` becomes false
5. New query: `results` is reset, `error` becomes null