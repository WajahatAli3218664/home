import React, { createContext, useState, useEffect, useContext, ReactNode } from 'react';
import { authService } from '../services/authService';

interface AuthContextType {
  user: any; // Replace with proper User type
  isAuthenticated: boolean;
  isLoading: boolean;
  signIn: (email: string, password: string) => Promise<any>;
  signUp: (userData: any) => Promise<any>;
  signOut: () => Promise<void>;
  initializeAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<any>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Initialize auth state on app load
  useEffect(() => {
    const initAuth = async () => {
      try {
        setIsLoading(true);
        const session = await authService.getSession();
        if (session && (session.user || session.id)) {
          setUser(session.user || session);
          setIsAuthenticated(true);
        } else {
          setUser(null);
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error('Error initializing auth:', error);
        setUser(null);
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();

    // Set up session change listener if supported by auth library
    // This is where we'd handle token refresh or session changes
  }, []);

  const signIn = async (email: string, password: string) => {
    try {
      const result = await authService.signIn('email', {
        email,
        password,
        callbackURL: window.location.href,
        redirect: false
      });

      if (result?.success) {
        // Get updated session after sign in
        const session = await authService.getSession();
        if (session && (session.user || session.id)) {
          setUser(session.user || session);
          setIsAuthenticated(true);
          return result;
        }
      } else {
        // Handle error case
        console.error('Sign in failed:', result?.error);
        return result;
      }
    } catch (error) {
      console.error('Sign in error:', error);
      throw error;
    }
  };

  const signUp = async (userData: any) => {
    try {
      const result = await authService.signUp(userData);
      if (result?.success) {
        // Get updated session after sign up
        const session = await authService.getSession();
        if (session && (session.user || session.id)) {
          setUser(session.user || session);
          setIsAuthenticated(true);
          return result;
        }
      } else {
        // Handle error case
        console.error('Sign up failed:', result?.error);
        return result;
      }
    } catch (error) {
      console.error('Sign up error:', error);
      throw error;
    }
  };

  const signOut = async () => {
    try {
      await authService.signOut();
      setUser(null);
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Sign out error:', error);
      throw error;
    }
  };

  const initializeAuth = async () => {
    try {
      setIsLoading(true);
      const session = await authService.getSession();
      if (session && (session.user || session.id)) {
        setUser(session.user || session);
        setIsAuthenticated(true);
      } else {
        setUser(null);
        setIsAuthenticated(false);
      }
    } catch (error) {
      console.error('Error initializing auth:', error);
      setUser(null);
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  };

  const value = {
    user,
    isAuthenticated,
    isLoading,
    signIn,
    signUp,
    signOut,
    initializeAuth
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};