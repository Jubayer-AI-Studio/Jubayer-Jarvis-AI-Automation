"""
Multilingual Voice Perception & TTS Engine for JARVIS-AETHER
Uses SoundDevice for low-latency audio capture and SpeechRecognition
to recognize English, Bengali (বাংলা), Urdu (اردو), and Arabic (العربية).
Uses pyttsx3 for offline, zero-cost futuristic voice feedback.
100% Free & Open-Source (No Paid APIs).
"""

import threading
import queue
import time
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import pyttsx3
from config import VOICE_COMMANDS, VOICE_RESPONSES

class VoiceEngine:
    def __init__(self, sample_rate=16000, chunk_duration=3.0, energy_threshold=500):
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.energy_threshold = energy_threshold

        self.recognizer = sr.Recognizer()
        self.command_queue = queue.Queue()
        self.tts_queue = queue.Queue()

        self.is_running = False
        self.last_recognized_text = "JARVIS LISTENING..."
        self.last_command = None
        self.audio_level = 0.0  # Normalized 0.0 to 1.0 for HUD waveform visualizer

        # Active voice language list (cycles through or attempts primary)
        self.supported_languages = [
            {"code": "en-US", "name": "ENGLISH"},
            {"code": "bn-BD", "name": "বাংলা (BENGALI)"},
            {"code": "ur-PK", "name": "اردو (URDU)"},
            {"code": "ar-SA", "name": "العربية (ARABIC)"}
        ]
        self.current_lang_idx = 0  # Default to English / Bengali dual

        # Initialize TTS in dedicated background thread
        self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
        self.tts_thread.start()

    def start(self):
        """Starts background voice listening thread"""
        if self.is_running:
            return
        self.is_running = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()

    def stop(self):
        """Stops background listening"""
        self.is_running = False

    def cycle_language(self):
        """Cycles active voice recognition language"""
        self.current_lang_idx = (self.current_lang_idx + 1) % len(self.supported_languages)
        lang = self.get_current_language()
        self.speak(f"Language set to {lang['name']}")
        return lang

    def get_current_language(self):
        return self.supported_languages[self.current_lang_idx]

    def speak(self, text):
        """Queues text to be spoken asynchronously without blocking"""
        if text:
            self.tts_queue.put(text)

    def _tts_worker(self):
        """Dedicated thread for pyttsx3 to prevent COM threading issues on Windows"""
        try:
            engine = pyttsx3.init()
            # Set futuristic fast rate & clear volume
            engine.setProperty('rate', 175)
            engine.setProperty('volume', 1.0)
            
            # Select best available voice (often Microsoft Zira or David on Windows)
            voices = engine.getProperty('voices')
            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id) # Often female/clearer
        except Exception as e:
            engine = None
            print(f"[VoiceEngine TTS Error] {e}")

        while True:
            text = self.tts_queue.get()
            if text and engine:
                try:
                    engine.say(text)
                    engine.runAndWait()
                except Exception as e:
                    print(f"[TTS Playback Error] {e}")
            self.tts_queue.task_done()

    def _listen_loop(self):
        """Audio capture and continuous speech recognition worker"""
        chunk_samples = int(self.sample_rate * self.chunk_duration)

        while self.is_running:
            try:
                # Record audio chunk via SoundDevice
                audio_block = sd.rec(
                    chunk_samples,
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype='int16'
                )
                sd.wait()

                # Calculate RMS audio energy for silence detection & HUD visualizer
                raw_data = audio_block.flatten()
                rms = np.sqrt(np.mean(raw_data.astype(np.float64) ** 2))
                self.audio_level = min(1.0, float(rms / 1200.0))

                # If sound energy is higher than background noise, process speech
                if rms > 250:
                    self.last_recognized_text = "PROCESSING AUDIO..."
                    audio_bytes = audio_block.tobytes()
                    audio_data = sr.AudioData(audio_bytes, self.sample_rate, 2)

                    # Recognize using current language, with automatic fallback
                    recognized_text = self._recognize_multilingual(audio_data)

                    if recognized_text:
                        self.last_recognized_text = f'"{recognized_text.strip()}"'
                        command = self._match_command(recognized_text)
                        if command:
                            self.last_command = command
                            self.command_queue.put(command)
                    else:
                        self.last_recognized_text = "LISTENING..."
                else:
                    self.audio_level = max(0.05, self.audio_level * 0.7)

            except Exception as e:
                time.sleep(0.5)

    def _recognize_multilingual(self, audio_data):
        """
        Attempts recognition in the primary active language.
        If that fails, tries fallback to English/Bengali.
        """
        primary_lang = self.get_current_language()["code"]
        languages_to_try = [primary_lang]

        # Add fallback languages if different from primary
        for fallback in ["en-US", "bn-BD", "ur-PK", "ar-SA"]:
            if fallback not in languages_to_try:
                languages_to_try.append(fallback)

        for lang in languages_to_try[:2]:  # Try primary + top fallback for low latency
            try:
                text = self.recognizer.recognize_google(audio_data, language=lang)
                if text:
                    return text.lower()
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                # Offline fallback or connection error
                break
            except Exception:
                continue

        return None

    def _match_command(self, text):
        """Matches recognized text against multilingual keyword dictionaries"""
        text_lower = text.lower().strip()

        for action_name, phrase_list in VOICE_COMMANDS.items():
            for phrase in phrase_list:
                if phrase.lower() in text_lower or text_lower in phrase.lower():
                    return action_name

        return None

    def get_latest_command(self):
        """Returns latest recognized command if available, else None"""
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None
