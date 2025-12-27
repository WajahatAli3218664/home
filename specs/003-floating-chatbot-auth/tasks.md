# Implementation Tasks: Floating Chatbot with Better Auth

**Feature**: Persistent Floating RAG Chatbot with Better Auth
**Branch**: 003-floating-chatbot-auth
**Date**: 2025-12-15
**Input**: spec.md, plan.md, data-model.md, contracts/chat-api.md

## Phase 1: Setup Tasks

### Goal
Initialize project structure and install required dependencies

### Tasks
- [X] T001 Set up feature branch and development environment
- [X] T002 Install Better Auth dependencies in frontend
- [X] T003 Install additional UI dependencies (if needed)
- [X] T004 Configure environment for new components
- [X] T005 Verify backend API endpoints are accessible

## Phase 2: Foundational Tasks

### Goal
Implement foundational components required by all user stories

### Tasks
- [X] T006 [P] Create AuthContext for global authentication state
- [X] T007 [P] Implement Better Auth client service
- [X] T008 [P] Create auth service layer with authentication functions
- [X] T009 [P] Set up chat API service for backend communication
- [X] T010 [P] Implement Better Auth middleware for backend
- [X] T011 [P] Create global CSS variables for color palette
- [X] T012 Update Layout theme to include floating chatbot

## Phase 3: User Story 1 - Floating chatbot button implementation

### Goal
Implement a floating chatbot button that is always visible at the bottom-left of the screen and opens an authentication modal when clicked for unauthenticated users.

### User Story
**Scenario 1**: User accesses chatbot from any page
- **Given**: User is on any page of the Physical AI & Humanoid Robotics textbook website
- **When**: User clicks the floating chatbot button at the bottom-left
- **Then**: If unauthenticated, authentication modal appears; if authenticated, chat interface opens

### Independent Test Criteria
- Chatbot button is visible on all pages at bottom-left
- Button click triggers auth check
- Unauthenticated users see auth modal
- Authenticated users see chat interface

