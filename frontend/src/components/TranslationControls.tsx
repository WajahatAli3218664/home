import React, { useState } from 'react';

interface TranslationControlsProps {
  onTranslate: (targetLanguage: string) => void;
  isTranslating: boolean;
  currentLanguage: string;
}

export const TranslationControls: React.FC<TranslationControlsProps> = ({
  onTranslate,
  isTranslating,
  currentLanguage
}) => {
  const [selectedLanguage, setSelectedLanguage] = useState<string>('ur'); // Default to Urdu
  
  const handleTranslateClick = () => {
    onTranslate(selectedLanguage);
  };

  return (
    <div className="flex items-center space-x-4 p-4 bg-blue-50 rounded-lg">
      <label htmlFor="language-select" className="text-gray-700">Translate to:</label>
      <select
        id="language-select"
        value={selectedLanguage}
        onChange={(e) => setSelectedLanguage(e.target.value)}
        className="border rounded px-2 py-1"
      >
        <option value="ur">Urdu</option>
        <option value="es">Spanish</option>
        <option value="fr">French</option>
        {/* Add more languages as needed */}
      </select>
      <button
        onClick={handleTranslateClick}
        disabled={isTranslating}
        className={`px-4 py-2 rounded ${
          isTranslating 
            ? 'bg-gray-400 cursor-not-allowed' 
            : 'bg-blue-600 text-white hover:bg-blue-700'
        }`}
      >
        {isTranslating ? 'Translating...' : 'Translate'}
      </button>
      {currentLanguage !== 'en' && (
        <button
          onClick={() => onTranslate('en')}
          className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
        >
          Switch back to English
        </button>
      )}
    </div>
  );
};