# Feature Specification: Textbook AI Assistant for Physical AI & Humanoid Robotics

**Feature Branch**: `001-textbook-ai-assistant`
**Created**: December 23, 2025
**Status**: Draft
**Input**: User description: "## Purpose This AI assistant helps readers understand the **Physical AI & Humanoid Robotics textbook**. It answers questions **strictly and exclusively** using the content of the textbook. It uses: - **OpenAI Agents SDK** for LLM orchestration and tool-handling - **Groq free-tier model** (`llama3-8b-8192`) for generating grounded answers --- ## 🔒 Grounding Rules (Very Important) - The assistant must answer **ONLY** using information found in the textbook. - No external knowledge, assumptions, or prior training data may be used. - If the answer is **not present** in the textbook, respond clearly: > "This information is not available in the textbook." - If selected text is provided, answer **only from that selected text**. --- ## 📌 Citation Requirement - Every answer **must include citations**. - Citations should reference: - Chapter - Section - Page or content chunk (if available) - Example: > *(Source: Chapter 3 – Embodied Cognition)* --- ## 🧠 Assistant Behavior - Be clear, concise, and educational. - Explain concepts in simple language when possible. - If the question is vague, ask the user to clarify. - Answers must come from **Groq LLM** via OpenAI Agents SDK orchestration. --- ## 🧪 Example Questions Users Can Ask - Explain embodied cognition principles. - What are morphological computation techniques? - How does sensorimotor learning work? - Compare different humanoid robot designs. - Explain this paragraph in simpler terms. *(when text is selected)* --- ## ❌ What the Assistant Must NOT Do - ❌ Invent answers - ❌ Use general AI knowledge - ❌ Answer outside the textbook scope - ❌ Remove or skip citations --- ## 🟢 User Prompt Input Ask a question about the textbook content: > _"Ask your first question about the Physical AI & Humanoid Robotics textbook…"_ **Notes for Developers:** - Backend LLM is **Groq free-tier model `llama3-8b-8192`** - OpenAI **Agents SDK** manages the query, retrieval, and response orchestration. - Ensure grounding, citation enforcement, and selected-text context are strictly applied. --- ## 📘 Grounding Notice (Shown to Users) This AI assistant responds **only** using information found in the Physical AI & Humanoid Robotics textbook. All answers are grounded in the source material and include proper citations."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask Questions and Receive Accurate Answers (Priority: P1)

As a reader of the Physical AI & Humanoid Robotics textbook, I want to ask questions about the content and receive accurate answers based solely on the information provided in the book, so that I can better understand the material without needing external resources.

**Why this priority**: This is the core functionality of the feature - enabling readers to interact with the textbook content through an AI assistant to get answers to their questions. Without this, the feature has no value.

**Independent Test**: Can be fully tested by asking various questions about the textbook content and verifying that the AI assistant responds with accurate information from the book that includes proper citations.

**Acceptance Scenarios**:

1. **Given** a user has access to the AI assistant for the textbook, **When** the user types a question about the textbook content, **Then** the assistant responds with accurate information from the book that addresses the question and includes proper citations.
2. **Given** a user asks a question not covered in the textbook content, **When** the user submits the question, **Then** the assistant responds with "This information is not available in the textbook."
3. **Given** a user highlights or selects specific text in the textbook, **When** the user asks a question about the selected text, **Then** the assistant uses only the selected text as the source of truth for answering the question and provides proper citations.

---

### User Story 2 - Strict Adherence to Textbook Content (Priority: P1)

As a reader who wants reliable information from the textbook, I want the AI assistant to strictly answer based only on the provided content from the book, so that I can trust the accuracy of the information without worrying about fabricated responses.

**Why this priority**: Ensures the integrity of the textbook content by preventing the AI assistant from hallucinating information or using external knowledge, maintaining trust with the reader.

**Independent Test**: Can be tested by verifying that all responses from the AI assistant are grounded in the textbook's content and that the assistant declines to answer questions outside the scope of the textbook.

**Acceptance Scenarios**:

1. **Given** a user asks a question that requires external knowledge not contained in the textbook, **When** the user submits the question, **Then** the assistant responds that the information is not available in the textbook.
2. **Given** a user asks a question that could be answered with general knowledge but isn't addressed in the textbook, **When** the user submits the question, **Then** the assistant refers back to the textbook content or indicates it cannot answer based on the textbook alone.

