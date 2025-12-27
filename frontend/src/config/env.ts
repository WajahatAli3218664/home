// Environment Configuration for Frontend

// Default values that can be overridden by environment variables
const config = {
  BACKEND_API_URL: process.env.BACKEND_API_URL || 'http://localhost:8000',
  CONTEXT7_API_URL: process.env.CONTEXT7_API_URL || 'https://api.context7.com',
  APP_NAME: process.env.APP_NAME || 'Textbook Generator',
  APP_DESCRIPTION: process.env.APP_DESCRIPTION || 'An AI-powered textbook generation platform'
};

export default config;