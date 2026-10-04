"""
=============================================================================
ভয়েস মডিউল: ভয়েস লিসেনার (VOICE LISTENER)
=============================================================================
মাইক্রোফোন থেকে ইউজারের মুখের কথা শোনা এবং র-টেক্সট ও কমান্ড কিউতে পাঠানো।
১০০% ফ্রি - SoundDevice এবং Google পাবলিক রিকগনিশন।
"""

import threading
import queue
import time
import numpy as np
import sounddevice as sd
import speech_recognition as sr
from config import ACTIVE_LANGUAGE
from languages import load_language

class VoiceListener:
    def __init__(self, sample_rate=16000, chunk_duration=1.2):
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.recognizer = sr.Recognizer()
        self.command_queue = queue.Queue()
        self.raw_text_queue = queue.Queue()

        self.lang_pack = load_language(ACTIVE_LANGUAGE)

        self.is_running = False
        self.audio_level = 0.0
        self.last_heard_text = "শুনছি..."

    def set_language(self, lang_name):
        self.lang_pack = load_language(lang_name)
        print(f"[ভয়েস মডিউল] ভাষা পরিবর্তন হয়েছে: {self.lang_pack.LANG_NAME}")

    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.thread = threading.Thread(target=self._listen_worker, daemon=True)
        self.thread.start()

    def stop(self):
        self.is_running = False

    def _listen_worker(self):
        chunk_samples = int(self.sample_rate * self.chunk_duration)

        while self.is_running:
            try:
                audio_block = sd.rec(
                    chunk_samples,
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype='int16'
                )
                sd.wait()

                raw = audio_block.flatten()
                rms = np.sqrt(np.mean(raw.astype(np.float64) ** 2))
                self.audio_level = min(1.0, float(rms / 1000.0))

                if rms > 160:
                    self.last_heard_text = "Processing audio..."
                    audio_bytes = audio_block.tobytes()
                    audio_data = sr.AudioData(audio_bytes, self.sample_rate, 2)

                    text = None
                    # 1. Try English (en-US) first so English words are transcribed in English
                    try:
                        text = self.recognizer.recognize_google(
                            audio_data,
                            language="en-US"
                        )
                    except Exception:
                        text = None

                    # 2. If English didn't match (user spoke Bengali), fallback to Bengali (bn-BD)
                    if not text:
                        try:
                            text = self.recognizer.recognize_google(
                                audio_data,
                                language="bn-BD"
                            )
                        except Exception:
                            text = None

                    if text:
                        text_clean = text.strip()
                        self.last_heard_text = f'"{text_clean}"'
                        self.raw_text_queue.put((text_clean, audio_bytes))

                        cmd = self._match_command(text_clean)
                        if cmd:
                            self.command_queue.put(cmd)
                    else:
                        self.last_heard_text = "Listening..."
                else:
                    self.audio_level = max(0.05, self.audio_level * 0.7)

            except Exception as e:
                time.sleep(0.5)

    def _match_command(self, text):
        text_lower = text.lower().strip()
        commands_dict = self.lang_pack.COMMANDS

        for action_name, phrase_list in commands_dict.items():
            for phrase in phrase_list:
                if phrase.lower() in text_lower or text_lower in phrase.lower():
                    return action_name
        return None

    def get_command(self):
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None

    def get_raw_text(self):
        try:
            return self.raw_text_queue.get_nowait()
        except queue.Empty:
            return None
