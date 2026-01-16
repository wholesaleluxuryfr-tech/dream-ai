# Replit.md

## Overview

This is a Flask-based API backend for an adult dating/chat application. The application provides AI-powered virtual companions with distinct personalities. Each companion has predefined characteristics (name, age, bio, appearance, personality) and uses an external AI API (PromptChan) to generate conversational responses.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask** serves as the web framework for handling HTTP requests
- Single-file architecture (`main.py`) containing all application logic
- RESTful API design for client communication

### Virtual Companion System
- Companions are defined as a dictionary (`GIRLS`) with static profile data
- Each companion has:
  - Identity info (name, age, tagline, bio)
  - Visual description for image generation (`appearance`)
  - Personality prompt for AI responses (`system`)
- Profiles are hardcoded rather than database-stored

### AI Integration Pattern
- External API integration with PromptChan service for generating AI responses
- API key stored in environment variable (`PROMPTCHAN_KEY`)
- System prompts define each companion's personality and behavior

### Design Decisions
- **Stateless design**: No database or persistent storage currently implemented
- **Monolithic structure**: All logic in single file for simplicity
- **Environment-based configuration**: API keys via environment variables

## External Dependencies

### Third-Party Services
- **PromptChan API**: External AI service for generating chat responses and potentially images
  - Authentication via API key (`PROMPTCHAN_KEY` environment variable)
  - Used for conversational AI and image generation features

### Python Libraries
- **Flask**: Web framework for API endpoints
- **Requests**: HTTP client for external API calls
- **JSON**: Data serialization (standard library)
- **OS**: Environment variable access (standard library)