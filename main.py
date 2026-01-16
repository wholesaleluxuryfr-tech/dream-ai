from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Promptchan Test</title>
        <style>
            body { background: #121212; color: white; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            button { background: #ff4081; color: white; border: none; padding: 15px 30px; border-radius: 8px; font-size: 1.2rem; cursor: pointer; }
            #result { margin-top: 20px; text-align: center; }
            img { max-width: 90%; border-radius: 8px; margin-top: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
            .loading { color: #ff4081; }
        </style>
    </head>
    <body>
        <button id="testBtn">Test Promptchan API</button>
        <div id="result"></div>

        <script>
            document.getElementById('testBtn').onclick = async () => {
                const resDiv = document.getElementById('result');
                resDiv.innerHTML = '<p class="loading">Generating image... please wait...</p>';
                try {
                    const response = await fetch('/photo', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ prompt: "a beautiful 35yo woman, high quality, cinematic" })
                    });
                    const data = await response.json();
                    if (data.url || (data.data && data.data[0] && data.data[0].url)) {
                        const url = data.url || data.data[0].url;
                        resDiv.innerHTML = '<p>Success!</p><img src="' + url + '">';
                    } else {
                        resDiv.innerHTML = '<p>Error: ' + JSON.stringify(data) + '</p>';
                    }
                } catch (e) {
                    resDiv.innerHTML = '<p>Error: ' + e.message + '</p>';
                }
            };
        </script>
    </body>
    </html>
    """

@app.route("/photo", methods=["POST"])
def photo():
    api_key = os.environ.get("PROMPTCHAN_KEY")
    if not api_key:
        return jsonify({"error": "PROMPTCHAN_KEY environment variable is missing"}), 400
        
    data = request.json
    payload = {
        "style": "cinematic",
        "pose": "standing",
        "prompt": data.get("prompt", "a beautiful woman"),
        "quality": "Ultra",
        "age_slider": 35,
        "creativity": 0.7,
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
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
