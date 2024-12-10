from flask import Flask, render_template, request, jsonify
from conversation import ConversationHandler
from language_analysis import LanguageAnalyzer
from speech_handler import SpeechHandler
from database import DatabaseManager
import os

app = Flask(__name__)

# Initialize components
conversation_handler = ConversationHandler()
language_analyzer = LanguageAnalyzer()
speech_handler = SpeechHandler()
db_manager = DatabaseManager()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    input_type = data.get('type', 'text')  # 'text' or 'speech'
    
    # Process input
    if input_type == 'speech':
        user_input = speech_handler.speech_to_text(user_input)
    
    # Analyze language
    analysis = language_analyzer.analyze(user_input)
    
    # Generate response
    response = conversation_handler.generate_response(user_input)
    
    # Store interaction
    db_manager.store_interaction(user_input, response, analysis)
    
    return jsonify({
        'response': response,
        'analysis': analysis,
        'suggestions': language_analyzer.get_suggestions(user_input)
    })

@app.route('/speak', methods=['POST'])
def speak():
    text = request.json.get('text', '')
    audio_path = speech_handler.text_to_speech(text)
    return jsonify({'audio_path': audio_path})

@app.route('/progress')
def progress():
    return jsonify(db_manager.get_progress_report())

if __name__ == '__main__':
    app.run(debug=True)
