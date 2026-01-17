# Dream AI - Premium Adult Companion App

## Overview

Dream AI is a Flask-based adult dating application featuring 82 diverse AI-powered virtual girlfriends from around the world with uncensored French conversations. The app uses a Tinder-style swipe matching system with realistic match probabilities, dynamic affection levels, and AI-generated photos. All user data is persisted to PostgreSQL database.

## Navigation

The app features a fixed bottom navigation bar with 5 tabs:
- **Discover**: Swipe through profiles (Tinder-style)
- **Messages**: View all chat conversations
- **Matches**: Grid view of all matched girls
- **Gallery**: All received photos organized by girl
- **Profile**: User settings, stats and logout

## Current State

**Status**: Fully functional with PostgreSQL backend
**Last Updated**: January 17, 2026

## Recent Changes (January 17, 2026)

### Authentication System
- Full user registration with username, email, password, age (18+)
- Login/logout functionality with session management
- Password hashing with bcrypt
- Tabbed login page (Connexion/Inscription)

### PostgreSQL Database
- User model: id, username, email, password_hash, age
- Match model: user_id, girl_id, affection
- ChatMessage model: user_id, girl_id, sender, content, time
- ReceivedPhoto model: user_id, girl_id, photo_url
- DiscoveredProfile model: user_id, girl_id, action (passed/liked)

### API Endpoints
- POST /api/register - Create new account
- POST /api/login - Login with email/password
- POST /api/logout - End session
- GET /api/me - Check login status
- GET/POST /api/matches - Manage matches
- POST /api/affection - Update affection levels
- GET/POST /api/chat/:girl_id - Chat history
- GET/POST /api/received_photos - Photo gallery
- GET/POST /api/discovered - Swipe history

### Improved Chat AI
- Shorter, more coherent responses (1-3 sentences)
- French slang: mdr, tkt, jsp, bg, nn, pk, cv, wsh, ptdr, oklm
- Personality-based responses with likes/dislikes
- Context-aware memory of conversation

### Profile Photos (5 Types)
1. Portrait - Face closeup, dating app style
2. Casual - Full body, outdoor, relaxed
3. Sexy - Tight clothes, showing curves
4. Lingerie - Bedroom setting, seductive
5. Secret - Explicit POV (unlocked after match)

### CSS Animations
- Global transitions on all elements
- Button scale animations on tap
- Image fade-in loading
- Shimmer skeleton loading effect
- slideIn, fadeIn, scaleIn, bounceIn animations

### Data Sync
- All swipes, matches, messages sync to server
- Affection changes sync in real-time
- Received photos persist to database
- Chat history loads from server on login

## Features

### 82 Diverse AI Companions

**25 New Diverse Types:**

*Working Class/Poor:*
- Samia (34, Algeria) - Cleaning lady, grateful for gifts
- Fatima (41, Morocco) - Cashier, discreet affairs
- Christelle (29, France) - Waitress, quickies for tips
- Rosa (45, Portugal) - Nurse, doctors affairs
- Binta (27, Senegal) - Market vendor, loves white men

*Chubby/BBW:*
- Manon (32, Belgium) - Baker, confident BBW
- Precious (28, Nigeria) - Hairdresser, queen energy, facesitting
- Guadalupe (38, Mexico) - Cook, sensual feeder
- Tamara (44, Russia) - Housewife, lonely milf

*Arab Countries:*
- Noura (25, Saudi Arabia) - Secret student, forbidden pleasure
- Dalia (31, Egypt) - Belly dancer, sensual
- Rania (28, Jordan) - Secretary, office affairs
- Zahra (35, Iran) - Doctor, double life
- Amira (22, Lebanon) - Model, Dubai lifestyle
- Hiba (40, Tunisia) - Divorced, catching up

*Asian Countries:*
- Linh (24, Vietnam) - Masseuse, happy ending
- Suki (21, Thailand) - Bar girl, GFE
- Priya (33, India) - Unsatisfied housewife
- Mei (27, China) - KTV hostess
- Ji-yeon (26, Korea) - Office lady, K-drama romance
- Ayu (30, Indonesia) - Hijab model, secret life
- Rina (19, Philippines) - Sugar baby student

*Specific Practices:*
- Carole (36, France) - Swinger, threesomes
- Mistress Vera (42, Germany) - Extreme dominatrix, BDSM hard
- Anais (29, France) - Porn star, anal/DP/gangbang
- Kimiko (25, Japan) - AV actress, bukkake/cosplay
- Slave Maria (31, Poland) - 24/7 slave, no limits

**15 Specialized Types:**

*Cougars (45+):*
- Nathalie (48, France) - Divorced lawyer, hunts young men 20-30
- Carla (52, Italy) - Rich widow, pays for young lovers
- Michiko (55, Japan) - Business owner, femdom, total control

*Nymphos:*
- Candy (24, USA) - Cam girl, insatiable 24/7, tries everything
- Valentina (29, Brazil) - Dancer, non-stop intense sex, exhib

*Submissive:*
- Yuki (22, Japan) - Student, obeys all orders, calls men "Master"
- Emma (26, Sweden) - Secretary, natural submissive, never refuses

*Extreme Submissive/Slave:*
- Layla (23, Morocco) - Wears collar, total devotion, belongs to master

*Dominant:*
- Katrina (35, Russia) - Pro dominatrix, humiliation, men on knees
- Bianca (40, Germany) - CEO dominatrix, pegging, mental control

