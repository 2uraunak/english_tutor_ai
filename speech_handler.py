from vosk import Model, KaldiRecognizer
import sounddevice as sd
import numpy as np
from gtts import gTTS
import os
import wave
import json

class SpeechHandler:
    def __init__(self):
        # Initialize Vosk model for speech recognition
        model_path = "models/vosk-model-en-us-0.22"
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        
        # Audio recording parameters
        self.samplerate = 16000
        self.duration = 5  # seconds
        
    def record_audio(self):
        print("Recording...")
        recording = sd.rec(
            int(self.samplerate * self.duration),
            samplerate=self.samplerate,
            channels=1,
            dtype=np.int16
        )
        sd.wait()
        return recording
        
    def speech_to_text(self, audio_data=None):
        if audio_data is None:
            audio_data = self.record_audio()
            
        # Convert audio data to bytes
        audio_bytes = audio_data.tobytes()
        
        if self.recognizer.AcceptWaveform(audio_bytes):
            result = json.loads(self.recognizer.Result())
            return result.get('text', '')
        return ''
    
    def text_to_speech(self, text):
        # Generate speech from text using gTTS
        tts = gTTS(text=text, lang='en')
        
        # Save to temporary file
        output_path = 'static/temp_audio.mp3'
        tts.save(output_path)
        
        return output_path
