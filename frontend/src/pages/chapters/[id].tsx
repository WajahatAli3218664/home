import React, { useEffect, useState } from 'react';
import { useLocation } from '@docusaurus/router';
import { ChapterContent } from '../../components/ChapterContent';
import { ChapterNavigation } from '../../components/ChapterNavigation';
import { TableOfContents } from '../../components/TableOfContents';
import { ChatComponent } from '../../components/ChatComponent';
import { getChapterById } from '../../services/chapterService';
import { Chapter } from '../../types/chapter';

const ChapterPage = () => {
  const location = useLocation();
  // Extract the chapter ID from the URL path
  const chapterIdFromUrl = location.pathname.match(/\/chapters\/(\d+)/)?.[1];
  const [chapter, setChapter] = useState<Chapter | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchChapter = async () => {
      try {
        if (chapterIdFromUrl) {
          const chapterId = parseInt(chapterIdFromUrl as string, 10);
          const chapterData = await getChapterById(chapterId);
          setChapter(chapterData);
        }
      } catch (err) {
        setError('Failed to load chapter');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (chapterIdFromUrl) {
      fetchChapter();
    }
  }, [chapterIdFromUrl]);

  if (loading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>;
  }

  if (error || !chapter) {
    return <div className="flex justify-center items-center h-screen">Error: {error || 'Chapter not found'}</div>;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-8">
          <h1 className="text-3xl font-bold mb-6">{chapter.title}</h1>
          <ChapterContent content={chapter.content} />
          <ChapterNavigation currentChapterId={chapter.id} />
        </div>

        <div className="lg:col-span-4 space-y-8">
          <div className="sticky top-4">
            <TableOfContents />
          </div>

          <div>
            <h2 className="text-xl font-semibold mb-4">Ask AI Assistant</h2>
            <ChatComponent chapterId={chapter.id} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChapterPage;