from flask import Flask, render_template, request, jsonify
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
        "personality": "Tu es Anastasia, 35 ans, PDG russe. Froide, directe et exigeante au début. Tu t'ouvres progressivement si l'homme est intéressant. Tu es sexy, sûre de toi et dominatrice.",
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

@app.route("/")
def index():
    return render_template("index.html", girls=GIRLS.values())

@app.route("/profile/<girl_id>")
def profile(girl_id):
    girl = GIRLS.get(girl_id)
    if not girl:
        return "Girl not found", 404
    return render_template("profile.html", girl=girl)

@app.route("/chat/<girl_id>")
def chat_view(girl_id):
    girl = GIRLS.get(girl_id)
    if not girl:
        return "Girl not found", 404
    return render_template("chat.html", girl=girl)

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json
    girl_id = data.get("girl_id")
    messages = data.get("messages", [])
    girl = GIRLS.get(girl_id)
    
    if not girl:
        return jsonify({"error": "Girl not found"}), 404

    system_prompt = f"{girl['personality']} Tu parles sur une app de rencontre nommée 'Dream AI'. Réponds en français. Sois flirty et séductrice. Quand tu veux envoyer une photo, termine TOUJOURS ton message par [PHOTO: description en anglais de la scène]."
    
    if not any(m.get("role") == "system" for m in messages):
        messages.insert(0, {"role": "system", "content": system_prompt})

    try:
        response = requests.post(
            "https://text.pollinations.ai/",
            json={
                "messages": messages,
                "model": "openai",
                "seed": random.randint(1, 1000000)
            },
            timeout=60
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/photo", methods=["POST"])
def photo():
    api_key = os.environ.get("PROMPTCHAN_KEY")
    if not api_key:
        return jsonify({"error": "API key missing"}), 400
        
    data = request.json
    girl_id = data.get("girl_id")
    description = data.get("prompt", "")
    girl = GIRLS.get(girl_id)
    
    base_prompt = girl["appearance"] if girl else "a beautiful woman"
    full_prompt = f"{base_prompt}, {description}, high quality, cinematic lighting, masterpiece"

    payload = {
        "style": "Photo XL+ v2",
        "pose": "Default",
        "prompt": full_prompt,
        "quality": "Ultra",
        "age_slider": girl["age"] if girl else 35,
        "creativity": 50,
        "restore_faces": True,
        "seed": -1
    }
    
    try:
        response = requests.post(
            "https://prod.aicloudnetservices.com/api/external/create",
            headers={"x-api-key": api_key},
            json=payload,
            timeout=60
        )
        print(f"DEBUG: API Response Status: {response.status_code}")
        response_data = response.json()
        print(f"DEBUG: API Response Body: {response_data}")
        return jsonify(response_data)
    except Exception as e:
        print(f"DEBUG: /photo error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
