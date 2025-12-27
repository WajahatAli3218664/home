# API Contract: Embedding Pipeline Services

## Overview
This document specifies the API contracts for the embedding pipeline services that process Docusaurus content and store embeddings in Qdrant.

## Service: URL Fetcher Service

### get_all_urls()
- **Purpose**: Retrieve the list of URLs to be processed
- **Input**: None
- **Output**: List of URL strings
- **Error Conditions**: 
  - Configuration error if URL list is not defined

## Service: Text Extraction Service

### extract_text_from_urls(urls: List[str])
- **Purpose**: Extract clean text content from a list of URLs
- **Input**: List of URL strings
- **Output**: Dictionary mapping URL to extracted content (Dict[str, str])
- **Error Conditions**: 
  - Network error when fetching a URL
  - Parsing error when extracting content

## Service: Text Chunker Service

### chunk_text(text: str, max_chunk_size: int = 1000, min_chunk_size: int = 500)
- **Purpose**: Split text into chunks of specified size
- **Input**: Text string and chunk size parameters
- **Output**: List of text chunks
- **Error Conditions**: None expected

## Service: Embedding Service

### embed(chunks: List[str])
- **Purpose**: Generate embeddings for text chunks using Cohere
- **Input**: List of text chunks
- **Output**: List of embedding vectors
- **Error Conditions**: 
  - API error from Cohere service
  - Invalid input format

### embed_single(text: str)
- **Purpose**: Generate a single embedding for a text string
- **Input**: Text string
- **Output**: Embedding vector
- **Error Conditions**: 
  - API error from Cohere service
  - Invalid input format

## Service: Vector Storage Service

### create_collection(collection_name: str)
- **Purpose**: Create a Qdrant collection for storing embeddings
- **Input**: Collection name
- **Output**: Success status
- **Error Conditions**: 
  - Connection error to Qdrant
  - Collection already exists error

### save_chunks_to_qdrant(chunks: List[Dict], collection_name: str = "rag_embeddings")
- **Purpose**: Store document chunks with embeddings in Qdrant
- **Input**: List of chunks (with text and metadata) and collection name
- **Output**: Success status and count of stored items
- **Error Conditions**: 
  - Connection error to Qdrant
  - Invalid data format

### validate_retrieval(query: str, top_k: int = 5)
- **Purpose**: Test retrieval accuracy by performing similarity search
- **Input**: Query string and number of results to return
- **Output**: List of relevant chunks with similarity scores
- **Error Conditions**: 
  - Connection error to Qdrant
  - Query processing error