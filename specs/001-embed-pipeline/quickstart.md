# Quickstart: Embedding Pipeline for Docusaurus URLs

## Prerequisites

- Python 3.11+
- Pip package manager
- Cohere API key
- Qdrant Cloud account and API key

## Setup

### 1. Clone and Navigate
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file based on `.env.example`:
```bash
COHERE_API_KEY=your_cohere_api_key
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_URL=your_qdrant_cluster_url
SOURCE_URLS=https://areejshaikh.github.io/book/,https://areejshaikh.github.io/book/docs/intro, # Add more URLs as needed
```

## Usage

### Run the Full Pipeline
```bash
python -m src.embedding_pipeline.main
```

### Run Individual Components (for development/testing)
```bash
# Fetch and clean URLs
python -c "from src.embedding_pipeline.url_fetcher import get_all_urls; print(get_all_urls())"

# Process specific URL
python -c "from src.embedding_pipeline.text_cleaner import extract_text_from_urls; extract_text_from_urls(['https://areejshaikh.github.io/book/'])"
```

## Architecture

The pipeline follows these steps:
1. `url_fetcher.py` - Fetches all URLs to process
2. `text_cleaner.py` - Extracts clean text from each URL
3. `chunker.py` - Breaks text into 500-1000 token segments
4. `embedder.py` - Generates embeddings using Cohere
5. `vector_store.py` - Stores embeddings in Qdrant with metadata

## Configuration

- URL list: Defined in environment variable `SOURCE_URLS`
- Chunk size: Configured in `chunker.py` (500-1000 token range)
- Qdrant collection: Named `rag_embeddings` by default
- Logging: Set to INFO level by default

## Troubleshooting

- If getting API errors: Verify your API keys in `.env`
- If URLs aren't loading: Check if the site structure has changed
- If embeddings aren't storing: Verify Qdrant connection details