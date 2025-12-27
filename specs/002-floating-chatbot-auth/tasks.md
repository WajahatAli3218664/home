# Implementation Tasks: Floating Chatbot with Authentication

**Feature**: Floating Chatbot with Authentication
**Branch**: 002-floating-chatbot-auth
**Date**: 2025-12-15
**Input**: spec.md, plan.md, data-model.md, contracts/chat-api.md

## Phase 1: Setup

### Goal
Initialize project structure and install required dependencies

### Tasks
- [X] T001 Set up project directories per plan
- [X] T002 Install Better Auth dependencies in frontend
- [X] T003 Install Docusaurus and related dependencies
- [X] T004 Install backend dependencies (FastAPI, etc.)
- [X] T005 Configure environment variables for development

## Phase 2: Foundational

### Goal
Implement foundational components required by all user stories

### Tasks
- [X] T006 [P] Create ChatbotButton.jsx component with basic styling
- [X] T007 [P] Create AuthContext.tsx for global authentication state
- [X] T008 [P] Create authClient.js for Better Auth integration
- [X] T009 [P] Create authService.js to manage Better Auth operations
- [X] T010 [P] Create chatAPI.js service for backend communication
- [X] T011 [P] Create Better Auth middleware for backend token verification
- [X] T012 Update Docusaurus theme Layout.tsx to include ChatbotButton
- [X] T013 Create ChatWindow.css styles
- [X] T014 Create ChatbotButton.css styles

## Phase 3: User Story 1 - First-time user accessing chatbot

### Goal
Enable first-time user to click the floating chatbot button, see authentication modal, authenticate, and access chat interface

### User Story
**Scenario 1**: First-time user accessing chatbot
- **Given**: User is on any page of the Physical AI & Humanoid Robotics website
- **When**: User clicks the floating chatbot button
- **Then**: Authentication modal appears prompting for credentials
- **And**: After successful authentication, chat interface opens

### Independent Test Criteria
- User can click the floating chatbot button
- Authentication modal appears when user is not authenticated
- User can authenticate using Better Auth
- Chat interface opens after successful authentication

### Tasks
- [X] T015 [US1] Create AuthModal.jsx component with Better Auth integration
- [X] T016 [US1] Implement authentication check in ChatbotButton.jsx
- [X] T017 [US1] Add authentication flow to authService.js
- [X] T018 [US1] Connect ChatbotButton click handler to authentication state
- [X] T019 [US1] Implement modal display logic in ChatbotButton.jsx

## Phase 4: User Story 2 - Returning authenticated user

### Goal
Enable returning authenticated users to access chat interface immediately without re-authentication

### User Story
**Scenario 2**: Returning authenticated user
- **Given**: User is already authenticated with valid session
- **When**: User clicks the floating chatbot button
- **Then**: Chat interface opens immediately without re-authentication

### Independent Test Criteria
- Authenticated user clicks chatbot button
- Chat interface opens immediately without showing auth modal
- Session state is properly checked

### Tasks
- [X] T020 [US2] Implement session validation in authService.js
- [X] T021 [US2] Add authentication state persistence to AuthContext
- [X] T022 [US2] Update ChatbotButton.jsx to check authentication status
- [X] T023 [US2] Connect chat interface opening logic to authentication state

## Phase 5: User Story 3 - User chatting with AI assistant

### Goal
Enable authenticated users to send queries to the RAG backend and receive responses with citations

### User Story
**Scenario 3**: User chatting with AI assistant
- **Given**: User has opened the chat interface after authentication
- **When**: User types a query and clicks send
- **Then**: Query is sent to RAG backend with proper authentication
- **And**: Response appears with citations when available

### Independent Test Criteria
- User can type a query in the chat interface
- Query is sent to backend with authentication token
- Response with citations appears in chat window
- Loading indicators show during processing

### Tasks
- [X] T024 [US3] Create ChatWindow.jsx component with message display
- [X] T025 [US3] Create ChatInput.tsx component with text input
- [X] T026 [US3] Create ChatMessage.tsx component for displaying messages
- [X] T027 [US3] Implement message sending functionality in chatAPI.js
- [X] T028 [US3] Add loading state management to ChatWindow.jsx
- [X] T029 [US3] Implement citation display in ChatMessage.tsx
- [X] T030 [US3] Connect ChatWindow to chatAPI.js for message sending

## Phase 6: User Story 4 - Network error handling

### Goal
Handle network errors gracefully during chat interactions

### User Story
**Scenario 4**: Network error during chat
- **Given**: User is chatting with the AI assistant
- **When**: Network request fails or backend is unreachable
- **Then**: User-friendly error message is displayed
- **And**: User can attempt to retry the request

### Independent Test Criteria
- Network error occurs during chat
- Error message is displayed to user
- User can retry the request
- No crashes or unhandled exceptions

### Tasks
- [X] T031 [US4] Add error handling to chatAPI.js
- [X] T032 [US4] Implement error display in ChatWindow.jsx
- [X] T033 [US4] Add retry functionality to ChatWindow.jsx
- [X] T034 [US4] Update chatAPI to handle connection failures

## Phase 7: Polish & Cross-Cutting Concerns

### Goal
Implement accessibility, performance, and design refinements

### Tasks
- [X] T035 Add accessibility attributes (ARIA) to all chat components
- [X] T036 Implement keyboard navigation for chat interface
- [ ] T037 Add responsive design to chat components for mobile
- [ ] T038 Optimize CSS for minimal loading impact
- [X] T039 Add animations for opening/closing chat window
- [X] T040 Implement smooth scrolling in chat window
- [X] T041 Add hover effects for user experience
- [X] T042 Ensure WCAG 2.1 AA compliance
- [X] T043 Implement proper loading states for authentication flow

## Dependencies

### User Story Completion Order
1. User Story 1 (Authentication flow) must be completed before User Story 2
2. User Story 2 (Authenticated access) depends on User Story 1
3. User Story 3 (Chat functionality) can start after User Story 1 is complete
4. User Story 4 (Error handling) can be implemented in parallel with User Story 3

### Component Dependencies
- ChatbotButton.jsx requires AuthContext.tsx and authService.js
- AuthModal.jsx requires authService.js and Better Auth dependencies
- ChatWindow.jsx requires chatAPI.js and ChatMessage.tsx
- Backend middleware must be in place before frontend can send authenticated requests

## Parallel Execution Examples

### Per User Story
- **User Story 1**: AuthModal.jsx creation can run in parallel with authService.js authentication flow implementation
- **User Story 2**: Session validation (T020) and state persistence (T021) can run in parallel
- **User Story 3**: UI components (ChatInput.tsx, ChatMessage.tsx) can be developed in parallel with chatAPI.js updates
- **User Story 4**: Error handling in chatAPI.js (T031) can run in parallel with error display in ChatWindow.jsx (T032)

## Implementation Strategy

### MVP First
Implement the minimum functionality for User Story 1: Basic floating button that opens authentication modal when clicked. This provides immediate value while establishing the foundational components.

### Incremental Delivery
1. Complete Phase 1 & 2 (foundational components)
2. Complete User Story 1 (authentication flow)
3. Complete User Story 2 (authenticated access)
4. Complete User Story 3 (chat functionality)
5. Complete User Story 4 (error handling)
6. Complete Phase 7 (polish)

### Risk Mitigation
- Prioritize authentication security and token handling
- Test cross-browser compatibility early
- Validate API endpoint contracts before full implementation
- Ensure accessibility requirements are met from the start