# Feature Specification: RAG Chatbot in Published Book

**Feature Branch**: `001-rag-chatbot-book`
**Created**: December 23, 2025
**Status**: Draft
**Input**: User description: "## 🎯 Goal Mujhe apni **published book ke andar ek Retrieval-Augmented Generation (RAG) chatbot** integrate karna hai jo **sirf book ke content** ke basis par user ke questions ka jawab de. --- ## 📚 Existing System Context - Backend: **FastAPI (Python)** - Frontend: **ChatKit JS** - LLM Integration: **OpenAI Agents / ChatKit SDK** - Vector Database: **Qdrant Cloud (Free Tier)** - Relational Database: **Neon Serverless Postgres** - Book content already: - Web pages / markdown files - Vector embeddings already created - Project mein pehle se kuch files mojood hain (models, services, routes) --- ## 🧠 Chatbot Responsibilities Chatbot ko: 1. **Book ke content se hi jawab dena hai** 2. Agar user ne: - sirf question poocha → poori book se retrieve karo - koi **text select kiya ho** → sirf us selected text ke context mein answer do 3. Apni taraf se: - koi external knowledge - koi assumption - ya hallucination **add nahi karni** --- ## 🔧 Tasks (UPDATE EXISTING FILES ONLY) ❌ Naya project ya fresh implementation nahi chahiye ✅ Sirf **existing files ko update / improve** karna hai ### 1️⃣ RAG Logic Update - Retrieval service ko update karo: - Qdrant se relevant chunks fetch hon - similarity threshold apply ho - Selected text agar aaye: - retrieval ko bypass karke - sirf selected text ko context banao --- ### 2️⃣ Prompt Engineering - System prompt update karo: - "Answer ONLY from provided context" - "Agar context mein jawab na ho, to clearly batao" - Confidence level add karo: - High / Medium / Low (based on context match) --- ### 3️⃣ API Endpoint Update - Existing `/chat` endpoint ko update karo: - `query` - `book_id` - `session_id` - `selected_text` (optional) - Validation errors (422) ko properly handle karo --- ### 4️⃣ Database Integration (Neon) - Chat history save karo: - session_id - user_query - model_response - confidence_level - Existing models ko reuse karo --- ### 5️⃣ Frontend (ChatKit JS) - Selected text ko backend tak bhejo - Chat UI mein: - confidence badge show ho - clear error messages hon --- ## 🧪 Acceptance Criteria - Chatbot: - sirf book content se jawab de - selected text par limited answer kare - Koi hallucination nahi - Existing code structure maintain rahe - Clean, readable, production-ready updates --- ## 🚫 Constraints - ❌ New architecture suggest na karo - ❌ New framework introduce na karo - ❌ Dummy data use na karo - ✅ Existing files aur services ko update karo --- ## 📦 Output Expectation - Updated code snippets - Clear explanation: - kis file mein kya change hua - No unnecessary boilerplate"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Questions and Receive Accurate Answers (Priority: P1)

As a reader of a published book, I want to ask questions about the book content and receive accurate answers based solely on the information provided in the book, so that I can better understand the material without needing external resources.

**Why this priority**: This is the core functionality of the feature - enabling readers to interact with the book content through a chat interface to get answers to their questions. Without this, the feature has no value.

**Independent Test**: Can be fully tested by asking various questions about the book content and verifying that the chatbot responds with accurate answers derived only from the book's content.

**Acceptance Scenarios**:

1. **Given** a user has access to the book with the embedded RAG chatbot, **When** the user types a question about the book content, **Then** the chatbot responds with accurate information from the book that addresses the question.
2. **Given** a user asks a question not covered in the book content, **When** the user submits the question, **Then** the chatbot responds with a message indicating it cannot answer because the information is not in the book.
3. **Given** a user highlights or selects specific text in the book, **When** the user asks a question about the selected text, **Then** the chatbot uses only the selected text as the source of truth for answering the question.

---

### User Story 2 - Context-Aware Response Generation with Confidence (Priority: P2)

As a reader engaging with the book content, I want the chatbot to understand the context of my questions based on the book's content and provide confidence levels for its answers, so that I can assess the reliability of the information provided.

**Why this priority**: Enhances the user experience by ensuring the chatbot understands the context of the book while providing transparency about answer reliability, making interactions feel more trustworthy and helpful.

