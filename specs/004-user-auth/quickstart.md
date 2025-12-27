# Quickstart Guide: Auth, Personalization, and Translation System

## Overview
This guide provides a quick setup and usage guide for the authentication, personalization, and translation system.

## Prerequisites
- Python 3.11+
- Node.js 18+
- Access to Neon Postgres database
- Access to AI service (OpenAI/Claude) for personalization and translation
- Frontend setup with Docusaurus

## Backend Setup

### 1. Install Dependencies
```bash
cd backend
pip install fastapi uvicorn python-multipart python-jose[cryptography] passlib[bcrypt] pydantic-settings psycopg2-binary sqlmodel
```

### 2. Environment Configuration
Create a `.env` file in the backend directory with the following variables:

```env
DATABASE_URL=postgresql://username:password@host:port/database
AI_API_KEY=your_ai_service_api_key
JWT_SECRET_KEY=your_jwt_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Database Setup
Ensure your Neon Postgres database is created and run the following to set up the tables:

```bash
# Create the database tables
python -c "from src.database.models import create_db_and_tables; create_db_and_tables()"
```

### 4. Run the Backend Server
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

The backend server will be running at `http://localhost:8000`.

## Frontend Integration

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Environment Configuration
Update your `.env` file in the frontend directory:

```env
REACT_APP_API_BASE_URL=http://localhost:8000
```

### 3. Run the Frontend
```bash
cd frontend
npm run start
```

## Usage Guide

### User Registration
1. Navigate to the signup page
2. Enter your email and password
3. Provide your profile information:
   - Programming Level (Beginner/Intermediate/Advanced)
   - AI Experience (None/Basic/Intermediate/Advanced)
   - GPU Availability (Yes/No)
   - RAM Size (4GB, 8GB, 16GB, 32GB)
4. Submit the form to create your account

### User Login
1. Navigate to the signin page
2. Enter your email and password
3. You'll be authenticated and can access personalized features

### Content Personalization
1. Log in to your account
2. Navigate to a chapter you want to read
3. Click the "Personalize Chapter" button
4. The system will adapt the content based on your profile information

### Urdu Translation
1. Log in to your account
2. Navigate to a chapter you want to translate
3. Click the "اردو میں پڑھیں" (Read in Urdu) button
4. The system will translate the content to Urdu

## API Endpoints

### Authentication
- `POST /auth/signup` - Create a new user
- `POST /auth/signin` - Authenticate a user
- `GET /user/profile` - Get user profile
- `PUT /user/profile` - Update user profile

### Content Services
- `POST /chapter/personalize` - Personalize chapter content
- `POST /chapter/translate` - Translate chapter to Urdu

## Troubleshooting

### Common Issues
1. **Authentication fails**: Ensure your JWT token is valid and hasn't expired
2. **Personalization/translation fails**: Check that your AI service API key is valid
3. **Database connection fails**: Verify your database URL is correct

### Useful Commands
```bash
# Check API status
curl http://localhost:8000/health

# Test authentication
curl -X POST http://localhost:8000/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "password":"password"}'
```

## Next Steps
1. Implement additional API endpoints as needed
2. Add more personalization options based on user feedback
3. Expand translation capabilities to support more languages
4. Optimize performance based on user usage patterns