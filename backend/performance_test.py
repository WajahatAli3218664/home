"""
Performance testing to ensure responses within 3 seconds
"""
import time
import requests
from concurrent.futures import ThreadPoolExecutor
import statistics


def test_single_request(url, payload):
    """
    Test a single request and measure response time
    """
    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        return {
            "status_code": response.status_code,
            "response_time": response_time,
            "success": response.status_code == 200,
            "content": response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        end_time = time.time()
        return {
            "status_code": 0,
            "response_time": end_time - start_time,
            "success": False,
            "error": str(e)
        }


def performance_test(base_url, num_requests=10, concurrency=5):
    """
    Perform performance testing on the ask endpoint
    """
    url = f"{base_url}/api/v1/ask"
    
    # Sample payload for testing
    payload = {
        "question": "What are the principles of embodied cognition?",
        "book_id": "physical-ai-humanoid-textbook",
        "session_id": "test-session-456",
        "selected_text": None
    }
    
    print(f"Starting performance test with {num_requests} requests and {concurrency} concurrent workers...")
    
    # Use ThreadPoolExecutor to make concurrent requests
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(test_single_request, url, payload) for _ in range(num_requests)]
        results = [future.result() for future in futures]
    
    # Analyze results
    successful_requests = [r for r in results if r["success"]]
    failed_requests = [r for r in results if not r["success"]]
    response_times = [r["response_time"] for r in successful_requests]
    
    print(f"\nTest Results:")
    print(f"Total requests: {len(results)}")
    print(f"Successful requests: {len(successful_requests)}")
    print(f"Failed requests: {len(failed_requests)}")
    print(f"Success rate: {len(successful_requests)/len(results)*100:.2f}%")
    
    if response_times:
        print(f"\nResponse Time Statistics:")
        print(f"Average response time: {statistics.mean(response_times):.4f}s")
        print(f"Median response time: {statistics.median(response_times):.4f}s")
        print(f"Min response time: {min(response_times):.4f}s")
        print(f"Max response time: {max(response_times):.4f}s")
        print(f"95th percentile: {sorted(response_times)[int(0.95*len(response_times))]:.4f}s")
        
        # Check if 95% of requests are under 3 seconds
        under_3s = [rt for rt in response_times if rt <= 3.0]
        print(f"Requests under 3s: {len(under_3s)/len(response_times)*100:.2f}%")
        
        if len(under_3s)/len(response_times) >= 0.95:
            print("✅ Performance requirement met: 95% of requests under 3 seconds")
        else:
            print("❌ Performance requirement not met: Less than 95% of requests under 3 seconds")
    
    # Show failed requests
    if failed_requests:
        print(f"\nFailed Requests:")
        for i, fr in enumerate(failed_requests[:5]):  # Show first 5 failures
            print(f"  {i+1}. Response time: {fr['response_time']:.4f}s, Error: {fr.get('error', 'Unknown')}")
    
    return results


if __name__ == "__main__":
    # Test against local development server
    BASE_URL = "http://localhost:8000"
    
    # Run performance test
    results = performance_test(BASE_URL, num_requests=20, concurrency=5)