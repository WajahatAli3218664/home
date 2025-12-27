// Client module to make environment variables available to the browser
// This file is referenced in docusaurus.config.js

// Set a global variable with the backend URL
if (typeof window !== 'undefined') {
  // Use window.ENV which can be set by a script tag or provided by Docusaurus
  window.REACT_APP_API_BASE_URL = window.ENV?.REACT_APP_API_BASE_URL ||
                                window.env?.REACT_APP_API_BASE_URL ||
                                window.REACT_APP_API_BASE_URL ||
                                'http://localhost:8000';
}