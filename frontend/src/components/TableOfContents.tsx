import React from 'react';
import Link from '@docusaurus/Link';
import { useEffect, useState } from 'react';
import { Chapter } from '../types/chapter';
import { getAllChapters } from '../services/chapterService';

export const TableOfContents: React.FC = () => {
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchChapters = async () => {
      try {
        const chaptersData = await getAllChapters();
        setChapters(chaptersData);
      } catch (err) {
        setError('Failed to load chapters');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchChapters();
  }, []);

  if (loading) {
    return <div>Loading table of contents...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="bg-gray-50 p-4 rounded-lg">
      <h2 className="text-xl font-bold mb-4">Table of Contents</h2>
      <ul className="space-y-2">
        {chapters
          .sort((a, b) => a.position - b.position)
          .map((chapter) => (
            <li key={chapter.id}>
              <Link
                href={`/chapters/${chapter.id}`}
                className="text-blue-600 hover:underline block p-2 hover:bg-gray-100 rounded"
              >
                {chapter.position}. {chapter.title}
              </Link>
            </li>
          ))}
      </ul>
    </div>
  );
};