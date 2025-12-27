import React from 'react';
import './LoadingIndicator.css';

const LoadingIndicator = ({ message = "Processing your request...", show = true }) => {
  if (!show) {
    return null;
  }

  return (
    <div className="loading-indicator-container">
      <div className="loading-indicator">
        <div className="loading-spinner"></div>
        <span className="loading-text">{message}</span>
      </div>
    </div>
  );
};

export default LoadingIndicator;