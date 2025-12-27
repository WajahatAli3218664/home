---
id: "1"
stage: "constitution"
title: "project-constitution-update"
date_iso: "2025-12-09"
surface: "agent"
model: "Qwen"
feature: "none"
branch: "main"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "project-setup", "governance"]
links: {"spec": null, "ticket": null, "adr": null, "pr": null}
files_yaml: []
tests_yaml: []
outcome: "Successfully updated the project constitution to reflect the Physical AI & Humanoid Robotics Book with Integrated RAG Chatbot project specifications."
evaluation: "The constitution was successfully updated with all required project details, principles, deliverables, and governance information. The Sync Impact Report was included, and all templates were verified for consistency."
---

# Prompt

```
/sp.constitution Project:

Physical AI & Humanoid Robotics Book with Integrated RAG Chatbot

1. Mission

Build a fully AI-native, interactive, intelligent textbook that teaches Physical AI, robotics fundamentals, and humanoid systems.
The product must be fast, simple, beautiful, and feel like a real AI-powered education system.

2. Core Deliverables

A Docusaurus-based interactive textbook with 12 short, clean, modern chapters.

A fully functional RAG chatbot that answers questions only from the book content.

User authentication (signup/login) using Better-Auth.

Personalized chapter content based on user background.

One-click Urdu translation for every chapter.

Auto-generated summaries, quizzes, and learning boosters for each chapter.

3. Success Criteria

Clean UI, fast loading, mobile-friendly.

Entire book readable in 45 minutes total.

RAG answers accurate, cited, and grounded.

Personalization visibly improves text quality.

Urdu translation high-quality and fast.

Fully deployed:

Frontend → Vercel

Backend → Railway

Vectors → Qdrant

Database → Neon

90-second demo successfully recorded.

4. Non-Goals

No extra animations beyond minimal helpful motion.

No long chapters — must remain short, simple, clear.

No complex robotics code — only educational content.

5. Architecture Principles

Keep frontend extremely simple and readable.

Keep backend modular (FastAPI + services + routes).

All data stored cleanly in Neon + Qdrant.

Use reusable agent skills for bonus scoring.

6. User Stories (Prioritized)

As a learner, I want to read the textbook smoothly.

As a learner, I want to ask the chatbot questions.

As a learner, I want personalized content.

As a learner, I want Urdu translation.

As a learner, I want summaries & quizzes.

As a tech student, I want clean architecture and deployment.

7. Constraints

Must work on free tiers (Qdrant, Neon).

Must deploy within 90 seconds on the demo.

Must support low-end devices, especially phones.

Must avoid heavy dependencies and unnecessary complexity.

8. Risks & Mitigation
RiskMitigation
RAG low accuracyBetter chunking + MiniLM embeddings
High token usageImplement in phases + caching
User confusionKeep UI minimal and guided
Backend errorsHealth checks + logs + retries
9. Definition of Done

All 12 chapters visible and readable.

Chatbot fully functional with grounded answers.

Auth + personalization + translation working.

Summaries + quizzes generated per chapter.

Deployment URLs working and stable.

90-second demo recorded.
```

# Response

```
I've created a comprehensive updated constitution document that incorporates the project specification provided by the user:

[Constitution content with Sync Impact Report, Mission, Core Principles, Core Deliverables, Success Criteria, Non-Goals, User Stories, Constraints, Architecture Principles, Risk & Mitigation table, Definition of Done, and Governance section]
```