# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Prerequisites

- Node.js 18+ (for Docusaurus frontend)
- Python 3.11+ (for FastAPI backend)
- Git
- A code editor (VS Code recommended)

## Setup

### 1. Clone the Repository

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

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration (Neon DB URL, Qdrant details, etc.)
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env
# Edit .env with API endpoints and other configuration
```

## Running the Application

### 1. Start the Backend

```bash
# From the backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the backend server
python -m src.api.main
```

### 2. Start the Frontend

```bash
# From the frontend directory
cd frontend

# Start the Docusaurus development server
npm run start
```

### 3. Initialize Content

```bash
# Once both servers are running, initialize the textbook content
# This will populate the database with the 12 chapters and modules

# Run the content initialization script
python scripts/init_content.py
```

## Key Components

### 1. Docusaurus Textbook
- Located in `frontend/`
- Main entry point: `frontend/src/pages/index.tsx`
- Chapter content: `frontend/src/pages/chapters/`
- Configuration: `frontend/docusaurus.config.js`

### 2. RAG Chatbot
- Backend API: `backend/src/api/v1/chat/`
- Embeddings: Using MiniLM models
- Vector storage: Qdrant database

### 3. User Authentication
- Using Better-Auth library
- User profiles and personalization settings

### 4. Curriculum Modules
- ROS 2: The Robotic Nervous System
- Simulation: The Digital Twin
- NVIDIA Isaac: The AI-Robot Brain
- VLA: Vision-Language-Action

## Configuration

### Environment Variables

#### Backend (.env)
```
NEON_DATABASE_URL=your_neon_db_url
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_api_key  # if applicable
EMBEDDING_MODEL=multi-qa-MiniLM2-cos-v1
BETTER_AUTH_SECRET=your_secret
BETTER_AUTH_URL=http://localhost:3000
```

#### Frontend (.env)
```
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_RAG_ENABLED=true
```

## Development Commands

### Backend
```bash
# Run tests
pytest

# Format code
black src/

# Check types
mypy src/
```

### Frontend
```bash
# Build for production
npm run build

# Run tests
npm test

# Format code
npm run format

# Lint code
npm run lint
```

## API Endpoints

### Textbook Content
- `GET /api/v1/chapters` - List all chapters
- `GET /api/v1/chapters/:id` - Get specific chapter
- `GET /api/v1/modules` - List all curriculum modules

### RAG Chatbot
- `POST /api/v1/chat/query` - Submit a question to the RAG system
- `GET /api/v1/chat/history/:user_id` - Get user's chat history

### User Management
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/user/profile` - Get user profile

### Translation
- `POST /api/v1/translate` - Translate content to Urdu
- `GET /api/v1/translate/terms` - Get technical term mappings

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port in `docusaurus.config.js` or backend configuration

2. **Database connection errors**
   - Verify your Neon database URL is correct
   - Check that your database is accessible

3. **RAG chatbot not responding**
   - Ensure Qdrant vector database is running
   - Verify embedding models are properly loaded

4. **Content not loading**
   - Check that the content initialization script has been run
   - Verify database connectivity

## Next Steps

1. Customize the curriculum modules based on your specific Physical AI and robotics content
2. Add your 12 textbook chapters with the required structure
3. Configure the RAG system with your specific book content
4. Add more languages beyond Urdu if needed
5. Implement additional personalization features based on user feedback