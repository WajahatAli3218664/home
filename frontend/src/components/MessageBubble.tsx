import React from 'react';
import './MessageBubble.css';

interface MessageBubbleProps {
  message: string;
  isUser: boolean;
  timestamp?: string;
  confidence?: 'high' | 'medium' | 'low';
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ 
  message, 
  isUser, 
  timestamp, 
  confidence 
}) => {
  const messageClass = `message-bubble ${isUser ? 'user-message' : 'ai-message'} ${
    confidence ? `confidence-${confidence}` : ''
  }`;

  return (
    <div className={messageClass}>
      <div className="message-content">
        {message}
      </div>
      {(timestamp || confidence) && (
        <div className="message-meta">
          {timestamp && <span className="message-time">{timestamp}</span>}
          {confidence && (
            <span className={`confidence-indicator confidence-${confidence}`}>
              {confidence.charAt(0).toUpperCase() + confidence.slice(1)} Confidence
            </span>
          )}
        </div>
      )}
    </div>
  );
};

export default MessageBubble;