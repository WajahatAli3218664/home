import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import ChatbotButton from './ChatbotButton';

// Root component that wraps the entire app
const Root = ({ children }) => {
  // Get backend URL from environment or default
  const backendUrl = typeof window !== 'undefined'
    ? (window as any).BACKEND_URL || (window as any).REACT_APP_API_BASE_URL || 'http://localhost:8000'
    : 'http://localhost:8000';

  return (
    <AuthProvider>
      {children}
      <ChatbotButton backendUrl={backendUrl} />
    </AuthProvider>
  );
};

export default Root;