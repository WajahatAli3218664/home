# Quickstart Guide: Frontend Authentication, Personalization, and Translation Integration

## Overview
This guide provides instructions for implementing and using the frontend authentication, personalization, and translation features in the Docusaurus textbook platform.

## Prerequisites
- Node.js 16+ installed
- Docusaurus project set up and running
- Backend API running at `http://localhost:8000` (or configured endpoint)
- Basic knowledge of React and Docusaurus

## Frontend Setup

### 1. Install Dependencies
The implementation uses standard Docusaurus/React functionality, so no additional dependencies are required beyond what's already in the project:
```bash
cd frontend
npm install
```

### 2. Add the Authentication Context
1. Create the auth context file at `frontend/src/components/Auth/AuthContext.jsx`:
2. This will provide global authentication state across the application

### 3. Create Authentication Pages
1. Create signup page at `frontend/src/pages/signup.jsx`
2. Create signin page at `frontend/src/pages/signin.jsx`

### 4. Implement the Root Wrapper
1. Update or create `frontend/src/theme/Root.jsx` to wrap the app with AuthContext

### 5. Create Chapter Components
1. Create `frontend/src/components/Chapter/ChapterActions.jsx` component
2. Create `frontend/src/components/Chapter/PersonalizeButton.jsx` component
3. Create `frontend/src/components/Chapter/TranslateButton.jsx` component
4. Create `frontend/src/components/Chapter/ContentDisplay.jsx` component

## Usage Guide

### User Registration
1. Navigate to `/signup` page
2. Fill in all required fields:
   - Email
   - Password
   - Programming Level (Beginner/Intermediate/Advanced)
   - AI Experience (None/Basic/Intermediate/Advanced)
   - GPU Availability (Yes/No)
   - RAM Size (4GB/8GB/16GB/32GB)
3. Submit the form to create an account
4. The JWT token will be stored in localStorage

### User Signin
1. Navigate to `/signin` page
2. Enter email and password
3. Submit the form
4. The JWT token will be stored in localStorage

### Chapter Personalization
1. Log in to your account
2. Navigate to any chapter page
3. Click the "Personalize Chapter" button
4. Wait for the loading indicator to complete
5. The chapter content will be replaced with a personalized version

### Urdu Translation
1. Log in to your account
2. Navigate to any chapter page
3. Click the "اردو میں پڑھیں" (Read in Urdu) button
4. Wait for the loading indicator to complete
5. The chapter content will be replaced with the Urdu translation (with proper RTL styling)

### Reverting Content
1. After personalizing or translating, you can revert to the original content
2. Look for the "Show Original" or similar button in the chapter interface

## API Integration

### Calling the Backend
All API calls will follow this pattern:
```js
const response = await fetch('http://localhost:8000/auth/signup', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`  // For authenticated endpoints
  },
  body: JSON.stringify(data)
});
```

### Available Endpoints
- `POST /auth/signup` - Create a new user
- `POST /auth/signin` - Authenticate a user
- `POST /chapter/personalize` - Personalize chapter content
- `POST /chapter/translate` - Translate chapter to Urdu

## Component Integration

### Adding to Chapter Pages
To add personalization and translation buttons to a chapter page, use the ChapterActions component:

The Docusaurus theme swizzling will automatically inject these components into all chapter pages.

### Error Handling
The components will display appropriate error messages when:
- API calls fail
- User is not authenticated for protected operations
- Network timeouts occur
- Backend services are temporarily unavailable

## Testing

### Manual Testing
1. Test signup with valid and invalid data
2. Test signin with valid and invalid credentials
3. Test JWT token persistence across sessions
4. Test personalization with different user profiles
5. Test translation to Urdu
6. Test reverting to original content
7. Test error handling scenarios

### Expected Behaviors
- Signup should create a user and store JWT token
- Signin should retrieve and store JWT token
- Personalization should replace content with a personalized version
- Translation should replace content with Urdu text in RTL layout
- Error states should show meaningful messages to users
- Content reversion should restore original content properly

## Troubleshooting

### Common Issues
1. **JWT Token Not Persisting**: Check localStorage access and token storage logic
2. **API Calls Failing**: Verify backend server is running and API endpoints are accessible
3. **Urdu Text Not Rendering RTL**: Ensure proper CSS direction attributes are applied
4. **Authentication Context Not Working**: Verify the Root.jsx wrapper is properly configured

### Useful Commands
```bash
# Start the Docusaurus development server
cd frontend
npm run start

# Build the static site
npm run build

# Serve the built site locally
npm run serve
```

## Next Steps
1. Add tests for the new components
2. Implement additional languages for translation
3. Enhance the personalization algorithm
4. Add analytics for feature usage
5. Optimize performance for large content