import os
from flask import Flask, render_template, request, jsonify
import ollama
import pyttsx3
from werkzeug.utils import secure_filename
import threading
import queue

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

engine = None
engine_lock = threading.Lock()
speech_queue = queue.Queue()

def create_engine():
    global engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Adjust speech rate (words per minute)
    engine.setProperty('volume', 1.0)  # Set speech volume (0.0 to 1.0)

def get_engine():
    global engine
    if engine is None:
        with engine_lock:
            if engine is None:
                create_engine()
    return engine

def speak_text(text):
    try:
        engine = get_engine()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak_text: {e}")

def process_speech_queue():
    while True:
        text = speech_queue.get()
        speak_text(text)
        speech_queue.task_done()

def init_speech_queue_worker():
    worker = threading.Thread(target=process_speech_queue)
    worker.daemon = True
    worker.start()

init_speech_queue_worker()

def get_image_description(image_path):
    response = ollama.chat(
        model="llava",
        messages=[
            {
                'role': 'user',
                'content': ('You are an AI assistant made for guiding blind people in India '
                            'and help them in their daily life by telling them about the '
                            'surrounding. give an very short answer to the user and tell them  about the  surroundingsdont answer like i cant guide just twll about the image in short '),
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
        speech_queue.put(description)
        return jsonify({'description': description})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)
