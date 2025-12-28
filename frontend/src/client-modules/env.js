// Client module to make environment variables available to the browser
// This file is referenced in docusaurus.config.js

// Set a global variable with the backend URL
if (typeof window !== 'undefined') {
  window.REACT_APP_API_BASE_URL = 'https://effective-cod-5g46g9pww5pxc7g96-8000.app.github.dev';
}