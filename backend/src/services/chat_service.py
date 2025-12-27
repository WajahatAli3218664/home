import logging
from typing import List, Optional
from uuid import UUID
from sqlmodel import Session, select
from datetime import datetime

from ..database.session import get_session
from ..database.models import ChatSession, QuestionContext, User, BookContent
from ..services.rag_service import RAGService
from ..services.translation_service import TranslationService


class ChatService:
    def __init__(self):
        self.rag_service = RAGService()
        self.translation_service = TranslationService()
        self.logger = logging.getLogger(__name__)

    async def process_query(self, user_id: UUID, query: str) -> str:
        """
        Process a user query using RAG (Retrieval Augmented Generation) based on textbook content
        """
        self.logger.info(f"Processing query for user {user_id}: {query[:50]}...")

        try:
            # Create or get chat session for this user
            session_id = await self._get_or_create_session(user_id, query)

            # For now, use a default book_id - in a real implementation, this would come from user context
            # or be specified in the request
            book_id = "default_book"  # This should be determined based on user context or request

            # Generate a response using the RAG service - this will handle retrieval internally
            # The RAG service will only use the user's query and retrieved textbook content
            # It will NOT use any previous AI responses as context
            self.logger.info(f"Generating response using RAG for user {user_id}")
            response_data = self.rag_service.generate_response(
                query_text=query,
                book_id=book_id,
                session_id=str(session_id),
                user_id=str(user_id)
            )

            # Extract the response text
            response_text = response_data.get("answer", "No response generated")

            # Create question context to track which content was used
            source_chunk_ids = response_data.get("source_chunks_used", [])
            await self._create_question_context(session_id, source_chunk_ids, query, response_text)

            self.logger.info(f"Successfully processed query for user {user_id}")
            return response_text

        except Exception as e:
            # Log the error with full details
            error_msg = f"Error processing query for user {user_id}: {str(e)}"
            self.logger.error(error_msg, exc_info=True)

            # Fallback behavior when external AI service is unavailable
            fallback_response = "Sorry, I encountered an error processing your query. Please try again later."

            # Even in error case, try to save the interaction
            try:
                session_id = await self._get_or_create_session(user_id, query)
                await self._create_question_context(session_id, [], query, fallback_response)
            except Exception as session_error:
                session_error_msg = f"Error saving question context for user {user_id}: {str(session_error)}"
                self.logger.error(session_error_msg, exc_info=True)

            return fallback_response

    async def get_chat_history(self, user_id: UUID) -> List[dict]:
        """
        Retrieve chat history for a specific user
        """
        self.logger.info(f"Retrieving chat history for user {user_id}")

        with get_session() as session:
            try:
                # Get chat sessions for this user
                chat_sessions = session.exec(
                    select(ChatSession).where(ChatSession.user_id == user_id)
                ).all()

                history = []
                for session_item in chat_sessions:
                    # Get question contexts for this session
                    question_contexts = session.exec(
                        select(QuestionContext)
                        .where(QuestionContext.session_id == session_item.id)
                        .order_by(QuestionContext.created_at)
                    ).all()

                    for context in question_contexts:
                        history.append({
                            "id": str(context.id),
                            "query": context.user_query,
                            "response": context.selected_text,  # This will contain the AI response with citations
                            "timestamp": context.created_at.isoformat()
                        })

                # Sort history by timestamp
                history.sort(key=lambda x: x["timestamp"])

                self.logger.info(f"Retrieved {len(history)} messages from chat history for user {user_id}")
                return history
            except Exception as e:
                error_msg = f"Error retrieving chat history for user {user_id}: {str(e)}"
                self.logger.error(error_msg, exc_info=True)
                return []

    async def _get_or_create_session(self, user_id: UUID, first_query: str) -> UUID:
        """
        Get an existing chat session or create a new one
        """
        self.logger.info(f"Getting or creating chat session for user {user_id}")

        with get_session() as session:
            # Create a title based on the first query
            title = first_query[:50] + "..." if len(first_query) > 50 else first_query

            # Create a new chat session
            chat_session = ChatSession(
                user_id=user_id,
                title=title
            )

            session.add(chat_session)
            session.commit()
            session.refresh(chat_session)

            self.logger.info(f"Created new chat session {chat_session.id} for user {user_id}")
            return chat_session.id

    async def _create_question_context(self, session_id: UUID, book_content_ids: List[UUID], user_query: str, response: str) -> None:
        """
        Create question context to track which content was used in the response
        """
        self.logger.info(f"Creating question context for session {session_id}")

        with get_session() as session:
            # For now, we'll use the first content ID if available, otherwise None
            # In a more complex implementation, we might want to link to multiple content sources
            book_content_id = book_content_ids[0] if book_content_ids else None

            question_context = QuestionContext(
                session_id=session_id,
                book_content_id=book_content_id,  # Link to the relevant book content
                selected_text=response,  # Store the AI response with citations
                user_query=user_query
            )

            session.add(question_context)
            session.commit()

            self.logger.info(f"Saved question context for session {session_id}")

    def _extract_content_ids_from_metadata(self, metadata: List[dict]) -> List[UUID]:
        """
        Extract content IDs from the context metadata returned by RAG service
        """
        content_ids = []
        for item in metadata:
            # The ID from Qdrant should map to our book content ID
            # For now, we'll assume they match, but in a real implementation
            # we might need a mapping table
            content_id_str = item.get("id")
            if content_id_str:
                try:
                    content_ids.append(UUID(content_id_str))
                except ValueError:
                    # If it's not a valid UUID, skip it
                    self.logger.warning(f"Invalid UUID in metadata: {content_id_str}")
                    continue
        self.logger.info(f"Extracted {len(content_ids)} content IDs from metadata")
        return content_ids

    def _add_citations_to_response(self, response: str, context_metadata: List[dict]) -> str:
        """
        Add citation information to the response to ensure proper attribution
        This prevents hallucinations by clearly indicating which sources were used
        """
        if not context_metadata:
            # If no references were used, note that this is a general response
            self.logger.warning("No context metadata provided, using fallback citation note")
            return f"{response} [Note: This response is based on general knowledge as no specific textbook content was found for this query.]"

        # Create citation references
        citations = []
        for i, metadata_item in enumerate(context_metadata, 1):
            title = metadata_item.get("metadata", {}).get("title", "Unknown Chapter")
            citations.append(f"[{i}] {title}")

        # Add citations to the response
        citation_text = "References: " + "; ".join(citations)
        self.logger.info(f"Added {len(citations)} citations to response")
        return f"{response} {citation_text}"