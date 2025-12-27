import React from 'react';
import './MessageBubble.css';

const MessageBubble = ({ message, isUser, isTyping = false, confidence }) => {
  const confidenceColor = {
    high: 'green',
    medium: 'orange',
    low: 'red'
  };

  return (
    <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-content">
        {isTyping ? (
          <div className="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        ) : (
          <div className="message-text">{message}</div>
        )}
      </div>
      {confidence && !isUser && !isTyping && (
        <div 
          className="confidence-indicator"
          style={{ color: confidenceColor[confidence] }}
        >
          Confidence: {confidence}
        </div>
      )}
    </div>
  );
};

export default MessageBubble;