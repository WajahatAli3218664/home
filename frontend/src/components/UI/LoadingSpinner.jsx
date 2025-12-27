// frontend/src/components/UI/LoadingSpinner.jsx
import React from 'react';

const LoadingSpinner = ({ size = 'medium', message = 'Loading...', centered = false }) => {
  const sizeClasses = {
    small: 'w-6 h-6',
    medium: 'w-10 h-10',
    large: 'w-16 h-16'
  };

  const spinnerClass = `animate-spin rounded-full border-4 border-t-transparent border-gray-300 ${sizeClasses[size]} ${
    centered ? 'mx-auto' : ''
  }`;

  return (
    <div className={`flex flex-col items-center justify-center ${centered ? 'my-8' : ''}`}>
      <div className={spinnerClass}></div>
      {message && (
        <p className="mt-2 text-gray-600 text-sm">
          {message}
        </p>
      )}
    </div>
  );
};

export default LoadingSpinner;