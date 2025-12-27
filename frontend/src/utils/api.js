// frontend/src/utils/api.js
// API client utilities for the textbook platform

import { authService } from '../services/authService';

const API_BASE_URL = (typeof process !== 'undefined' ? process.env.REACT_APP_API_BASE_URL : null) || 'http://localhost:8000';

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Generic request method
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add authorization header if token exists
    const token = await this.getToken();
    if (token && !config.headers.Authorization) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);

      // Handle different response statuses
      if (!response.ok) {
        // If it's an authentication error, clear the token
        if (response.status === 401 || response.status === 403) {
          // Clear the invalid token
          localStorage.removeItem('jwt_token');
          localStorage.removeItem('access_token');
        }

        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API request error: ${endpoint}`, error);
      throw error;
    }
  }

  // Get JWT token from authService
  async getToken() {
    return await authService.getAuthToken();
  }

  // Authentication endpoints
  async signup(userData) {
    try {
      // Use authService directly for signup instead of making API call
      return await authService.signUp(userData);
    } catch (error) {
      console.error('Signup error:', error);
      throw error;
    }
  }

  async signin(credentials) {
    try {
      // Use authService directly for signin instead of making API call
      return await authService.signIn('email', credentials);
    } catch (error) {
      console.error('Signin error:', error);
      throw error;
    }
  }

  // Chapter personalization endpoint
  async personalizeChapter(chapterData) {
    return this.request('/chapter/personalize', {
      method: 'POST',
      body: JSON.stringify(chapterData),
    });
  }

  // Chapter translation endpoint
  async translateChapter(chapterData) {
    return this.request('/chapter/translate', {
      method: 'POST',
      body: JSON.stringify(chapterData),
    });
  }

  // Get user profile
  async getUserProfile() {
    return this.request('/user/profile');
  }

  // Update user profile
  async updateUserProfile(profileData) {
    return this.request('/user/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData),
    });
  }
}

// Export a singleton instance
const apiClient = new ApiClient();
export default apiClient;

// Export individual methods for convenience
export const {
  signup,
  signin,
  personalizeChapter,
  translateChapter,
  getUserProfile,
  updateUserProfile
} = apiClient;

// Export the client instance in case consumers need to call request() directly
export { apiClient };