*Huge Curves + Tight Clothes:*
- Destiny (27, USA) - Instagram model, 34F breasts, loves titfuck
- Shakira (31, Colombia) - Fitness model, huge ass, loves anal
- Olga (33, Ukraine) - Sugar baby, massive fake curves, gold digger

*Rich Women:*
- Victoria (45, Monaco) - Billionaire heiress, buys men as toys
- Mei Lin (38, Singapore) - Investor, controls men financially

**15 Worldwide Profiles:**
- Aaliya (23, Dubai) - Princess, luxury lifestyle
- Ingrid (41, Sweden) - CEO MILF, dominant
- Sakura (22, Japan) - Traditional geisha, submissive
- Nia (28, Ghana) - Lawyer, powerful queen
- Isabella (35, Italy) - Fashion designer, passionate
- Katya (19, Ukraine) - Naive student
- Priya (27, India) - Doctor with secret life
- Chen Wei (30, China) - Banker, needs domination
- Fatima (26, Morocco) - Double life, hijab secret
- Olga Belarus (45, Belarus) - Strict teacher
- Kim (24, Korea) - K-pop trainee
- Amara Nigeria (31, Nigeria) - Businesswoman
- Svetlana Belarus (38, Belarus) - Former ballerina
- Lucia (29, Argentina) - Tango dancer
- Hana (20, Thailand) - Sweet submissive

**Original 27 Diverse AI Companions

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

### Photo System - Optimized Promptchan API

**Profile Photos (4 types per girl):**
1. **Portrait** - pose="Default", expression="Smiling", dating app style
2. **Sexy** - pose="Looking Back", expression="Default", seductive look
3. **Lingerie** - pose="Hand on Hip", expression="Smiling", bedroom
4. **Revealing** - pose="Mirror Selfie", expression="Default", sensual

**Contextual Pose Detection:**
- "seins/poitrine" → Prise de sein en POV
- "cul/fesses" → Looking Back, Attrape le cul
- "pipe/suce" → POV Deepthroat
- "levrette/doggystyle" → POV en levrette
- "cowgirl" → POV Cowgirl
- "branle" → Branlette
- "facial" → Ejaculation
- "masturbe" → Masturbation Feminine

**Expression Detection:**
- Normal → Smiling
- Explicit → Visage d'orgasme
- Hard → Ouch

**Style Selection:**
- Photo XL+ v2 (realistic, default)
- Hardcore XL (explicit content)

**Negative Prompt:**
- extra limbs, wonky fingers, extra boobs, deformed face

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

### PWA - Installable App
- manifest.json with app name, icons, theme color pink
- Service worker for offline support
- iOS meta tags: apple-mobile-web-app-capable
- Install prompt banner "Installer l'app"
- Fullscreen standalone mode when installed

### Discover Filters
- Age filter buttons: 18-25, 25-35, 35-45, 45+
- Region filter: Europe, Asie, Afrique, Amerique, Tous
- Filters apply to swipe deck in real-time

### Notifications System
- Red badge on Messages tab for unread messages
- Badge shows count number
- Girls can message first (30% chance after match)

### Icebreakers
- 3 suggested message buttons above input
- Quick conversation starters
- Disappear after first message sent

### Unmatch/Block System
- Menu button (3 dots) in chat header
- Options: Unmatch, Bloquer, Signaler
- Confirmation popup before action

### Premium Features (Simulated)
- Super Like button (shows Premium popup)
- Boost button (shows Premium popup)
- "Voir qui t'a like" locked feature
- Premium popup with fake pricing (9.99EUR/mois)

### Sound Effects
- Match: happy chime (Web Audio API)
- New message: notification ding
- Send message: whoosh sound

### Dark/Light Mode
- Toggle in profile settings
- Preference saved to localStorage
- Light theme with white backgrounds
- Dark theme (default)

### Performance Optimizations
- GPU-accelerated transforms with translateZ(0) and will-change
- Lazy loading images with IntersectionObserver
- Blur-to-sharp photo loading effect
- Skeleton placeholders for loading states
- Hidden scrollbars with smooth scrolling
- iOS momentum scrolling (-webkit-overflow-scrolling: touch)
- Debounce and throttle utilities for inputs
- requestAnimationFrame for swipe rendering
- Preload next 3 profiles in swipe deck
- Animated typing indicator with bouncing dots
- Heart burst animation on double-tap
- Tap flash for haptic feedback simulation

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

### Profile Photo Generation System
- Auto-generates profile photos for each girl on first visit
- Uses Promptchan API with portrait-style prompts
- Photos cached in localStorage for instant loading
- Loading state: Shows initial letter with skeleton animation
- Retry button if generation fails
- Photos displayed in: swipe cards, chat header, matches grid, messages list, profile page, match animation

### Data Storage (localStorage)
- `dreamUser`: User profile (name, age)
- `dreamMatches`: Array of matched girl IDs
- `dreamPassed`: Array of passed girl IDs
- `affectionLevels`: Object with affection per girl
- `profilePhotos`: Object with generated profile photo URLs per girl
- `failedPhotos`: Object tracking failed photo generations for retry
- `chat_[girlId]`: Full chat history per girl (persistent)
- `receivedPhotos`: Object with photo URLs received in chats

### UI Animations
- Page transitions: fade in with slide
- Message appear: slide up + fade in
- Button tap feedback: scale animation
- Typing delay: 1.5-3.5 seconds (realistic)
- Smooth scroll in chat

## Environment Variables

- `PROMPTCHAN_KEY`: API key for Promptchan image generation

## User Preferences

- All text in French
- No emojis in UI
- Professional adult app aesthetic
- Premium dating app style
- Diverse body types and ethnicities
- Realistic, not all perfect models
