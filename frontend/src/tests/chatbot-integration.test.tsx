import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from '../contexts/AuthContext';
import ChatbotButton from '../components/ChatbotButton';
import AuthModal from '../components/AuthModal';
import ChatWindow from '../components/ChatWindow';

// Mock the auth service
jest.mock('../services/authService', () => ({
  authService: {
    isAuthenticated: jest.fn().mockResolvedValue(false),
    getAuthToken: jest.fn().mockResolvedValue(null),
    getSession: jest.fn().mockResolvedValue(null),
    signIn: jest.fn().mockResolvedValue({ success: true }),
    signOut: jest.fn().mockResolvedValue(undefined),
    refreshToken: jest.fn().mockResolvedValue(true),
  }
}));

// Mock the chat API
jest.mock('../components/chatAPI', () => ({
  chatAPI: {
    sendMessage: jest.fn().mockResolvedValue({
      response: "Test response from AI",
      sources: ["Chapter 1", "Chapter 2"]
    })
  }
}));

describe('Chatbot Integration Tests', () => {
  test('Chatbot button renders correctly', () => {
    render(
      <AuthProvider>
        <ChatbotButton backendUrl={undefined} />
      </AuthProvider>
    );
    
    const button = screen.getByLabelText(/Open chat with AI assistant/i);
    expect(button).toBeInTheDocument();
    expect(button).toHaveTextContent('💬');
  });

  test('Auth modal appears when clicking chatbot without auth', async () => {
    render(
      <AuthProvider>
        <ChatbotButton backendUrl={undefined} />
      </AuthProvider>
    );
    
    const button = screen.getByLabelText(/Open chat with AI assistant/i);
    fireEvent.click(button);
    
    await waitFor(() => {
      expect(screen.getByText(/Sign in to Chat/i)).toBeInTheDocument();
    });
  });

  test('Chat window appears after authentication', async () => {
    // Mock authenticated state
    require('../services/authService').authService.isAuthenticated.mockResolvedValue(true);
    
    render(
      <AuthProvider>
        <ChatbotButton backendUrl={undefined} />
      </AuthProvider>
    );
    
    const button = screen.getByLabelText(/Open chat with AI assistant/i);
    fireEvent.click(button);
    
    await waitFor(() => {
      expect(screen.getByText(/AI Textbook Assistant/i)).toBeInTheDocument();
    });
  });

  test('Messages can be sent and received', async () => {
    render(
      <AuthProvider>
        <ChatWindow backendUrl="http://localhost:8000" onLogout={() => { } } onClose={undefined} />
      </AuthProvider>
    );
    
    const input = screen.getByLabelText(/Type your message/i);
    const submitButton = screen.getByLabelText(/Send message/i);
    
    fireEvent.change(input, { target: { value: 'Test message' } });
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Test response from AI/i)).toBeInTheDocument();
    });
  });
});