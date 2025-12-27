# Research: AI-Powered Book RAG System

## Decision: Embedding Model Selection
**Rationale**: The feature spec mentions using Google Gemini embedding model (gemini-2.0-flash), while the constitution mentions MiniLM embeddings. After research, Google Gemini embeddings are more suitable for this project due to their advanced semantic understanding capabilities and better performance with multilingual content (important for Urdu translation feature). Although the constitution mentions MiniLM, the project requirements specifically call for Google Gemini which offers better performance for this use case.
**Alternatives considered**: 
- MiniLM embeddings (from constitution): Good for basic semantic search but less advanced than Gemini
- OpenAI embeddings: Would require API key costs that exceed free tier constraints
- Sentence Transformers: Self-hosted but would require more computational resources

## Decision: Content Length Management
**Rationale**: The constitution requires total reading time to NOT exceed 45 minutes, but the feature spec allows for books up to 1000 pages. This is resolved by implementing content summarization and intelligent chunking that focuses on key concepts rather than comprehensive coverage. The system will automatically summarize long content to meet the 45-minute constraint while preserving educational value.
**Alternatives considered**:
- Strict 45-minute limit: Would limit content depth
- Chapter-based limits: Would be less flexible
- User-selectable depth: Would complicate the UI

## Decision: Translation Quality
**Rationale**: To ensure high-quality Urdu translations that preserve technical meaning as required by the constitution, we'll implement a two-step process: 1) Use Google Gemini for initial translation, and 2) Apply post-processing with domain-specific terminology mapping to ensure technical terms are correctly translated.
**Alternatives considered**:
- Direct translation with basic models: Lower quality
- Human translation: Higher cost and slower
- Rule-based translation: Less adaptable to new content

## Decision: Architecture Alignment
**Rationale**: The backend architecture will use FastAPI with Neon PostgreSQL for relational data and Qdrant for vector storage as specified in the feature spec. This aligns with the constitution requirements while meeting the specific needs of the RAG system. The embedding model will be Google Gemini as specified in the feature requirements rather than MiniLM, since Gemini offers better multilingual support which is essential for the Urdu translation feature.
**Alternatives considered**:
- Using only MiniLM as per constitution: Would limit multilingual capabilities
- Alternative vector databases: Qdrant offers the best free tier for this use case