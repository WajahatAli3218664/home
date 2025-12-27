# Implementation Plan: Floating Chatbot with Authentication

**Branch**: `002-floating-chatbot-auth` | **Date**: 2025-12-15 | **Spec**: [link]
**Input**: Feature specification from `/specs/002-floating-chatbot-auth/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan implements a floating AI textbook assistant chatbot that appears on all pages of the Physical AI & Humanoid Robotics website. The feature includes a persistent round button at the bottom-left corner that triggers authentication via Better Auth before opening the chat interface. The implementation involves both frontend components (using Docusaurus theme override) and backend security updates (custom middleware to verify Better Auth tokens).

## Technical Context

**Language/Version**: TypeScript/JavaScript (frontend), Python 3.8+ (backend)
**Primary Dependencies**: Better Auth, Docusaurus, FastAPI, React, Qdrant Client
**Storage**: Qdrant for vector storage, Neon for relational data (user sessions)
**Testing**: Jest for frontend, pytest for backend
**Target Platform**: Web (desktop and mobile browsers)
**Project Type**: Web (frontend Docusaurus site + backend FastAPI server)
**Performance Goals**: Chat interface opens within 500ms, responses under 5 seconds in 95% of cases
**Constraints**: Must follow accessibility standards (WCAG 2.1 AA), responsive design
**Scale/Scope**: Support for thousands of concurrent users with authenticated sessions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gate 1: Frontend Minimalism & Speed
- [x] Floating button implementation follows minimal design principles
- [x] No unnecessary animations or visual noise added
- [x] Typography and layout follows constitution requirements
- [x] Pages maintain fast loading on 3G connections

### Gate 2: Content Constraints
- [x] Chatbot responses adhere to textbook content only (no hallucinations)
- [x] Answers are factually correct and grounded in textbook content

### Gate 3: Backend Architecture
- [x] FastAPI backend with modular services maintained
- [x] Qdrant continues to be used for vector storage
- [x] MiniLM embeddings maintained for RAG implementation

### Gate 4: RAG Implementation Requirements
- [x] Chatbot MUST only answer using textbook content
- [x] No hallucinations in responses
- [x] All answers MUST be grounded and factual with proper citations

### Gate 5: Authentication
- [x] Uses Better-Auth as required by constitution
- [x] Authentication system is secure and follows best practices

## Project Structure

```text
specs/002-floating-chatbot-auth/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
```text
backend/
├── src/
│   ├── api/
│   │   └── chat.py
│   ├── services/
│   │   └── chat_service.py
│   ├── middleware/
│   │   └── better_auth.py
│   ├── models/
│   └── schemas/
│       └── chat.py

frontend/
├── src/
│   ├── components/
│   │   ├── ChatbotButton.jsx
│   │   ├── ChatWindow.jsx
│   │   ├── AuthModal.jsx
│   │   ├── ChatMessage.tsx
│   │   └── ChatInput.tsx
│   ├── services/
│   │   ├── authClient.js
│   │   ├── authService.js
│   │   └── chatAPI.js
│   ├── contexts/
│   │   └── AuthContext.tsx
│   ├── styles/
│   │   ├── ChatWindow.css
│   │   └── ChatbotButton.css
│   └── theme/
│       └── Layout.tsx
└── static/
    └── backend-url.js
```

**Structure Decision**: This is a web application requiring both frontend (Docusaurus) and backend (FastAPI) modifications. The floating chatbot is implemented as a Docusaurus theme override with authentication using Better Auth, and backend security via custom middleware to verify Better Auth tokens.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
