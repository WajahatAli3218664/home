import React from 'react';

interface ChapterProps {
  title: string;
  content: string;
  learningObjectives: string[];
  prerequisites: string[];
  quizQuestions?: any[];
  onProgressUpdate?: (progress: number) => void;
}

export const ChapterComponent: React.FC<ChapterProps> = ({
  title,
  content,
  learningObjectives,
  prerequisites,
  quizQuestions = [],
  onProgressUpdate
}) => {
  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{title}</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="bg-blue-50 p-4 rounded-lg">
            <h2 className="font-semibold text-blue-800 mb-2">Learning Objectives</h2>
            <ul className="list-disc pl-5 space-y-1">
              {learningObjectives.map((objective, index) => (
                <li key={index} className="text-gray-700">{objective}</li>
              ))}
            </ul>
          </div>

          <div className="bg-green-50 p-4 rounded-lg">
            <h2 className="font-semibold text-green-800 mb-2">Prerequisites</h2>
            <ul className="list-disc pl-5 space-y-1">
              {prerequisites.map((prereq, index) => (
                <li key={index} className="text-gray-700">{prereq}</li>
              ))}
            </ul>
          </div>
        </div>
      </header>

      <div className="prose prose-lg max-w-none mb-8">
        <div
          className="chapter-content"
          dangerouslySetInnerHTML={{ __html: content }}
        />
      </div>

      {quizQuestions.length > 0 && (
        <div className="mt-12 pt-8 border-t border-gray-200">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Knowledge Check</h2>
          <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
            <p className="text-gray-700">Knowledge check functionality not available in this version.</p>
          </div>
        </div>
      )}

      <div className="mt-8 pt-4 border-t border-gray-100 flex justify-between">
        <button className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition">
          ← Previous Chapter
        </button>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
          Next Chapter →
        </button>
      </div>
    </div>
  );
};