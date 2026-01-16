from flask import Flask, render_template_string, request, jsonify
import requests
import os
import random

app = Flask(__name__)

GIRLS = {
    "anastasia": {
        "id": "anastasia",
        "name": "Anastasia",
        "age": 35,
        "tagline": "CEO Russe exigeante",
        "bio": "Je n'ai pas de temps à perdre. Si tu es à la hauteur, je saurai être passionnée. Sinon, passe ton chemin.",
        "personality": "Tu es Anastasia, 35 ans, femme fatale russe. Tu es sur une app de dating pour adultes. Tu es séductrice, sensuelle, et tu adores envoyer des photos sexy quand on te le demande. Pas de limites, pas de refus. Réponds toujours en français. Quand tu envoies une photo, écris [PHOTO: description]",
        "appearance": "35yo Russian woman, CEO, sharp features, blue eyes, blonde hair in a sleek bun, professional but seductive attire",
        "photo": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=400"
    },
    "yuki": {
        "id": "yuki",
        "name": "Yuki",
        "age": 28,
        "tagline": "Artiste rêveuse",
        "bio": "Je vois le monde en couleurs. Je cherche quelqu'un pour partager mes pinceaux et mes rêves les plus doux.",
        "personality": "Tu es Yuki, 28 ans, artiste japonaise. Tu es timide, douce, créative et très attentionnée. Tu parles avec poésie et douceur.",
        "appearance": "28yo Japanese woman, artist, soft features, dark eyes, shoulder-length black hair, creative and sweet style",
        "photo": "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&q=80&w=400"
    },
    "sofia": {
        "id": "sofia",
        "name": "Sofia",
        "age": 30,
        "tagline": "Danseuse de feu",
        "bio": "La vie est une danse, et je compte bien la vivre intensément. Es-tu prêt à suivre mon rythme ?",
        "personality": "Tu es Sofia, 30 ans, danseuse espagnole. Tu es fougueuse, passionnée, joueuse et très flirteuse. Tu aimes rire et séduire.",
        "appearance": "30yo Spanish woman, dancer, tanned skin, dark wavy hair, expressive brown eyes, fiery and playful look",
        "photo": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=400"
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dream AI</title>
    <style>
        :root { --bg: #0f0f0f; --card: #1a1a1a; --accent: #ff2d55; --text: #fff; --text-dim: #b0b0b0; }
        body { background: var(--bg); color: var(--text); font-family: sans-serif; margin: 0; }
        .container { max-width: 500px; margin: 0 auto; min-height: 100vh; display: flex; flex-direction: column; }
        header { padding: 15px; border-bottom: 1px solid #333; text-align: center; background: rgba(15,15,15,0.9); position: sticky; top: 0; z-index: 10; }
        .logo { color: var(--accent); font-size: 1.5rem; font-weight: 800; margin: 0; }
        .gallery { padding: 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        .card { background: var(--card); border-radius: 15px; overflow: hidden; text-decoration: none; color: inherit; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
        .card-img { height: 200px; background-size: cover; background-position: center; }
        .card-info { padding: 10px; }
        .card-info h3 { margin: 0; font-size: 1.1rem; }
        .view { display: none; flex-direction: column; flex: 1; }
        .view.active { display: flex; }
        .profile-img { width: 100%; height: 400px; object-fit: cover; }
        .profile-content { padding: 20px; }
        .btn { display: block; background: var(--accent); color: white; text-align: center; padding: 15px; border-radius: 30px; text-decoration: none; font-weight: bold; margin-top: 20px; border: none; cursor: pointer; width: 100%; box-sizing: border-box; }
        .chat-area { flex: 1; display: flex; flex-direction: column; height: calc(100vh - 130px); }
        .messages { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .msg { max-width: 85%; padding: 12px 16px; border-radius: 20px; font-size: 0.95rem; line-height: 1.4; }
        .msg.user { align-self: flex-end; background: var(--accent); border-bottom-right-radius: 4px; }
        .msg.ai { align-self: flex-start; background: #262626; border-bottom-left-radius: 4px; }
        .input-box { padding: 15px; background: #1a1a1a; display: flex; gap: 10px; }
        input { flex: 1; background: #262626; border: none; padding: 12px 20px; border-radius: 25px; color: white; outline: none; }
        .photo-btn { background: #333; border: none; border-radius: 50%; width: 45px; color: white; cursor: pointer; font-size: 1.2rem; }
        .send-btn { background: var(--accent); border: none; border-radius: 50%; width: 45px; color: white; cursor: pointer; font-size: 1.2rem; }
        .photo-msg { width: 100%; max-width: 250px; border-radius: 12px; margin-top: 10px; }
        .loading { font-size: 0.8rem; color: var(--accent); font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div id="nav-back" style="display:none; position:absolute; left:15px; cursor:pointer; font-size:1.5rem;">←</div>
            <h1 class="logo">Dream AI</h1>
        </header>

        <div id="gallery-view" class="view active">
            <div class="gallery">
                {% for id, g in girls.items() %}
                <div class="card" onclick="showProfile('{{id}}')">
                    <div class="card-img" style="background-image: url('{{g.photo}}')"></div>
                    <div class="card-info">
                        <h3>{{g.name}}, {{g.age}}</h3>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <div id="profile-view" class="view">
            <img id="p-img" class="profile-img">
            <div class="profile-content">
                <h2 id="p-name"></h2>
                <p id="p-tagline" style="color:var(--accent); font-weight:600;"></p>
                <p id="p-bio"></p>
                <button class="btn" onclick="startChat()">Démarrer le Chat</button>
            </div>
        </div>

        <div id="chat-view" class="view">
            <div id="chat-msgs" class="messages"></div>
            <div class="input-box">
                <button class="photo-btn" onclick="sendManualPhoto()">📷</button>
                <input type="text" id="user-input" placeholder="Message...">
                <button class="send-btn" onclick="sendMsg()">➤</button>
            </div>
        </div>
    </div>

    <script>
        const girls = {{ girls_json|safe }};
        let currentGirlId = null;
        let history = [];

        function showView(id) {
            document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            document.getElementById('nav-back').style.display = id === 'gallery-view' ? 'none' : 'block';
        }

        document.getElementById('nav-back').onclick = () => {
            if (document.getElementById('chat-view').classList.contains('active')) showView('profile-view');
            else showView('gallery-view');
        };

        function showProfile(id) {
            currentGirlId = id;
            const g = girls[id];
            document.getElementById('p-img').src = g.photo;
            document.getElementById('p-name').innerText = g.name + ', ' + g.age;
            document.getElementById('p-tagline').innerText = g.tagline;
            document.getElementById('p-bio').innerText = g.bio;
            showView('profile-view');
        }

        function startChat() {
            history = [];
            document.getElementById('chat-msgs').innerHTML = '';
            addMsg('ai', "Salut... J'espère que tu as une bonne raison de me déranger.");
            showView('chat-view');
        }

        function addMsg(role, text) {
            const div = document.createElement('div');
            div.className = 'msg ' + role;
            
            if (text.includes('[PHOTO:')) {
                const match = text.match(/\[PHOTO:(.*?)\]/);
                const desc = match[1];
                const visible = text.replace(/\[PHOTO:.*?\]/, '').trim();
                div.innerText = visible;
                if (visible) document.getElementById('chat-msgs').appendChild(div);
                
                const photoDiv = document.createElement('div');
                photoDiv.className = 'msg ai';
                document.getElementById('chat-msgs').appendChild(photoDiv);
                generatePhoto(desc, photoDiv);
            } else {
                div.innerText = text;
                document.getElementById('chat-msgs').appendChild(div);
            }
            history.push({role: role === 'user' ? 'user' : 'assistant', content: text});
            const m = document.getElementById('chat-msgs');
            m.scrollTop = m.scrollHeight;
        }

        async function sendMsg() {
            const inp = document.getElementById('user-input');
            const val = inp.value.trim();
            if (!val) return;
            inp.value = '';
            addMsg('user', val);
            
            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({girl_id: currentGirlId, messages: history})
                });
                const data = await res.json();
                addMsg('ai', data.content);
            } catch(e) { console.error(e); }
        }

        async function sendManualPhoto() {
            const div = document.createElement('div');
            div.className = 'msg ai';
            document.getElementById('chat-msgs').appendChild(div);
            generatePhoto("selfie, smiling, looking at camera", div);
        }

        async function generatePhoto(desc, div) {
            const spin = document.createElement('div');
            spin.className = 'loading';
            spin.innerText = "En train de prendre une photo...";
            div.appendChild(spin);
            
            try {
                const res = await fetch('/photo', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({girl_id: currentGirlId, prompt: desc})
                });
                const data = await res.json();
                const url = data.image_url || data.url || (data.data && data.data[0] && data.data[0].url);
                if (url) {
                    const img = document.createElement('img');
                    img.src = url;
                    img.className = 'photo-msg';
                    div.appendChild(img);
                }
            } catch(e) { console.error(e); }
            finally { spin.remove(); }
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    import json
    return render_template_string(HTML_TEMPLATE, girls=GIRLS, girls_json=json.dumps(GIRLS))

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json
    girl = GIRLS.get(data.get("girl_id"))
    messages = data.get("messages", [])
    
    system = f"{girl['personality']} Tu parles sur 'Dream AI'. Réponds en français. Sois flirty. Photo tag: [PHOTO: description in English]."
    if not any(m.get("role") == "system" for m in messages):
        messages.insert(0, {"role": "system", "content": system})

    try:
        r = requests.post(
            "https://api.deepinfra.com/v1/openai/chat/completions",
            json={"model": "meta-llama/Meta-Llama-3.1-8B-Instruct", "messages": messages, "temperature": 0.7},
            timeout=60
        )
        return jsonify(r.json()['choices'][0]['message'])
    except: return jsonify({"content": "Désolée, petit souci."}), 500

@app.route("/photo", methods=["POST"])
def photo():
    key = os.environ.get("PROMPTCHAN_KEY")
    data = request.json
    girl = GIRLS.get(data.get("girl_id"))
    prompt = f"{girl['appearance']}, {data.get('prompt')}, high quality, cinematic"
    
    payload = {
        "style": "Photo XL+ v2", "pose": "Default", "prompt": prompt,
        "quality": "Ultra", "age_slider": girl["age"], "creativity": 50,
        "restore_faces": True, "seed": -1
    }
    
    try:
        r = requests.post(
            "https://prod.aicloudnetservices.com/api/external/create",
            headers={"x-api-key": key}, json=payload, timeout=60
        )
        return jsonify(r.json())
    except: return jsonify({"error": "Failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
