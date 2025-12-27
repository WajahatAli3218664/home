<!--

Sync Impact Report:
Version change: 1.0.0 -> 1.1.0
Modified principles: Mission, Frontend Minimalism & Speed, Core Constraints, Architecture Principles, RAG Rules, Personalization, Localization, Deployment requirements
Added sections: CONTENT STRUCTURE, BACKEND ARCHITECTURE, RAG CHATBOT RULES, PERSONALIZATION, LOCALIZATION, DEPLOYMENT
Removed sections: Core Deliverables, Success Criteria, Non-Goals, User Stories, Risk & Mitigation
Templates requiring updates:
- .specify/templates/plan-template.md: ⚠ pending
- .specify/templates/spec-template.md: ⚠ pending
- .specify/templates/tasks-template.md: ⚠ pending
- .specify/templates/commands/*.md: ⚠ pending
Follow-up TODOs: None

-->
# Physical AI & Humanoid Robotics Book with Integrated RAG Chatbot Constitution

## Mission

Create a fast, simple, beautiful educational platform that teaches Physical AI, robotics fundamentals, and humanoid systems using an AI-powered, interactive textbook.

## Core Principles

### I. Frontend Minimalism & Speed
The frontend MUST be extremely minimal, mobile-first, and readable on low-end phones. No unnecessary animations, libraries, or visual noise are allowed. Large readable typography with maximum 2 font weights, card-based layout only, light shadows, no heavy gradients. Pages MUST load fast on 3G connections.

### II. Content Constraints
All content MUST be beginner-friendly but technically correct. Total reading time of all chapters combined MUST NOT exceed 45 minutes. This ensures focused, efficient learning without overwhelming users with excessive information.

### III. Backend Architecture
The backend MUST be modular, utilizing FastAPI with clearly defined services and routes. Data MUST be stored cleanly in Neon for relational data and Qdrant for vector storage. MiniLM embeddings MUST be used for RAG implementation.

### IV. RAG Implementation Requirements
The RAG chatbot MUST only answer using textbook content with no hallucinations. All answers MUST be grounded and factual with proper chunking and citation logic. This ensures educational accuracy and reliability.

## Content Structure

- Total chapters: 12
- Each chapter MUST include:
  - Short introduction
  - Core concept explanation
  - One visual/diagram placeholder
  - 3-bullet summary
  - 3-question quiz

## Backend Architecture

- FastAPI with modular services and routes
- Neon for relational data
- Qdrant for vector storage
- MiniLM embeddings for RAG

## RAG Chatbot Rules

- MUST only answer using textbook content
- No hallucinations
- All answers MUST be grounded and factual
- Use chunking + citation logic

## Personalization

- Implement user authentication using Better-Auth
- Adapt content depth based on user background

## Localization

- Provide one-click Urdu translation
- Translation MUST preserve technical meaning

## Deployment

- Must run on free tiers
- Support Vercel, Railway, Neon, Qdrant

## Governance

This Constitution supersedes all other practices. Amendments require documentation, approval, and a migration plan. All Pull Requests and code reviews MUST verify compliance with these principles. Any increase in complexity MUST be justified. The `QWEN.md` file serves as runtime development guidance.

**Version**: 1.1.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-13