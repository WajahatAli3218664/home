// services/api.ts

// Default backend URL - this can be overridden by setting window.__BACKEND_URL__
// in the HTML template or by using a build-time environment variable
const DEFAULT_BACKEND_URL = 'http://localhost:8000';

// Get the backend URL from a global variable if available, otherwise use the default
const BACKEND_URL =
  typeof window !== 'undefined' && (window as any).__BACKEND_URL__
    ? (window as any).__BACKEND_URL__
    : DEFAULT_BACKEND_URL;

// Generic HTTP client methods
const apiClient = {
  get: async (endpoint: string) => {
    try {
      const response = await fetch(`${BACKEND_URL}${endpoint}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return await response.json();
    } catch (error) {
      console.error('GET request failed:', error);
      throw error;
    }
  },

  post: async (endpoint: string, data?: any) => {
    try {
      const response = await fetch(`${BACKEND_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      return await response.json();
    } catch (error) {
      console.error('POST request failed:', error);
      throw error;
    }
  },

  put: async (endpoint: string, data?: any) => {
    try {
      const response = await fetch(`${BACKEND_URL}${endpoint}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      return await response.json();
    } catch (error) {
      console.error('PUT request failed:', error);
      throw error;
    }
  },

  delete: async (endpoint: string) => {
    try {
      const response = await fetch(`${BACKEND_URL}${endpoint}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      return await response.json();
    } catch (error) {
      console.error('DELETE request failed:', error);
      throw error;
    }
  }
};

// Specific API functions for text generation
const generateText = async (): Promise<string> => {
  try {
    const response = await fetch(`${BACKEND_URL}/generate-text`);
    const data = await response.json();
    return data.text;
  } catch (error) {
    console.error('Error generating text:', error);
    return "Error generating text. Please try again.";
  }
};

const generateMultipleTexts = async (count: number = 5): Promise<string[]> => {
  try {
    const response = await fetch(`${BACKEND_URL}/generate-text-multiple?count=${count}`);
    const data = await response.json();
    return data.texts;
  } catch (error) {
    console.error('Error generating multiple texts:', error);
    return ["Error generating text. Please try again."];
  }
};

// Export both the HTTP client and the specific functions
export default {
  ...apiClient,
  generateText,
  generateMultipleTexts
};