"""
Performance test for the RAG context flow
Ensures response times are under 500ms as specified in the requirements
"""
import time
import sys
import os
from typing import Dict, List
import statistics

# Add the backend src directory to the path so we can import modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.services.rag_service import RAGService


def performance_test(query: str, iterations: int = 10) -> Dict[str, any]:
    """
    Performance test for the RAG context flow
    """
    print(f"Running performance test for query: '{query}'")
    print(f"Running {iterations} iterations...")
    print("-" * 50)
    
    rag_service = RAGService()
    
    response_times = []
    
    for i in range(iterations):
        start_time = time.time()
        
        try:
            # Execute the RAG service to get an answer
            result = rag_service.get_answer(
                query=query,
                book_id="default_book",
                session_id=f"perf_test_{i}"
            )
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            response_times.append(response_time)
            
            print(f"Iteration {i+1}: {response_time:.2f}ms - Success")
            
        except Exception as e:
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            response_times.append(response_time)
            
            print(f"Iteration {i+1}: {response_time:.2f}ms - Error: {str(e)}")
    
    # Calculate statistics
    avg_response_time = statistics.mean(response_times)
    median_response_time = statistics.median(response_times)
    min_response_time = min(response_times)
    max_response_time = max(response_times)
    std_deviation = statistics.stdev(response_times) if len(response_times) > 1 else 0
    
    # Check if requirements are met
    under_500ms_count = sum(1 for rt in response_times if rt < 500)
    success_rate = (under_500ms_count / len(response_times)) * 100
    
    results = {
        "query": query,
        "iterations": iterations,
        "response_times": response_times,
        "avg_response_time": avg_response_time,
        "median_response_time": median_response_time,
        "min_response_time": min_response_time,
        "max_response_time": max_response_time,
        "std_deviation": std_deviation,
        "under_500ms_count": under_500ms_count,
        "success_rate": success_rate,
        "requirements_met": avg_response_time < 500
    }
    
    print("\n" + "=" * 50)
    print("PERFORMANCE TEST RESULTS")
    print("=" * 50)
    print(f"Query: {query}")
    print(f"Average Response Time: {avg_response_time:.2f}ms")
    print(f"Median Response Time: {median_response_time:.2f}ms")
    print(f"Min Response Time: {min_response_time:.2f}ms")
    print(f"Max Response Time: {max_response_time:.2f}ms")
    print(f"Std Deviation: {std_deviation:.2f}ms")
    print(f"Under 500ms: {under_500ms_count}/{iterations} ({success_rate:.1f}%)")
    print(f"Requirements Met (avg < 500ms): {'YES' if results['requirements_met'] else 'NO'}")
    
    return results


def run_performance_tests():
    """
    Run a series of performance tests
    """
    test_queries = [
        "What are the principles of robot kinematics?",
        "Explain the concept of forward kinematics",
        "How does inverse kinematics work?",
        "What is the Jacobian matrix in robotics?",
        "Briefly describe robot dynamics"
    ]
    
    print("Running RAG Context Flow Performance Tests")
    print("=" * 60)
    
    all_results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}/{len(test_queries)}:")
        result = performance_test(query, iterations=5)  # Fewer iterations for multiple queries
        all_results.append(result)
        print()
    
    # Overall summary
    print("=" * 60)
    print("OVERALL PERFORMANCE SUMMARY")
    print("=" * 60)
    
    all_response_times = []
    all_requirements_met = True
    
    for i, result in enumerate(all_results, 1):
        print(f"Query {i}: {result['query']}")
        print(f"  Avg: {result['avg_response_time']:.2f}ms | Under 500ms: {result['success_rate']:.1f}%")
        
        all_response_times.extend(result['response_times'])
        if not result['requirements_met']:
            all_requirements_met = False
    
    overall_avg = statistics.mean(all_response_times)
    print(f"\nOverall Average Response Time: {overall_avg:.2f}ms")
    print(f"All Requirements Met: {'YES' if all_requirements_met and overall_avg < 500 else 'NO'}")
    
    return all_results


if __name__ == "__main__":
    run_performance_tests()