import React from 'react';
import { useLocation } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import clsx from 'clsx';
import { useLanguage } from '@site/src/contexts/LanguageContext';

const LocaleDropdown = () => {
  const location = useLocation();
  const { i18n } = useDocusaurusContext();
  const { locales, currentLocale, localeConfigs } = i18n;
  const { switchLanguage } = useLanguage();

  const localeLabels = {
    en: 'English',
    ur: 'اردو'
  };

  if (locales.length <= 1) return null;

  // Function to handle language switching without routing
  const handleLanguageSwitch = (locale: string) => {
    switchLanguage(locale as 'en' | 'ur');
  };

  return (
    <div className="dropdown dropdown--hoverable dropdown--right">
      <button
        aria-label="Language"
        className={clsx(
          'navbar__link',
          'dropdown__trigger',
          'button button--secondary button--sm'
        )}
        type="button"
      >
        {localeLabels[currentLocale] || currentLocale} {/* Show current language as button label */}
      </button>
      <ul className="dropdown__menu">
        {locales.map((locale) => (
          <li key={locale}>
            <button
              className="dropdown__link"
              onClick={() => handleLanguageSwitch(locale)}
            >
              {localeLabels[locale] || locale}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LocaleDropdown;
