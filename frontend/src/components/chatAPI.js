import { authService } from '../services/authService';

// Function to get the base URL safely
const getBaseURL = () => {
  // Check if we're in a browser environment and the variable is set via client module
  if (typeof window !== 'undefined' && window.REACT_APP_API_BASE_URL) {
    return window.REACT_APP_API_BASE_URL;
  }
  // Check for environment variable in different possible locations
  if (typeof window !== 'undefined' && window.ENV?.REACT_APP_API_BASE_URL) {
    return window.ENV.REACT_APP_API_BASE_URL;
  }
  // Default fallback
  return 'http://localhost:8000';
};

export const chatAPI = {
  /**
   * Sends a message to the chat backend
   * @param {string} query - The user's query
   * @param {string} backendUrlOverride - Optional backend URL override
   * @returns {Promise<Object>} The response from the backend
   */
  sendMessage: async (query, backendUrlOverride = null) => {
    const backendUrl = backendUrlOverride || getBaseURL();

    // Validate query length
    if (!query || query.trim().length === 0) {
      throw new Error('Query cannot be empty');
    }

    if (query.length > 1000) {
      throw new Error('Query is too long. Please limit to 1000 characters.');
    }

    try {
      // Note: Using the correct backend endpoint for chat based on backend structure
      const response = await fetch(`${backendUrl}/api/v1/chat/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query.trim(),
        }),
        // Include credentials to send session cookies if needed
        credentials: 'include'
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || errorData.error || `HTTP error! Status: ${response.status}`;

        // Make sure error messages are in English for consistent UI display
        const isString = typeof errorMessage === 'string';
        const standardizedErrorMessage = !isString || !errorMessage.match(/[a-zA-Z]/) ?
          'An error occurred processing your request' :
          errorMessage;

        throw new Error(standardizedErrorMessage);
      }

      return await response.json();
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Network error - unable to connect to the chat service');
      }

      // Ensure any non-English error messages are handled correctly
      const isErrorMessageString = typeof error.message === 'string';
      const message = error.message && isErrorMessageString && !error.message.match(/[a-zA-Z]/) ?
        'An error occurred connecting to the chat service' :
        error.message || 'An error occurred connecting to the chat service';

      throw new Error(message);
    }
  },

  /**
   * Gets the history of a conversation
   * @param {string} userId - The user ID (UUID format)
   * @param {string} backendUrlOverride - Optional backend URL override
   * @returns {Promise<Object>} The conversation history
   */
  getConversationHistory: async (userId, backendUrlOverride = null) => {
    const backendUrl = backendUrlOverride || getBaseURL();

    if (!userId) {
      throw new Error('User ID is required to get conversation history');
    }

    try {
      const response = await fetch(`${backendUrl}/api/v1/chat/history/${userId}`, {
        method: 'GET',
        // Include credentials to send session cookies if needed
        credentials: 'include'
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || errorData.error || `HTTP error! Status: ${response.status}`;
        throw new Error(errorMessage);
      }

      return await response.json();
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Network error - unable to connect to the chat service');
      }
      throw error;
    }
  }
};