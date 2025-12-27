from typing import List, Dict, Any, Optional
from uuid import UUID, uuid4
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()

class GeminiService:
    def __init__(self):
        # Initialize Gemini API key
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        
        # Initialize LangChain ChatGoogleGenerativeAI model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",  # You can change this to gemini-1.5-pro for better performance
            temperature=0.3,  # Lower temperature for more consistent responses
            max_tokens=1000,
            google_api_key=api_key
        )
        
        # Create a RAG prompt template
        self.rag_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Retrieval-Augmented Generation (RAG) chatbot embedded inside a published book. Your primary responsibility is to answer user questions accurately and clearly using ONLY the information provided in the retrieved context from the book.

            SYSTEM CONTEXT:
            - Retrieved passages are provided to you as "context".
            - Sometimes the user will highlight or select specific text from the book; when this happens, that selected text MUST be treated as the only allowed source of truth.

            STRICT RULES:
            1. You MUST NOT use outside knowledge, training data, or assumptions.
            2. You MUST answer strictly based on the provided context.
            3. If the answer is not present in the provided context, respond with: "The selected content does not contain enough information to answer this question."
            4. Do NOT hallucinate, infer, or extend beyond the given text in the context.
            5. Do NOT mention technical implementation details like Qdrant, embeddings, vector search, or system architecture in your answers.
            6. Do NOT quote large passages unless explicitly asked by the user.
            7. Keep responses concise and helpful.

            ANSWER STYLE:
            - Be concise, clear, and helpful.
            - Prefer bullet points for explanations when appropriate.
            - Use simple language suitable for readers of the book.
            - Avoid unnecessary verbosity."""),
            ("human", "Question: {question}\n\nContext: {context}"),
        ])
        
        # Create the RAG chain
        self.rag_chain = (
            {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
            | self.rag_prompt
            | self.llm
            | StrOutputParser()
        )

    def generate_response(self, query: str, context: str) -> str:
        """Generate an answer using the context and query with Gemini RAG chain"""
        try:
            # Use the RAG chain to generate a response based on the context and query
            response = self.rag_chain.invoke({"context": context, "question": query})
            return response
        except Exception as e:
            # If there's an error with the LLM call, return a default message
            print(f"Error generating response with Gemini: {str(e)}")
            return "The selected content does not contain enough information to answer this question."