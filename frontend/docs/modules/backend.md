---
sidebar_position: 3
---

# Backend Module

## Overview
The `backend` directory contains the FastAPI-based backend for the Physical AI & Humanoid Robotics textbook platform. It provides all the API endpoints and business logic.

## Contents
- `src/` - Main source code for the backend
  - `api/` - API route definitions
  - `auth/` - Authentication and authorization
  - `config/` - Configuration settings
  - `middleware/` - Request/response middleware
  - `models/` - Database models (SQLAlchemy)
  - `schemas/` - Pydantic schemas for API validation
  - `services/` - Business logic services
  - `utils/` - Utility functions
- `main.py` - Main application entry point
- `requirements.txt` - Python dependencies

## Key Services
- RAG (Retrieval Augmented Generation) service for the AI chatbot
- Chapter content management
- Learning materials generation
- User authentication and personalization
- Translation services

## Purpose
The backend handles all server-side logic, database interactions, and provides APIs for the Docusaurus frontend.