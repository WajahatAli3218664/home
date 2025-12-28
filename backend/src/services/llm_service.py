"""
LLM service using Groq and OpenAI models
"""
from openai import OpenAI
from groq import Groq
from typing import Optional
from ..config.settings import settings
from ..utils.prompt_formatter import PromptFormatter


class LLMService:
    """
    Service for interacting with Large Language Models (using Groq with fallback to OpenAI)
    """
    
    def __init__(self):
        # Initialize Groq client
        self.groq_client = Groq(api_key=settings.groq_api_key)
        self.groq_model = settings.groq_model
        
        # Initialize OpenAI client as backup (v1.0.0+ syntax)
        if settings.openai_api_key:
            self.openai_client = OpenAI(api_key=settings.openai_api_key)
        else:
            self.openai_client = None
        self.openai_model = "gpt-3.5-turbo"  # Default fallback model
    
    def generate_response(self, query: str, context: str) -> str:
        """
        Generate a response to the user query based on the provided context

        Args:
            query: The user's question
            context: The relevant context retrieved from the textbook

        Returns:
            Generated response string
        """
        # Validate the prompt components
        validation = PromptFormatter.validate_prompt_components(query, context)
        if not validation["context_valid"]:
            return "This information is not available in the textbook."

        # Format the prompt using the PromptFormatter utility
        formatted_prompt = PromptFormatter.format_rag_prompt(query, context)

        try:
            # Try to use Groq first (as specified in requirements)
            response = self.groq_client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {"role": "system", "content": formatted_prompt["system"]},
                    {"role": "user", "content": formatted_prompt["user"]}
                ],
                temperature=0.3,  # Lower temperature for more consistent responses
                max_tokens=500  # Limit response length
            )

            # Extract the response text
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error calling Groq API: {str(e)}")
            print("Falling back to OpenAI API")

            # Fallback to OpenAI API (v1.0.0+ syntax)
            if not self.openai_client:
                raise Exception("No OpenAI API key configured for fallback")
            
            try:
                response = self.openai_client.chat.completions.create(
                    model=self.openai_model,
                    messages=[
                        {"role": "system", "content": formatted_prompt["system"]},
                        {"role": "user", "content": formatted_prompt["user"]}
                    ],
                    temperature=0.3,  # Lower temperature for more consistent responses
                    max_tokens=500  # Limit response length
                )

                # Extract the response text (v1.0.0+ syntax)
                return response.choices[0].message.content.strip()

            except Exception as e:
                # Handle any errors from the API
                raise Exception(f"Error calling LLM API: {str(e)}")
    
    def _get_system_prompt(self) -> str:
        """
        Get the system prompt that enforces answering only from provided context
        """
        return (
            "You are an AI assistant for the Physical AI & Humanoid Robotics textbook. "
            "You MUST answer ONLY based on the information provided in the context. "
            "If the context does not contain enough information to answer the question, "
            "clearly state: 'This information is not available in the textbook.' "
            "Do NOT use external knowledge, training data, or assumptions beyond the provided context. "
            "Do NOT mention technical implementation details like vector search or system architecture. "
            "Provide concise, clear, and helpful answers. Use bullet points when appropriate. "
            "Use simple language suitable for readers of the textbook. Do NOT quote large passages unless explicitly asked. "
            "Include proper citations with each response indicating the source chapter and section."
        )
    
    def check_external_knowledge_needed(self, query: str) -> bool:
        """
        Check if a query requires external knowledge not available in the textbook
        This is a simple heuristic - in practice, this would be more sophisticated
        """
        external_knowledge_indicators = [
            "current events",
            "recent news",
            "latest",
            "today",
            "real-time",
            "live",
            "2023",  # Assuming the textbook content is not from 2023
            "2024",
            "2025",
            "2026",
            "future",
            "stock price",
            "weather",
            "today's date"
        ]
        
        query_lower = query.lower()
        for indicator in external_knowledge_indicators:
            if indicator in query_lower:
                return True
        
        return False