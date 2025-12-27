// frontend/src/utils/auth.js
// Authentication helper functions for the textbook platform

// Check if user is authenticated by verifying JWT token presence and validity
export const isAuthenticated = () => {
  const token = localStorage.getItem('jwt_token');
  if (!token) {
    return false;
  }

  // Decode the token to check for expiry
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Math.floor(Date.now() / 1000);
    
    // Token is valid if it hasn't expired
    return payload.exp > currentTime;
  } catch (error) {
    console.error('Error decoding token:', error);
    return false;
  }
};

// Get user profile data from localStorage or return null
export const getUserProfile = () => {
  const userData = localStorage.getItem('user_profile');
  if (userData) {
    try {
      return JSON.parse(userData);
    } catch (error) {
      console.error('Error parsing user profile:', error);
      return null;
    }
  }
  return null;
};

// Save user profile data to localStorage
export const setUserProfile = (profile) => {
  try {
    localStorage.setItem('user_profile', JSON.stringify(profile));
  } catch (error) {
    console.error('Error saving user profile:', error);
  }
};

// Remove user profile data from localStorage
export const clearUserProfile = () => {
  localStorage.removeItem('user_profile');
};

// Get JWT token from localStorage
export const getToken = () => {
  return localStorage.getItem('jwt_token');
};

// Set JWT token in localStorage
export const setToken = (token) => {
  localStorage.setItem('jwt_token', token);
};

// Remove JWT token from localStorage
export const removeToken = () => {
  localStorage.removeItem('jwt_token');
  clearUserProfile(); // Also clear user profile when token is removed
};

// Validate token expiry and refresh if needed (placeholder for actual refresh logic)
export const validateToken = async () => {
  const token = getToken();
  if (!token) {
    return false;
  }

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const currentTime = Math.floor(Date.now() / 1000);
    const timeUntilExpiry = payload.exp - currentTime;

    // If token expires in less than 5 minutes, consider it expired
    if (timeUntilExpiry < 5 * 60) {
      // Attempt token refresh (in a real implementation, you would call your refresh endpoint)
      // For now, we'll just return false to indicate need to re-authenticate
      return false;
    }

    return true;
  } catch (error) {
    console.error('Error validating token:', error);
    return false;
  }
};

// Check if user has specific permissions (placeholder implementation)
export const hasPermission = (permission) => {
  // In a real implementation, this would check the user's permissions from their token or profile
  const userProfile = getUserProfile();
  // Placeholder logic - in real implementation, check permissions based on user role/profile
  return !!userProfile; // Simply return true if user is authenticated for now
};

// Format authorization header for API requests
export const getAuthHeader = () => {
  const token = getToken();
  if (token) {
    return {
      'Authorization': `Bearer ${token}`,
    };
  }
  return {};
};