import React from 'react';
import './CitationDisplay.css';

const CitationDisplay = ({ citations, style = "inline" }) => {
  if (!citations || citations.length === 0) {
    return null;
  }

  const renderCitations = () => {
    if (style === "list") {
      return (
        <div className="citation-list">
          <h4>References:</h4>
          <ul>
            {citations.map((citation, index) => (
              <li key={index} className="citation-item">
                {citation}
              </li>
            ))}
          </ul>
        </div>
      );
    } else {
      // Default to inline style
      return (
        <div className="citation-inline">
          <span className="citation-label">Sources:</span>
          {citations.map((citation, index) => (
            <span key={index} className="citation-item">
              {citation}
              {index < citations.length - 1 && <span className="citation-separator">,&nbsp;</span>}
            </span>
          ))}
        </div>
      );
    }
  };

  return <div className="citation-display">{renderCitations()}</div>;
};

export default CitationDisplay;