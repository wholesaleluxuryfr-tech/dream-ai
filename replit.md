# Dream AI - Premium Adult Companion App

## Overview

Dream AI is a Flask-based adult dating application featuring 27 diverse AI-powered virtual girlfriends with uncensored French conversations. The app uses a Tinder-style swipe matching system with realistic match probabilities, dynamic affection levels, and AI-generated photos.

## Current State

**Status**: Fully functional
**Last Updated**: January 2026

## Features

### 27 Diverse AI Companions

**Young (18-23):**
- Jade (19, French art student) - petite, natural, amateur look
- Chloe (21, American college girl) - freckles, girl next door
- Yuna (20, Japanese student) - petite, innocent, kawaii
- Amara (22, Nigerian fashion student) - curvy, dark skin, natural hair
- Zoe (19, Australian surfer) - athletic, tanned, beach girl
- Lina (23, German alternative) - tattoos, piercings, dyed hair

**Classic Beauties (24-30):**
- Emma (25, LA model) - slim, perfect, blonde
- Sofia (30, Spanish dancer) - curvy, passionate, Mediterranean
- Anastasia (28, Russian) - elegant, cold beauty, platinum blonde
- Priya (26, Indian) - exotic, long black hair
- Aisha (26, Moroccan) - can wear hijab, modest to wild
- Fatou (24, Senegalese) - dark ebony skin, African beauty
- Mei (29, Chinese businesswoman) - professional, refined

**MILF/Cougar (35-50):**
- Nathalie (42, French businesswoman) - elegant, big natural breasts
- Carmen (38, Spanish MILF) - very curvy, experienced look
- Jennifer (45, American cougar) - fake tits, tanned, plastic surgery
- Keiko (40, Japanese MILF) - petite, mature cute face
- Olga (48, Russian mature) - dominant, experienced
- Leila (35, Persian) - exotic, mysterious
- Valentina (33, Italian mom) - maternal, soft curves

**Bimbo Type:**
- Candy (28, Vegas bimbo) - huge fake breasts, plastic barbie look
- Nikita (30, Dubai Russian) - plastic surgery, Instagram model
- Bianca (26, Brazilian influencer) - huge butt, pouty lips

**Natural/Amateur:**
- Marie (34, French) - average body, authentic, real woman
- Sarah (29, British) - chubby, big natural breasts, BBW
- Agathe (31, Belgian) - no makeup, hairy, hippie natural

**Athletic:**
- Mia (32, Brazilian fitness) - muscular, abs, round athletic butt
- Svetlana (27, Ukrainian athlete) - tall, strong, powerful

### Photo System - 4 Varied Types Per Girl
1. **Selfie** - Face closeup, smartphone angle, natural home settings
2. **Outdoor** - Full body, various locations (beach, park, city, pool)
3. **Night Out** - Dressed up, club/bar/restaurant backgrounds
4. **Intimate** - Bedroom/bathroom, affection-based clothing level

### Photo Backgrounds
- **Day**: beach, city street, park, cafe terrace, gym, office
- **Night**: club, bar, restaurant, bedroom with dim lights
- **Home**: living room, kitchen, bathroom mirror, bedroom
- **Outdoor**: nature, mountain, pool, garden

### Stories Feature
- Instagram-style photo slideshow
- Auto-advances every 5 seconds
- Progress bars at top
- Tap left/right to navigate
- Text overlays on each photo

### Login/Signup System
- Name and age input
- Age verification (18+)
- User data saved to localStorage

### Tinder-Style Swipe System
- Variable match probabilities (30-90% depending on girl)
- "C'est un Match!" animation with hearts
- "Elle n'a pas matché avec toi" for failed matches

### Affection-Based Content
- 0-30: Elegant, dressed photos
- 30-50: Sexy, showing more skin
- 50-75: Lingerie photos
- 75+: Nude/intimate photos

## Architecture

### Single-File Structure
- `main.py`: Complete Flask app with embedded HTML/CSS/JavaScript

### External APIs
- **Pollinations**: Primary chat API (GET method, URL-encoded prompt)
- **DeepInfra**: Fallback with Sao10K/L3.1-70B-Euryale-v2.3
- **Promptchan**: Photo generation via PROMPTCHAN_KEY secret

### Realistic Chat Behavior
- **Mood System**: happy, neutral, annoyed, horny - affects responses
- **Behavior Detection**: Detects rude, rushing, too_early behavior
- **Rejections**: Girls say no if affection is low or user is disrespectful
- **Personalities**: Each girl has unique personality traits

### Smart Photo Detection
Keywords in user messages trigger auto-photo generation:
- culotte/panties → showing panties
- seins/poitrine → topless
- nue/naked → fully nude
- fesses/cul → showing butt
- douche/bain → wet/shower scenes
- And many more French/English keywords

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
- Diverse body types and ethnicities
- Realistic, not all perfect models