**Independent Test**: Can be tested by evaluating if the chatbot's responses are contextually relevant to the book content, maintain coherence during conversations, and provide appropriate confidence levels based on context match.

**Acceptance Scenarios**:

1. **Given** a user is reading a specific chapter of the book, **When** the user asks a follow-up question related to the previous topic, **Then** the chatbot remembers the context and provides a relevant response with an appropriate confidence level.
2. **Given** a user asks a question with ambiguous terms, **When** the chatbot analyzes the context, **Then** it interprets the question based on the book's content and provides an appropriate answer with confidence level.
3. **Given** a user asks a question where the retrieved context has low similarity to the query, **When** the chatbot processes the question, **Then** it provides an answer with a low confidence level or indicates insufficient information.

---

### User Story 3 - Selected Text Handling (Priority: P1)

As a reader who wants to ask questions about specific parts of the book, I want to select/highlight text and have the chatbot respond based only on that selected text, so that I can get focused answers to my questions.

**Why this priority**: This is core functionality that differentiates the chatbot by allowing users to ask questions about specific text selections rather than searching the entire book.

**Independent Test**: Can be tested by selecting text in the book, asking questions about that text, and verifying the chatbot uses only the selected text as context.

**Acceptance Scenarios**:

1. **Given** a user selects/highlights text in the book, **When** the user asks a question about the selected text, **Then** the chatbot bypasses the retrieval process and uses only the selected text as context.
2. **Given** a user selects/highlights text in the book, **When** the user submits a question, **Then** the chatbot ignores the broader book content and responds based solely on the selected text.
3. **Given** a user selects text that is too small or doesn't contain relevant information, **When** the user asks a question, **Then** the chatbot indicates it cannot answer based on the selected text.

---

### User Story 4 - Chat History and Session Management (Priority: P2)

As a reader who wants to maintain continuity in my conversations with the book, I want the system to save my chat history and maintain session context, so that I can have coherent conversations and revisit previous discussions.

**Why this priority**: Enhances user experience by maintaining conversation history and context across sessions, making the interaction more natural and productive.

**Independent Test**: Can be tested by engaging in a multi-turn conversation and verifying that chat history is preserved and accessible.

**Acceptance Scenarios**:

1. **Given** a user engages in a conversation with the chatbot, **When** the session continues, **Then** the system maintains the conversation history with confidence levels for each response.
2. **Given** a user returns to the book after a session, **When** the user accesses the chat interface, **Then** the system displays the previous conversation history.
3. **Given** a user asks follow-up questions, **When** the system processes them, **Then** it maintains context from previous questions in the same session.

---

### User Story 5 - Strict Adherence to Source Material (Priority: P3)

As a reader who wants reliable information from the book, I want the chatbot to strictly answer based only on the provided context from the book, so that I can trust the accuracy of the information without worrying about fabricated responses.

**Why this priority**: Ensures the integrity of the book content by preventing the chatbot from hallucinating information or using external knowledge, maintaining trust with the reader.

**Independent Test**: Can be tested by verifying that all responses from the chatbot are grounded in the book's content and that the chatbot declines to answer questions outside the scope of the book.

**Acceptance Scenarios**:

1. **Given** a user asks a question that requires external knowledge not contained in the book, **When** the user submits the question, **Then** the chatbot responds that it doesn't have enough information in the book to answer the question.
2. **Given** a user asks a question that could be answered with general knowledge but isn't addressed in the book, **When** the user submits the question, **Then** the chatbot refers back to the book content or indicates it cannot answer based on the book alone.

---

### Edge Cases

