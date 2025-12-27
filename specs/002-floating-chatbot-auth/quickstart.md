# Quickstart: Floating Chatbot with Authentication

## Prerequisites
- Node.js v18+ for frontend development
- Python 3.8+ for backend development
- Access to Qdrant vector database
- Better Auth account/credentials

## Setup

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   npm install better-auth @better-auth/client
   ```

3. Create environment file `.env`:
   ```env
   REACT_APP_API_BASE_URL=http://localhost:8000
   ```

4. Start the Docusaurus development server:
   ```bash
   npm start
   ```

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create environment file `.env`:
   ```env
   SECRET_KEY=your-secret-key-here
   BETTER_AUTH_SECRET=your-better-auth-secret-here
   QDRANT_URL=your-qdrant-url
   QDRANT_PORT=6333
   COHERE_API_KEY=your-cohere-api-key
   ```

4. Start the backend server:
   ```bash
   python main.py
   ```

## Usage

### For Developers
- The floating chatbot button will appear at the bottom-left of all pages
- Clicking the button will trigger authentication flow for unauthenticated users
- Authenticated users will see the chat interface open directly
- API requests to the chat endpoint will require proper authentication headers

### For End Users
- Visit the textbook website
- Look for the floating chatbot button at the bottom-left corner
- Click the button to start chatting with the AI assistant
- Follow the authentication prompts if not already logged in
- Ask questions about the textbook content
- View responses with citations to source material

## Testing
To run tests:
```bash
# Frontend
cd frontend
npm test

# Backend
cd backend
pytest
```

## Environment Variables
- `REACT_APP_API_BASE_URL` - Frontend: Base URL of the backend API
- `SECRET_KEY` - Backend: Secret key for JWT token signing
- `BETTER_AUTH_SECRET` - Backend: Better Auth secret for token validation
- `QDRANT_URL` - Backend: URL of the Qdrant vector database
- `QDRANT_PORT` - Backend: Port of the Qdrant vector database
- `COHERE_API_KEY` - Backend: API key for Cohere (if used)