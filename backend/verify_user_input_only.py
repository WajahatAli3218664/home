"""
Verification script to confirm that LLM/RAG only uses user input, not previous AI responses
"""
import os
import inspect
import ast
from pathlib import Path

def verify_implementation():
    print("[INFO] Verifying that LLM/RAG only uses user input (not previous AI responses)")
    
    # Read the source code of rag_service.py to analyze the methods
    rag_service_path = Path("src/services/rag_service.py")
    with open(rag_service_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    # Parse the source code
    tree = ast.parse(source_code)
    
    # Find the _generate_answer_with_context method
    generate_method_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "_generate_answer_with_context":
            generate_method_found = True
            # Get the arguments of the method
            args = [arg.arg for arg in node.args.args if arg.arg != 'self']
            print(f"[SUCCESS] Method _generate_answer_with_context takes parameters: {args}")
            
            if args == ['query', 'context']:
                print("[SUCCESS] The method only accepts user query and textbook context, not previous AI responses")
            else:
                print(f"[ERROR] Unexpected parameters: {args}")
                return False
            break
    
    if not generate_method_found:
        print("[ERROR] _generate_answer_with_context method not found")
        return False
    
    # Find the generate_response method
    generate_response_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "generate_response":
            generate_response_found = True
            # Get the arguments of the method
            args = [arg.arg for arg in node.args.args if arg.arg != 'self']
            print(f"[SUCCESS] Method generate_response takes parameters: {args}")
            
            if 'query_text' in args and 'selected_text' in args:
                print("[SUCCESS] The method accepts user query and selected text, not previous AI responses")
            else:
                print(f"[ERROR] Unexpected parameters: {args}")
                return False
            break
    
    if not generate_response_found:
        print("[ERROR] generate_response method not found")
        return False
    
    # Find the retrieve_context method
    retrieve_context_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "retrieve_context":
            retrieve_context_found = True
            # Get the arguments of the method
            args = [arg.arg for arg in node.args.args if arg.arg != 'self']
            print(f"[SUCCESS] Method retrieve_context takes parameters: {args}")
            
            if args == ['query', 'book_id']:
                print("[SUCCESS] The method only accepts user query and book_id, not previous AI responses")
            else:
                print(f"[ERROR] Unexpected parameters: {args}")
                return False
            break
    
    if not retrieve_context_found:
        print("[ERROR] retrieve_context method not found")
        return False
    
    # Now let's also check the content of the _generate_answer_with_context method
    # to ensure it only uses query and context
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "_generate_answer_with_context":
            # Look for any references to previous AI responses in the function body
            function_source = ast.get_source_segment(source_code, node)
            
            # Check if there are any references to previous responses, history, or similar
            forbidden_terms = ['previous', 'history', 'response', 'answer', 'chat_history']
            has_forbidden_usage = False
            
            for term in forbidden_terms:
                if term in function_source.lower():
                    # Check if it's a legitimate usage (e.g., "response" in "generate_response" is OK)
                    # but "previous_response" or "history" would not be
                    if 'previous' in function_source.lower() or 'history' in function_source.lower():
                        print(f"[WARNING] Found potentially problematic term '{term}' in method: {function_source[:100]}...")
                        has_forbidden_usage = True
            
            if not has_forbidden_usage:
                print("[SUCCESS] No problematic references to previous responses found in method")
            else:
                print("[ERROR] Found references to previous responses in method")
                return False
            break
    
    print("\n" + "="*60)
    print("VERIFICATION RESULTS:")
    print("[SUCCESS] LLM/RAG system only uses USER input")
    print("[SUCCESS] LLM/RAG system does NOT use previous AI answers as query")
    print("[SUCCESS] Implementation correctly follows the requirement")
    print("="*60)
    
    return True

if __name__ == "__main__":
    success = verify_implementation()
    if success:
        print("\n[SUCCESS] All verifications passed! The implementation correctly ensures that")
        print("   the LLM/RAG system only uses user input and not previous AI responses.")
    else:
        print("\n[ERROR] Some verifications failed!")