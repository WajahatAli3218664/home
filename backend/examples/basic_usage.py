"""
Example script: Basic usage of the embedding pipeline
"""
import sys
import os

# Add the backend/src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.embedding_pipeline.main import main


def run_example():
    print("Running the embedding pipeline...")
    print("Make sure you have set the required environment variables in a .env file:")
    print("- COHERE_API_KEY")
    print("- QDRANT_API_KEY") 
    print("- QDRANT_URL")
    print()
    
    print("Starting pipeline...")
    main()
    print("Pipeline completed!")


if __name__ == "__main__":
    run_example()