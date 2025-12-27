import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';

const LanguageToggle: React.FC = () => {
  const { currentLanguage, switchLanguage, t } = useLanguage();

  const handleLanguageChange = () => {
    const newLanguage = currentLanguage === 'en' ? 'ur' : 'en';
    switchLanguage(newLanguage);
  };

  return (
    <button
      onClick={handleLanguageChange}
      className="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-500 to-purple-600 text-white hover:from-blue-600 hover:to-purple-700 transition-all duration-300 shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
      aria-label={currentLanguage === 'en' ? 'Switch to Urdu' : 'Switch to English'}
    >
      {currentLanguage === 'en' ? (
        <span className="font-semibold">اُردو</span>
      ) : (
        <span className="font-semibold">English</span>
      )}
    </button>
  );
};

export default LanguageToggle;