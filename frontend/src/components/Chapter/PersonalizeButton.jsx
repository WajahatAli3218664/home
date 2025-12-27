// frontend/src/components/Chapter/PersonalizeButton.jsx
import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import apiClient from '../../utils/api';
import LoadingSpinner from '../UI/LoadingSpinner';
import ErrorMessage from '../UI/ErrorMessage';

const PersonalizeButton = ({
  chapterId,
  chapterContent,
  onContentUpdate,
  isAuthenticated: isAuthenticatedProp,  // Accept isAuthenticated as prop
  className = ""
}) => {
  const { isAuthenticated: isAuthenticatedContext } = useAuth();
  // Use prop value if provided, otherwise use context value
  const isAuthenticated = isAuthenticatedProp !== undefined ? isAuthenticatedProp : isAuthenticatedContext;

  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);

  const handleClick = async () => {
    if (!isAuthenticated) {
      // Redirect to signin page if not authenticated
      window.location.href = '/signin';
      return;
    }

    if (!chapterContent) {
      setError("No chapter content available for personalization");
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      const response = await apiClient.personalizeChapter({
        chapter_id: chapterId,
        chapter_content: chapterContent
      });

      if (response.success && response.personalized_content) {
        if (onContentUpdate) {
          onContentUpdate(response.personalized_content, 'personalized');
        }
      } else {
        setError("Failed to get personalized content from server");
      }
    } catch (err) {
      setError(err.message || "Failed to personalize chapter content");
    } finally {
      setIsProcessing(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <button
        onClick={() => window.location.href = '/signin'}
        className={`px-4 py-2 bg-yellow-500 hover:bg-yellow-600 text-white rounded-md ${className}`}
      >
        Sign In to Personalize
      </button>
    );
  }

  return (
    <div className="personalize-component">
      {error && <ErrorMessage message={error} />}

      <button
        onClick={handleClick}
        disabled={isProcessing}
        className={`
          px-4 py-2 rounded-md font-medium transition-colors
          ${isProcessing
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700 text-white'
          } ${className}
        `}
      >
        {isProcessing ? (
          <div className="flex items-center">
            <LoadingSpinner size="small" />
            <span className="ml-2">Personalizing...</span>
          </div>
        ) : (
          'Personalize Chapter'
        )}
      </button>
    </div>
  );
};

export default PersonalizeButton;