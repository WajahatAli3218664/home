// frontend/src/components/Chapter/ContentDisplay.jsx
import React, { useState, useImperativeHandle } from 'react';

const ContentDisplay = React.forwardRef(({
  initialContent,
  title = "Chapter Content",
  allowReset = true,
  onResetComplete
}, ref) => {
  const [currentContent, setCurrentContent] = useState(initialContent);
  const [contentType, setContentType] = useState('original'); // 'original', 'personalized', 'translated'
  const [isResetting, setIsResetting] = useState(false);

  const handleReset = () => {
    setIsResetting(true);
    setCurrentContent(initialContent);
    setContentType('original');

    if (onResetComplete) {
      onResetComplete();
    }

    setTimeout(() => setIsResetting(false), 300);
  };

  const updateContent = (newContent, type) => {
    setCurrentContent(newContent);
    setContentType(type);
  };

  // Expose updateContent method via a ref so parent components can update the content
  useImperativeHandle(ref, () => ({
    updateContent,
    resetContent: handleReset
  }));

  return (
    <div className="chapter-content">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-gray-800">{title}</h2>
        {allowReset && contentType !== 'original' && (
          <button
            onClick={handleReset}
            disabled={isResetting}
            className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-md text-sm font-medium disabled:opacity-50"
          >
            {isResetting ? 'Resetting...' : 'Show Original'}
          </button>
        )}
      </div>

      <div
        className={`prose prose-lg max-w-none ${contentType === 'translated' ? 'rtl' : ''}`}
        dir={contentType === 'translated' ? 'rtl' : 'ltr'}
        lang={contentType === 'translated' ? 'ur' : undefined}
      >
        {currentContent && (
          <div dangerouslySetInnerHTML={{ __html: currentContent }} />
        )}
        {!currentContent && (
          <div className="text-gray-500 italic">No content available</div>
        )}
      </div>

      {contentType !== 'original' && (
        <div className="mt-4 text-sm text-gray-600">
          {contentType === 'personalized'
            ? 'Content has been personalized based on your profile.'
            : 'Content has been translated to Urdu.'}
        </div>
      )}
    </div>
  );
});

ContentDisplay.displayName = 'ContentDisplay';

export default ContentDisplay;