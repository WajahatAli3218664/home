// Better Auth client implementation
// This interfaces with the existing backend auth API
// Since the Better Auth client API doesn't work with the alpha version,
// we'll implement direct API calls to the backend auth routes

// Get base URL for API requests
const getBaseURL = () => {
  // First check for environment variable in browser (for Docusaurus)
  if (typeof window !== 'undefined' && window.ENV && window.ENV.REACT_APP_API_BASE_URL) {
    return window.ENV.REACT_APP_API_BASE_URL;
  }

  // Check for environment variable in process (for React apps)
  if (typeof process !== 'undefined' && process.env && process.env.REACT_APP_API_BASE_URL) {
    return process.env.REACT_APP_API_BASE_URL;
  }

  // Check for window variable (set by Docusaurus)
  if (typeof window !== 'undefined' && window.REACT_APP_API_BASE_URL) {
    return window.REACT_APP_API_BASE_URL;
  }

  // Default fallback
  return 'http://localhost:8000'; // Backend API URL
};

// Sign in functionality
export const signIn = {
  /**
   * Sign in with email and password
   * @param {{email: string, password: string}} params
   * @returns {Promise<Object>} The sign in result
   */
  email: async (params) => {
    const { email, password } = params || {};

    // Validation
    if (!email || !password) {
      return { error: { message: 'Email and password are required' } };
    }

    try {
      // Use the backend auth routes
      const response = await fetch(`${getBaseURL()}/api/v1/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded', // OAuth2PasswordRequestForm format
        },
        body: new URLSearchParams({
          username: email, // FastAPI expects 'username' field for email
          password: password
        })
      });

      // Check if the response is ok before trying to parse JSON
      if (!response.ok) {
        // Try to get error details from response
        let errorDetails;
        try {
          errorDetails = await response.json();
        } catch (jsonError) {
          // If we can't parse JSON, use status text
          errorDetails = { detail: `HTTP error! status: ${response.status}` };
        }

        return {
          error: {
            message: errorDetails.detail || errorDetails.message || `HTTP error! status: ${response.status}`
          }
        };
      }

      const result = await response.json();

      // Success response from backend
      return {
        success: true,
        ...result
      };
    } catch (error) {
      console.error('Sign in error:', error);
      // Check if it's a network error
      if (error instanceof TypeError && error.message.includes('fetch')) {
        return {
          error: {
            message: `Network error: Unable to connect to the authentication server at ${getBaseURL()}. Please make sure the backend is running.`
          }
        };
      }

      return {
        error: {
          message: error.message || 'Sign in failed'
        }
      };
    }
  },

  /**
   * Sign in with Google
   * @param {{callbackURL?: string}} params
   * @returns {Promise<Object>} The sign in result
   */
  google: async (params) => {
    // Google OAuth is not implemented in the current backend
    // This would require Google OAuth setup in the backend
    return {
      error: {
        message: 'Google sign-in is not configured in the backend. Please use email/password sign-in.'
      }
    };
  }
};

/**
 * Sign up with email and additional user background info
 * @param {{email: string, password: string, name?: string, programming_level?: string, ai_experience?: string, gpu_available?: boolean, ram_size?: string}} userData
 * @returns {Promise<Object>} The sign up result
 */
export const signUp = async (userData) => {
  const {
    email,
    password,
    name,
    programming_level = 'beginner',
    ai_experience = 'none',
    gpu_available = false,
    ram_size = '8GB'
  } = userData || {};

  // Validation
  if (!email || !password) {
    return { error: { message: 'Email and password are required' } };
  }

  try {
    // Use the backend auth routes
    const response = await fetch(`${getBaseURL()}/api/v1/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
        name: name || email.split('@')[0],
        programming_level,
        ai_experience,
        gpu_available,
        ram_size
      })
    });

    const result = await response.json();

    if (!response.ok) {
      return {
        error: {
          message: result.detail || result.message || 'Sign up failed'
        }
      };
    }

    return {
      success: true,
      ...result
    };
  } catch (error) {
    console.error('Sign up error:', error);
    return {
      error: {
        message: error.message || 'Sign up failed'
      }
    };
  }
};

// Sign out functionality
export const signOut = async () => {
  // For the current backend, sign out is handled client-side by clearing tokens
  // since it uses JWT tokens stored in memory/localStorage
  localStorage.removeItem('jwt_token');
  localStorage.removeItem('access_token');
  return { success: true };
};

// Get current session
export const getSession = async () => {
  // Try to get user info from the /me endpoint which requires authentication
  try {
    // Get the auth token from wherever it's stored
    const token = localStorage.getItem('jwt_token') || localStorage.getItem('access_token');

    if (!token) {
      return null;
    }

    const response = await fetch(`${getBaseURL()}/api/v1/auth/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (!response.ok) {
      // If the token is invalid or expired, return null
      if (response.status === 401 || response.status === 403) {
        // Clear the invalid token
        localStorage.removeItem('jwt_token');
        localStorage.removeItem('access_token');
        return null;
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const user = await response.json();

    // Return a session-like object that includes both user data and token
    return {
      user: user,
      token: token
    };
  } catch (error) {
    console.error('Get session error:', error);
    return null;
  }
};

// Get user account
export const getAccount = async () => {
  try {
    const session = await getSession();
    return session?.user || null;
  } catch (error) {
    console.error('Get user error:', error);
    return null;
  }
};

// Get auth token
export const getAuthToken = async () => {
  try {
    // Get token from localStorage where it would be stored after login
    return localStorage.getItem('jwt_token') || localStorage.getItem('access_token') || null;
  } catch (error) {
    console.error('Get auth token error:', error);
    return null;
  }
};

// Check if user is authenticated
export const isAuthenticated = async () => {
  try {
    const session = await getSession();
    return !!session && !!session.user;
  } catch (error) {
    console.error('Check authentication error:', error);
    return false;
  }
};

// Initialize auth state
export const initializeAuth = async () => {
  try {
    return await getSession();
  } catch (error) {
    console.error('Initialize auth error:', error);
    return null;
  }
};