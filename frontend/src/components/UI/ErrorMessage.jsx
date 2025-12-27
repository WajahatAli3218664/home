// frontend/src/components/UI/ErrorMessage.jsx
import React from 'react';

const ErrorMessage = ({ message, onClose, variant = 'error' }) => {
  const variantStyles = {
    error: {
      container: 'bg-red-50 border-l-4 border-red-500 p-4',
      title: 'text-red-800 text-sm font-medium',
      message: 'text-red-700 text-sm mt-1',
      closeBtn: 'text-red-500 hover:text-red-700'
    },
    warning: {
      container: 'bg-yellow-50 border-l-4 border-yellow-500 p-4',
      title: 'text-yellow-800 text-sm font-medium',
      message: 'text-yellow-700 text-sm mt-1',
      closeBtn: 'text-yellow-500 hover:text-yellow-700'
    },
    info: {
      container: 'bg-blue-50 border-l-4 border-blue-500 p-4',
      title: 'text-blue-800 text-sm font-medium',
      message: 'text-blue-700 text-sm mt-1',
      closeBtn: 'text-blue-500 hover:text-blue-700'
    }
  };

  const styles = variantStyles[variant];

  return (
    <div className={styles.container} role="alert">
      <div className="flex justify-between items-start">
        <div>
          <h3 className={styles.title}>{
            variant === 'error' ? 'Error' : 
            variant === 'warning' ? 'Warning' : 
            'Information'
          }</h3>
          <p className={styles.message}>{message}</p>
        </div>
        {onClose && (
          <button 
            onClick={onClose}
            className={`ml-4 ${styles.closeBtn} focus:outline-none`}
            aria-label="Close"
          >
            <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
};

export default ErrorMessage;