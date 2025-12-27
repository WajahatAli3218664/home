# Data Model: Book Project Critical Fixes

## User Entity

**Description**: Represents a registered user with profile information and authentication credentials

**Fields**:
- `id` (string): Unique identifier for the user
- `email` (string): User's email address
- `username` (string): User's chosen username
- `password_hash` (string): Hashed password for authentication
- `programming_level` (string): User's programming experience level (beginner, intermediate, expert)
- `software_experience` (string): Years of software experience
- `hardware_background` (string): Hardware knowledge level
- `created_at` (datetime): When the account was created
- `updated_at` (datetime): When the account was last updated
- `is_active` (boolean): Whether the account is active

**Validation Rules**:
- Email must be valid format
- Username must be unique
- Password must meet security requirements

## BookContent Entity

**Description**: Represents the book chapters and text that can be translated and personalized

**Fields**:
- `id` (string): Unique identifier for the content
- `title` (string): Title of the chapter/section
- `content` (string): The actual book content in English
- `chapter_number` (integer): Sequential number of the chapter
- `created_at` (datetime): When the content was created
- `updated_at` (datetime): When the content was last updated
- `status` (enum): Content status (draft, published, archived)

**Validation Rules**:
- Title and content must not be empty
- Chapter number must be unique within the book

## Translation Entity

**Description**: Represents the translated versions of book content in different languages

**Fields**:
- `id` (string): Unique identifier for the translation
- `content_id` (string): Reference to the original BookContent
- `language` (string): The target language (e.g., "ur")
- `translated_content` (string): The content translated to the target language
- `created_at` (datetime): When the translation was created
- `updated_at` (datetime): When the translation was last updated
- `status` (enum): Translation status (pending, completed, failed)

**Validation Rules**:
- Language must be a valid language code
- Reference to content_id must be valid
- Translated_content must not be empty when status is completed

## ChatSession Entity

**Description**: Represents a conversation between the user and the AI chatbot with context from book content

**Fields**:
- `id` (string): Unique identifier for the chat session
- `user_id` (string): Reference to the user who started the session
- `created_at` (datetime): When the session was created
- `updated_at` (datetime): When the session was last updated
- `title` (string): Brief title for the chat session

**Validation Rules**:
- user_id must reference a valid user
- created_at must be in the past

## QuestionContext Entity

**Description**: Represents selected text or sections of book content that user wants the chatbot to focus on when answering

**Fields**:
- `id` (string): Unique identifier for the question context
- `session_id` (string): Reference to the chat session
- `book_content_id` (string): Reference to the relevant book content
- `selected_text` (string): The specific text the question refers to
- `created_at` (datetime): When the context was created
- `user_query` (string): The user's question about the selected text

**Validation Rules**:
- session_id must reference a valid chat session
- book_content_id must reference valid content
- selected_text and user_query must not be empty

## Relationships

- **User** (1) to **ChatSession** (many): A user can have multiple chat sessions
- **BookContent** (1) to **Translation** (many): A book content can have multiple translations
- **ChatSession** (1) to **QuestionContext** (many): A chat session can have multiple question contexts
- **BookContent** (1) to **QuestionContext** (many): A book content can be referenced in multiple question contexts

## State Transitions

### Translation Status
- `pending` → `completed`: Translation process finished successfully
- `pending` → `failed`: Translation process encountered an error
- `failed` → `pending`: Retry translation attempt

### User Authentication
- `logged_out` → `logging_in`: User initiates login process
- `logging_in` → `authenticated`: Login credentials validated
- `logging_in` → `login_failed`: Login credentials invalid
- `authenticated` → `logged_out`: User logs out