import React, { useState, useRef, useEffect } from 'react';
import MessageBubble from './MessageBubble';
import './ChatInterface.css';

const ChatInterface = ({ sessionId, bookId, onSend, messages, loading }) => {
  const [inputValue, setInputValue] = useState('');
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() && onSend) {
      onSend(inputValue, selectedText);
      setInputValue('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h3>Book Assistant</h3>
      </div>
      
      <div className="chat-messages">
        {messages && messages.length > 0 ? (
          messages.map((msg, index) => (
            <MessageBubble
              key={index}
              message={msg.text}
              isUser={msg.isUser}
              confidence={msg.confidence}
            />
          ))
        ) : (
          <div className="empty-state">
            Ask a question about the book content, and I'll do my best to answer based on the provided text.
          </div>
        )}
        {loading && (
          <MessageBubble
            message="Thinking..."
            isUser={false}
            isTyping={true}
          />
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <form className="chat-input-form" onSubmit={handleSubmit}>
        {selectedText && (
          <div className="selected-text-indicator">
            Using selected text: "{selectedText.substring(0, 50)}{selectedText.length > 50 ? '...' : ''}"
            <button 
              type="button" 
              className="clear-selection"
              onClick={() => setSelectedText('')}
            >
              Clear
            </button>
          </div>
        )}
        <div className="input-area">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about the book..."
            disabled={loading}
            rows="1"
          />
          <button 
            type="submit" 
            disabled={!inputValue.trim() || loading}
            className="send-button"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;