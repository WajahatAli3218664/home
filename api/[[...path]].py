import os
import sys
from mangum import Mangum

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

try:
    # Import the main FastAPI application
    from backend.main import app

    # Create the Mangum adapter for serverless deployment
    # Disable lifespan to prevent issues in serverless environment
    handler = Mangum(app, lifespan="off")
except Exception as e:
    print(f"Error importing backend.main: {e}")

    # Create a minimal fallback app
    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"error": f"Failed to load main application: {e}"}

    handler = Mangum(app, lifespan="off")