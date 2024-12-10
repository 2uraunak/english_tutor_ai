# English Tutor AI Assistant

An offline-first English learning assistant that helps improve your English fluency through natural conversations and provides feedback on grammar, vocabulary, and pronunciation.

## Features

- Interactive conversations about daily topics
- Grammar and vocabulary analysis
- Speech-to-text and text-to-speech support
- Progress tracking and improvement suggestions
- Completely offline functionality for core features
- Free and open-source

## Setup Instructions

1. Install Python 3.8 or higher
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```
3. Download Vosk model:
   - Create a `models` directory
   - Download the English model from https://alphacephei.com/vosk/models
   - Extract it to the `models` directory

4. Run the application:
   ```
   python app.py
   ```

## Usage

1. Launch the application using the command above
2. Choose between text or speech input mode
3. Start conversing with the AI tutor
4. View feedback and suggestions in real-time
5. Check your progress in the History tab

## Project Structure

- `app.py`: Main application file
- `conversation.py`: Conversation handling and response generation
- `language_analysis.py`: Grammar and vocabulary analysis
- `speech_handler.py`: Speech-to-text and text-to-speech processing
- `database.py`: Progress tracking and storage
- `models/`: Directory for Vosk speech recognition models
- `static/`: Static files for the web interface
- `templates/`: HTML templates
