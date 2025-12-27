# Quickstart: Qdrant Search Interface

## Overview
This guide explains how to integrate and use the Qdrant search interface component in your React application.

## Prerequisites
- React 17+ installed in your project
- Backend API running at `http://localhost:8000` (or configured endpoint)
- `/retrieve` endpoint available with the expected API contract

## Installation
The component is self-contained and doesn't require any additional dependencies beyond React and standard browser APIs.

1. Copy the component file (`QdrantSearch.jsx`) to your components directory
2. Copy the CSS file (`QdrantSearch.css`) to your styles directory
3. Import and use the component as shown below

## Basic Usage

```jsx
import React from 'react';
import QdrantSearch from './components/QdrantSearch';

function App() {
  return (
    <div className="App">
      <QdrantSearch backendUrl="http://localhost:8000" />
    </div>
  );
}

export default App;
```

## Props

### backendUrl (optional)
- **Type**: String
- **Default**: `"http://localhost:8000"`
- **Description**: Base URL of your backend API

## Backend API Contract

The component expects your backend to provide the following endpoint:

- **URL**: `{backendUrl}/retrieve`
- **Method**: POST
- **Request Content-Type**: `application/json`
- **Request Body**: `{"query": "user question"}`
- **Response Content-Type**: `application/json`
- **Response Format**: `{"results": [{"content": "...", "source": "...", "score": 0.92}, ...]}`

## Expected Response Format

```json
{
  "results": [
    {
      "content": "Content snippet here...",
      "source": "https://example.com/source-url",
      "score": 0.92
    },
    {
      "content": "Another content snippet...",
      "source": "https://example.com/another-source",
      "score": 0.78
    }
  ]
}
```

## Styling

The component comes with minimal default styling, but you can customize it by:
1. Modifying the included CSS file
2. Overriding styles with your own CSS classes
3. Using CSS variables if needed

## Local Development

To test the component locally:

1. Start your backend API
2. Run your React application
3. Navigate to the page containing the search component
4. Enter queries and verify that results appear correctly

## Troubleshooting

### Component not making requests
- Verify that your backend is running at the specified URL
- Check browser console for CORS errors
- Verify that the `/retrieve` endpoint is available

### No results showing
- Confirm that your backend is returning properly formatted JSON
- Check browser network tab to verify request/response format

### Styling issues
- Verify that CSS file is properly linked
- Check for CSS conflicts with existing styles