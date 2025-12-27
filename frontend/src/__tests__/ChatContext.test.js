// Basic test for the ChatContext
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ChatProvider, useChatContext } from '../contexts/ChatContext';

// A simple component to test the context
const TestComponent = () => {
  const {
    sessionId,
    messages,
    selectedText,
    isProcessing,
    error,
    setSessionId,
    addMessage,
    setSelectedText,
    setProcessing,
    setError
  } = useChatContext();

  return (
    <div>
      <div data-testid="session-id">{sessionId || 'No Session'}</div>
      <div data-testid="message-count">{messages.length}</div>
      <div data-testid="selected-text">{selectedText || 'No Selection'}</div>
      <div data-testid="is-processing">{isProcessing ? 'Processing' : 'Not Processing'}</div>
      <div data-testid="error">{error || 'No Error'}</div>
    </div>
  );
};

describe('ChatContext', () => {
  test('provides initial state values', () => {
    render(
      <ChatProvider>
        <TestComponent />
      </ChatProvider>
    );

    expect(screen.getByTestId('session-id')).toHaveTextContent('No Session');
    expect(screen.getByTestId('message-count')).toHaveTextContent('0');
    expect(screen.getByTestId('selected-text')).toHaveTextContent('No Selection');
    expect(screen.getByTestId('is-processing')).toHaveTextContent('Not Processing');
    expect(screen.getByTestId('error')).toHaveTextContent('No Error');
  });
});