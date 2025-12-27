import React from 'react';

interface ReadingTimeEstimateProps {
  content: string;
}

export const ReadingTimeEstimate: React.FC<ReadingTimeEstimateProps> = ({ content }) => {
  // Calculate reading time based on average reading speed (200 words per minute)
  const wordsPerMinute = 200;
  const wordCount = content.trim().split(/\s+/).length;
  const readingTime = Math.ceil(wordCount / wordsPerMinute);

  return (
    <div className="bg-blue-50 p-4 rounded-lg mb-6">
      <p className="text-gray-700">
        Estimated reading time: <span className="font-semibold">{readingTime} minute{readingTime !== 1 ? 's' : ''}</span>
      </p>
    </div>
  );
};