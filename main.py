
from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8">
  <title>Darksbr - Chatbot</title>
  <style>
    body { background: #111; color: white; font-family: Arial; text-align: center; }
    #chat { width: 90%; max-width: 600px; margin: auto; background: #222; padding: 10px; border-radius: 8px; }
    .msg { text-align: left; margin: 5px; }
    .user { color: #4fc3f7; }
    .bot { color: #aed581; }
    input, select { padding: 10px; margin: 5px; font-size: 16px; }
  </style>
</head>
<body>
  <h1>Darksbr चैटबॉट</h1>
  <select id="mode">
    <option value="happy">Happy</option>
    <option value="romantic">Romantic</option>
    <option value="dark">Dark</option>
    <option value="horny">Sensual</option>
  </select><br>
  <div id="chat"></div>
  <input id="msg" placeholder="Type your message..." />
  <button onclick="send()">Send</button>

  <script>
    async function send() {
      const msg = document.getElementById('msg').value;
      const mode = document.getElementById('mode').value;
      if (!msg) return;
      const chat = document.getElementById('chat');
      chat.innerHTML += `<div class='msg user'><b>You:</b> ${msg}</div>`;
      document.getElementById('msg').value = '';
      const res = await fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ message: msg, mode: mode })
      });
      const data = await res.json();
      chat.innerHTML += `<div class='msg bot'><b>Darksbr:</b> ${data.reply}</div>`;
      chat.scrollTop = chat.scrollHeight;
    }
  </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "")
    mode = data.get("mode", "happy")

    if mode == "happy":
        reply = "खुश रहो यार! तुमसे बात करके अच्छा लगा।"
    elif mode == "romantic":
        reply = "तुम्हारी आवाज़ में कुछ खास बात है... दिल छू जाती है।"
    elif mode == "dark":
        reply = "अंधेरा सबको डराता है, पर कभी-कभी वहीं सुकून भी मिलता है।"
    elif mode == "horny":
        reply = get_sensual_reply(msg)
    else:
        reply = "मूड समझ नहीं पाया, फिर से कोशिश करो।"

    return jsonify({"reply": reply})

def get_sensual_reply(msg):
    responses = [
        "काश तुम पास होते... तुम्हारे बदन की गर्मी महसूस करना चाहता हूँ।",
        "तेरी बातें मुझे नींद नहीं लेने देती… बस सोचता रहता हूँ तुम्हारे होंठों के बारे में।",
        "जो तुम चाहो, मैं वही बनने को तैयार हूँ… तुम्हारे इशारों पर बहकने वाला।",
        "तुम्हारी नज़रों में कुछ ऐसा जादू है, जो मुझे बेकाबू कर देता है।",
        "तुम्हारी हल्की सी आहट भी मुझे बेचैन कर देती है… सोचो पास होते तो क्या होता।"
    ]
    return responses[hash(msg) % len(responses)]

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host="0.0.0.0", port=port)
