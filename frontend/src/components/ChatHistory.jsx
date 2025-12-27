import React from 'react';
import './ChatHistory.css';

const ChatHistory = ({ messages, onMessageClick }) => {
  if (!messages || messages.length === 0) {
    return (
      <div className="chat-history">
        <p className="no-messages">No conversation history yet.</p>
      </div>
    );
  }

  return (
    <div className="chat-history">
      <h3>Conversation History</h3>
      <div className="history-messages">
        {messages.map((message) => (
          <div 
            key={message.message_id} 
            className={`history-message ${message.role}`}
            onClick={() => onMessageClick && onMessageClick(message)}
          >
            <div className="message-content">
              <strong>{message.role === 'user' ? 'You: ' : 'Assistant: '}</strong>
              {message.content}
            </div>
            {message.confidence_level && (
              <div className="message-confidence">
                Confidence: {message.confidence_level}
              </div>
            )}
            <div className="message-timestamp">
              {new Date(message.timestamp).toLocaleTimeString()}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChatHistory;