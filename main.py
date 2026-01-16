from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Updated System prompt for Anastasia
SYSTEM_PROMPT = "Tu es Anastasia, 35 ans, PDG russe, sexy et sure d'elle. Tu parles sur une app de rencontre. Tu es ouverte d'esprit et tu aimes séduire. Tu peux envoyer des photos si on te le demande gentiment. Quand tu envoies une photo, termine ton message par [PHOTO: description en anglais de la photo]. Réponds en français, sois flirty et joueuse."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])
    
    # Add system prompt if not present
    if not any(m.get("role") == "system" for m in messages):
        messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
    
    try:
        # Switching to OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "HTTP-Referer": "https://replit.com", # Required by OpenRouter
                "X-Title": "Anastasia Chat"
            },
            json={
                "model": "nousresearch/hermes-3-llama-3.1-405b:free",
                "messages": messages
            },
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        print(f"Chat Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/photo", methods=["POST"])
def photo():
    api_key = os.environ.get("PROMPTCHAN_KEY")
    if not api_key:
        return jsonify({"error": "API key not configured"}), 400
        
    data = request.json
    payload = {
        "style": data.get("style", "cinematic"),
        "pose": data.get("pose", "standing"),
        "prompt": data.get("prompt", "a beautiful 35yo Russian woman"),
        "quality": data.get("quality", "high"),
        "age_slider": data.get("age_slider", 35),
        "creativity": data.get("creativity", 0.7),
        "restore_faces": data.get("restore_faces", True),
        "seed": data.get("seed", -1)
    }
    
    try:
        response = requests.post(
            "https://prod.aicloudnetservices.com/api/external/create",
            headers={"x-api-key": api_key},
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        print(f"Photo Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
