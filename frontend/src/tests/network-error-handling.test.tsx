import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AuthProvider } from '../contexts/AuthContext';
import ChatWindow from '../components/ChatWindow';

// Mock the auth service with all required methods
jest.mock('../services/authService', () => ({
  authService: {
    getAuthToken: jest.fn().mockResolvedValue('mock-token'),
    getSession: jest.fn().mockResolvedValue({ user: { id: 1, name: 'Test User' } }),
  }
}));

// Mock the chat API
jest.mock('../components/chatAPI', () => ({
  chatAPI: {
    sendMessage: jest.fn()
  }
}));

describe('Network Error Handling Tests', () => {
  test('displays user-friendly network error message', async () => {
    // Mock a network error for chatAPI.sendMessage
    require('../components/chatAPI').chatAPI.sendMessage.mockRejectedValue(
      new Error('Network error - unable to connect to the chat service')
    );

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
      expect(screen.getByText(/Network error - unable to connect to the chat service/i)).toBeInTheDocument();
    });
  });

  test('handles non-English error messages', async () => {
    // Mock a non-English error message (like "ya error q da rha h" which means "why is this error happening" in Hindi/Urdu)
    require('../components/chatAPI').chatAPI.sendMessage.mockRejectedValue(
      new Error('ya error q da rha h')  // Hindi/Urdu text meaning "why is this error happening"
    );

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
      // The ChatWindow should convert non-English messages to English
      const errorElement = screen.getByRole('alert');
      expect(errorElement).toHaveTextContent(/An error occurred connecting to the chat service/);
    });
  });
});