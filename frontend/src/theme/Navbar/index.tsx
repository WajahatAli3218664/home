import React from 'react';
import OriginalNavbar from '@theme-original/Navbar';
import LanguageToggle from '@site/src/components/LanguageToggle';

export default function Navbar(props) {
  React.useEffect(() => {
    const handleNavClick = (e) => {
      const target = e.target.closest('a');
      if (target) {
        const text = target.textContent.trim();
        if (text === 'Sign In') {
          e.preventDefault();
          e.stopPropagation();
          setTimeout(() => {
            if (window.openLogin) window.openLogin();
          }, 100);
        }
        if (text === 'Sign Up') {
          e.preventDefault();
          e.stopPropagation();
          setTimeout(() => {
            if (window.openSignup) window.openSignup();
          }, 100);
        }
      }
    };
    
    document.addEventListener('click', handleNavClick, true);
    return () => document.removeEventListener('click', handleNavClick, true);
  }, []);

  return (
    <>
      <div className="fixed top-0 right-4 z-50 mt-2">
        <LanguageToggle />
      </div>
      <OriginalNavbar {...props} />
    </>
  );
}