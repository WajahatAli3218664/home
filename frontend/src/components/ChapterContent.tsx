import React, { useState, useEffect } from 'react';
import { ReadingTimeEstimate } from '../ReadingTimeEstimate';
import { addIdsToHeadings } from '../utils/headingProcessor';
import { useLanguage } from '../contexts/LanguageContext';
import { translateContentBlock } from '../services/translationService';

interface ChapterContentProps {
  content: string;
  showReadingTime?: boolean;
  chapterTitle?: string;
  chapterNumber?: number;
  duration?: string;
  objectives?: string[];
  prerequisites?: string[];
}

export const ChapterContent: React.FC<ChapterContentProps> = ({
  content,
  showReadingTime = true,
  chapterTitle = '',
  chapterNumber,
  duration,
  objectives,
  prerequisites
}) => {
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [backgroundLevel, setBackgroundLevel] = useState<'beginner' | 'intermediate' | 'advanced'>('intermediate');
  const [translatedContent, setTranslatedContent] = useState<string>(content);
  const [translatedTitle, setTranslatedTitle] = useState<string>(chapterTitle);
  const [isTranslating, setIsTranslating] = useState(false);
  const { currentLanguage, t } = useLanguage();

  // Function to simulate content personalization
  const togglePersonalization = () => {
    setIsPersonalized(!isPersonalized);
  };

  // Handle translation when language changes
  useEffect(() => {
    const handleTranslation = async () => {
      if (currentLanguage === 'en') {
        // Switch back to original content
        setTranslatedContent(content);
        setTranslatedTitle(chapterTitle);
      } else {
        // Translate content to Urdu
        setIsTranslating(true);
        try {
          // Translate content
          const translatedContentResult = await translateContentBlock(content, currentLanguage);
          setTranslatedContent(translatedContentResult);

          // Translate title
          const translatedTitleResult = await translateContentBlock(chapterTitle, currentLanguage);
          setTranslatedTitle(translatedTitleResult);
        } catch (error) {
          console.error('Translation error:', error);
          // Fallback to original content if translation fails
          setTranslatedContent(content);
          setTranslatedTitle(chapterTitle);
        } finally {
          setIsTranslating(false);
        }
      }
    };

    handleTranslation();
  }, [currentLanguage, content, chapterTitle]);

  // Add direction attribute based on language
  const contentDirection = currentLanguage === 'ur' ? 'rtl' : 'ltr';
  const contentLang = currentLanguage === 'ur' ? 'ur' : 'en';

  return (
    <div className="chapter-card bg-white rounded-xl shadow-sm p-6" dir={contentDirection}>
      <div className="flex justify-between items-start mb-6">
        <div>
          {chapterNumber && <div className="text-sm font-semibold text-blue-600">CHAPTER {chapterNumber}</div>}
          <h1 className="text-2xl md:text-3xl font-bold text-gray-900 mt-1" lang={contentLang}>
            {isTranslating ? chapterTitle : translatedTitle}
          </h1>
        </div>
        <div className="flex space-x-2">
          <select
            value={backgroundLevel}
            onChange={(e) => setBackgroundLevel(e.target.value as any)}
            className="border rounded px-2 py-1 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
          <button
            onClick={togglePersonalization}
            className="bg-blue-100 hover:bg-blue-200 text-blue-800 text-sm px-3 py-1 rounded transition"
          >
            {isPersonalized ? 'Standard' : 'Personalize'}
          </button>
        </div>
      </div>

      {(objectives || prerequisites || duration) && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8 p-4 bg-blue-50 rounded-lg">
          {objectives && (
            <div>
              <h3 className="font-semibold text-blue-800 mb-2">Learning Objectives</h3>
              <ul className="text-sm text-gray-700 list-disc pl-5 space-y-1">
                {objectives.map((obj, i) => <li key={i}>{obj}</li>)}
              </ul>
            </div>
          )}
          {prerequisites && (
            <div>
              <h3 className="font-semibold text-green-800 mb-2">Prerequisites</h3>
              <ul className="text-sm text-gray-700 list-disc pl-5 space-y-1">
                {prerequisites.map((prereq, i) => <li key={i}>{prereq}</li>)}
              </ul>
            </div>
          )}
          {duration && (
            <div>
              <h3 className="font-semibold text-purple-800 mb-2">Duration</h3>
              <p className="text-sm text-gray-700">{duration}</p>
            </div>
          )}
        </div>
      )}

      <div className="flex flex-wrap justify-between items-center mb-6 gap-4">
        {showReadingTime && <ReadingTimeEstimate content={currentLanguage === 'en' ? content : translatedContent} />}
        <div className="flex space-x-2 ml-auto">
          <button className="text-sm bg-gray-100 hover:bg-gray-200 text-gray-800 px-3 py-1 rounded transition flex items-center">
            <span className="mr-1">📤</span> Share
          </button>
          <button className="text-sm bg-gray-100 hover:bg-gray-200 text-gray-800 px-3 py-1 rounded transition flex items-center">
            <span className="mr-1">🔖</span> Bookmark
          </button>
          <button className="text-sm bg-gray-100 hover:bg-gray-200 text-gray-800 px-3 py-1 rounded transition flex items-center">
            <span className="mr-1">📥</span> Download
          </button>
        </div>
      </div>

      <div className={`prose prose-lg max-w-none ${currentLanguage === 'ur' ? 'rtl' : ''}`} dir={contentDirection}>
        <div
          className="chapter-content"
          lang={contentLang}
          dangerouslySetInnerHTML={{ __html: addIdsToHeadings(currentLanguage === 'en' ? content : translatedContent) }}
        />
      </div>

      <div className="mt-10 pt-6 border-t border-gray-200 flex flex-col sm:flex-row justify-between items-center gap-4">
        <button className="w-full sm:w-auto px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition flex items-center justify-center">
          <span className="mr-2">←</span>Previous Chapter
        </button>
        <button className="w-full sm:w-auto px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition flex items-center justify-center">
          Next Chapter<span className="ml-2">→</span>
        </button>
      </div>
    </div>
  );
};