# Quickstart: Debug RAG Context Flow

## Overview
This guide helps you quickly set up and run the debugging tools for the RAG context flow issue. This will help identify why retrieved context from Qdrant is not reaching the LLM.

## Prerequisites
- Python 3.11+
- Access to Qdrant vector database with textbook data ingested
- Access to Qwen LLM API
- Backend dependencies installed (FastAPI, etc.)

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Qdrant and Qwen API details
   ```

## Running the Debug Tools

### 1. Run the minimal working RAG implementation
This serves as a reference for the correct implementation:

```bash
python -m backend.src.debug.minimal_rag
```

### 2. Test the context flow
Use the debug endpoint to test the complete flow:

```bash
curl -X GET "http://localhost:8000/debug/context-flow?query=What+are+the+principles+of+robot+kinematics&debug=true"
```

### 3. Check the logs
To see what context is being sent to the LLM:

```bash
curl -X GET "http://localhost:8000/debug/log-context"
```

### 4. Test custom prompts
To test specific prompt formatting:

```bash
curl -X POST "http://localhost:8000/debug/test-prompt" \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "What are the principles of robot kinematics?",
    "retrieved_context": [
      {
        "content": "Robot kinematics is the study of motion in robotic systems...",
        "source_document": "chapter_3_kinematics.md"
      }
    ]
  }'
```

## Key Files for Debugging

1. `backend/src/services/rag_service.py` - Main RAG service where context flow issues likely exist
2. `backend/src/services/qdrant_service.py` - Context retrieval from Qdrant
3. `backend/src/services/llm_service.py` - LLM interaction and prompt formatting
4. `backend/src/debug/minimal_rag.py` - Minimal working implementation reference

## Common Debugging Steps

1. **Add logging to track context flow**: Check what context is retrieved and if it's being passed to the LLM
2. **Verify prompt formatting**: Ensure the retrieved context is properly formatted into the LLM prompt
3. **Check API calls**: Verify that the context is actually sent to the LLM API
4. **Compare with minimal implementation**: Use the minimal working example as a reference

## Troubleshooting

### Issue: No context being retrieved
- Check Qdrant connection and query parameters
- Verify the vector database contains the expected textbook data

### Issue: Context retrieved but not in LLM response
- Check if the context is properly formatted into the prompt
- Verify the prompt with context is actually being sent to the LLM

### Issue: Generic responses despite proper context
- Check LLM prompt formatting and length limits
- Verify the LLM is actually receiving the formatted prompt