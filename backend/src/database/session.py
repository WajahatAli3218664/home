from sqlmodel import create_engine, Session
from .config.settings import settings


# Create the database engine using the effective database URL
engine = create_engine(
    settings.effective_database_url,
    echo=True,  # Set to False in production
    pool_pre_ping=True  # Ensures connections are valid before use
)


def get_session():
    """Dependency to get a database session"""
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Create database tables based on models"""
    from .models import User, BookContent, Translation, ChatSession, QuestionContext
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)