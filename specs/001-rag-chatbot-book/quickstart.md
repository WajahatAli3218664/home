# Quickstart Guide: RAG Chatbot Integration

## Overview
This guide provides instructions for setting up and running the enhanced RAG chatbot system that integrates with published book content. The system allows users to ask questions about book content and receive accurate answers based solely on the information provided in the book.

## Prerequisites
- Python 3.9+
- Node.js 16+
- Access to Qdrant Cloud (Free Tier)
- Access to Neon Serverless Postgres
- OpenAI API key (or alternative LLM provider)

## Setup Instructions

### 1. Environment Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Set up Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. Set up Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

### 2. Environment Configuration
1. Create a `.env` file in the backend directory with the following variables:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_cloud_url
   QDRANT_API_KEY=your_qdrant_api_key
   DATABASE_URL=your_neon_postgres_connection_string
   BETTER_AUTH_SECRET=your_auth_secret
   BETTER_AUTH_URL=http://localhost:8000
   ```

2. Ensure your Qdrant Cloud instance has the required collections set up with appropriate vector dimensions for MiniLM embeddings.

### 3. Database Setup
1. Run database migrations:
   ```bash
   cd backend
   alembic upgrade head
   ```

2. Ensure Neon Postgres is properly configured with the necessary tables for chat history and session management.

### 4. Running the Application

#### Backend (FastAPI)
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

#### Frontend (React)
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

## Key Features

### 1. RAG Chatbot with Book Content
- Ask questions about book content and receive accurate answers
- The system only uses information from the book, with no hallucinations
- Responses include confidence levels (High/Medium/Low)

### 2. Selected Text Handling
- Select/highlight text in the book to ask focused questions
- The system will only use the selected text as context
- Bypasses the retrieval process for more precise answers

### 3. Session Management
- Conversations are saved to Neon Postgres database
- Chat history is maintained across sessions
- Each session is identified by a unique session_id

## API Usage Examples

### 1. Sending a Query
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_auth_token" \
  -d '{
    "query": "What is the main concept of chapter 3?",
    "book_id": "book-123",
    "session_id": "session-456",
    "selected_text": null
  }'
```

### 2. Sending a Query with Selected Text
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_auth_token" \
  -d '{
    "query": "Explain this concept?",
    "book_id": "book-123",
    "session_id": "session-456",
    "selected_text": "The main concept of this chapter is about RAG systems..."
  }'
```

### 3. Retrieving Chat History
```bash
curl -X GET http://localhost:8000/api/v1/chat/session-456 \
  -H "Authorization: Bearer your_auth_token"
```

## Troubleshooting

### Common Issues
1. **Qdrant Connection Issues**: Ensure your Qdrant URL and API key are correct
2. **Database Connection Issues**: Verify your Neon Postgres connection string
3. **LLM Provider Issues**: Check that your OpenAI API key is valid and has sufficient quota

### Performance Tips
1. Adjust the similarity threshold in the retrieval service based on your content
2. Monitor Qdrant query performance and adjust indexing as needed
3. Use appropriate vector dimensions for your embeddings

## Next Steps
1. Customize the system prompts to match your book's tone and style
2. Add more sophisticated confidence scoring if needed
3. Implement additional analytics to track user engagement
4. Consider adding support for multiple books