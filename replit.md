# Dream AI - Premium Adult Companion App

## Overview

Dream AI is a Flask-based adult dating/companion application featuring 6 AI-powered virtual girlfriends with distinct personalities. The app provides uncensored conversations in French with dynamic affection levels that influence AI behavior and photo content.

## Current State

**Status**: Fully functional
**Last Updated**: January 2026

## Features

### Core Features
- 6 AI Companions: Anastasia (35, Russian CEO), Yuki (28, Japanese artist), Sofia (30, Spanish dancer), Emma (25, LA model), Léa (27, Paris nurse), Mia (32, Brazilian fitness coach)
- Affection System: 0-100 scale stored in localStorage, affects AI personality and photo types
- AI Chat: Llama-3.1-70B via DeepInfra for intelligent, uncensored French conversations
- Photo Generation: Promptchan API with affection-based prompts

### UI Features
- Premium dark theme (#0a0a0c background, #e91e63 pink accents)
- Clean design without emojis
- Gallery with gradient cards and "NEW" badges
- Profile page with affection stats
- Chat with timestamps (HH:MM), typing indicators, read receipts
- Fullscreen photo viewing
- Online status with green dot

### Photo System
- Low affection (<30): Elegant dressed photos
- Medium affection (30-75): Lingerie/seductive photos  
- High affection (75+): Nude/intimate photos
- Auto-triggers on keywords: photo, nude, montre, voir, déshabille
- Proactive sending after 5+ messages with high affection

### Profile Photo Gallery
- 4 auto-generated photos per girl on first profile visit
- Photo types: Portrait, Full body, Sexy pose, Lingerie
- Photos saved to localStorage to avoid regeneration
- Fullscreen viewing with prev/next navigation
- Loading spinners during generation
- "Appel Vidéo" button with "Bientôt disponible" toast

## Architecture

### Single-File Structure
- `main.py`: Complete Flask app with embedded HTML/CSS/JavaScript

### External APIs
- **DeepInfra**: meta-llama/Meta-Llama-3.1-8B-Instruct for chat (30s timeout)
- **Pollinations**: Fallback chat API (text.pollinations.ai)
- **Promptchan**: Photo generation via PROMPTCHAN_KEY secret (30s timeout)

### Girl Appearances (Unique)
- Anastasia (35): Platinum blonde, ice blue eyes, Russian
- Yuki (28): Black hair, dark Asian eyes, Japanese
- Sofia (30): Dark brown wavy hair, olive skin, Spanish
- Emma (25): Golden blonde beach waves, green eyes, American
- Léa (27): Brown wavy hair, hazel eyes, French
- Mia (32): Dark curly hair, tan skin, Brazilian

### Data Storage
- localStorage for affection levels and read states
- No database required

## Environment Variables

- `PROMPTCHAN_KEY`: API key for Promptchan image generation

## User Preferences

- All text in French
- No emojis in UI
- Professional adult app aesthetic
- Premium dating app style
