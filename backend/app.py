from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

openai.api_key = 'YOUR_OPENAI_API_KEY'  # Replace with your OpenAI API key

@app.route('/update_text', methods=['POST'])
def update_text():
    data = request.json
    text = data['text']
    target_language = data['target_language']

    detected_language = detect_language(text)
    translated_text = translate_text(text, target_language)

    return jsonify({
        'detected_language': detected_language,
        'translated_text': translated_text
    })

def detect_language(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Detect the language of the following text:\n\n{text}",
        max_tokens=10,
        n=1,
        stop=None,
        temperature=0.0,
    )
    return response.choices[0].text.strip()

def translate_text(text, target_language):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate the following text to {target_language}:\n\n{text}",
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.0,
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    app.run(debug=True)
