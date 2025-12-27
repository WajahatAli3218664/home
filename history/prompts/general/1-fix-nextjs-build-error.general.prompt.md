---
id: 1
title: Fix Next.js Build Error
stage: general
date: 2025-12-25
surface: agent
model: gpt-4o
feature: none
branch: main
user: user
command: npm run build
labels: ["build", "typescript", "configuration", "docusaurus", "nextjs"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - F:\hackthone-q-4\tsconfig.json
 - F:\hackthone-q-4\pages\index.js
tests:
 - npm run build
---

## Prompt

Resolved Next.js build error caused by TypeScript checking Docusaurus files in the frontend subdirectory. The error was "Cannot find module '@site/src/components/Homepage/HeroSection' or its corresponding type declarations" when running npm run build.

## Response snapshot

Fixed the issue by:

1. Updating tsconfig.json to exclude the "frontend" directory from TypeScript checking, as it contains Docusaurus files with Docusaurus-specific aliases that are not valid in the Next.js project.
2. Fixed a syntax error in pages/index.js where the return statement wasn't properly wrapped in parentheses.

After these changes, the Next.js build command completed successfully.

## Outcome

- ✅ Impact: Fixed build error that was preventing Next.js project from building
- 🧪 Tests: npm run build now passes
- 📁 Files: Modified tsconfig.json and pages/index.js
- 🔁 Next prompts: None needed
- 🧠 Reflection: The project has both a Next.js app in the root and a Docusaurus app in the frontend subdirectory. Needed to ensure TypeScript configuration doesn't mix files from both projects.

## Evaluation notes (flywheel)

- Failure modes observed: TypeScript attempting to check files with framework-specific imports
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A