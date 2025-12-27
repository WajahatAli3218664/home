"""
End-to-end test script for the embedding pipeline
"""
import os
import sys

# Add the backend/src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.embedding_pipeline.main import main

if __name__ == "__main__":
    print("Starting end-to-end test of the embedding pipeline...")
    print(f"Environment variables loaded:")
    print(f"- COHERE_API_KEY exists: {'COHERE_API_KEY' in os.environ or os.path.exists('../backend/.env')}")
    print(f"- QDRANT_URL: {os.environ.get('QDRANT_URL', 'Not set')}")
    print(f"- QDRANT_API_KEY exists: {'QDRANT_API_KEY' in os.environ or os.path.exists('../backend/.env')}")
    
    try:
        main()
        print("Pipeline executed successfully!")
    except Exception as e:
        print(f"Pipeline failed with error: {e}")
        import traceback
        traceback.print_exc()