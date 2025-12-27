# Common RAG Implementation Mistakes

Based on our analysis and research, here are the common mistakes that cause RAG systems to ignore retrieved context:

## 1. Context not included in prompt template
The retrieved context is retrieved but not included in the prompt sent to the LLM.

**Solution**: Ensure the retrieved context is explicitly added to the prompt template.

## 2. Prompt template formatting issues
The context and query are not properly formatted in the prompt, causing the LLM to ignore the context.

**Solution**: Use a clear, consistent format that clearly separates the context from the query.

## 3. Variable scoping issues
The retrieved context variable is out of scope when constructing the LLM call.

**Solution**: Ensure the context variable is properly passed through the function call chain.

## 4. Overwriting context
The context is retrieved but then overwritten by an empty value or default query.

**Solution**: Trace the context variable from retrieval to LLM call to ensure it's not being overwritten.

## 5. Incorrect API call parameters
The context is available but not passed as a parameter to the LLM API.

**Solution**: Verify that the context is being passed to the LLM service call.

## 6. Timing issues
The context is retrieved asynchronously but the LLM call happens before retrieval completes.

**Solution**: Ensure proper async/await handling or synchronous execution where needed.

## 7. Size limitations
The context is retrieved but exceeds token limits and gets truncated or skipped.

**Solution**: Implement context chunking and token counting to manage size.

## 8. Pathway not executed
The RAG pathway is not being executed at all, and the system defaults to a simple chat pathway.

**Solution**: Verify that the RAG service is being called instead of a simple chat service.