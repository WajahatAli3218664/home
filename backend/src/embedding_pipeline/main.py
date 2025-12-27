import sys
import os
from typing import List, Dict
import uuid
from datetime import datetime

# Add the backend/src directory to the Python path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.embedding_pipeline.config import Config, validate_config
from src.embedding_pipeline.url_fetcher import get_all_urls
from src.embedding_pipeline.text_cleaner import extract_text_from_urls
from src.embedding_pipeline.chunker import chunk_text
from src.embedding_pipeline.embedder import CohereClient
from src.embedding_pipeline.vector_store import QdrantStore
from src.embedding_pipeline.models import DocumentChunk, EmbeddingVector
from src.embedding_pipeline.logging_config import logger


def main():
    """
    Main function to orchestrate the complete embedding pipeline:
    1. Fetch URLs
    2. Extract text content
    3. Chunk the text
    4. Generate embeddings
    5. Store in Qdrant
    """
    # Validate configuration first
    if not validate_config():
        logger.error("Configuration validation failed. Please check your environment variables.")
        return

    logger.info("Starting embedding pipeline...")

    try:
        # 1. Get all URLs to process
        urls = get_all_urls()
        logger.info(f"Processing {len(urls)} URLs: {urls}")

        # 2. Extract text content from URLs
        url_to_content = extract_text_from_urls(urls)

        # 3. Initialize Cohere client and Qdrant store
        cohere_client = CohereClient()
        qdrant_store = QdrantStore()

        # 4. Create Qdrant collection if it doesn't exist
        if not qdrant_store.create_collection():
            logger.error("Failed to create Qdrant collection")
            return

        # 5. Process each URL's content
        all_chunks_with_embeddings = []

        for url, content in url_to_content.items():
            if not content.strip():
                logger.warning(f"No content extracted from {url}, skipping")
                continue

            logger.info(f"Processing content from {url} ({len(content)} characters)")

            # 6. Chunk the text
            text_chunks = chunk_text(content)
            logger.info(f"Text from {url} chunked into {len(text_chunks)} parts")

            # 7. Generate embeddings for each chunk
            for idx, chunk_content in enumerate(text_chunks):
                if not chunk_content.strip():
                    continue  # Skip empty chunks

                # Create DocumentChunk instance
                chunk_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{url}#{idx}"))
                doc_chunk = DocumentChunk(
                    id=chunk_id,
                    content=chunk_content,
                    source_url=url,
                    chunk_index=idx
                )

                if not doc_chunk.validate():
                    logger.warning(f"Document chunk {chunk_id} failed validation, skipping")
                    continue

                # Generate embedding for the chunk
                try:
                    embedding_vector = cohere_client.embed_single(chunk_content)

                    # Create EmbeddingVector instance
                    emb_vector = EmbeddingVector(
                        chunk_id=chunk_id,
                        vector=embedding_vector,
                        model="embed-multilingual-v2.0"
                    )

                    if not emb_vector.validate():
                        logger.warning(f"Embedding vector for chunk {chunk_id} failed validation, skipping")
                        continue

                    # Prepare data for storage in Qdrant
                    chunk_data = {
                        'id': chunk_id,
                        'content': chunk_content,
                        'source_url': url,
                        'chunk_index': idx,
                        'embedding': embedding_vector,
                        'metadata': {
                            'created_at': datetime.now().isoformat(),
                            'source_url': url,
                            'chunk_index': idx
                        }
                    }

                    all_chunks_with_embeddings.append(chunk_data)

                    logger.debug(f"Processed chunk {idx} for {url}")

                except Exception as e:
                    logger.error(f"Error generating embedding for chunk {idx} of {url}: {str(e)}")
                    continue

        # 8. Save all chunks to Qdrant
        if all_chunks_with_embeddings:
            logger.info(f"Saving {len(all_chunks_with_embeddings)} chunks to Qdrant")
            success = qdrant_store.save_chunks_to_qdrant(all_chunks_with_embeddings)

            if success:
                logger.info(f"Successfully saved {len(all_chunks_with_embeddings)} chunks to Qdrant")
            else:
                logger.error("Failed to save chunks to Qdrant")
        else:
            logger.warning("No chunks to save to Qdrant")

        logger.info("Embedding pipeline completed successfully")

    except Exception as e:
        logger.error(f"Embedding pipeline failed with error: {str(e)}")
        raise


if __name__ == "__main__":
    main()