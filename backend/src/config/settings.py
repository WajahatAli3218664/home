"""
Configuration settings for the AI-powered book RAG system
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "Textbook Generation API"
    api_description: str = "API for generating textbooks using AI"
    api_version: str = "1.0.0"

    # Security Configuration
    secret_key: str = "QmxwloIKk2JG3uxzRK4kyUjlgzKPFGRXAOYu2LuKQnY"

    # Database Configuration
    database_url: str = "postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
    neon_database_url: str = ""

    # Qdrant Vector Database Configuration
    qdrant_url: str = "https://c7037b66-6e44-4312-9979-db1cb85c4eb5.us-east4-0.gcp.cloud.qdrant.io:6333"
    qdrant_api_key: Optional[str] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.ch7uZur2kx0ity3JhZAwhAQzaSqS0mW4TDg8GITC8jM"
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_https: str = "false"

    # Qdrant Collection Configuration
    qdrant_collection_name: str = "textbook_vectors"
    qdrant_vector_size: int = 1536
    qdrant_distance: str = "Cosine"

    # AI Provider Keys
    openrouter_api_key: Optional[str] = None
    cohere_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None

    # Application Configuration
    debug: bool = True
    log_level: str = "INFO"

    # Source URLs
    source_urls: str = "https://areejshaikh.github.io/book/,https://areejshaikh.github.io/book/docs/intro"

    # Context7 MCP Configuration
    context7_api_key: Optional[str] = None
    context7_base_url: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


# Create a global settings instance
settings = Settings()