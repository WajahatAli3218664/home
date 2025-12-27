import React from 'react';
import OriginalNavbar from '@theme-original/Navbar';
import LanguageToggle from '@site/src/components/LanguageToggle';

export default function Navbar(props) {
  return (
    <>
      <div className="fixed top-0 right-4 z-50 mt-2">
        <LanguageToggle />
      </div>
      <OriginalNavbar {...props} />
    </>
  );
}