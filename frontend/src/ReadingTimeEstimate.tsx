import React from 'react';

interface ReadingTimeEstimateProps {
  content: string;
}

export const ReadingTimeEstimate: React.FC<ReadingTimeEstimateProps> = ({ content }) => {
  // Calculate reading time based on average reading speed of 200 words per minute
  const wordsPerMinute = 200;
  const wordCount = content.trim().split(/\s+/).length;
  const readingTime = Math.ceil(wordCount / wordsPerMinute);

  return (
    <div className="reading-time text-sm text-gray-600 mb-4">
      Reading time: ~{readingTime} min
    </div>
  );
};