### Tasks
- [X] T013 [US1] Create ChatbotButton component with persistent positioning
- [X] T014 [US1] Implement button styles with requested color palette (#AA60C8, #D69ADE, #EABDE6, #FFDFEF)
- [X] T015 [US1] Add hover animations and interaction effects to button
- [X] T016 [US1] Create slide-up panel functionality for chat interface
- [X] T017 [US1] Integrate authentication check in button click handler

## Phase 4: User Story 2 - Authentication flow implementation

### Goal
Implement Better Auth integration with email and social login options that prevents unauthenticated access to the chat functionality.

### User Story
**Scenario 2**: User authenticates to access chat
- **Given**: User has clicked the chatbot button but is not authenticated
- **When**: Authentication modal appears
- **Then**: User can sign in via email or social provider and gain access to chat

### Independent Test Criteria
- Authentication modal appears when unauthenticated user clicks button
- Email and social login options work correctly
- Authentication tokens are properly handled
- Authenticated users can access chat functionality

### Tasks
- [X] T018 [US2] Create AuthModal component with Better Auth integration
- [X] T019 [US2] Implement email authentication flow
- [X] T020 [US2] Implement social authentication options (Google, etc.)
- [X] T021 [US2] Add proper error handling and user feedback to auth flow
- [X] T022 [US2] Securely store and handle auth tokens
- [X] T023 [US2] Implement session validation and persistence

## Phase 5: User Story 3 - Chat interface with RAG integration

### Goal
Create a chat interface that connects to the RAG backend, displays responses with citations, and follows the modern UI design.

### User Story
**Scenario 3**: Authenticated user chats with AI assistant
- **Given**: User is authenticated and has opened the chat interface
- **When**: User types a query and submits it
- **Then**: Query is sent to RAG backend, response is received with citations, and displayed to user

### Independent Test Criteria
- Authenticated users can type and submit queries
- Queries are sent to RAG backend with proper authentication
- Responses are received with source citations
- Chat interface follows modern UI design with requested color palette

### Tasks
- [X] T024 [US3] Create ChatWindow component with message display
- [X] T025 [US3] Implement chat message components with citation display
- [X] T026 [US3] Add chat input with proper styling and functionality
- [X] T027 [US3] Connect frontend to RAG backend API with auth tokens
- [X] T028 [US3] Implement loading states and error handling
- [X] T029 [US3] Apply modern UI design with requested color palette and animations
- [X] T030 [US3] Add accessibility features (keyboard nav, ARIA labels)

## Phase 6: User Story 4 - UI/UX enhancements with animations

### Goal
Apply the requested color palette consistently across all components and implement smooth hover and interaction animations.

### User Story
**Scenario 4**: User interacts with chat interface
- **Given**: User is using the chat interface
- **When**: User hovers over buttons, types messages, or navigates
- **Then**: Smooth animations and transitions provide feedback with the specified color scheme

### Independent Test Criteria
- All UI elements use the specified color palette consistently
- Hover effects provide smooth visual feedback
- Animations are smooth and professional
- Interface respects prefers-reduced-motion setting

### Tasks
- [X] T031 [US4] Apply color palette globally (Primary: #AA60C8, Secondary: #D69ADE, etc.)
- [X] T032 [US4] Add smooth transitions to buttons and interactive elements
- [X] T033 [US4] Implement hover animations (scale, shadow, transform effects)
- [X] T034 [US4] Add loading animations using the primary color
- [X] T035 [US4] Ensure animations respect user motion preferences
- [X] T036 [US4] Optimize CSS for performance with minimal repaints

## Phase 7: Polish & Cross-Cutting Concerns

### Goal
Implement final touches, accessibility improvements, and cross-browser compatibility

### Tasks
- [X] T037 Add comprehensive accessibility attributes (ARIA) to all components
- [X] T038 Implement keyboard navigation support for all interactive elements
- [X] T039 Ensure responsive design works across all device sizes
- [X] T040 Add error boundaries and proper error handling
- [X] T041 Optimize component performance and minimize re-renders
- [X] T042 Test functionality on localhost and GitHub Pages deployment
- [X] T043 Document component APIs and integration points
- [X] T044 Perform final QA and bug fixes

## Dependencies

### User Story Completion Order
1. Foundational components (Phase 1-2) must be completed before any user story
2. User Story 1 (Floating button) can be developed in parallel with User Story 2 (Auth flow)
3. User Story 3 (Chat interface) depends on completion of User Story 2
4. User Story 4 (UI/UX) can be implemented in parallel with other stories but requires all components to be available

### Component Dependencies
- ChatbotButton.jsx requires AuthContext and auth service
- AuthModal.jsx requires auth service and Better Auth client
- ChatWindow.jsx requires chat API service and auth token
- Backend middleware must be in place before frontend can authenticate requests

## Parallel Execution Examples

### Per User Story
- **User Story 1**: Button creation (T013) and styling (T014) can run in parallel
- **User Story 2**: Email auth (T019) and social auth (T020) implementations can run in parallel
- **User Story 3**: Message display (T025) and input components (T026) can be developed in parallel
- **User Story 4**: Color implementation (T031) and animation implementation (T032) can run in parallel

## Implementation Strategy

### MVP First
Implement the minimum functionality: Basic floating button that appears on all pages and opens an authentication modal when clicked. This provides immediate value while establishing the foundational components.

### Incremental Delivery
1. Complete Phase 1-2 (foundational components)
2. Complete User Story 1 (floating button implementation)
3. Complete User Story 2 (authentication flow)
4. Complete User Story 3 (chat functionality with RAG)
5. Complete User Story 4 (UI/UX enhancements)
6. Complete Phase 7 (polish and integration)

### Risk Mitigation
- Prioritize authentication security and token handling
- Validate API endpoint contracts before full integration
- Test accessibility requirements early in development
- Implement proper error handling from the beginning