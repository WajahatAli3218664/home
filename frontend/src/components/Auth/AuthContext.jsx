// frontend/src/components/Auth/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';
import { isAuthenticated as checkAuthStatus, getToken, setToken, removeToken, getUserProfile, setUserProfile } from '../../utils/auth';
import { apiClient } from '../../utils/api';

const AuthContext = createContext(null);

// The AuthProvider component that wraps the application
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  // Check authentication status on initial load and whenever the token might have changed
  useEffect(() => {
    const checkAuth = async () => {
      if (checkAuthStatus()) {
        try {
          // Try to get the user profile using the stored token
          const token = getToken();
          if (token) {
            // In a real implementation, this would fetch user details from the backend
            const profile = getUserProfile();
            setUser(profile);
            setIsAuthenticated(true);
          }
        } catch (error) {
          console.error('Error verifying authentication:', error);
          // If verification fails, clear any stored tokens
          removeToken();
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const signup = async (userData) => {
    try {
      setLoading(true);
      const response = await apiClient.signup(userData);
      
      if (response.success) {
        // Store the returned token
        setToken(response.access_token);
        
        // Store user profile data
        setUserProfile(response.user);
        setUser(response.user);
        setIsAuthenticated(true);
        
        return { success: true, user: response.user };
      } else {
        return { success: false, error: response.detail || 'Signup failed' };
      }
    } catch (error) {
      console.error('Signup error:', error);
      return { success: false, error: error.message || 'An error occurred during signup' };
    } finally {
      setLoading(false);
    }
  };

  const signin = async (credentials) => {
    try {
      setLoading(true);
      const response = await apiClient.signin(credentials);
      
      if (response.success && response.token) {
        // Store the returned token
        setToken(response.token);
        
        // In a real implementation, we'd fetch user profile here
        // For now, we'll use a placeholder approach
        const profile = { 
          ...credentials, 
          programming_level: 'beginner',  // Default values until we fetch from API
          ai_experience: 'none',
          gpu_available: false,
          ram_size: '8GB'
        };
        
        setUserProfile(profile); 
        setUser(profile);
        setIsAuthenticated(true);
        
        return { success: true, user: profile };
      } else {
        return { success: false, error: response.detail || 'Signin failed' };
      }
    } catch (error) {
      console.error('Signin error:', error);
      return { success: false, error: error.message || 'An error occurred during signin' };
    } finally {
      setLoading(false);
    }
  };

  const signout = () => {
    removeToken();
    setUser(null);
    setIsAuthenticated(false);
  };

  // Value that will be provided to consuming components
  const value = {
    user,
    isAuthenticated,
    loading,
    signup,
    signin,
    signout,
    // Additional auth-related functions can be added here
    updateProfile: async (profileData) => {
      try {
        // Placeholder for update profile implementation
        setUser(prev => ({ ...prev, ...profileData }));
        setUserProfile({ ...getUserProfile(), ...profileData });
        return { success: true, user: { ...user, ...profileData } };
      } catch (error) {
        console.error('Profile update error:', error);
        return { success: false, error: error.message || 'Failed to update profile' };
      }
    }
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;