---
id: "7"
title: "Implement Urdu Translation Feature"
stage: "green"
date: "2025-12-19"
model: "Qwen"
feature: "book-project-fixes"
branch: "001-book-project-fixes"
user: "user"
command: "implement translation"
labels: ["frontend", "translation", "urdu", "i18n"]
links:
  spec: "../001-book-project-fixes/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "F:\\hackthone-q-4\\frontend\\src\\contexts\\LanguageContext.tsx"
  - "F:\\hackthone-q-4\\frontend\\src\\components\\LanguageToggle.tsx"
  - "F:\\hackthone-q-4\\frontend\\src\\theme\\Root.jsx"
  - "F:\\hackthone-q-4\\frontend\\src\\theme\\Navbar\\index.tsx"
  - "F:\\hackthone-q-4\\frontend\\src\\css\\custom.css"
  - "F:\\hackthone-q-4\\frontend\\src\\components\\ChapterContent.tsx"
  - "F:\\hackthone-q-4\\frontend\\src\\pages\\sample-chapter.tsx"
tests: []
---

# Implement Urdu Translation Feature

## User Prompt

openai agent  k use karo or urdu par click karny sa new rorute nh balkay book k complete text urdu ma convert karo or english par click karny sa complete english ma ho jay..

## Response Summary

Successfully implemented a global language translation feature that converts the entire book content between English and Urdu. When the user clicks the "Urdu" button, the entire book content is translated to Urdu with right-to-left (RTL) layout support. When the user clicks the "English" button, the content switches back to English with left-to-right (LTR) layout.

Key implementations:

1. Created LanguageContext to manage global language state
2. Implemented LanguageToggle component that appears in the navbar
3. Updated Root.jsx to include the LanguageProvider
4. Added RTL CSS support for Urdu text display
5. Modified ChapterContent component to translate content based on the selected language
6. Updated sample chapter page to support language switching
7. Added translation API integration using the existing translation service

The translation is now global - clicking the language toggle in the navbar will translate all book content across the entire site, not just individual pages. The implementation includes proper RTL styling for Urdu content and maintains a consistent user experience.