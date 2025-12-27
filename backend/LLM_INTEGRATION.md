# OpenAI and Gemini LLM Integration

This document explains how to use the OpenAI and Gemini integration in the backend.

## Configuration

To use the LLM integration, you need to configure the following environment variables:

### OpenAI Configuration
```bash
OPENAI_API_KEY=your_openai_api_key_here
LLM_PROVIDER=openai  # Optional, defaults to 'openai'
```

### Gemini Configuration
```bash
GEMINI_API_KEY=your_gemini_api_key_here
LLM_PROVIDER=gemini
```

## How It Works

The RAG (Retrieval-Augmented Generation) service is designed to work with both OpenAI and Google's Gemini models:

1. **Dynamic LLM Selection**: Based on the `LLM_PROVIDER` environment variable, the system will automatically use either OpenAI or Gemini.
2. **RAG Pipeline**: The system retrieves relevant textbook content and passes it to the selected LLM along with the user's query.
3. **Response Generation**: The LLM generates a response based only on the provided context, ensuring no hallucinations.

## Implementation Details

- The `RAGService` class in `src/services/rag_service.py` handles the integration
- The `GeminiService` class in `src/services/gemini_service.py` handles Gemini-specific functionality
- Both services use LangChain for prompt management and response handling
- The system enforces strict rules to ensure responses are grounded in the provided context

## Using the Service

The RAG service is used in the chat API endpoint (`/api/v1/chat`) and can be accessed programmatically:

```python
from src.services.rag_service import get_rag_service

rag_service = get_rag_service()
response = rag_service.generate_response(
    query_text="Your question here",
    book_id="book_identifier",
    session_id="session_identifier",
    user_id="user_identifier",  # Optional
    selected_text="selected_text_content"  # Optional
)
```

## Dependencies

The integration uses the following packages:
- `openai`: For OpenAI API access
- `google-generativeai`: For Gemini API access
- `langchain`: For prompt management
- `langchain-openai`: For OpenAI integration with LangChain
- `langchain-google-genai`: For Gemini integration with LangChain

## Troubleshooting

1. **API Key Errors**: Ensure your API keys are correctly set in environment variables
2. **Model Unavailability**: Make sure the specified model (e.g., gpt-3.5-turbo) is available in your account
3. **Network Issues**: Check your internet connection and firewall settings

## Notes

- The system is designed to work without API keys during development, but will show appropriate error messages
- Responses are cached in memory for the duration of the session
- All interactions are logged for debugging and analytics purposes