import React, { ReactNode } from 'react';
import MDXContent from '@theme-original/MDXContent';
import type MDXContentType from '@theme/MDXContent';
import type { WrapperProps } from '@docusaurus/types';
import { useLocation } from '@docusaurus/router';
import ChapterActions from '@site/src/components/Chapter/ChapterActions';
import { useAuth } from '@site/src/contexts/AuthContext';

type Props = WrapperProps<typeof MDXContentType>;

export default function MDXContentWrapper(props: Props): ReactNode {
  const location = useLocation();
  const { user, isAuthenticated } = useAuth();

  // Check if this is a chapter-related route
  const isChapterPage =
    location.pathname.includes('/docs/chapters/') ||
    location.pathname.includes('/chapters/') ||
    location.pathname.includes('/docs/modules/') ||
    location.pathname.includes('/modules/') ||
    (location.pathname.startsWith('/docs/') && (location.pathname.includes('chapter') || location.pathname.includes('module')));

  return (
    <>
      {isChapterPage && (
        <div className="chapter-actions-container mb-8">
          <ChapterActions
            chapterId={location.pathname.split('/').pop() || 'unknown'}
            chapterContent={""} // Actual content will be extracted by the component itself
            onContentUpdate={(newContent, type) => {
              // Handler for when content is updated by personalization/translation
              console.log(`${type} content updated`, newContent);
            }}
          />
        </div>
      )}
      <MDXContent {...props} />
    </>
  );
}
