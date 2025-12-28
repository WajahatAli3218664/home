# Vercel Deployment Guide

## Backend Deployment (Vercel Serverless)

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

### Step 2: Deploy Backend
1. Go to https://vercel.com
2. Click "New Project"
3. Import your GitHub repository
4. Select "Other" as framework
5. Set Root Directory to `/` (root)
6. Add Environment Variables:
   - `GROQ_API_KEY`: Your Groq API key
7. Click "Deploy"

Your backend will be available at: `https://your-project-name.vercel.app`

### Step 3: Update Frontend API URL
After backend deployment, update the API URL in `frontend/src/components/ChatInterface.jsx`:

```javascript
const API_URL = typeof window !== 'undefined' 
  ? (window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://your-project-name.vercel.app')
  : 'http://localhost:8000';
```

## Frontend Deployment (Vercel)

### Step 1: Deploy Frontend
1. Go to https://vercel.com
2. Click "New Project"
3. Import your GitHub repository
4. Select "Docusaurus" as framework
5. Set Root Directory to `frontend`
6. Click "Deploy"

Your frontend will be available at: `https://your-frontend-name.vercel.app`

## API Endpoints After Deployment

- Backend: `https://your-project-name.vercel.app/api/v1/chat`
- Frontend: `https://your-frontend-name.vercel.app`

## Testing Chatbot on Vercel

1. Open your frontend URL
2. Click the chat button (💬)
3. Type a message
4. Chatbot should respond from the backend

## Troubleshooting

### Chatbot not responding
- Check that backend is deployed and running
- Verify API URL in ChatInterface.jsx
- Check browser console for CORS errors
- Ensure environment variables are set in Vercel

### CORS Issues
The backend already has CORS enabled for all origins. If you still get CORS errors:
1. Check that the API URL is correct
2. Verify the backend is running
3. Check Vercel logs for errors

### Environment Variables
Make sure to add `GROQ_API_KEY` in Vercel project settings:
1. Go to Project Settings
2. Click "Environment Variables"
3. Add `GROQ_API_KEY` with your key value

## Local Testing Before Deployment

```bash
# Terminal 1 - Backend
cd backend && python demo_main.py

# Terminal 2 - Frontend
cd frontend && npm start
```

Visit http://localhost:3000 and test the chatbot before deploying.

## Production Checklist

- ✅ Backend deployed on Vercel
- ✅ Frontend deployed on Vercel
- ✅ API URL updated in ChatInterface.jsx
- ✅ Environment variables set
- ✅ Chatbot tested and working
- ✅ CORS configured
- ✅ All endpoints responding

## Support

For issues:
1. Check Vercel deployment logs
2. Check browser console (F12)
3. Verify API endpoints are accessible
4. Ensure environment variables are set