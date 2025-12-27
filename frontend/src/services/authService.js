// Import the authClient that implements Better Auth API
import { signIn, signUp, signOut, getSession, getAuthToken, isAuthenticated as checkAuth, getAccount } from './authClient';

// Better Auth service interface to maintain compatibility with existing code
export const authService = {
  /**
   * Checks if the user is currently authenticated
   * @returns {Promise<boolean>} Whether the user is authenticated
   */
  isAuthenticated: async () => {
    try {
      return await checkAuth();
    } catch (error) {
      console.error('Error checking authentication status:', error);
      return false;
    }
  },

  /**
   * Gets the current auth token
   * @returns {Promise<string|null>} The auth token or null if not authenticated
   */
  getAuthToken: async () => {
    try {
      return await getAuthToken();
    } catch (error) {
      console.error('Error getting auth token:', error);
      return null;
    }
  },

  /**
   * Gets the current user session
   * @returns {Promise<Object|null>} The session object or null if not authenticated
   */
  getSession: async () => {
    try {
      return await getSession();
    } catch (error) {
      console.error('Error getting session:', error);
      return null;
    }
  },

  /**
   * Registers a new user account
   * @param {Object} userData - User registration data including email, password, and profile info
   * @returns {Promise<Object>} The registration result
   */
  signUp: async (userData) => {
    try {
      const result = await signUp({
        email: userData.email,
        password: userData.password,
        name: userData.name || userData.email.split('@')[0], // Use email prefix as name if not provided
        programming_level: userData.programming_level || 'beginner',
        ai_experience: userData.ai_experience || 'none',
        gpu_available: userData.gpu_available || false,
        ram_size: userData.ram_size || '8GB'
      });

      if (result && !result.error) {
        // Store the token in localStorage for future requests
        if (result.access_token) {
          localStorage.setItem('jwt_token', result.access_token);
          localStorage.setItem('access_token', result.access_token);
        }

        return {
          success: true,
          user: result.user || result,
          session: result
        };
      } else {
        return { success: false, error: result.error?.message || result.error || 'Sign up failed' };
      }
    } catch (error) {
      console.error('Error signing up:', error);
      return { success: false, error: error.message || 'Sign up failed' };
    }
  },

  /**
   * Gets the current user's ID
   * @returns {Promise<string|null>} The user ID or null if not authenticated
   */
  getUserId: async () => {
    try {
      const session = await getSession();
      return session?.user?.id || session?.id || null;
    } catch (error) {
      console.error('Error getting user ID:', error);
      return null;
    }
  },

  /**
   * Initiates the sign-in process with the specified provider
   * @param {string} provider - The authentication provider ('email', 'google', etc.)
   * @param {Object} options - Additional options like email, password
   * @returns {Promise<Object>} The sign-in result
   */
  signIn: async (provider = 'email', options = {}) => {
    try {
      if (provider === 'email' && options.email && options.password) {
        // For email sign in with credentials
        const result = await signIn.email({
          email: options.email,
          password: options.password,
        });

        // Handle response based on format returned by auth client
        if (result && !result.error) {
          // Store the token in localStorage for future requests
          if (result.access_token) {
            localStorage.setItem('jwt_token', result.access_token);
            localStorage.setItem('access_token', result.access_token);
          }

          return {
            success: true,
            user: result.user || result,
            session: result
          };
        } else {
          return { success: false, error: result.error?.message || result.error || 'Sign in failed' };
        }
      } else if (provider === 'google') {
        // For Google sign in
        const result = await signIn.google({
          callbackURL: options.callbackURL || window.location.href,
        });

        if (result && !result.error) {
          // Store the token if provided
          if (result.access_token) {
            localStorage.setItem('jwt_token', result.access_token);
            localStorage.setItem('access_token', result.access_token);
          }

          return {
            success: true,
            user: result.user || result,
            session: result
          };
        } else {
          return { success: false, error: result.error?.message || result.error || 'Google sign in failed' };
        }
      } else {
        // For other providers or when no credentials provided
        return { success: false, error: `Sign in with ${provider} is not supported` };
      }
    } catch (error) {
      console.error(`Error signing in with ${provider}:`, error);
      return { success: false, error: error.message || `Sign in with ${provider} failed` };
    }
  },

  /**
   * Signs out the current user
   * @returns {Promise<void>}
   */
  signOut: async () => {
    try {
      const result = await signOut();

      // Clear the stored tokens
      localStorage.removeItem('jwt_token');
      localStorage.removeItem('access_token');

      if (result.success) {
        console.log('User signed out successfully');
      } else {
        console.error('Sign out failed:', result.error);
        throw new Error(result.error || 'Sign out failed');
      }
    } catch (error) {
      console.error('Error signing out:', error);
      throw error;
    }
  },

  /**
   * Refreshes the authentication token if needed
   * @returns {Promise<boolean>} Whether the token was successfully refreshed
   */
  refreshToken: async () => {
    try {
      // Better Auth handles token refresh automatically
      // We'll just verify that the session is still valid
      const session = await getSession();
      return !!session;
    } catch (error) {
      console.error('Error refreshing token:', error);
      return false;
    }
  }
};