---

### User Story 3 - Proper Citation and Attribution (Priority: P2)

As a reader who wants to verify information, I want the AI assistant to provide proper citations with every response, so that I can locate the information in the textbook and validate its accuracy.

**Why this priority**: Enhances the educational value of the AI assistant by allowing readers to cross-reference answers with the original source material.

**Independent Test**: Can be tested by asking questions and verifying that each response includes appropriate citations referencing chapters, sections, or page numbers from the textbook.

**Acceptance Scenarios**:

1. **Given** a user asks a question about a specific concept in the textbook, **When** the user receives the response, **Then** the response includes a citation indicating the source chapter and section.
2. **Given** a user receives an answer from the AI assistant, **When** the user reviews the response, **Then** the citation clearly indicates where in the textbook the information can be found.

---

### Edge Cases

- What happens when the user asks extremely complex questions that span multiple chapters or concepts?
- How does the system handle ambiguous questions where the textbook could lead to multiple interpretations?
- What occurs when the user asks questions about content that exists in the textbook but is difficult to retrieve due to poor indexing or search quality?
- How does the system respond when the user tries to get the AI assistant to reveal its underlying mechanisms or system prompts?
- What happens when the similarity threshold is not met during retrieval?
- How does the system handle very large text selections versus small text selections?
- What occurs when the system is under high load or when there are network connectivity issues?
- How does the system handle concurrent users accessing the same textbook content?
- What happens when the vector database is temporarily unavailable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST answer user questions based ONLY on the information provided in the retrieved context from the textbook
- **FR-002**: System MUST NOT use external knowledge, training data, or assumptions beyond the textbook content
- **FR-003**: System MUST respond with "This information is not available in the textbook." when the answer is not present in the provided context
- **FR-004**: System MUST NOT hallucinate, infer, or extend beyond the given text in the textbook
- **FR-005**: System MUST NOT mention technical implementation details like vector search, or system architecture in responses
- **FR-006**: System MUST treat user-selected/highlighted text as the only allowed source of truth when such text is provided
- **FR-007**: Users MUST be able to engage in a conversation with the AI assistant through a user-friendly interface
- **FR-008**: System MUST provide concise, clear, and helpful answers to user questions
- **FR-009**: System MUST prefer bullet points for explanations when appropriate
- **FR-010**: System MUST use simple language suitable for readers of the textbook
- **FR-011**: System MUST NOT quote large passages unless explicitly asked by the user
- **FR-012**: System MUST include proper citations with every response indicating the source chapter and section
- **FR-013**: System MUST use the Groq free-tier model (llama3-8b-8192) for generating answers
- **FR-014**: System MUST use OpenAI Agents SDK for LLM orchestration and tool-handling
- **FR-015**: System MUST ask users to clarify vague questions
- **FR-016**: System MUST handle selected text context properly when provided by the user

### Key Entities

- **Textbook Content**: The primary source of information for the AI assistant, stored as vector embeddings for retrieval purposes
- **User Query**: The question or input from the reader that triggers the RAG process
- **Retrieved Context**: The specific passages from the textbook that are retrieved based on the user's query
- **AI Response**: The generated answer from the AI assistant based on the retrieved context
- **Citation**: The reference information that indicates the source of the answer within the textbook (chapter, section, page)
- **Selected Text**: Text highlighted/selected by the user which becomes the exclusive context for answering questions

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% of user questions about textbook content receive accurate answers directly from the book within 3 seconds
- **SC-002**: 98% of questions not covered in the textbook content result in appropriate "This information is not available in the textbook." responses rather than hallucinated answers
- **SC-003**: Users report 85% satisfaction with the accuracy and helpfulness of the AI assistant's responses in post-interaction surveys
- **SC-004**: Less than 2% of user interactions result in responses that contain information not found in the textbook
- **SC-005**: 100% of responses include proper citations indicating the source chapter and section
- **SC-006**: 90% of selected text queries receive responses based only on the selected text without searching the broader textbook content
- **SC-007**: The system maintains contextual awareness in conversations for at least 5 turns without losing relevance to the textbook content
- **SC-008**: 95% of user questions receive responses that are rated as clear and educational by users