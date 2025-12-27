# Implementation Plan: Physical AI & Humanoid Robotics – Capstone Quarter

**Branch**: `001-physical-ai-textbook` | **Date**: 2025-12-13 | **Spec**: [link to spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-physical-ai-textbook/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Develop a Docusaurus-based interactive textbook for Physical AI and humanoid robotics with an embedded RAG chatbot. The system will include 12 short chapters (≤45 min total), curriculum modules for ROS 2, simulation, NVIDIA Isaac, and Vision-Language-Action systems, mobile-first UI, user personalization, and Urdu translation capabilities.

## Technical Context

**Language/Version**: TypeScript/JavaScript (for Docusaurus), Python 3.11 (for FastAPI backend)
**Primary Dependencies**: Docusaurus (frontend), FastAPI (backend), Neon Postgres, Qdrant (vector DB), Better-Auth (authentication), MiniLM (embeddings), OpenAI/ChatKit (RAG)
**Storage**: Neon (relational data), Qdrant (vector storage for RAG)
**Testing**: Jest (frontend), pytest (backend)
**Target Platform**: Web application (GitHub Pages frontend, cloud backend)
**Project Type**: Web (frontend + backend architecture)
**Performance Goals**: Page load time < 3 seconds on 3G, 95% accurate RAG responses with proper citations
**Constraints**: Free-tier infrastructure (Neon, Qdrant), mobile-first design, ≤45 min total reading time, no hallucinations in RAG responses
**Scale/Scope**: Educational platform for Physical AI students, 12 chapters with quizzes, multi-language support

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Assessment:
- ✅ **Frontend Minimalism & Speed**: Docusaurus with mobile-first approach, minimal UI, 3G optimization
- ✅ **Content Constraints**: 12 chapters ≤ 45 min total reading time, technically correct content
- ✅ **Backend Architecture**: FastAPI with modular services, Neon for relational data, Qdrant for vectors
- ✅ **RAG Implementation**: Chatbot answers only from book content, no hallucinations, chunking + citation
- ✅ **Personalization**: Better-Auth for user authentication, content adaptation by background
- ✅ **Localization**: One-click Urdu translation preserving technical meaning
- ✅ **Deployment**: Free-tier infrastructure (Neon, Qdrant) as required

## Project Structure

### Documentation (this feature)

```text
specs/001-physical-ai-textbook/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application (frontend + backend)
frontend/
├── src/
│   ├── pages/
│   │   ├── index.tsx
│   │   ├── modules.tsx
│   │   └── get-started.tsx
│   ├── components/
│   │   ├── Chapter/
│   │   ├── RAGChat/
│   │   └── Curriculum/
│   ├── services/
│   │   ├── chapterService.ts
│   │   └── ragService.ts
│   └── css/
│       └── custom.css
│
backend/
├── src/
│   ├── models/
│   │   ├── chapter.py
│   │   ├── user.py
│   │   └── chat_query.py
│   ├── services/
│   │   ├── rag_service.py
│   │   ├── translation_service.py
│   │   └── personalization_service.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── chapters/
│   │   │   ├── chat/
│   │   │   ├── auth/
│   │   │   └── translation/
│   │   └── main.py
│   └── utils/
│
tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Web application with Docusaurus frontend and FastAPI backend, following the specified architecture from the constitution (FastAPI, Neon, Qdrant, MiniLM embeddings). The frontend handles the interactive textbook experience while the backend manages RAG, authentication, and personalization services.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |