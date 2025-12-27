# Data Model: Floating Chatbot with Authentication

## User Session Entity
- **sessionId**: string (unique identifier)
- **userId**: string (user identifier from Better Auth)
- **authToken**: string (JWT token)
- **expiresAt**: datetime (token expiration time)
- **authenticated**: boolean (current authentication status)

**Validation Rules**:
- sessionId must be unique
- authToken must be properly formatted JWT
- expiresAt must be in the future
- authenticated must be boolean

## Chat Message Entity
- **messageId**: string (unique identifier)
- **content**: string (message text)
- **timestamp**: datetime (when message was created)
- **sender**: enum ['user', 'ai'] (who sent the message)
- **sessionId**: string (reference to user session)
- **citations**: array of objects (for AI responses)

**Citation Structure**:
- **title**: string (source title)
- **url**: string (source URL)
- **chapter**: string (textbook chapter reference)

**Validation Rules**:
- content must not be empty
- timestamp must be current or past
- sender must be either 'user' or 'ai'
- citations only valid for 'ai' sender

## Authentication Flow Entity
- **flowId**: string (unique identifier)
- **provider**: enum ['google', 'facebook', 'email'] (authentication provider)
- **state**: enum ['initial', 'pending', 'success', 'error'] (current state)
- **createdAt**: datetime (when flow was initiated)
- **completedAt**: datetime (when flow was completed)
- **userId**: string (resulting user identifier)

**Validation Rules**:
- flowId must be unique
- provider must be valid option
- state must be one of allowed values
- completedAt must be after createdAt if set

## State Transitions

### User Session
- Unauthenticated → Authenticating: User clicks chat button
- Authenticating → Authenticated: Successful authentication
- Authenticated → Expired: Token expires
- Expired → Unauthenticated: Token refresh fails
- Any state → Unauthenticated: User logs out

### Authentication Flow
- Initial → Pending: User starts authentication
- Pending → Success: Authentication successful
- Pending → Error: Authentication fails
- Success → Completed: Token stored
- Error → Initial: User retries