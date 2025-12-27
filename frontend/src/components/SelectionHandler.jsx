import React from 'react';

// This component is primarily a utility to handle text selection
// The actual selection handling is done in the BookReader component
const SelectionHandler = ({ selectedText, onClearSelection }) => {
  if (!selectedText) {
    return null;
  }

  return (
    <div className="selection-handler">
      <div className="selected-text-preview">
        <strong>Selected text:</strong> "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
      </div>
      <button onClick={onClearSelection} className="clear-button">
        Clear Selection
      </button>
    </div>
  );
};

export default SelectionHandler;