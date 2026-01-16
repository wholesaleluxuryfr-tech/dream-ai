# Dream AI - Premium Adult Companion App

## Overview

Dream AI is a Flask-based adult dating application featuring 15 diverse AI-powered virtual girlfriends with uncensored French conversations. The app uses a Tinder-style swipe matching system with realistic match probabilities, dynamic affection levels, and AI-generated photos.

## Current State

**Status**: Fully functional
**Last Updated**: January 2026

## Features

### Core Features
- 15 AI Companions with diverse ethnicities:
  - Anastasia (35, Russian CEO) - 60% match chance
  - Yuki (28, Japanese artist) - 80% match chance
  - Sofia (30, Spanish dancer) - 65% match chance
  - Emma (25, LA model) - 50% match chance
  - Léa (27, Paris nurse) - 85% match chance
  - Mia (32, Brazilian fitness coach) - 75% match chance
  - Zara (24, Moroccan student) - 40% match chance
  - Ingrid (29, Swedish photographer) - 70% match chance
  - Priya (26, Indian developer) - 80% match chance
  - Mei (31, Chinese businesswoman) - 55% match chance
  - Giulia (33, Italian chef) - 72% match chance
  - Olivia (22, British actress) - 45% match chance
  - Awa (28, Senegalese model) - 68% match chance
  - Valentina (29, Colombian dancer) - 78% match chance
  - Hana (25, Korean K-pop backup dancer) - 45% match chance

### Login/Signup System
- Name and age input
- Age verification (18+)
- User data saved to localStorage
- User name displayed in header

### Tinder-Style Swipe System
- Swipe cards with girl info (name, age, location, bio)
- X button to pass, ♥ button to like
- Variable match probabilities per girl (40-85%)
- "C'est un Match!" animation with hearts
- "Elle n'a pas matché avec toi" notification for failed matches

### Tab Navigation
- "Découvrir" tab: Swipe through profiles
- "Matchs" tab: View matched profiles grid
- Chat restricted to matched girls only

### Affection System
- 0-100 scale stored in localStorage
- Affects AI personality and photo types
- Increases based on interaction

### Photo System
- Low affection (<30): Elegant dressed photos
- Medium affection (30-75): Lingerie/seductive photos  
- High affection (75+): Nude/intimate photos
- Auto-triggers on keywords: photo, nude, montre, voir, déshabille
- 4 auto-generated photos per girl on profile visit

### UI Features
- Premium dark theme (#0a0a0c background, #e91e63 pink accents)
- Clean design without emojis
- Profile page with affection stats
- Chat with timestamps (HH:MM), typing indicators, read receipts
- Fullscreen photo viewing with navigation

## Architecture

### Single-File Structure
- `main.py`: Complete Flask app with embedded HTML/CSS/JavaScript

### External APIs
- **DeepInfra**: meta-llama/Meta-Llama-3.1-8B-Instruct for chat (30s timeout)
- **Pollinations**: Fallback chat API (text.pollinations.ai)
- **Promptchan**: Photo generation via PROMPTCHAN_KEY secret (30s timeout)

### Data Storage (localStorage)
- `dreamUser`: User profile (name, age)
- `dreamMatches`: Array of matched girl IDs
- `dreamPassed`: Array of passed girl IDs
- `affectionLevels`: Object with affection per girl
- `profilePhotos`: Object with photo arrays per girl

## Environment Variables

- `PROMPTCHAN_KEY`: API key for Promptchan image generation

## User Preferences

- All text in French
- No emojis in UI
- Professional adult app aesthetic
- Premium dating app style
