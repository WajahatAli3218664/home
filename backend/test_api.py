"""
Test script for the RAG Chatbot API

This script demonstrates how to use the API endpoints for the RAG-based chatbot
"""
import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Health check error: {e}")

def test_api_routes():
    """Test the available API routes"""
    try:
        # Test the root endpoint
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✓ Root endpoint working")
        else:
            print(f"✗ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"✗ API routes error: {e}")

def test_chat_endpoint():
    """Test the chat endpoint (will fail without auth token)"""
    try:
        # This will fail with 401 since we don't have a token
        response = requests.post(
            f"{BASE_URL}/api/v1/chat/",
            json={"query": "Test query"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 401:
            print("✓ Chat endpoint authentication working (401 expected without token)")
        elif response.status_code == 200:
            print("✓ Chat endpoint working")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Chat endpoint unexpected status: {response.status_code}")
    except Exception as e:
        print(f"✗ Chat endpoint error: {e}")

def test_register_user():
    """Test user registration (to get auth token)"""
    try:
        # This is a mock test - actual implementation may vary
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "programming_level": "beginner",
                "ai_experience": "none",
                "gpu_available": False,
                "ram_size": "8GB"
            },
            headers={"Content-Type": "application/json"}
        )
        print(f"User registration response: {response.status_code}")
    except Exception as e:
        print(f"✗ Registration error: {e}")

if __name__ == "__main__":
    print("Testing RAG Chatbot API endpoints...\n")
    
    test_health_check()
    test_api_routes()
    test_chat_endpoint()
    test_register_user()
    
    print("\nFor full functionality testing, you need to:")
    print("1. Register a user and get an access token")
    print("2. Use the token to call the chat endpoint")
    print("3. Ask questions about the Physical AI & Humanoid Robotics textbook")