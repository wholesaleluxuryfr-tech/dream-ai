# Dream AI - Premium Adult Companion App

## Overview

Dream AI is a Flask-based adult dating application designed to offer a unique interactive experience. It features 134 diverse AI-powered virtual companions from around the world, engaging in uncensored French conversations. The application integrates a Tinder-style swipe matching system, realistic match probabilities, dynamic affection levels, and AI-generated photos. Its core purpose is to provide an engaging and immersive adult dating simulation, with all user data securely persisted in a PostgreSQL database.

## User Preferences

- All text in French
- No emojis in UI
- Professional adult app aesthetic
- Premium dating app style
- Diverse body types and ethnicities
- Realistic, not all perfect models

## System Architecture

The application is built as a single-file Flask application (`main.py`), embedding all HTML, CSS, and JavaScript.

**UI/UX Decisions:**
- Fixed bottom navigation bar with 5 tabs: Discover, Messages, Matches, Gallery, Profile.
- Global CSS transitions and animations: button scale, image fade-in, shimmer skeleton loading, slideIn, fadeIn, scaleIn, bounceIn.
- PWA features for installability: `manifest.json`, service worker for offline support, iOS meta tags, install prompt banner, fullscreen standalone mode.
- Customizable Dark/Light Mode with preference saved locally.
- Performance optimizations including GPU-accelerated transforms, lazy loading with IntersectionObserver, blur-to-sharp photo loading, skeleton placeholders, hidden scrollbars, iOS momentum scrolling, debounce/throttle utilities, `requestAnimationFrame` for swipe rendering, and preload of next profiles.
- Heart burst animation on double-tap and tap flash for haptic feedback simulation.
- Sound effects for match, new message, and message sent.

**Technical Implementations & Feature Specifications:**
- **Authentication System:** Full user registration (username, email, password, age 18+), login/logout with session management, password hashing (bcrypt), and a tabbed login page.
- **Tinder-Style Swipe System:** Variable match probabilities (30-90%), "C'est un Match!" animation, and "Elle n'a pas matché avec toi" feedback.
- **AI Companions:** 134 diverse AI companions with unique personalities, mood systems (happy, neutral, annoyed, horny), behavior detection (rude, rushing, too_early), and rejection logic based on affection or disrespect.
- **Chat AI:** Provides short, coherent responses (1-3 sentences) with French slang and context-aware memory. Enhanced with 10 distinct agent archetypes (soumise, dominante, nympho, timide, exhib, fetichiste, romantique, perverse, cougar, salope) - each with unique conversation styles, expressions, fantasies, games to propose, and personal anecdotes. Archetype is auto-detected from profile personality keywords.
- **Photo System:** Auto-generates 5 profile photos per girl using Promptchan API: Portrait, Fullbody, Sexy, Lingerie, and Secret (explicit). Photos cached locally. Secret photo locked until match - unlocks automatically after matching. Context-based photo generation triggered by keywords in user messages.
- **Affection-Based Content:** Dynamic content unlocking based on affection levels (Elegant, Sexy, Lingerie, Nude/Intimate photos).
- **Stories Feature:** Instagram-style photo slideshow with auto-advance, navigation, and text overlays.
- **Discover Filters:** Age (18-25, 25-35, 35-45, 45+) and Region (Europe, Asie, Afrique, Amerique, Tous) filters applied in real-time.
- **Notifications System:** Red badge for unread messages, with girls having a 30% chance to message first after a match.
- **Icebreakers:** 3 suggested message buttons for conversation starters.
- **Unmatch/Block System:** Options to unmatch, block, or report within chat, with confirmation.
- **Premium Features (Simulated):** Super Like, Boost buttons, "Voir qui t'a like" locked feature, and a premium popup with fake pricing.

**System Design Choices:**
- **Data Sync:** All user interactions (swipes, matches, messages, affection changes, received photos) are synced with the server and persisted.
- **Database Schema (PostgreSQL):**
    - `User`: id, username, email, password_hash, age
    - `Match`: user_id, girl_id, affection
    - `ChatMessage`: user_id, girl_id, sender, content, time
    - `ReceivedPhoto`: user_id, girl_id, photo_url
    - `DiscoveredProfile`: user_id, girl_id, action (passed/liked)
- **Local Storage:** Used for client-side data persistence including `dreamUser`, `dreamMatches`, `dreamPassed`, `affectionLevels`, `profilePhotos`, `failedPhotos`, `chat_[girlId]`, and `receivedPhotos`.

## External Dependencies

- **PostgreSQL Database:** Primary data persistence layer.
- **Pollinations API:** Primary API for AI chat interactions.
- **DeepInfra:** Fallback API for AI chat, utilizing the Sao10K/L3.1-70B-Euryale-v2.3 model.
- **Promptchan API:** Used for AI photo generation.