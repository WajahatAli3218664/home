// frontend/src/components/Chapter/ChapterActions.jsx
import React from 'react';
import PersonalizeButton from './PersonalizeButton';
import TranslateButton from './TranslateButton';

const ChapterActions = ({
  chapterId,
  chapterContent,
  onContentUpdate,
  isAuthenticated,
  className = ""
}) => {
  return (
    <div className={`chapter-actions flex gap-4 mb-6 ${className}`}>
      <div className="personalize-section">
        <PersonalizeButton
          chapterId={chapterId}
          chapterContent={chapterContent}
          onContentUpdate={onContentUpdate}
          isAuthenticated={isAuthenticated}
          className="w-full sm:w-auto"
        />
      </div>

      <div className="translate-section">
        <TranslateButton
          chapterId={chapterId}
          chapterContent={chapterContent}
          onContentUpdate={onContentUpdate}
          isAuthenticated={isAuthenticated}
          className="w-full sm:w-auto"
        />
      </div>
    </div>
  );
};

export default ChapterActions;