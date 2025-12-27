# Quickstart Guide: AI-Powered Book RAG System

## Prerequisites

- Python 3.11+
- Node.js 18+
- Access to Google Gemini API
- Access to Groq API
- Qdrant Cloud account (free tier)
- Neon PostgreSQL account (free tier)

## Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 3. Environment Configuration
Create `.env` file in the backend directory with the following:
```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=your_neon_database_url
```

### 4. Frontend Setup
```bash
cd frontend
npm install
```

## Running the Application

### 1. Start the Backend
```bash
cd backend
python main.py
```
Backend will start on `http://localhost:8000`

### 2. Start the Frontend
In a new terminal:
```bash
cd frontend
npm start
```
Frontend will start on `http://localhost:3000`

## Key Features

### 1. Book Content Processing
- Upload a book in digital format
- System automatically processes and creates vector embeddings
- Content is chunked intelligently and stored in Qdrant with metadata

### 2. RAG Chatbot
- Ask questions about the book content
- Responses are grounded in the book content with no hallucinations
- Citations are provided for referenced content

### 3. Multilingual Support
- Toggle between English and Urdu using the language button
- Content is automatically translated while preserving formatting
- Chatbot responds in the selected language

## API Endpoints

### Embedding Generation
- `POST /api/v1/embeddings/process-book` - Process a book and create embeddings

### RAG Queries
- `POST /api/v1/rag/query` - Ask questions about book content
- `POST /api/v1/rag/query-selected` - Ask questions about selected text only

### Language Switching
- `GET /api/v1/translation/translate` - Translate content to Urdu
- `GET /api/v1/translation/toggle` - Toggle language preference

## Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```