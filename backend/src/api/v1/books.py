from fastapi import APIRouter, HTTPException, BackgroundTasks
from uuid import UUID
from src.models.book_content import BookContentCreate
from src.services.book_service import book_service

router = APIRouter()

@router.post("/books/process")
async def process_book(background_tasks: BackgroundTasks, book_data: BookContentCreate):
    """
    Process a book and create vector embeddings for RAG system.

    Request Body:
    {
      "title": "string",
      "author": "string",
      "content": "string (full text of the book)",
      "chunk_size": "integer (optional, default: 512)",
      "embedding_model": "string (optional, default: 'MiniLM')"
    }

    Response (200 OK):
    {
      "status": "success",
      "message": "Book processed successfully",
      "book_id": "uuid",
      "embedding_count": "number",
      "processing_time": "number"
    }
    """
    try:
        # Process the book using the book service
        result = book_service.process_book(book_data)

        return {
            "status": "success",
            "message": "Book processed successfully",
            "book_id": result.get("book_id"),
            "embedding_count": result.get("embedding_count", 0),
            "processing_time": result.get("processing_time", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing book: {str(e)}")


@router.post("/books")
async def create_book(book_data: BookContentCreate):
    """
    Upload a new book for the RAG system to use.

    Request Body:
    {
      "title": "string",
      "author": "string",
      "content": "string (full text of the book)",
      "chunk_size": "integer (optional, default: 512)",
      "embedding_model": "string (optional, default: 'MiniLM')"
    }

    Response (201 Created):
    {
      "book_id": "uuid",
      "title": "string",
      "author": "string",
      "status": "processing|ready|error",
      "created_at": "datetime"
    }
    """
    try:
        # Create the book using the book service
        book = book_service.create_book(book_data)

        return {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "status": "ready",  # In a real implementation, this might be "processing" initially
            "created_at": book.created_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating book: {str(e)}")

@router.get("/books/{book_id}")
async def get_book(book_id: str):
    """
    Get information about a specific book.

    Path Parameters:
    - book_id: UUID of the book

    Response (200 OK):
    {
      "book_id": "uuid",
      "title": "string",
      "author": "string",
      "status": "processing|ready|error",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
    """
    try:
        book = book_service.get_book(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        return {
            "book_id": book.book_id,
            "title": book.title,
            "author": book.author,
            "status": "ready" if book.is_active else "inactive",
            "created_at": book.created_at,
            "updated_at": book.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving book: {str(e)}")

@router.get("/books")
async def list_books():
    """
    List all available books.

    Response (200 OK):
    [
      {
        "book_id": "uuid",
        "title": "string",
        "author": "string",
        "status": "processing|ready|error",
        "created_at": "datetime"
      }
    ]
    """
    try:
        books = book_service.list_books()
        return [
            {
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "status": "ready" if book.is_active else "inactive",
                "created_at": book.created_at
            }
            for book in books
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing books: {str(e)}")