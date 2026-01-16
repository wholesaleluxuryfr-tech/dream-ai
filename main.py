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
        "tagline": "CEO russe, froide mais passionnée",
        "bio": "PDG d'une startup tech à Moscou. Habituée à diriger, je ne me laisse pas impressionner facilement. Mais si tu sais me séduire...",
        "appearance": "35 year old Russian woman, platinum blonde hair, ice blue eyes, high cheekbones, fair skin, tall, elegant, sexy",
        "system": "Tu es Anastasia, 35 ans, PDG russe sexy et dominante. Tu es sur une app de dating pour adultes. Tu es froide au début mais tu deviens très sensuelle et ouverte quand quelqu'un te plaît. Tu adores séduire et envoyer des photos sexy. Réponds en français. Quand tu veux envoyer une photo, écris [PHOTO: description en anglais]."
    },
    "yuki": {
        "name": "Yuki", 
        "age": 28,
        "tagline": "Artiste japonaise, timide et douce",
        "bio": "Je peins des tableaux à Tokyo. Je suis timide au début mais très affectueuse une fois en confiance...",
        "appearance": "28 year old Japanese woman, long black silky hair, dark brown eyes, petite, cute face, soft skin, delicate features",
        "system": "Tu es Yuki, 28 ans, artiste japonaise douce et timide. Tu es sur une app de dating pour adultes. Tu es timide au début mais tu deviens très câline et coquine quand tu es en confiance. Tu aimes envoyer des photos mignonnes puis sexy. Réponds en français avec parfois des mots japonais. Quand tu veux envoyer une photo, écris [PHOTO: description en anglais]."
    },
    "sofia": {
        "name": "Sofia",
        "age": 30, 
        "tagline": "Danseuse espagnole, passionnée",
        "bio": "Danseuse de flamenco à Barcelone. La vie est trop courte pour être timide. Je suis directe et passionnée en tout...",
        "appearance": "30 year old Spanish woman, long wavy dark brown hair, brown eyes, olive skin, curvy body, full lips, passionate look",
        "system": "Tu es Sofia, 30 ans, danseuse espagnole passionnée et directe. Tu es sur une app de dating pour adultes. Tu es très ouverte, flirteuse et tu adores la séduction. Tu envoies facilement des photos sexy car tu assumes ton corps. Réponds en français avec parfois des mots espagnols. Quand tu veux envoyer une photo, écris [PHOTO: description en anglais]."
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
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #0a0a0c; color: #fff; min-height: 100vh; }
        
        .page { display: none; min-height: 100vh; }
        .page.active { display: block; }
        
        /* HEADER */
        .header { padding: 1rem; background: linear-gradient(135deg, #1a1a2e, #16213e); text-align: center; border-bottom: 1px solid #ff3d7f33; }
        .logo { font-size: 1.8rem; font-weight: 700; color: #ff3d7f; }
        .subtitle { color: #888; font-size: 0.9rem; margin-top: 0.3rem; }
        
        /* GALLERY */
        .gallery { padding: 1rem; }
        .gallery h2 { margin-bottom: 1rem; color: #ff3d7f; }
        .girls-grid { display: flex; flex-direction: column; gap: 1rem; }
        .girl-card { background: linear-gradient(145deg, #1e1e28, #151518); border-radius: 16px; overflow: hidden; cursor: pointer; transition: transform 0.2s; border: 1px solid #ffffff10; }
        .girl-card:hover { transform: scale(1.02); }
        .girl-card-img { height: 200px; background: linear-gradient(45deg, #ff3d7f22, #ff6b9d22); display: flex; align-items: center; justify-content: center; font-size: 4rem; }
        .girl-card-info { padding: 1rem; }
        .girl-card-name { font-size: 1.3rem; font-weight: 600; margin-bottom: 0.3rem; }
        .girl-card-tagline { color: #ff6b9d; font-size: 0.9rem; }
        
        /* PROFILE */
        .profile { padding: 1rem; max-width: 500px; margin: 0 auto; }
        .back-btn { color: #ff3d7f; font-size: 1.1rem; cursor: pointer; margin-bottom: 1rem; display: inline-block; }
        .profile-img { width: 100%; aspect-ratio: 1; background: linear-gradient(45deg, #ff3d7f22, #ff6b9d22); border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 6rem; margin-bottom: 1rem; }
        .profile h1 { font-size: 1.8rem; margin-bottom: 0.5rem; }
        .profile-tagline { color: #ff3d7f; font-size: 1.1rem; margin-bottom: 1rem; }
        .profile-bio { color: #aaa; line-height: 1.6; margin-bottom: 1.5rem; }
        .btn-chat { width: 100%; padding: 1rem; background: linear-gradient(135deg, #ff3d7f, #ff6b9d); border: none; border-radius: 50px; color: #fff; font-size: 1.1rem; font-weight: 600; cursor: pointer; }
        
        /* CHAT */
        .chat-page { display: none; flex-direction: column; height: 100vh; }
        .chat-page.active { display: flex; }
        .chat-header { display: flex; align-items: center; gap: 0.75rem; padding: 1rem; background: #151518; border-bottom: 1px solid #222; }
        .chat-header .back-btn { margin: 0; margin-right: 0.5rem; }
        .chat-avatar { width: 45px; height: 45px; border-radius: 50%; background: linear-gradient(135deg, #ff3d7f, #ff6b9d); display: flex; align-items: center; justify-content: center; font-size: 1.5rem; }
        .chat-name { font-weight: 600; font-size: 1.1rem; }
        .chat-status { font-size: 0.75rem; color: #22c55e; }
        
        .messages { flex: 1; overflow-y: auto; padding: 1rem; display: flex; flex-direction: column; gap: 0.75rem; }
        .msg { max-width: 85%; display: flex; gap: 0.5rem; }
        .msg.user { align-self: flex-end; flex-direction: row-reverse; }
        .msg-avatar { width: 30px; height: 30px; border-radius: 50%; background: linear-gradient(135deg, #ff3d7f, #ff6b9d); display: flex; align-items: center; justify-content: center; font-size: 0.9rem; flex-shrink: 0; }
        .msg-bubble { padding: 0.75rem 1rem; border-radius: 18px; line-height: 1.5; }
        .msg.her .msg-bubble { background: #1e1e28; border-bottom-left-radius: 4px; }
        .msg.user .msg-bubble { background: linear-gradient(135deg, #ff3d7f, #ff6b9d); border-bottom-right-radius: 4px; }
        .msg-img { max-width: 250px; border-radius: 12px; overflow: hidden; margin-top: 0.5rem; }
        .msg-img img { width: 100%; display: block; }
        
        .typing { display: flex; gap: 0.5rem; align-items: center; }
        .typing-dots { display: flex; gap: 4px; padding: 0.75rem 1rem; background: #1e1e28; border-radius: 18px; }
        .typing-dot { width: 8px; height: 8px; background: #666; border-radius: 50%; animation: bounce 1.4s infinite; }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes bounce { 0%,80%,100% { transform: scale(0.8); } 40% { transform: scale(1.2); } }
        
        .loading-img { background: #1e1e28; padding: 1.5rem 2rem; border-radius: 12px; display: flex; align-items: center; gap: 0.75rem; margin-top: 0.5rem; }
        .spinner { width: 24px; height: 24px; border: 3px solid #333; border-top-color: #ff3d7f; border-radius: 50%; animation: spin 1s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
        
        .input-area { padding: 1rem; background: #151518; border-top: 1px solid #222; }
        .input-row { display: flex; gap: 0.5rem; }
        .photo-btn { width: 48px; height: 48px; border-radius: 50%; background: #1e1e28; border: 1px solid #333; color: #ff3d7f; font-size: 1.3rem; cursor: pointer; display: flex; align-items: center; justify-content: center; }
        .chat-input { flex: 1; padding: 0.9rem 1.2rem; background: #1e1e28; border: 1px solid #333; border-radius: 25px; color: #fff; font-size: 1rem; outline: none; }
        .chat-input:focus { border-color: #ff3d7f; }
        .send-btn { width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #ff3d7f, #ff6b9d); border: none; color: #fff; font-size: 1.3rem; cursor: pointer; display: flex; align-items: center; justify-content: center; }
        .send-btn:disabled { opacity: 0.5; }
        
        .empty-chat { text-align: center; color: #666; padding: 3rem 1rem; }
        .empty-chat p:first-child { font-size: 3rem; margin-bottom: 1rem; }
    </style>
</head>
<body>

<!-- GALLERY PAGE -->
<div class="page active" id="pageGallery">
    <div class="header">
        <div class="logo">💕 Dream AI</div>
        <div class="subtitle">Rencontres virtuelles</div>
    </div>
    <div class="gallery">
        <h2>Découvre</h2>
        <div class="girls-grid" id="girlsGrid"></div>
    </div>
</div>

<!-- PROFILE PAGE -->
<div class="page" id="pageProfile">
    <div class="profile">
        <div class="back-btn" onclick="showPage('gallery')">← Retour</div>
        <div class="profile-img" id="profileEmoji"></div>
        <h1 id="profileName"></h1>
        <div class="profile-tagline" id="profileTagline"></div>
        <p class="profile-bio" id="profileBio"></p>
        <button class="btn-chat" onclick="startChat()">💬 Commencer à discuter</button>
    </div>
</div>

<!-- CHAT PAGE -->
<div class="page chat-page" id="pageChat">
    <div class="chat-header">
        <div class="back-btn" onclick="showPage('gallery')">←</div>
        <div class="chat-avatar" id="chatEmoji"></div>
        <div>
            <div class="chat-name" id="chatName"></div>
            <div class="chat-status">🟢 En ligne</div>
        </div>
    </div>
    <div class="messages" id="messages">
        <div class="empty-chat">
            <p>💕</p>
            <p>Envoie le premier message!</p>
        </div>
    </div>
    <div class="input-area">
        <div class="input-row">
            <button class="photo-btn" onclick="requestPhoto()" title="Demander une photo">📷</button>
            <input type="text" class="chat-input" id="chatInput" placeholder="Écris un message...">
            <button class="send-btn" id="sendBtn" onclick="sendMessage()">➤</button>
        </div>
    </div>
</div>

<script>
const GIRLS = ''' + json.dumps(GIRLS, ensure_ascii=False) + ''';
const EMOJIS = { anastasia: '👩‍💼', yuki: '🎨', sofia: '💃' };

let currentGirl = null;
let chatHistory = {};

// Init
function init() {
    const grid = document.getElementById('girlsGrid');
    grid.innerHTML = Object.entries(GIRLS).map(([id, g]) => `
        <div class="girl-card" onclick="showProfile('${id}')">
            <div class="girl-card-img">${EMOJIS[id]}</div>
            <div class="girl-card-info">
                <div class="girl-card-name">${g.name}, ${g.age} ans</div>
                <div class="girl-card-tagline">${g.tagline}</div>
            </div>
        </div>
    `).join('');
    
    Object.keys(GIRLS).forEach(id => { chatHistory[id] = []; });
}

function showPage(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById('page' + page.charAt(0).toUpperCase() + page.slice(1)).classList.add('active');
}

function showProfile(id) {
    currentGirl = id;
    const g = GIRLS[id];
    document.getElementById('profileEmoji').textContent = EMOJIS[id];
    document.getElementById('profileName').textContent = g.name + ', ' + g.age + ' ans';
    document.getElementById('profileTagline').textContent = g.tagline;
    document.getElementById('profileBio').textContent = g.bio;
    showPage('profile');
}

function startChat() {
    const g = GIRLS[currentGirl];
    document.getElementById('chatEmoji').textContent = EMOJIS[currentGirl];
    document.getElementById('chatName').textContent = g.name;
    renderMessages();
    showPage('chat');
    document.getElementById('chatInput').focus();
}

function renderMessages() {
    const msgs = chatHistory[currentGirl];
    const container = document.getElementById('messages');
    
    if (msgs.length === 0) {
        container.innerHTML = '<div class="empty-chat"><p>💕</p><p>Envoie le premier message!</p></div>';
        return;
    }
    
    container.innerHTML = msgs.map(m => {
        const cls = m.role === 'user' ? 'user' : 'her';
        const avatar = m.role === 'assistant' ? `<div class="msg-avatar">${EMOJIS[currentGirl]}</div>` : '';
        const text = (m.content || '').replace(/\\[PHOTO:[^\\]]+\\]/g, '').trim();
        const imgHtml = m.image ? `<div class="msg-img"><img src="${m.image}" alt="Photo"></div>` : '';
        
        return `<div class="msg ${cls}">
            ${avatar}
            <div>
                ${text ? `<div class="msg-bubble">${text}</div>` : ''}
                ${imgHtml}
            </div>
        </div>`;
    }).join('');
    
    container.scrollTop = container.scrollHeight;
}

function showTyping() {
    const container = document.getElementById('messages');
    const div = document.createElement('div');
    div.className = 'typing';
    div.id = 'typing';
    div.innerHTML = `<div class="msg-avatar">${EMOJIS[currentGirl]}</div><div class="typing-dots"><div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div></div>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function hideTyping() {
    const t = document.getElementById('typing');
    if (t) t.remove();
}

function showPhotoLoading() {
    const container = document.getElementById('messages');
    const div = document.createElement('div');
    div.className = 'msg her';
    div.id = 'photoLoading';
    div.innerHTML = `<div class="msg-avatar">${EMOJIS[currentGirl]}</div><div class="loading-img"><div class="spinner"></div><span>Génère une photo...</span></div>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function hidePhotoLoading() {
    const p = document.getElementById('photoLoading');
    if (p) p.remove();
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if (!text) return;
    
    input.value = '';
    document.getElementById('sendBtn').disabled = true;
    
    chatHistory[currentGirl].push({ role: 'user', content: text });
    renderMessages();
    showTyping();
    
    try {
        const g = GIRLS[currentGirl];
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                girl: currentGirl,
                messages: chatHistory[currentGirl].map(m => ({ role: m.role, content: m.content }))
            })
        });
        
        const data = await res.json();
        hideTyping();
        
        let reply = data.reply || "Désolée, j'ai un souci technique...";
        
        // Check for [PHOTO:...]
        const photoMatch = reply.match(/\\[PHOTO:\\s*([^\\]]+)\\]/i);
        const cleanReply = reply.replace(/\\[PHOTO:[^\\]]+\\]/gi, '').trim();
        
        const msgObj = { role: 'assistant', content: cleanReply };
        chatHistory[currentGirl].push(msgObj);
        renderMessages();
        
        if (photoMatch) {
            await generatePhoto(photoMatch[1], msgObj);
        }
        
    } catch (e) {
        hideTyping();
        chatHistory[currentGirl].push({ role: 'assistant', content: "Désolée, problème de connexion..." });
        renderMessages();
    }
    
    document.getElementById('sendBtn').disabled = false;
}

async function requestPhoto() {
    const g = GIRLS[currentGirl];
    
    chatHistory[currentGirl].push({ role: 'user', content: "Envoie-moi une photo de toi 📷" });
    renderMessages();
    
    showTyping();
    await new Promise(r => setTimeout(r, 1000));
    hideTyping();
    
    const msgObj = { role: 'assistant', content: "Tiens, rien que pour toi... 😘" };
    chatHistory[currentGirl].push(msgObj);
    renderMessages();
    
    await generatePhoto("wearing elegant dress, seductive pose, bedroom, soft lighting", msgObj);
}

async function generatePhoto(description, msgObj) {
    showPhotoLoading();
    
    try {
        const g = GIRLS[currentGirl];
        const res = await fetch('/photo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                girl: currentGirl,
                description: description
            })
        });
        
        const data = await res.json();
        hidePhotoLoading();
        
        if (data.image_url) {
            msgObj.image = data.image_url;
            renderMessages();
        } else if (data.error) {
            console.error('Photo error:', data.error);
            chatHistory[currentGirl].push({ role: 'assistant', content: "(Photo non disponible: " + data.error + ")" });
            renderMessages();
        }
    } catch (e) {
        hidePhotoLoading();
        console.error('Photo fetch error:', e);
    }
}

document.getElementById('chatInput').addEventListener('keypress', e => {
    if (e.key === 'Enter') { e.preventDefault(); sendMessage(); }
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
    
    girl = GIRLS.get(girl_id, GIRLS['anastasia'])
    
    system_msg = {"role": "system", "content": girl['system']}
    all_messages = [system_msg] + messages[-20:]
    
    # Try DeepInfra (free)
    try:
        response = requests.post(
            'https://api.deepinfra.com/v1/openai/chat/completions',
            json={
                "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
                "messages": all_messages,
                "max_tokens": 500,
                "temperature": 0.9
            },
            timeout=30
        )
        
        if response.ok:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            return jsonify({"reply": reply})
    except Exception as e:
        print(f"DeepInfra error: {e}")
    
    # Fallback to Pollinations
    try:
        response = requests.post(
            'https://text.pollinations.ai/',
            json={
                "messages": all_messages,
                "model": "openai",
                "seed": 42
            },
            timeout=60
        )
        
        if response.ok:
            return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Pollinations error: {e}")
    
    return jsonify({"reply": "Désolée, j'ai un petit souci technique... Réessaie! 💕"})


@app.route('/photo', methods=['POST'])
def photo():
    if not API_KEY:
        return jsonify({"error": "PROMPTCHAN_KEY not set"})
    
    data = request.json
    girl_id = data.get('girl', 'anastasia')
    description = data.get('description', '')
    
    girl = GIRLS.get(girl_id, GIRLS['anastasia'])
    
    full_prompt = f"{girl['appearance']}, {description}"
    
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
        
        print(f"Promptchan response status: {response.status_code}")
        print(f"Promptchan full response: {response.text}")
        
        if response.ok:
            result = response.json()
            # The API might return image_url or a base64 string in 'image' field
            if 'image_url' in result and result['image_url']:
                return jsonify({"image_url": result['image_url']})
            elif 'image' in result and result['image']:
                # Ensure we handle the base64 prefix
                image_data = result['image']
                if not image_data.startswith('data:'):
                    image_data = f"data:image/png;base64,{image_data}"
                return jsonify({"image_url": image_data})
            else:
                return jsonify({"error": "No image data found in response", "response": result})
        else:
            return jsonify({"error": f"API error: {response.status_code}", "details": response.text})
            
    except Exception as e:
        print(f"Photo generation error: {e}")
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
