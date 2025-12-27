// frontend/src/components/Chapter/TranslateButton.jsx
import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import apiClient from '../../utils/api';
import LoadingSpinner from '../UI/LoadingSpinner';
import ErrorMessage from '../UI/ErrorMessage';

const TranslateButton = ({
  chapterId,
  chapterContent,
  onContentUpdate,
  isAuthenticated: isAuthenticatedProp,  // Accept isAuthenticated as prop
  className = ""
}) => {
  const { isAuthenticated: isAuthenticatedContext } = useAuth();
  // Use prop value if provided, otherwise use context value
  const isAuthenticated = isAuthenticatedProp !== undefined ? isAuthenticatedProp : isAuthenticatedContext;

  const [isTranslating, setIsTranslating] = useState(false);
  const [error, setError] = useState(null);

  const handleClick = async () => {
    if (!isAuthenticated) {
      // Redirect to signin page if not authenticated
      window.location.href = '/signin';
      return;
    }

    if (!chapterContent) {
      setError("No chapter content available for translation");
      return;
    }

    setIsTranslating(true);
    setError(null);

    try {
      const response = await apiClient.translateChapter({
        chapter_content: chapterContent
      });

      if (response.success && response.translated_content) {
        if (onContentUpdate) {
          onContentUpdate(response.translated_content, 'translated');
        }
      } else {
        setError("Failed to get translated content from server");
      }
    } catch (err) {
      setError(err.message || "Failed to translate chapter content");
    } finally {
      setIsTranslating(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <button
        onClick={() => window.location.href = '/signin'}
        className={`px-4 py-2 bg-yellow-500 hover:bg-yellow-600 text-white rounded-md ${className}`}
      >
        Sign In to Translate
      </button>
    );
  }

  return (
    <div className="translate-component">
      {error && <ErrorMessage message={error} />}

      <button
        onClick={handleClick}
        disabled={isTranslating}
        className={`
          px-4 py-2 rounded-md font-medium transition-colors
          ${isTranslating
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-green-600 hover:bg-green-700 text-white'
          } ${className}
        `}
      >
        {isTranslating ? (
          <div className="flex items-center">
            <LoadingSpinner size="small" />
            <span className="ml-2">Translating...</span>
          </div>
        ) : (
          'اردو میں پڑھیں'
        )}
      </button>
    </div>
  );
};

export default TranslateButton;