// frontend/src/theme/MDXContent/index.js
import React, { useMemo } from 'react';
import { useActiveDocContext } from '@docusaurus/plugin-content-docs/client';
import { useLocation } from '@docusaurus/router';
import ChapterActions from '@site/src/components/Chapter/ChapterActions';
import { useAuth } from '@site/src/contexts/AuthContext';

// Check if the current page is a chapter page
const useIsChapterPage = () => {
  const location = useLocation();
  // Check if we're on a chapter page in docs/chapters or docs/modules
  return useMemo(() => {
    return location.pathname.includes('/docs/chapters/') ||
           location.pathname.includes('/chapters/') ||
           location.pathname.includes('/docs/modules/') ||
           location.pathname.includes('/modules/');
  }, [location.pathname]);
};

const CustomMDXContent = (props) => {
  const location = useLocation(); // Get location inside component
  const isChapter = useIsChapterPage();
  const { user, isAuthenticated } = useAuth();

  if (!isChapter) {
    // If not a chapter page, render normally
    return props.children;
  }

  // Extract a chapter ID from the URL path
  const chapterId = location.pathname.split('/').pop() || 'unknown';

  // For chapter pages, wrap with ChapterActions
  return (
    <div className="chapter-wrapper">
      <ChapterActions
        chapterId={chapterId}
        chapterContent={""} // The content will be extracted by the component itself
        isAuthenticated={isAuthenticated}
      />
      <div className="chapter-content-body">
        {props.children}
      </div>
    </div>
  );
};

export default CustomMDXContent;