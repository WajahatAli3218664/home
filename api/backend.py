import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

# Import the FastAPI app from main.py
from backend.main import app

# For Vercel Python runtime with serverless functions
def handler(event, context):
    # Vercel serverless function handler
    # This is a simplified example - in practice, you'd use something like Mangum
    # to convert FastAPI app to AWS Lambda/Serverless format
    import json
    
    # Extract path and method from the event
    path = event.get('path', '/')
    method = event.get('method', 'GET')
    
    # For a complete implementation, you would need to properly handle the request
    # and response using ASGI, but for Vercel deployment, we'll use the approach below
    
    # Return a simple response to indicate the API is working
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({
            "message": "Backend API is running on Vercel",
            "path": path,
            "method": method
        })
    }