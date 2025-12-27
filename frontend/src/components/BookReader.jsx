import React, { useState, useEffect } from 'react';
import './BookReader.css';

const BookReader = ({ bookContent, onTextSelect }) => {
  const [content, setContent] = useState('');
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    if (bookContent) {
      setContent(bookContent);
    }
  }, [bookContent]);

  const handleTextSelection = () => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      setSelectedText(selectedText);
      if (onTextSelect) {
        onTextSelect(selectedText);
      }
    }
  };

  return (
    <div className="book-reader">
      <div 
        className="book-content" 
        onMouseUp={handleTextSelection}
        onKeyUp={handleTextSelection}
      >
        {content ? (
          <div className="book-text">{content}</div>
        ) : (
          <div className="placeholder">No book content loaded</div>
        )}
      </div>
      {selectedText && (
        <div className="selection-indicator">
          Selected: "{selectedText.substring(0, 50)}{selectedText.length > 50 ? '...' : ''}"
        </div>
      )}
    </div>
  );
};

export default BookReader;