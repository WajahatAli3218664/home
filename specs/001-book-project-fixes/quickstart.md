# Quickstart Guide: Book Project Critical Fixes

## Prerequisites

- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- Access to Neon Postgres database (free tier)
- Access to Qdrant Cloud (free tier)
- OpenAI API key (for RAG functionality)
- Claude API key (for translation)
- Git for version control

## Setting Up the Development Environment

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup (FastAPI)

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual API keys and database URLs
```

5. Run the backend server:
```bash
python -m uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup (Docusaurus)

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your backend API URL
```

4. Run the development server:
```bash
npm run start
```

## Key Configuration Files

### Backend Configuration
- `backend/src/config/settings.py` - Main application settings
- `backend/.env` - Environment-specific variables

### Frontend Configuration
- `frontend/docusaurus.config.ts` - Docusaurus configuration
- `frontend/src/css/custom.css` - Custom styles
- `frontend/.env` - Environment variables

## Running Tests

### Backend Tests
```bash
cd backend
python -m pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/signin` - User login
- `GET /api/v1/auth/me` - Get current user

### Chat
- `POST /api/v1/chat/` - RAG-enabled chat endpoint
- `GET /api/v1/chat/history/{session_id}` - Get chat history

### Translation
- `POST /api/v1/translate/` - Translate content
- `GET /api/v1/translate/{content_id}/{language}` - Get translated content

### Personalization
- `POST /api/v1/personalize/{content_id}` - Personalize content
- `PUT /api/v1/user/preferences` - Update user preferences

## Key Components to Implement

### 1. Better-Auth Integration
- Set up user registration with background information collection
- Implement sign-in/sign-out functionality
- Create middleware for protected routes

### 2. RAG Chatbot
- Implement API endpoint that uses book content for responses
- Integrate with Qdrant for vector storage and retrieval
- Add proper citation logic to avoid hallucinations

### 3. Translation System
- Create API endpoints for content translation
- Implement caching for translated content
- Add UI controls for language switching

### 4. Personalization Engine
- Develop content adaptation based on user background
- Create API for profile management
- Add UI for personalization preferences

## Database Models

The system uses:
- Neon Postgres for relational data (users, preferences, etc.)
- Qdrant Cloud for vector storage (RAG embeddings)

## Deployment

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Backend (Railway)
1. Connect your GitHub repository to Railway
2. Set up environment variables in Railway dashboard
3. Configure auto-deployment from main branch

## Troubleshooting

### Common Issues
1. **API 404 errors**: Check that backend is running on http://localhost:8000
2. **Auth errors**: Verify Better-Auth is properly configured
3. **Translation errors**: Check Claude API key and rate limits
4. **Chat errors**: Ensure Qdrant is properly configured and has content indexed

### Useful Commands
- Check backend status: `curl http://localhost:8000/health`
- Check frontend build: `npm run build`
- Run all tests: `npm run test && python -m pytest`

## Next Steps

1. Implement the authentication system with Better-Auth
2. Set up the RAG chatbot with Qdrant integration
3. Create the translation functionality
4. Implement content personalization
5. Add the UI components to the Docusaurus frontend