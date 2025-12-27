import React, { useState, useEffect, useRef, useCallback } from 'react';
import { chatAPI } from './chatAPI';
import '../styles/ChatWindow.css';

const ChatWindow = ({ onClose, backendUrl }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [focusedMessageIndex, setFocusedMessageIndex] = useState(-1);
  const messagesEndRef = useRef(null);
  const messageElements = useRef([]);

  const scrollToBottom = () => {
    if (messagesEndRef.current && typeof messagesEndRef.current.scrollIntoView === 'function') {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    scrollToBottom();
    // Update focused message index when messages change
    setFocusedMessageIndex(messages.length - 1);
  }, [messages]);

  // Handle keyboard navigation for messages
  const handleKeyDown = useCallback((e) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setFocusedMessageIndex(prev => Math.min(prev + 1, messages.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setFocusedMessageIndex(prev => Math.max(prev - 1, 0));
    } else if (e.key === 'Home') {
      e.preventDefault();
      setFocusedMessageIndex(0);
    } else if (e.key === 'End') {
      e.preventDefault();
      setFocusedMessageIndex(messages.length - 1);
    }
  }, [messages.length]);

  // Add event listener for keyboard navigation
  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleKeyDown]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage = {
      id: Date.now(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError('');

    try {
      // Call the chat API - update to match new interface
      const response = await chatAPI.sendMessage(inputValue, backendUrl);

      // Add AI response to the chat - update to handle response structure
      const aiMessage = {
        id: Date.now() + 1,
        content: response.response || response.answer, // Handle both possible response field names
        sender: 'ai',
        timestamp: response.timestamp || new Date().toISOString(),
        // Try to extract sources/citations from response
        citations: response.sources || response.citations || []
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      // Use the enhanced error message from chatAPI if available
      let errorMessage = err.message;

      // If the error is a TypeError related to fetch, ensure we provide a user-friendly message
      if (err.name === 'TypeError' && err.message.includes('fetch')) {
        errorMessage = 'Network error - unable to connect to the chat service';
      } else {
        // Check if the error message might not be in English
        // A simple heuristic that works for both cases:
        // 1. Messages with non-Latin characters (e.g., Chinese, Arabic)
        // 2. Messages that mix languages or contain specific non-English phrases
        const nonLatinRegex = /[^\x00-\xFF]/;  // Contains non-Latin characters
        let isNonEnglish = nonLatinRegex.test(err.message);

        // Additional check: look for specific non-English patterns like "q da rha h" (Urdu/Hindi)
        // This is a more targeted approach for Indian language phrases
        if (!isNonEnglish) {
          const specificNonEnglishPhrases = ['q da rha h', 'kiya', 'kyun', 'kya', 'kaise', 'hai', 'ho raha', 'raha h', 'hoga'];
          isNonEnglish = specificNonEnglishPhrases.some(phrase =>
            err.message.toLowerCase().includes(phrase)
          );
        }

        // If it appears to be non-English, use a standard English error message
        if (isNonEnglish) {
          errorMessage = 'An error occurred connecting to the chat service';
        }
      }

      setError(`Failed to get response: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      className="chat-window show"
      role="dialog"
      aria-modal="true"
      aria-labelledby="chat-window-title"
      tabIndex={-1}
    >
      <div className="chat-header">
        <h3 id="chat-window-title">AI Textbook Assistant</h3>
        <div className="chat-actions">
          <button
            className="close-button"
            onClick={onClose}
            aria-label="Close chat"
            aria-describedby="chat-window-title"
          >
            ×
          </button>
        </div>
      </div>

      <div
        className="chat-messages"
        aria-live="polite"
        aria-relevant="additions"
        role="log"
        aria-label="Chat messages"
        onKeyDown={handleKeyDown}
        tabIndex={0}
      >
        {messages.length === 0 ? (
          <div className="welcome-message" role="status" aria-live="polite">
            <p>Hello! I'm your AI textbook assistant. How can I help you today?</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={message.id}
              ref={el => messageElements.current[index] = el}
              className={`message ${message.sender}-message ${focusedMessageIndex === index ? 'focused' : ''}`}
              role="listitem"
              aria-label={`${message.sender} message: ${message.content.substring(0, 50)}${message.content.length > 50 ? '...' : ''}`}
              tabIndex={focusedMessageIndex === index ? 0 : -1}
              onFocus={() => setFocusedMessageIndex(index)}
              onClick={() => setFocusedMessageIndex(index)}
            >
              <div className="message-content">
                {message.content}
              </div>
              {message.citations && message.citations.length > 0 && (
                <div className="citations" role="region" aria-labelledby="citations-title">
                  <p id="citations-title"><strong>Citations:</strong></p>
                  <ul aria-label="Sources">
                    {message.citations.map((citation, citationIndex) => (
                      <li key={citationIndex}>
                        <a
                          href={citation.sourceUrl}
                          target="_blank"
                          rel="noopener noreferrer"
                          aria-label={`Source: ${citation.sourceTitle || citation.sourceUrl}`}
                        >
                          {citation.sourceTitle || citation.sourceUrl}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))
        )}
        {isLoading && (
          <div className="message ai-message" role="status" aria-live="polite">
            <div className="loading-indicator">
              <div className="loading-spinner" aria-label="Loading"></div>
              <span>Thinking...</span>
            </div>
          </div>
        )}
        {error && (
          <div className="message error-message" role="alert" aria-live="assertive">
            <div className="message-content">
              {error}
            </div>
          </div>
        )}
        <div ref={messagesEndRef} aria-hidden="true" />
      </div>

      <form onSubmit={handleSubmit} className="chat-input-form" role="form" aria-label="Chat input form">
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask me anything about the textbook..."
          disabled={isLoading}
          aria-label="Type your message"
          aria-describedby="chat-instructions"
          autoFocus
        />
        <button
          type="submit"
          disabled={isLoading || !inputValue.trim()}
          aria-label="Send message"
        >
          Send
        </button>
        <div id="chat-instructions" className="sr-only">
          Press Enter to submit your message, Arrow keys to navigate messages, Home/End to go to first/last message
        </div>
      </form>
    </div>
  );
};

export default ChatWindow;