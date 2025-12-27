import React, { createContext, useState, useEffect, useContext } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  const initializeAuth = async () => {
    try {
      // Use authService to check authentication
      const session = await authService.getSession();
      if (session && (session.user || session.id)) {
        // Set user from session data
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
      try {
        // Attempt to sign out if there's an auth-related error
        await authService.signOut();
      } catch (signOutError) {
        console.error('Error during sign out:', signOutError);
      }
    }
  };

  useEffect(() => {
    initializeAuth();
  }, []);

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, initializeAuth }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
