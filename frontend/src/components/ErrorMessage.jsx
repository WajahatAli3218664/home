import React from 'react';
import './ErrorMessage.css';

const ErrorMessage = ({ message, onClose }) => {
  if (!message) {
    return null;
  }

  return (
    <div className="error-message-container">
      <div className="error-message">
        <span className="error-text">{message}</span>
        {onClose && (
          <button className="error-close-button" onClick={onClose}>
            ×
          </button>
        )}
      </div>
    </div>
  );
};

export default ErrorMessage;