# Vercel Deployment Guide

## Deploying the Backend to Vercel

This guide explains how to deploy the backend API to Vercel.

### Prerequisites

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Have a Vercel account (sign up at https://vercel.com)

### Deployment Steps

1. Navigate to the project root:
   ```bash
   cd F:\hackthone-q-4
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy the project:
   ```bash
   vercel
   ```

4. Follow the prompts to set up your project (accept defaults for most options)

5. Set environment variables in the Vercel dashboard:
   - `OPENAI_API_KEY` (if using OpenAI)
   - `GEMINI_API_KEY` (if using Gemini)
   - `LLM_PROVIDER` (either 'openai' or 'gemini')
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `QDRANT_COLLECTION_NAME`
   - `DATABASE_URL`
   - `JWT_SECRET_KEY`

### Vercel Configuration

The project is configured with the following `vercel.json`:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build",
        "buildCommand": "cd frontend && npm install && npm run build"
      }
    },
    {
      "src": "api/[[...path]].py",
      "use": "@vercel/python",
      "config": {
        "runtime": "python3.9"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/[[...path]].py"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html",
      "headers": {
        "Cache-Control": "public, max-age=0"
      }
    },
    {
      "src": "/(.*\\.\\w+)$",
      "dest": "/$1",
      "headers": {
        "Cache-Control": "public, max-age=31536000"
      }
    },
    {
      "src": "/(.+)",
      "dest": "/index.html"
    }
  ]
}
```

### API Endpoints

After deployment, your API will be available at:
- `https://your-project-name.vercel.app/api/` - Main API endpoints
- `https://your-project-name.vercel.app/api/chat/` - Chat endpoint
- `https://your-project-name.vercel.app/health` - Health check

### Troubleshooting

1. If you get import errors during build, make sure all dependencies are in `backend/requirements.txt`
2. For database connections, ensure your database is accessible from Vercel's network
3. For Qdrant, make sure your URL and API key allow external connections

### Environment Variables Setup

After deployment, go to your Vercel project dashboard:
1. Navigate to Settings → Environment Variables
2. Add the required environment variables as mentioned above

### Connecting to AI Services

The backend supports both OpenAI and Google Gemini:
- Set `LLM_PROVIDER=openai` and provide `OPENAI_API_KEY`
- Or set `LLM_PROVIDER=gemini` and provide `GEMINI_API_KEY`

The system will automatically use the configured provider for RAG operations.