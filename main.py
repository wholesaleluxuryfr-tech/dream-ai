import os
import json
import requests
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

API_KEY = os.environ.get('PROMPTCHAN_KEY', '')

GIRLS = {
    "anastasia": {
        "name": "Anastasia",
        "age": 35,
        "location": "Moscou, Russie",
        "tagline": "CEO russe, froide mais passionnée",
        "bio": "PDG d'une startup tech à Moscou. Habituée à diriger, je ne me laisse pas impressionner facilement. Mais si tu sais me séduire...",
        "appearance": "35 year old Russian woman, platinum blonde hair, ice blue eyes, high cheekbones, fair skin, tall, elegant, sexy",
        "system": "Tu es Anastasia, 35 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "yuki": {
        "name": "Yuki", 
        "age": 28,
        "location": "Tokyo, Japon",
        "tagline": "Artiste japonaise, timide et douce",
        "bio": "Je peins des tableaux à Tokyo. Je suis timide au début mais très affectueuse une fois en confiance...",
        "appearance": "28 year old Japanese woman, long black silky hair, dark brown eyes, petite, cute face, soft skin, delicate features",
        "system": "Tu es Yuki, 28 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "sofia": {
        "name": "Sofia",
        "age": 30, 
        "location": "Barcelone, Espagne",
        "tagline": "Danseuse espagnole, passionnée",
        "bio": "Danseuse de flamenco à Barcelone. La vie est trop courte pour être timide. Je suis directe et passionnée en tout...",
        "appearance": "30 year old Spanish woman, long wavy dark brown hair, brown eyes, olive skin, curvy body, full lips, passionate look",
        "system": "Tu es Sofia, 30 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "emma": {
        "name": "Emma",
        "age": 25,
        "location": "Los Angeles, USA",
        "tagline": "Mannequin, Los Angeles",
        "bio": "Mannequin à LA. J'adore la caméra et elle me le rend bien.",
        "appearance": "25 year old American woman, long blonde hair, green eyes, tall slim body, tanned skin, large breasts, perfect curves",
        "system": "Tu es Emma, 25 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "lea": {
        "name": "Léa", 
        "age": 27,
        "location": "Paris, France",
        "tagline": "Infirmière, Paris",
        "bio": "Je prends soin de mes patients le jour, et de mes envies la nuit.",
        "appearance": "27 year old French woman, medium brown hair, hazel eyes, curvy body, large natural breasts, soft skin",
        "system": "Tu es Léa, 27 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "mia": {
        "name": "Mia",
        "age": 32,
        "location": "Rio, Brésil",
        "tagline": "Coach fitness, Rio",
        "bio": "Mon corps est mon art. Je travaille dur pour lui, autant en profiter.",
        "appearance": "32 year old Brazilian woman, long dark curly hair, brown eyes, athletic toned body, tan skin, round butt, abs",
        "system": "Tu es Mia, 32 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    }
}

HTML = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Dream AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #0a0a0c; color: #ffffff; min-height: 100vh; -webkit-tap-highlight-color: transparent; }
        
        .page { display: none; min-height: 100vh; overflow-x: hidden; }
        .page.active { display: flex; flex-direction: column; }
        
        /* HEADER */
        .header { padding: 1.5rem 1rem; text-align: center; background: rgba(10, 10, 12, 0.8); backdrop-filter: blur(10px); position: sticky; top: 0; z-index: 100; border-bottom: 1px solid rgba(233, 30, 99, 0.1); }
        .logo { font-size: 2rem; font-weight: 800; color: #e91e63; letter-spacing: -0.5px; }
        .subtitle { color: #888888; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; margin-top: 0.2rem; }
        
        /* GALLERY */
        .gallery { padding: 1rem; flex: 1; }
        .gallery h2 { margin-bottom: 1.5rem; font-size: 1.2rem; font-weight: 700; color: #ffffff; padding-left: 0.5rem; border-left: 3px solid #e91e63; }
        .girls-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1rem; }
        .girl-card { background: #12121a; border-radius: 20px; overflow: hidden; cursor: pointer; transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease; position: relative; border: 1px solid rgba(255, 255, 255, 0.05); }
        .girl-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5); }
        .girl-card-img { height: 240px; background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0) 50%, rgba(10,10,12,0.9) 100%); position: relative; display: flex; align-items: center; justify-content: center; font-size: 3rem; font-weight: 700; color: rgba(233, 30, 99, 0.3); }
        .girl-card-info { position: absolute; bottom: 0; left: 0; right: 0; padding: 1rem; background: linear-gradient(to top, #12121a, transparent); }
        .girl-card-name { font-size: 1rem; font-weight: 700; color: #ffffff; }
        .girl-card-tagline { color: #888888; font-size: 0.75rem; margin-top: 0.2rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .badge-new { position: absolute; top: 10px; right: 10px; background: #e91e63; color: white; padding: 4px 8px; border-radius: 10px; font-size: 0.6rem; font-weight: 800; text-transform: uppercase; box-shadow: 0 2px 5px rgba(233, 30, 99, 0.4); z-index: 5; }
        
        /* PROFILE */
        .profile { max-width: 500px; margin: 0 auto; width: 100%; flex: 1; }
        .back-btn { color: #ffffff; font-size: 1.5rem; cursor: pointer; padding: 1rem; display: inline-block; transition: color 0.2s; }
        .back-btn:hover { color: #e91e63; }
        .profile-img { width: 100%; height: 450px; background: #12121a; display: flex; align-items: center; justify-content: center; font-size: 8rem; font-weight: 800; color: rgba(233, 30, 99, 0.1); position: relative; }
        .profile-img::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 150px; background: linear-gradient(to top, #0a0a0c, transparent); }
        .profile-content { padding: 1.5rem; margin-top: -2rem; position: relative; z-index: 10; }
        .profile h1 { font-size: 2rem; font-weight: 800; margin-bottom: 0.2rem; }
        .profile-tagline { color: #e91e63; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1.5rem; }
        .profile-stats { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
        .stat-item { background: #12121a; padding: 0.75rem 1.25rem; border-radius: 15px; border: 1px solid rgba(233, 30, 99, 0.2); flex: 1; text-align: center; }
        .stat-label { font-size: 0.7rem; color: #888888; text-transform: uppercase; margin-bottom: 0.3rem; }
        .stat-value { font-size: 1.1rem; font-weight: 700; color: #e91e63; }
        .profile-bio { color: #888888; line-height: 1.7; font-size: 0.95rem; margin-bottom: 2rem; }
        .profile-actions { display: flex; flex-direction: column; gap: 1rem; }
        .btn-premium { width: 100%; padding: 1.1rem; border: none; border-radius: 15px; font-size: 1rem; font-weight: 700; cursor: pointer; transition: transform 0.2s, opacity 0.2s; text-align: center; text-decoration: none; }
        .btn-chat { background: #e91e63; color: #ffffff; box-shadow: 0 5px 15px rgba(233, 30, 99, 0.3); }
        .btn-photo { background: #12121a; color: #ffffff; border: 1px solid rgba(255, 255, 255, 0.1); }
        .btn-premium:active { transform: scale(0.98); }
        
        /* CHAT */
        .chat-page { display: none; height: 100vh; overflow: hidden; }
        .chat-header { display: flex; align-items: center; padding: 1rem; background: rgba(10, 10, 12, 0.9); backdrop-filter: blur(10px); border-bottom: 1px solid #1a1a1f; position: sticky; top: 0; z-index: 100; }
        .chat-avatar-circle { width: 42px; height: 42px; border-radius: 50%; background: #12121a; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: 800; color: #e91e63; margin-right: 0.75rem; border: 1px solid rgba(233, 30, 99, 0.3); }
        .chat-info { flex: 1; }
        .chat-name { font-weight: 700; font-size: 1.1rem; }
        .chat-status { font-size: 0.7rem; color: #888888; display: flex; align-items: center; gap: 4px; }
        .status-dot { width: 6px; height: 6px; background: #22c55e; border-radius: 50%; display: inline-block; box-shadow: 0 0 5px #22c55e; }
        
        .messages { flex: 1; overflow-y: auto; padding: 1.5rem 1rem; display: flex; flex-direction: column; gap: 1.2rem; scroll-behavior: smooth; }
        .msg { max-width: 80%; display: flex; flex-direction: column; }
        .msg.user { align-self: flex-end; }
        .msg.her { align-self: flex-start; }
        .msg-bubble { padding: 0.9rem 1.1rem; border-radius: 20px; font-size: 0.95rem; line-height: 1.5; position: relative; }
        .msg.her .msg-bubble { background: #12121a; border-bottom-left-radius: 4px; color: #ffffff; }
        .msg.user .msg-bubble { background: #e91e63; border-bottom-right-radius: 4px; color: #ffffff; }
        .msg-meta { font-size: 0.65rem; color: #555555; margin-top: 0.3rem; display: flex; align-items: center; gap: 4px; }
        .msg.user .msg-meta { align-self: flex-end; }
        .read-receipt { color: #e91e63; font-weight: 800; }
        
        .msg-img { max-width: 280px; border-radius: 18px; overflow: hidden; margin-top: 0.5rem; border: 1px solid rgba(255, 255, 255, 0.05); cursor: pointer; transition: opacity 0.2s; }
        .msg-img img { width: 100%; display: block; }
        .msg-img:active { opacity: 0.8; }
        
        .typing-indicator { font-size: 0.75rem; color: #e91e63; margin-bottom: 0.5rem; font-style: italic; display: none; }
        
        .input-area { padding: 1.2rem 1rem; background: #0a0a0c; border-top: 1px solid #1a1a1f; padding-bottom: calc(1.2rem + env(safe-area-inset-bottom)); }
        .input-row { display: flex; gap: 0.75rem; align-items: center; }
        .chat-input { flex: 1; padding: 1rem 1.5rem; background: #12121a; border: 1px solid #1a1a1f; border-radius: 30px; color: #ffffff; font-size: 1rem; outline: none; transition: border-color 0.2s; }
        .chat-input:focus { border-color: #e91e63; }
        .send-btn { width: 50px; height: 50px; border-radius: 50%; background: #e91e63; border: none; color: #ffffff; font-size: 1.2rem; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(233, 30, 99, 0.3); transition: transform 0.2s; }
        .send-btn:active { transform: scale(0.9); }
        .send-btn:disabled { opacity: 0.5; cursor: default; }
        
        .empty-chat { text-align: center; color: #444444; padding: 4rem 1rem; font-size: 0.9rem; letter-spacing: 1px; }

        /* Fullscreen Overlay */
        #img-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 1000; display: none; align-items: center; justify-content: center; padding: 1rem; }
        #img-overlay img { max-width: 100%; max-height: 100%; border-radius: 10px; }
    </style>
</head>
<body>

<!-- GALLERY PAGE -->
<div class="page active" id="pageGallery">
    <div class="header">
        <div class="logo">DREAM AI</div>
        <div class="subtitle">Premium Companion Experience</div>
    </div>
    <div class="gallery">
        <h2>Découvrir</h2>
        <div class="girls-grid" id="girlsGrid"></div>
    </div>
</div>

<!-- PROFILE PAGE -->
<div class="page" id="pageProfile">
    <div class="profile">
        <div class="back-btn" onclick="showPage('gallery')">←</div>
        <div class="profile-img" id="profileInitials"></div>
        <div class="profile-content">
            <h1 id="profileName"></h1>
            <div class="profile-tagline" id="profileTagline"></div>
            
            <div class="profile-stats">
                <div class="stat-item">
                    <div class="stat-label">Affection</div>
                    <div class="stat-value" id="profileAffection">20%</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Statut</div>
                    <div class="stat-value" style="color:#22c55e">Online</div>
                </div>
            </div>
            
            <div class="profile-bio" id="profileBio"></div>
            
            <div class="profile-actions">
                <button class="btn-premium btn-chat" onclick="startChat()">Envoyer un Message</button>
                <button class="btn-premium btn-photo" onclick="requestProfilePhoto()">Demander une Photo</button>
            </div>
        </div>
    </div>
</div>

<!-- CHAT PAGE -->
<div class="page chat-page" id="pageChat">
    <div class="chat-header">
        <div class="back-btn" onclick="showPage('profile')">←</div>
        <div class="chat-avatar-circle" id="chatInitials"></div>
        <div class="chat-info">
            <div class="chat-name" id="chatName"></div>
            <div class="chat-status"><span class="status-dot"></span> Online</div>
        </div>
    </div>
    <div class="messages" id="messages"></div>
    <div class="input-area">
        <div id="typing-indicator" class="typing-indicator"></div>
        <div class="input-row">
            <input type="text" class="chat-input" id="chatInput" placeholder="Écris un message...">
            <button class="send-btn" id="sendBtn" onclick="sendMessage()">➤</button>
        </div>
    </div>
</div>

<div id="img-overlay" onclick="this.style.display='none'"><img id="overlay-img" src=""></div>

<script>
const GIRLS = ''' + json.dumps(GIRLS, ensure_ascii=False) + ''';
const INITIALS = { anastasia: 'A', yuki: 'Y', sofia: 'S', emma: 'E', lea: 'L', mia: 'M' };

let currentGirl = null;
let chatHistory = {};
let affectionLevels = JSON.parse(localStorage.getItem('affectionLevels') || '{}');
let readConversations = JSON.parse(localStorage.getItem('readConversations') || '{}');

function init() {
    const grid = document.getElementById('girlsGrid');
    grid.innerHTML = Object.entries(GIRLS).map(([id, g]) => `
        <div class="girl-card" onclick="showProfile('${id}')">
            ${!readConversations[id] ? '<div class="badge-new">NEW</div>' : ''}
            <div class="girl-card-img">${INITIALS[id]}</div>
            <div class="girl-card-info">
                <div class="girl-card-name">${g.name}, ${g.age}</div>
                <div class="girl-card-tagline">${g.tagline}</div>
            </div>
        </div>
    `).join('');
    
    Object.keys(GIRLS).forEach(id => { 
        chatHistory[id] = []; 
        if (affectionLevels[id] === undefined) affectionLevels[id] = 20;
    });
    localStorage.setItem('affectionLevels', JSON.stringify(affectionLevels));
}

function showPage(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById('page' + page.charAt(0).toUpperCase() + page.slice(1)).classList.add('active');
    if (page === 'gallery') init();
}

function showProfile(id) {
    currentGirl = id;
    const g = GIRLS[id];
    document.getElementById('profileInitials').textContent = INITIALS[id];
    document.getElementById('profileName').textContent = g.name + ', ' + g.age;
    document.getElementById('profileTagline').textContent = g.tagline;
    document.getElementById('profileBio').textContent = g.bio;
    document.getElementById('profileAffection').textContent = affectionLevels[id] + '%';
    
    readConversations[id] = true;
    localStorage.setItem('readConversations', JSON.stringify(readConversations));
    
    showPage('profile');
}

function startChat() {
    const g = GIRLS[currentGirl];
    document.getElementById('chatInitials').textContent = INITIALS[currentGirl];
    document.getElementById('chatName').textContent = g.name;
    renderMessages();
    showPage('chat');
    document.getElementById('chatInput').focus();
}

function getTime() {
    const now = new Date();
    return now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
}

function renderMessages() {
    const msgs = chatHistory[currentGirl];
    const container = document.getElementById('messages');
    
    if (msgs.length === 0) {
        container.innerHTML = '<div class="empty-chat">DÉBUT DE LA CONVERSATION</div>';
        return;
    }
    
    container.innerHTML = msgs.map(m => {
        const cls = m.role === 'user' ? 'user' : 'her';
        const text = (m.content || '').replace(/\\[PHOTO:[^\\]]+\\]/g, '').trim();
        const imgHtml = m.image ? `<div class="msg-img" onclick="fullscreenImg('${m.image}')"><img src="${m.image}" alt="Photo"></div>` : '';
        const receipt = m.role === 'user' ? '<span class="read-receipt">✓✓</span>' : '';
        
        return `<div class="msg ${cls}">
            ${text ? `<div class="msg-bubble">${text}</div>` : ''}
            ${imgHtml}
            <div class="msg-meta">${m.time} ${receipt}</div>
        </div>`;
    }).join('');
    
    container.scrollTop = container.scrollHeight;
}

function fullscreenImg(url) {
    document.getElementById('overlay-img').src = url;
    document.getElementById('img-overlay').style.display = 'flex';
}

function setTyping(isTyping) {
    const el = document.getElementById('typing-indicator');
    if (isTyping) {
        el.innerText = GIRLS[currentGirl].name + ' écrit...';
        el.style.display = 'block';
    } else {
        el.style.display = 'none';
    }
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if (!text) return;
    
    input.value = '';
    document.getElementById('sendBtn').disabled = true;
    
    const lowerText = text.toLowerCase();
    if (['belle', 'jolie', 'adore', 'sexy', 'magnifique', 'charme', 'parfaite', 'canon', 'plait'].some(word => lowerText.includes(word))) {
        affectionLevels[currentGirl] = Math.min(100, affectionLevels[currentGirl] + 5);
    }
    
    // Auto-trigger photo if keywords detected
    let autoRequestPhoto = false;
    if (['photo', 'nude', 'montre', 'voir', 'déshabille', 'nu', 'corps', 'poitrine', 'fesse'].some(word => lowerText.includes(word))) {
        affectionLevels[currentGirl] = Math.min(100, affectionLevels[currentGirl] + 2);
        autoRequestPhoto = true;
    }
    
    localStorage.setItem('affectionLevels', JSON.stringify(affectionLevels));
    
    chatHistory[currentGirl].push({ role: 'user', content: text, time: getTime() });
    renderMessages();
    
    setTimeout(() => setTyping(true), 1000);
    
    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                girl: currentGirl,
                affection: affectionLevels[currentGirl],
                auto_photo: autoRequestPhoto,
                messages: chatHistory[currentGirl].map(m => ({ role: m.role, content: m.content }))
            })
        });
        
        const data = await res.json();
        setTyping(false);
        
        let reply = data.reply || "Désolée, j'ai un souci technique...";
        const photoMatch = reply.match(/\\[PHOTO:\\s*([^\\]]+)\\]/i);
        const cleanReply = reply.replace(/\\[PHOTO:[^\\]]+\\]/gi, '').trim();
        
        const msgObj = { role: 'assistant', content: cleanReply, time: getTime() };
        chatHistory[currentGirl].push(msgObj);
        renderMessages();
        
        if (photoMatch) {
            await generatePhoto(photoMatch[1], msgObj);
        }
    } catch (e) {
        setTyping(false);
        chatHistory[currentGirl].push({ role: 'assistant', content: "Désolée, erreur réseau.", time: getTime() });
        renderMessages();
    }
    
    document.getElementById('sendBtn').disabled = false;
}

async function requestProfilePhoto() {
    startChat();
    const msgObj = { role: 'assistant', content: "Tiens, c'est pour toi... 😘", time: getTime() };
    chatHistory[currentGirl].push(msgObj);
    renderMessages();
    await generatePhoto("casual selfie, beautiful smile, high quality", msgObj);
}

async function generatePhoto(description, msgObj) {
    try {
        const res = await fetch('/photo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                girl: currentGirl,
                affection: affectionLevels[currentGirl],
                description: description
            })
        });
        
        const data = await res.json();
        if (data.image_url) {
            msgObj.image = data.image_url;
            renderMessages();
        }
    } catch (e) { console.error('Photo error:', e); }
}

document.getElementById('chatInput').addEventListener('keypress', e => {
    if (e.key === 'Enter') sendMessage();
});

init();
</script>
</body>
</html>'''


@app.route('/')
def home():
    return Response(HTML, mimetype='text/html')


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    girl_id = data.get('girl', 'anastasia')
    messages = data.get('messages', [])
    affection = data.get('affection', 20)
    
    girl = GIRLS.get(girl_id, GIRLS['anastasia'])
    
    mood_desc = ""
    if affection < 30:
        mood_desc = "Tu es réservée, tu testes l'utilisateur. Tu es un peu sur la défensive."
    elif affection < 50:
        mood_desc = "Tu es flirty et suggestive. Tu commences à t'ouvrir."
    elif affection < 75:
        mood_desc = "Tu es très flirty et excitée. Tu proposes d'aller dans un endroit plus privé. Tu peux envoyer des photos sexy [PHOTO: lingerie]."
    elif affection < 90:
        mood_desc = "Tu es intime et passionnée. Tu n'as plus de tabous. Tu peux envoyer des photos nues [PHOTO: nude]."
    else:
        mood_desc = "Tu es totalement déchaînée et explicite. Tu es prête à tout pour lui plaire."

    # Update system prompt with dynamic affection
    system_base = girl['system'].replace("{affection}", str(affection))
    system_msg_content = f"{system_base} Mood actuel: {mood_desc}. Tu as une mémoire parfaite de la conversation. Sois proactive: si la conversation est chaude, propose une photo ou suggère de passer à quelque chose de plus privé."
    
    system_msg = {"role": "system", "content": system_msg_content}
    all_messages = [system_msg] + messages[-20:]
    
    try:
        response = requests.post(
            'https://api.deepinfra.com/v1/openai/chat/completions',
            json={
                "model": "meta-llama/Meta-Llama-3.1-70B-Instruct",
                "messages": all_messages,
                "max_tokens": 1000,
                "temperature": 0.9
            },
            timeout=60
        )
        
        if response.ok:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            return jsonify({"reply": reply})
    except Exception as e:
        print(f"Chat error: {e}")
    
    return jsonify({"reply": "Désolée, j'ai un petit souci technique... Réessaie! 💕"})


@app.route('/photo', methods=['POST'])
def photo():
    if not API_KEY:
        return jsonify({"error": "PROMPTCHAN_KEY not set"})
    
    data = request.json
    girl_id = data.get('girl', 'anastasia')
    description = data.get('description', '')
    affection = data.get('affection', 20)
    
    girl = GIRLS.get(girl_id, GIRLS['anastasia'])
    
    mood_prompt = ""
    if affection < 30:
        mood_prompt = "wearing elegant dress, cleavage"
    elif affection < 50:
        mood_prompt = "wearing tight dress, showing legs, seductive"
    elif affection < 75:
        mood_prompt = "wearing lingerie, lace bra, bedroom"
    else:
        mood_prompt = "nude, topless, naked, bedroom, seductive pose"

    full_prompt = f"{girl['appearance']}, {mood_prompt}, {description}"
    
    try:
        response = requests.post(
            'https://prod.aicloudnetservices.com/api/external/create',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': API_KEY
            },
            json={
                "style": "Photo XL+ v2",
                "pose": "Default",
                "prompt": full_prompt,
                "quality": "Ultra",
                "expression": "Neutral",
                "age_slider": girl['age'],
                "creativity": 50,
                "restore_faces": True,
                "seed": -1
            },
            timeout=120
        )
        
        if response.ok:
            result = response.json()
            image_val = result.get('image', result.get('image_url', ''))
            
            if image_val:
                if isinstance(image_val, str) and not image_val.startswith('http') and not image_val.startswith('data:'):
                    image_val = 'https://cdn.promptchan.ai/' + image_val
                return jsonify({"image_url": image_val})
            
        return jsonify({"error": "No image in response"})
            
    except Exception as e:
        print(f"Photo error: {e}")
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
