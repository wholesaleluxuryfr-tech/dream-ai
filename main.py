from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# System prompt for Anastasia
SYSTEM_PROMPT = "Tu es Anastasia, 35 ans, PDG russe. Froide au début, tu t'ouvres progressivement. Si tu envoies une photo: [PHOTO: description]"

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
        response = requests.post(
            "https://text.pollinations.ai/",
            json={"messages": messages, "model": "openai"},
            timeout=30
        )
        response.raise_for_status()
        return response.text
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/photo", methods=["POST"])
def photo():
    api_key = os.environ.get("PROMPTCHAN_KEY")
    if not api_key:
        return jsonify({"error": "API key not configured"}), 400
        
    data = request.json
    # Expected fields: style, pose, prompt, quality, age_slider, creativity, restore_faces, seed
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
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
