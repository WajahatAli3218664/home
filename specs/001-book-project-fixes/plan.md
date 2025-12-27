# Implementation Plan: Book Project Critical Fixes

**Branch**: `001-book-project-fixes` | **Date**: 2025-12-18 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-book-project-fixes/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Addresses critical issues in the book project: authentication (Better-Auth), RAG chatbot (FastAPI + Qdrant), Urdu translation (Claude API), and content personalization. Implementation uses Docusaurus frontend with FastAPI backend, Neon Postgres for relational data, and Qdrant Cloud for vector storage. Follows constitution principles for frontend minimalism, RAG accuracy, and free-tier deployment.

## Technical Context

**Language/Version**: TypeScript/JavaScript (Frontend), Python 3.11 (Backend with FastAPI)
**Primary Dependencies**: Docusaurus (Frontend), FastAPI (Backend), Better-Auth (Authentication), OpenAI/ChatKit SDK (AI), Qdrant Cloud (Vector storage), Neon Postgres (Database), Claude (Translation)
**Storage**: Neon Postgres (relational data), Qdrant Cloud (vector embeddings for RAG)
**Testing**: Jest/Vitest (Frontend), pytest (Backend)
**Target Platform**: Web application (Docusaurus frontend + FastAPI backend)
**Project Type**: Web application (frontend/backend split)
**Performance Goals**: Pages must load within 3 seconds on 3G, chat responses under 5 seconds, RAG accuracy >90%
**Constraints**: Must run on free tiers (Neon, Qdrant Cloud, Vercel), mobile-first responsive design, offline-capable content where possible
**Scale/Scope**: Support thousands of users, handle book content with RAG functionality, translation between English and Urdu

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance with Constitution Principles:
- ✅ Frontend Minimalism & Speed: Docusaurus supports minimal, fast frontend that meets mobile-first requirements
- ✅ Content Constraints: Existing book content will be maintained within 45-minute reading time requirement
- ✅ Backend Architecture: Using FastAPI with Neon for relational data and Qdrant for vector storage as required
- ✅ RAG Implementation: Chatbot will use textbook content with proper chunking and citation logic to prevent hallucinations
- ✅ Personalization: Implementation includes user authentication via Better-Auth and content adaptation based on user background
- ✅ Localization: One-click Urdu translation will be implemented with preservation of technical meaning
- ✅ Deployment: Solution designed for free tiers (Vercel, Neon, Qdrant)

### Gates to Pass:
- GATE 1: Architecture must use FastAPI, Neon, and Qdrant as specified in constitution
- GATE 2: RAG implementation must prevent hallucinations and use proper citation logic
- GATE 3: Frontend must be mobile-optimized and load quickly on 3G connections

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Option 2: Web application (frontend + backend)
backend/
├── src/
│   ├── models/
│   ├── services/
│   │   ├── auth/
│   │   ├── chat/
│   │   ├── translation/
│   │   └── personalization/
│   ├── api/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   └── translation.py
│   └── config/
│       └── settings.py
└── tests/

frontend/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   ├── Chapter/
│   │   ├── Chat/
│   │   └── UI/
│   ├── pages/
│   │   ├── signup.jsx
│   │   └── signin.jsx
│   ├── services/
│   │   ├── authClient.js
│   │   ├── api.js
│   │   └── chatAPI.js
│   ├── contexts/
│   │   └── AuthContext.jsx
│   ├── theme/
│   └── utils/
├── static/
└── docusaurus.config.ts

# Existing project directories
docs/                    # Book content and chapters
.history/               # Prompt history records
.specify/               # Specification toolkit
```

**Structure Decision**: Web application structure with a clear separation between backend (FastAPI) and frontend (Docusaurus). This allows for proper implementation of authentication, RAG chatbot, translation, and personalization features. The structure aligns with the project's requirements for Better-Auth, AI integration, and database storage using Neon and Qdrant.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
