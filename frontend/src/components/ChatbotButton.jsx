import React, { useState } from 'react';
import '../styles/ChatbotButton.css';
import '../styles/ChatWindow.css'; // Also import chat window styles
import ChatWindow from './ChatWindow';

const ChatbotButton = ({ position = "bottom-left", size = "large", backendUrl }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isClosing, setIsClosing] = useState(false);

  const handleClick = () => {
    // Toggle chat window directly without authentication
    if (isOpen) {
      // Trigger close animation
      setIsClosing(true);
      // Reset the closing state after animation completes
      setTimeout(() => {
        setIsOpen(false);
        setIsClosing(false);
      }, 300); // Match the duration of the CSS animation
    } else {
      setIsOpen(true);
    }
  };

  const handleWindowClose = () => {
    // Trigger close animation
    setIsClosing(true);
    // Reset the closing state after animation completes
    setTimeout(() => {
      setIsOpen(false);
      setIsClosing(false);
    }, 300); // Match the duration of the CSS animation
  };

  const buttonPositionClass = `chatbot-button-${position}`;
  const buttonSizeClass = `chatbot-button-${size}`;

  return (
    <div className="chatbot-container">
      {isOpen && !isClosing && (
        <ChatWindow
          onClose={handleWindowClose}
          backendUrl={backendUrl}
        />
      )}

      {isClosing && (
        <div className="chat-window-container slide-down">
          <ChatWindow
            onClose={handleWindowClose}
            backendUrl={backendUrl}
          />
        </div>
      )}

      <button
        className={`chatbot-button ${buttonPositionClass} ${buttonSizeClass} ${isOpen ? 'active' : ''}`}
        onClick={handleClick}
        aria-label={isOpen ? "Close chat" : "Open chat with AI assistant"}
        title="Chat with AI textbook assistant"
        tabIndex="0"
        onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
        onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
      >
        💬
      </button>
    </div>
  );
};

export default ChatbotButton;