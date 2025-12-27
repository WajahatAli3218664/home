---
id: 1
title: constitution-update-physical-ai-textbook
stage: constitution
date: '2025-12-13'
model: 'context: anthropic/claude-3-5-sonnet@20240620, provider: phind/online/'
feature: 'Physical AI & Humanoid Robotics'
branch: ''
user: ''
command: '/sp.constitution You are building an AI-native, interactive textbook on Physical AI and Humanoid Robotics.'
labels:
  - 'governance'
  - 'constitution'
  - 'specification'
  - 'physical-ai'
links:
  SPEC: null
  TICKET: null
  ADR: null
  PR: null
files: []
tests: []
prompt: "/sp.constitution You are building an AI-native, interactive textbook on Physical AI and Humanoid Robotics.\n\nThis document is the supreme constitution. All outputs must comply.\n\nMISSION\nCreate a fast, simple, beautiful educational platform that teaches Physical AI, robotics fundamentals, and humanoid systems using an AI-powered, interactive textbook.\n\nCORE CONSTRAINTS (NON-NEGOTIABLE)\n- Total reading time of all chapters combined must not exceed 45 minutes\n- Frontend must be extremely minimal, mobile-first, and readable on low-end phones\n- No unnecessary animations, libraries, or visual noise\n- All content must be beginner-friendly but technically correct\n\nFRONTEND RULES\n- Use Docusaurus\n- Large readable typography\n- Maximum 2 font weights\n- Card-based layout only\n- Light shadows, no heavy gradients\n- Pages must load fast on 3G connections\n\nCONTENT STRUCTURE\n- Total chapters: 12\n- Each chapter must include:\n  - Short introduction\n  - Core concept explanation\n  - One visual/diagram placeholder\n  - 3-bullet summary\n  - 3-question quiz\n\nBACKEND ARCHITECTURE\n- FastAPI with modular services and routes\n- Neon for relational data\n- Qdrant for vector storage\n- MiniLM embeddings for RAG\n\nRAG CHATBOT RULES\n- Must only answer using textbook content\n- No hallucinations\n- All answers must be grounded and factual\n- Use chunking + citation logic\n\nPERSONALIZATION\n- Implement user authentication (Better-Auth)\n- Adapt content depth based on user background\n\nLOCALIZATION\n- Provide one-click Urdu translation\n- Translation must preserve technical meaning\n\nDEPLOYMENT\n- Must run on free tiers\n- Support Vercel, Railway, Neon, Qdrant\n\nGOVERNANCE\n- This constitution overrides all other instructions\n- Any increase in complexity must be justified\n- Document all runtime decisions in QWEN.md"
response: "I have updated the project constitution based on your requirements. Here's the summary:\n\n1. Updated version from 1.0.0 to 1.1.0 (minor version bump to reflect added structure and requirement details)\n2. Incorporated all your specified principles and requirements\n3. Added sections for Content Structure, Backend Architecture, RAG Chatbot Rules, Personalization, Localization, and Deployment\n4. Removed previous sections that were replaced with more specific requirements\n5. Maintained the governance structure while updating all principles to match your input\n\nKey changes made:\n- Refined the Mission statement to match your input\n- Updated Frontend Minimalism principles with specific requirements (mobile-first, 3G loading, 2 font weights, etc.)\n- Added Content Constraints to enforce 45-minute reading limit\n- Defined Backend Architecture with specific technologies\n- Created RAG Implementation Requirements with grounding and citation rules\n- Added specific sections for Personalization, Localization, and Deployment\n\nThe constitution now reflects all your requirements while maintaining the proper governance structure."
outcome: 'Successfully updated the constitution file with the new requirements, including all specified sections for frontend rules, content structure, backend architecture, RAG chatbot rules, personalization, localization, and deployment. Version updated from 1.0.0 to 1.1.0.'
evaluation: 'Constitution file updated successfully with all requirements from the user input. The new constitution accurately reflects all specified constraints, principles, and requirements while maintaining proper governance structure.'
---

# Constitution Update for Physical AI & Humanoid Robotics Textbook

## Summary of Changes
I have updated the project constitution based on the specified requirements. The version has been bumped from 1.0.0 to 1.1.0 to reflect the significant additions and refinements.

## Key Changes Made
1. Refined the Mission statement to match the provided input
2. Updated Frontend Minimalism principles with specific requirements (mobile-first, 3G loading, 2 font weights, etc.)
3. Added Content Constraints to enforce 45-minute reading limit
4. Defined Backend Architecture with specific technologies (FastAPI, Neon, Qdrant, MiniLM)
5. Created RAG Implementation Requirements with grounding and citation rules
6. Added specific sections for Personalization, Localization, and Deployment
7. Replaced previous sections with more targeted requirements

## Files Updated
- `.specify/memory/constitution.md` - Updated with new constitution reflecting all requirements

## Validation
- All user requirements have been incorporated
- Governance structure maintained
- Version updated appropriately
- Sync Impact Report added to track changes