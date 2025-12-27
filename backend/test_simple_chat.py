import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def test_simple_chat_endpoint():
    """Test the simple chat endpoint"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chat/",  # The endpoint we defined
            json={"message": "Hello, this is a test message!"},
            headers={"Content-Type": "application/json"}
        )

        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error calling chat endpoint: {e}")

def test_simple_chat_endpoint_no_slash():
    """Test the simple chat endpoint without trailing slash"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/chat",  # The endpoint we defined without trailing slash
            json={"message": "Hello, this is a test message!"},
            headers={"Content-Type": "application/json"}
        )

        print(f"Status Code (no slash): {response.status_code}")
        if response.status_code == 200:
            print(f"Response (no slash): {response.json()}")
        else:
            print(f"Error (no slash): {response.text}")
    except Exception as e:
        print(f"Error calling chat endpoint (no slash): {e}")

if __name__ == "__main__":
    print("Testing the simple chat endpoint...")
    test_simple_chat_endpoint()
    test_simple_chat_endpoint_no_slash()