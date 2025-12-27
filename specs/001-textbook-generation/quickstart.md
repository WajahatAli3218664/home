# Quickstart Guide: Textbook Generation Feature

## Overview
This guide provides a quick setup and run instructions for the textbook generation feature of the Physical AI & Humanoid Robotics educational platform.

## Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- npm or yarn package manager
- Git
- Access to Neon database instance
- Access to Qdrant vector database instance
- OpenAI API key (or equivalent for RAG functionality)

## Environment Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
# If requirements.txt doesn't exist yet, install the basic dependencies:
pip install fastapi uvicorn python-multipart python-jose[cryptography] passlib[bcrypt] psycopg2-binary sqlalchemy python-dotenv qdrant-client openai
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend  # (from project root)

# Install dependencies
npm install
# or
yarn install
```

## Environment Variables

### Backend (.env file in backend directory)
```env
DATABASE_URL=postgresql://username:password@ep-wisec-authority.us-east-1.aws.neon.tech/dbname
QDRANT_URL=https://your-cluster-url.qdrant.tech
QDRANT_API_KEY=your-qdrant-api-key
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-secret-key-for-jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local file in frontend directory)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SITE_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret
NEXTAUTH_URL=http://localhost:3000
```

## Database Setup

### 1. Neon Database Setup
1. Create a Neon account and project
2. Create the following tables based on data-model.md:

```sql
-- User profiles table
CREATE TABLE user_profiles (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    background_level VARCHAR(20) NOT NULL, -- 'beginner', 'intermediate', 'advanced'
    preferences JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Textbook chapters table
CREATE TABLE textbook_chapters (
    id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    slug VARCHAR(500) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    version VARCHAR(20) DEFAULT '1.0.0',
    position INTEGER UNIQUE NOT NULL,
    word_count INTEGER DEFAULT 0,
    estimated_reading_time INTEGER DEFAULT 0, -- in minutes
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User progress tracking
CREATE TABLE user_progress (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES user_profiles(id),
    chapter_id VARCHAR(255) REFERENCES textbook_chapters(id),
    content_version VARCHAR(20) NOT NULL,
    progress_percentage DECIMAL(5,2) DEFAULT 0.00,
    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed BOOLEAN DEFAULT FALSE,
    quiz_score JSONB,
    time_spent INTEGER DEFAULT 0, -- in seconds
    UNIQUE(user_id, chapter_id)
);

-- Learning materials
CREATE TABLE learning_materials (
    id VARCHAR(255) PRIMARY KEY,
    chapter_id VARCHAR(255) REFERENCES textbook_chapters(id),
    material_type VARCHAR(20) NOT NULL, -- 'summary', 'quiz', 'learning_booster'
    content TEXT NOT NULL,
    version VARCHAR(20) DEFAULT '1.0.0',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI chat interactions
CREATE TABLE ai_chat_interactions (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES user_profiles(id),
    session_id VARCHAR(255) NOT NULL,
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    context_used TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    feedback JSONB
);

-- Content versions
CREATE TABLE content_versions (
    id VARCHAR(255) PRIMARY KEY,
    chapter_id VARCHAR(255) REFERENCES textbook_chapters(id),
    version VARCHAR(20) NOT NULL,
    content_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Translation cache
CREATE TABLE translation_cache (
    id VARCHAR(255) PRIMARY KEY,
    chapter_id VARCHAR(255) REFERENCES textbook_chapters(id),
    content_version VARCHAR(20) NOT NULL,
    target_language VARCHAR(10) NOT NULL,
    translated_content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);
```

### 2. Qdrant Collection Setup
1. Set up a collection for textbook content embeddings:
```python
# This would typically be done in a setup script
from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# Create collection for textbook content
client.create_collection(
    collection_name="textbook_content",
    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),  # Adjust size based on embedding model used
)
```

## Running the Application

### 1. Start the Backend
```bash
# From the backend directory
cd backend
source venv/bin/activate  # or appropriate activation command for your system

# Run the backend server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start the Frontend
```bash
# From the frontend directory
cd frontend

# Run the development server
npm run dev
# or
yarn dev
```

### 3. Access the Application
- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Backend redoc: http://localhost:8000/redoc

## Seeding Initial Content

### 1. Add Sample Chapters
To add the 12 textbook chapters required by the feature:

```python
# Example script to add chapters (to be implemented in backend)
import asyncio
from src.services.chapter_service import create_chapter

async def seed_chapters():
    chapters = [
        {
            "title": "Introduction to Physical AI",
            "slug": "introduction-to-physical-ai",
            "content": "Physical AI is an interdisciplinary field...",
            "position": 1,
            "word_count": 1500,
            "estimated_reading_time": 6
        },
        # Add remaining chapters...
    ]
    
    for chapter_data in chapters:
        await create_chapter(chapter_data)

# Run the seed function
asyncio.run(seed_chapters())
```

### 2. Index Content for RAG
The system should index textbook content for the RAG chatbot:

```python
# Example of indexing content (to be implemented in backend)
from src.services.rag_service import index_chapter_content

async def index_all_content():
    # Index all chapters for RAG retrieval
    chapters = await get_all_chapters()  # Implementation needed
    for chapter in chapters:
        await index_chapter_content(chapter.id, chapter.content)

asyncio.run(index_all_content())
```

## Key Features Walkthrough

### 1. User Authentication
- Users can sign up/login via Better-Auth
- Authentication tokens are used for API requests
- User background level is captured during onboarding

### 2. Textbook Navigation
- Chapters are displayed in sequence based on their position
- Progress tracking updates as users read
- Estimated reading time helps manage the 45-minute total requirement

### 3. AI-Powered Chatbot
- Ask questions related to textbook content
- Responses are grounded in textbook material only
- Context is maintained during conversations

### 4. Content Personalization
- Content adapts based on user's background level
- Different versions of content provided for different skill levels

### 5. Urdu Translation
- One-click translation available for all chapters
- Translated content cached for performance

### 6. Learning Materials
- Auto-generated summaries for each chapter
- Chapter-specific quizzes
- Learning boosters to reinforce key concepts

## Testing the Implementation

### Backend Tests
```bash
# Run backend tests
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
# Run frontend tests
cd frontend
npm run test
# or
yarn test
```

## Deployment

### Frontend to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Backend to Railway
1. Connect Railway to your GitHub repository
2. Set up environment variables in Railway dashboard
3. Deploy via GitHub integration

## Troubleshooting

### Common Issues

1. **Database connection errors**: Verify environment variables and database access
2. **API rate limits**: Check OpenAI usage and implement appropriate fallbacks
3. **Slow loading**: Verify CDN setup and image optimization
4. **Qdrant connection issues**: Confirm API keys and endpoints are correct

### Performance Tips

- Use a CDN for content delivery
- Optimize images and assets
- Implement caching strategies
- Monitor API usage to avoid rate limiting