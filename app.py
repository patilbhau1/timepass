import os
from flask import Flask, render_template, request, jsonify
import ollama
import pyttsx3
from werkzeug.utils import secure_filename
import threading

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

engine = pyttsx3.init()

def speak_text(text):
    def _speak():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak).start()

def get_image_description(image_path):
    response = ollama.chat(
        model="llava",
        messages=[
            {
                'role': 'user',
                'content': ('You are an AI assistant made to guide blind people in India '
                            'and help them in their daily life by telling them about the '
                            'image provided to you. Give answers in short and simple words '
                            'so the blind person can react to it quickly.'),
                'images': [image_path]
            }
        ]
    )
    return response['message']['content']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        description = get_image_description(file_path)
        speak_text(description)
        return jsonify({'description': description})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
