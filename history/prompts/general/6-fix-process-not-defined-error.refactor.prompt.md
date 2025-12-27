---
id: "6"
title: "Fix Process Not Defined Error"
stage: "refactor"
date: "2025-12-19"
model: "Qwen"
feature: "none"
branch: "main"
user: "user"
command: "edit authClient.js"
labels: ["frontend", "auth", "bug-fix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "F:\\hackthone-q-4\\frontend\\src\\services\\authClient.js"
tests: []
---

# Fix Process Not Defined Error

## User Prompt

Uncaught ReferenceError: process is not defined
    at eval (authClient.js:8:1)
    at ./src/services/authClient.js (main.js:2617:1)
    at __webpack_require__ (runtime~main.js:34:32)
    at fn (runtime~main.js:321:21)
    at eval (AuthContext.jsx:9:78)
    at ./src/contexts/AuthContext.jsx (main.js:2601:1)
    at __webpack_require__ (runtime~main.js:34:32)
    at fn (runtime~main.js:321:21)
    at eval (Root.jsx:7:79)
    at ./src/theme/Root.jsx (main.js:2673:1)

## Response Summary

Fixed the "process is not defined" error in authClient.js by updating how environment variables are accessed. The issue occurred because the code was trying to access Node.js specific process object in the browser environment. 

The fix replaces:
```javascript
baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000'
```

With:
```javascript
baseURL:
  (typeof window !== 'undefined' && window.REACT_APP_API_BASE_URL) ||
  (typeof process !== 'undefined' && process.env.REACT_APP_API_BASE_URL) ||
  'http://localhost:8000'
```

This change makes the code work in both browser and server environments by checking for the appropriate environment before accessing environment variables. The fix allows the Docusaurus frontend application to run without the JavaScript error.