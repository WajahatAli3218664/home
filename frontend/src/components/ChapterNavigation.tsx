import React from 'react';
import Link from '@docusaurus/Link';

interface ChapterNavigationProps {
  currentChapterId: number;
}

export const ChapterNavigation: React.FC<ChapterNavigationProps> = ({ currentChapterId }) => {
  // In a real implementation, these would be fetched from the backend
  const previousChapterId = currentChapterId > 1 ? currentChapterId - 1 : null;
  const nextChapterId = currentChapterId < 12 ? currentChapterId + 1 : null; // Assuming 12 chapters

  return (
    <div className="flex justify-between items-center mt-8 pt-8 border-t">
      <div>
        {previousChapterId && (
          <Link href={`/chapters/${previousChapterId}`} className="text-blue-600 hover:underline">
            ← Previous Chapter
          </Link>
        )}
      </div>
      <div>
        <Link href="/table-of-contents" className="text-blue-600 hover:underline">
          Table of Contents
        </Link>
      </div>
      <div>
        {nextChapterId && (
          <Link href={`/chapters/${nextChapterId}`} className="text-blue-600 hover:underline">
            Next Chapter →
          </Link>
        )}
      </div>
    </div>
  );
};