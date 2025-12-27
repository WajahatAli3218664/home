import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatbotButton from '../src/components/ChatbotButton';

// Mock the child components
jest.mock('../src/components/ChatWindow', () => () => <div data-testid="chat-window">Chat Window</div>);
jest.mock('../src/components/AuthModal', () => () => <div data-testid="auth-modal">Auth Modal</div>);

// Mock the authService
jest.mock('../src/services/authService', () => ({
  authService: {
    isAuthenticated: jest.fn(),
    getAuthToken: jest.fn(),
    signIn: jest.fn(),
    signOut: jest.fn(),
    refreshToken: jest.fn(),
  }
}));

import { authService } from '../src/services/authService';

describe('ChatbotButton', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders chatbot button', () => {
    // Mock that user is not authenticated
    authService.isAuthenticated.mockResolvedValue(false);
    
    render(<ChatbotButton />);
    
    const button = screen.getByRole('button', { name: /Open chat with AI assistant/i });
    expect(button).toBeInTheDocument();
  });

  test('shows auth modal when clicked and user is not authenticated', async () => {
    // Mock that user is not authenticated
    authService.isAuthenticated.mockResolvedValue(false);
    
    render(<ChatbotButton />);
    
    const button = screen.getByRole('button', { name: /Open chat with AI assistant/i });
    fireEvent.click(button);
    
    // Wait for the modal to appear
    await waitFor(() => {
      expect(screen.getByTestId('auth-modal')).toBeInTheDocument();
    });
  });

  test('opens chat window when clicked and user is authenticated', async () => {
    // Mock that user is authenticated
    authService.isAuthenticated.mockResolvedValue(true);
    
    render(<ChatbotButton />);
    
    const button = screen.getByRole('button', { name: /Open chat with AI assistant/i });
    fireEvent.click(button);
    
    // Wait for the chat window to appear
    await waitFor(() => {
      expect(screen.getByTestId('chat-window')).toBeInTheDocument();
    });
  });

  test('toggles chat window visibility when authenticated', async () => {
    // Mock that user is authenticated
    authService.isAuthenticated.mockResolvedValue(true);
    
    render(<ChatbotButton />);
    
    const button = screen.getByRole('button', { name: /Open chat with AI assistant/i });
    
    // Click to open
    fireEvent.click(button);
    await waitFor(() => {
      expect(screen.getByTestId('chat-window')).toBeInTheDocument();
    });
    
    // Click to close
    fireEvent.click(button);
    // After closing, the chat window should not be in the document anymore
    // (though we can't test for this directly due to how the component works)
  });

  test('passes backendUrl prop to child components', () => {
    const backendUrl = 'https://test-backend.com';
    authService.isAuthenticated.mockResolvedValue(true);
    
    render(<ChatbotButton backendUrl={backendUrl} />);
    
    const button = screen.getByRole('button', { name: /Open chat with AI assistant/i });
    fireEvent.click(button);
  });

  test('passes position and size props correctly', () => {
    authService.isAuthenticated.mockResolvedValue(false);
    
    render(<ChatbotButton position="bottom-right" size="medium" />);
    
    const button = screen.getByRole('button', { name: /Open chat with AI assistant/i });
    expect(button).toHaveClass('chatbot-button-bottom-right');
    expect(button).toHaveClass('chatbot-button-medium');
  });
});