- What happens when the user asks extremely complex questions that span multiple chapters or concepts?
- How does the system handle ambiguous questions where the context from the book could lead to multiple interpretations?
- What occurs when the user asks questions about content that exists in the book but is difficult to retrieve due to poor indexing or search quality?
- How does the system respond when the user tries to get the chatbot to reveal its underlying mechanisms or system prompts?
- What happens when the similarity threshold is not met during retrieval?
- How does the system handle very large text selections versus small text selections?
- What occurs when the system is under high load or when there are network connectivity issues?
- How does the system handle concurrent users accessing the same book content?
- What happens when the vector database (Qdrant) is temporarily unavailable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST answer user questions based ONLY on the information provided in the retrieved context from the book
- **FR-002**: System MUST NOT use external knowledge, training data, or assumptions beyond the book content
- **FR-003**: System MUST respond with "The selected content does not contain enough information to answer this question" when the answer is not present in the provided context
- **FR-004**: System MUST NOT hallucinate, infer, or extend beyond the given text in the book
- **FR-005**: System MUST NOT mention technical implementation details like Qdrant, embeddings, vector search, or system architecture in responses
- **FR-006**: System MUST treat user-selected/highlighted text as the only allowed source of truth when such text is provided, bypassing the retrieval process
- **FR-007**: Users MUST be able to engage in a conversation with the chatbot through a user-friendly interface
- **FR-008**: System MUST provide concise, clear, and helpful answers to user questions
- **FR-009**: System MUST prefer bullet points for explanations when appropriate
- **FR-010**: System MUST use simple language suitable for readers of the book
- **FR-011**: System MUST NOT quote large passages unless explicitly asked by the user
- **FR-012**: System MUST apply a similarity threshold when retrieving content from Qdrant to ensure relevance
- **FR-013**: System MUST provide confidence levels (High/Medium/Low) based on context match quality
- **FR-014**: System MUST accept `query`, `book_id`, `session_id`, and optional `selected_text` parameters in the API endpoint
- **FR-015**: System MUST properly handle validation errors (422) in the API
- **FR-016**: System MUST save chat history to Neon Postgres database including session_id, user_query, model_response, and confidence_level
- **FR-017**: System MUST reuse existing models in the project for database integration
- **FR-018**: Frontend MUST send selected text to the backend when user selects/highlights text
- **FR-019**: Frontend MUST display confidence badge in the chat UI showing the confidence level of each response
- **FR-020**: Frontend MUST show clear error messages to users when appropriate
- **FR-021**: System MUST retrieve relevant content chunks from Qdrant based on user query when no selected text is provided
- **FR-022**: System MUST bypass retrieval process when selected text is provided and use only that text as context
- **FR-023**: System MUST update system prompts to enforce answering only from provided context
- **FR-024**: System MUST clearly indicate when the context does not contain enough information to answer a question

### Key Entities

- **Book Content**: The primary source of information for the chatbot, stored as vector embeddings in Qdrant for retrieval purposes
- **User Query**: The question or input from the reader that triggers the RAG process
- **Selected Text**: Text highlighted/selected by the user which becomes the exclusive context for answering questions
- **Retrieved Context**: The specific passages from the book that are retrieved from Qdrant based on the user's query when no text is selected
- **Chat Response**: The generated answer from the chatbot based on the retrieved context or selected text
- **Confidence Level**: A measure (High/Medium/Low) of how well the retrieved context matches the user's query
- **Chat Session**: A collection of interactions between a user and the chatbot, identified by a session_id
- **Chat History**: Persistent record of user queries and model responses stored in Neon Postgres
- **API Endpoint**: The `/chat` endpoint that accepts query, book_id, session_id, and optional selected_text parameters

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 90% of user questions about book content receive accurate answers directly from the book within 3 seconds
- **SC-002**: 95% of questions not covered in the book content result in appropriate "not enough information" responses rather than hallucinated answers
- **SC-003**: Users report 80% satisfaction with the accuracy and helpfulness of the chatbot's responses in post-interaction surveys
- **SC-004**: Less than 5% of user interactions result in responses that contain information not found in the book
- **SC-005**: The system maintains contextual awareness in conversations for at least 5 turns without losing relevance to the book content
- **SC-006**: 90% of selected text queries receive responses based only on the selected text without searching the broader book content
- **SC-007**: 85% of responses include appropriate confidence levels that accurately reflect the relevance of the retrieved context
- **SC-008**: 95% of chat sessions have their history properly saved to the Neon Postgres database
- **SC-009**: The system properly handles 98% of validation errors without crashing or returning inappropriate responses
- **SC-010**: Frontend displays confidence badges and error messages in 100% of relevant scenarios
- **SC-011**: 90% of retrieval requests from Qdrant return relevant context within 1.5 seconds
- **SC-012**: 95% of API requests properly accept and process the query, book_id, session_id, and optional selected_text parameters
