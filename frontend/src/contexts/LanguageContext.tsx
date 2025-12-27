import React, { createContext, useContext, ReactNode, useState, useEffect } from 'react';

interface LanguageContextType {
  currentLanguage: string;
  switchLanguage: (lang: 'en' | 'ur') => void;
  t: (key: string) => string; // Translation function for static UI elements
}

const translations = {
  en: {
    switchToUrdu: 'Switch to Urdu',
    switchToEnglish: 'Switch to English',
    contentTranslatedToUrdu: 'Content has been translated to Urdu',
    contentTranslatedToEnglish: 'Content has been translated to English',
  },
  ur: {
    switchToUrdu: 'اردو میں تبدیل کریں',
    switchToEnglish: 'انگریزی میں تبدیل کریں',
    contentTranslatedToUrdu: 'مواد اردو میں ترجمہ کر دیا گیا ہے',
    contentTranslatedToEnglish: 'مواد انگریزی میں ترجمہ کر دیا گیا ہے',
  }
};

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState<'en' | 'ur'>('en');

  useEffect(() => {
    // Check for saved language preference in localStorage
    const savedLanguage = localStorage.getItem('preferredLanguage');
    if (savedLanguage === 'en' || savedLanguage === 'ur') {
      setCurrentLanguage(savedLanguage);
    }
  }, []);

  const switchLanguage = (lang: 'en' | 'ur') => {
    setCurrentLanguage(lang);
    localStorage.setItem('preferredLanguage', lang);
  };

  const t = (key: string): string => {
    // @ts-ignore - we're using dynamic key access safely
    return translations[currentLanguage][key] || key;
  };

  return (
    <LanguageContext.Provider value={{ currentLanguage, switchLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = (): LanguageContextType => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};