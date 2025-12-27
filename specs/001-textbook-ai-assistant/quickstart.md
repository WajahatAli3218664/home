# Quickstart Guide: Textbook AI Assistant

## Overview
This guide provides instructions for setting up and running the Textbook AI Assistant system that helps readers understand the Physical AI & Humanoid Robotics textbook. The system answers questions strictly and exclusively using the content of the textbook using OpenAI Agents SDK and Groq's free-tier model.

## Prerequisites
- Python 3.9+
- Node.js 16+
- Access to Groq API (for llama3-8b-8192 model)
- Access to Qdrant Cloud (Free Tier)
- OpenAI API key for Agents SDK

## Setup Instructions

### 1. Environment Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Set up Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

4. Set up Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

### 2. Environment Configuration
1. Create a `.env` file in the backend directory with the following variables:
   ```env
   GROQ_API_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_cloud_url
   QDRANT_API_KEY=your_qdrant_api_key
   BETTER_AUTH_SECRET=your_auth_secret
   BETTER_AUTH_URL=http://localhost:8000
   ```

2. Ensure your Qdrant Cloud instance has the required collections set up with textbook content embeddings.

### 3. Running the Application

#### Backend (FastAPI)
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

#### Frontend (Docusaurus)
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start the development server:
   ```bash
   npm run start
   ```

## Key Features

### 1. Textbook-Only Responses
- The AI assistant answers questions using only information found in the textbook
- If the answer is not present in the textbook, it responds: "This information is not available in the textbook."
- No external knowledge or assumptions are used

### 2. Citation Requirement
- Every response includes proper citations indicating the source chapter and section
- Citations follow the format: *(Source: Chapter X – Section Name)*

### 3. Selected Text Handling
- Users can select/highlight text in the textbook
- When text is selected, the AI assistant responds only based on that selected text
- Bypasses the general retrieval process for focused answers

### 4. Grounding Enforcement
- Strict validation ensures all responses are grounded in textbook content
- Multi-layered approach with system prompts and response validation

## API Usage Examples

### 1. Asking a Question
```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_auth_token" \
  -d '{
    "question": "Explain embodied cognition principles?",
    "book_id": "physical-ai-humanoid-textbook",
    "session_id": "session-456",
    "selected_text": null
  }'
```

### 2. Asking with Selected Text
```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_auth_token" \
  -d '{
    "question": "Explain this concept?",
    "book_id": "physical-ai-humanoid-textbook",
    "session_id": "session-456",
    "selected_text": "Embodied cognition theory states that cognitive processes are deeply rooted in the body's interactions with the world..."
  }'
```

### 3. Getting Citations
```bash
curl -X GET "http://localhost:8000/api/v1/citations?content_id=content-abc&book_id=physical-ai-humanoid-textbook" \
  -H "Authorization: Bearer your_auth_token"
```

## Troubleshooting

### Common Issues
1. **Groq API Connection Issues**: Ensure your Groq API key is correct and you have access to the llama3-8b-8192 model
2. **OpenAI Agents Issues**: Check that your OpenAI API key is valid and has sufficient quota
3. **Qdrant Connection Issues**: Verify your Qdrant URL and API key are correct
4. **Grounding Enforcement**: If responses seem to have hallucinations, review the validation settings

### Performance Tips
1. Adjust the similarity threshold in the retrieval service based on your textbook content
2. Monitor Groq API usage to stay within free tier limits
3. Use appropriate chunk sizes for textbook content in Qdrant

## Next Steps
1. Customize the system prompts to match your textbook's tone and style
2. Add more sophisticated citation formatting if needed
3. Implement additional validation for response accuracy
4. Consider adding support for additional textbooks