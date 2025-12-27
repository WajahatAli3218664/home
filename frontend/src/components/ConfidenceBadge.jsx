import React from 'react';
import './ConfidenceBadge.css';

const ConfidenceBadge = ({ level, tooltip }) => {
  // Convert level to uppercase to match our enum values
  const levelUpper = level ? level.toUpperCase() : 'LOW';
  
  // Determine the class name and display text based on the level
  let className = 'confidence-badge ';
  let displayText = 'Unknown';
  
  switch(levelUpper) {
    case 'HIGH':
      className += 'confidence-high';
      displayText = 'High';
      break;
    case 'MEDIUM':
      className += 'confidence-medium';
      displayText = 'Medium';
      break;
    case 'LOW':
      className += 'confidence-low';
      displayText = 'Low';
      break;
    default:
      className += 'confidence-unknown';
  }
  
  return (
    <span className={className} title={tooltip || `Confidence level: ${displayText}`}>
      {displayText} Confidence
    </span>
  );
};

export default ConfidenceBadge;