
# --- IMPORTURI ---
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from backend.recommend import Chatbot
from backend.covergen import generate_cover
import os

# --- APP & INIT ---
app = Flask(__name__)
CORS(app)
chatbot = Chatbot()

# --- ROUTES ---
@app.route('/cover', methods=['POST'])
def cover():
    data = request.get_json()
    title = data.get('title', '')
    summary = data.get('summary', '')
    if not title or not summary:
        return jsonify({'error': 'Titlu și rezumat necesare'}), 400
    img_path = generate_cover(title, summary)
    if not img_path:
        return jsonify({'error': 'Eroare la generarea imaginii'}), 500
    return send_file(img_path, mimetype='image/png', as_attachment=False)

@app.route('/voice', methods=['POST'])
def voice():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'Textul este necesar'}), 400
    chatbot.get_voice(text)
    return send_file('out.mp3', mimetype='audio/mpeg', as_attachment=True, download_name='voce.mp3')

@app.route('/recommend', methods=['POST', 'GET'])
def recommend():
    if request.method == 'GET':
        return jsonify({"info": "Folosește metoda POST pentru a primi recomandări."}), 200
    data = request.get_json()
    user_message = data.get('message', '')
    ai_reply = chatbot.get_request(user_message)
    response = {
        'reply': ai_reply
    }
    return jsonify(response)

@app.route('/')
def index():
    return send_from_directory('frontend', 'main.html')

# --- MAIN ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
