from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from src.models.book_content import BookContent, BookContentCreate, BookContentUpdate
from src.models.content_chunk import ContentChunk, ContentChunkCreate
from src.services.embedding_service import embedding_service
from src.services.qdrant_service import qdrant_manager
import re

class BookService:
    def __init__(self):
        self.embedding_service = embedding_service
        self.qdrant_manager = qdrant_manager
        # In a real implementation, this would connect to a database like Neon Postgres
        # For now, we'll use an in-memory store as a placeholder
        self.books_db = {}
        self.chunks_db = {}

    def create_book(self, book_data: BookContentCreate) -> BookContent:
        """Create a new book and process its content"""
        book_id = str(uuid4())

        # Create the book object
        book = BookContent(
            book_id=book_id,
            title=book_data.title,
            author=book_data.author,
            content=book_data.content,
            embedding_model=book_data.embedding_model,
            chunk_size=book_data.chunk_size,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True
        )

        # Store in "database" (in-memory for now)
        self.books_db[book_id] = book

        # Chunk the content and generate embeddings
        self._process_book_content(book_id, book_data.content, book_data.chunk_size)

        return book

    def _process_book_content(self, book_id: str, content: str, chunk_size: int):
        """Chunk the book content and generate embeddings for each chunk"""
        # Simple chunking by sentences
        sentences = re.split(r'[.!?]+', content)

        # Group sentences into chunks of approximately chunk_size characters
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Add a period back to sentences that had one
            if sentence[-1] not in ['.', '!', '?']:
                sentence += '.'

            if len(current_chunk + " " + sentence) <= chunk_size:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence

        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(current_chunk.strip())

        # Process each chunk
        for idx, chunk_text in enumerate(chunks):
            if chunk_text.strip():  # Only process non-empty chunks
                self._process_chunk(book_id, idx, chunk_text)

    def _process_chunk(self, book_id: str, chunk_index: int, chunk_text: str):
        """Process a single chunk: generate embedding and store in Qdrant"""
        # Generate embedding for the chunk
        embedding = self.embedding_service.generate_embedding(chunk_text)

        # Create chunk ID
        chunk_id = str(uuid4())

        # Store in Qdrant
        self.qdrant_manager.store_embedding(
            book_id=book_id,
            chunk_id=chunk_id,
            chunk_text=chunk_text,
            embedding=embedding,
            metadata={
                "chunk_index": chunk_index,
                "created_at": datetime.now().isoformat()
            }
        )

        # Store in "database" (in-memory for now)
        chunk = ContentChunk(
            chunk_id=chunk_id,
            book_id=book_id,
            chunk_text=chunk_text,
            chunk_index=chunk_index,
            embedding_vector=embedding,
            created_at=datetime.now()
        )
        self.chunks_db[chunk_id] = chunk

    def get_book(self, book_id: str) -> Optional[BookContent]:
        """Get a book by ID"""
        return self.books_db.get(book_id)

    def list_books(self) -> List[BookContent]:
        """List all books"""
        return list(self.books_db.values())

    def update_book(self, book_id: str, book_data: BookContentUpdate) -> Optional[BookContent]:
        """Update a book"""
        if book_id not in self.books_db:
            return None

        book = self.books_db[book_id]

        # Update fields that are provided
        if book_data.title is not None:
            book.title = book_data.title
        if book_data.author is not None:
            book.author = book_data.author
        if book_data.content is not None:
            # If content is updated, we need to reprocess the entire book
            book.content = book_data.content
            # Remove old embeddings from Qdrant
            self.qdrant_manager.delete_book_embeddings(book_id)
            # Process new content
            self._process_book_content(book_id, book_data.content, book.chunk_size)
        if book_data.is_active is not None:
            book.is_active = book_data.is_active

        book.updated_at = datetime.now()
        self.books_db[book_id] = book

        return book

    def process_book(self, book_data: BookContentCreate):
        """Process a book and create vector embeddings for RAG system"""
        import time
        start_time = time.time()

        # Create the book which will also process its content
        book = self.create_book(book_data)

        # Count the number of embeddings created
        book_chunks = [chunk for chunk in self.chunks_db.values() if chunk.book_id == book.book_id]
        embedding_count = len(book_chunks)

        processing_time = time.time() - start_time

        return {
            "book_id": book.book_id,
            "embedding_count": embedding_count,
            "processing_time": round(processing_time, 2)
        }

    def delete_book(self, book_id: str):
        """Delete a book and its embeddings"""
        if book_id in self.books_db:
            # Remove embeddings from Qdrant
            self.qdrant_manager.delete_book_embeddings(book_id)
            # Remove from "database"
            del self.books_db[book_id]
            # Remove related chunks
            chunks_to_delete = [chunk_id for chunk_id, chunk in self.chunks_db.items() if str(chunk.book_id) == book_id]
            for chunk_id in chunks_to_delete:
                del self.chunks_db[chunk_id]

# Create a singleton instance
book_service = BookService()