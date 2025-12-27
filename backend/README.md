# RAG Chatbot for Physical AI & Humanoid Robotics Textbook

This is a RAG (Retrieval-Augmented Generation) chatbot that answers questions based only on the Physical AI & Humanoid Robotics textbook content.

## Features

- RAG-based question answering using textbook content
- Strict book-only answering (no hallucinations)
- Authentication required for chat access
- Vector database for efficient content retrieval
- Detailed logging and error handling
- Deployable to Hugging Face Spaces

## Architecture

- **Backend**: FastAPI server
- **Vector Database**: Qdrant
- **LLM Integration**: OpenAI GPT, Google Gemini, or Cohere
- **Frontend**: Docusaurus-based documentation site
- **Database**: PostgreSQL (Neon)

## Setup

### 1. Clone the repository

```bash
git clone https://huggingface.co/spaces/areejzaheer/bookBackend
cd bookBackend
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file with the following variables:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Security Configuration
JWT_SECRET_KEY=your-very-secure-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM Provider Configuration (Choose one)
# Options: openai, gemini (default: openai)
LLM_PROVIDER=openai

# AI Service Configuration (Choose one or more)
OPENAI_API_KEY=your-openai-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here
COHERE_API_KEY=your-cohere-api-key-here

# Qdrant Vector Database Configuration
QDRANT_URL=your-qdrant-url-here
QDRANT_API_KEY=your-qdrant-api-key-here
QDRANT_COLLECTION_NAME=textbook_content

# Database Configuration
DATABASE_URL=your-postgresql-database-url-here
```

### 4. Run the application

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Usage

### Authentication

First register/login to get an access token:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "programming_level": "beginner",
    "ai_experience": "none",
    "gpu_available": false,
    "ram_size": "8GB"
  }'
```

### Chat with the bot

```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "query": "What are the principles of embodied cognition?"
  }'
```

## Frontend Integration

The frontend is built with Docusaurus and expects:

- Backend API at `http://localhost:8000`
- Chat endpoint: `POST /api/v1/chat/`
- Authentication: Bearer token in Authorization header

## Deployment

### Hugging Face Spaces

To deploy to Hugging Face Spaces:

1. Create a Space with Docker or Python SDK template
2. Add all files from the backend directory
3. Ensure `requirements.txt`, `Dockerfile`, and `space.yaml` are present
4. Set environment variables in Space settings

### Environment Variables for Production

- `PORT` (set by Hugging Face, defaults to 8000)
- `OPENAI_API_KEY` or `COHERE_API_KEY`
- `QDRANT_URL`, `QDRANT_API_KEY`
- `DATABASE_URL`
- `JWT_SECRET_KEY`

## Book-only Answering Guarantee

The system is designed with strict safeguards:
- Answers are generated only from retrieved textbook content
- LLM is prompted not to use external knowledge
- If content is not in the book, the system responds: "This information is not available in the book."

## Troubleshooting

- Ensure all environment variables are set
- Verify Qdrant connection
- Check that textbook content was loaded at startup
- Review logs for detailed error information

## Development

For local development:

1. Run Qdrant locally or ensure cloud connection
2. Set up the database
3. Load textbook content (happens automatically on startup)
4. Start the API server