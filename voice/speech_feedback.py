"""
=============================================================================
ভয়েস মডিউল: হাইব্রিড স্পিচ ফিডব্যাক (BENGALI NEURAL TTS + SAPI5)
=============================================================================
- খাঁটি ও বিশুদ্ধ বাংলাদেশী বাংলা কণ্ঠ (Microsoft Neural: bn-BD-PradeepNeural)
- কোনো রোবোটিক বা ভাঙা উচ্চারণ নয়, ১০০% মানুষের মতো স্বাভাবিক বাংলা কথা বলা
- উইন্ডোজ বিল্ট-ইন MCI মাল্টিমিডিয়া ড্রাইভার দিয়ে কোনো উইন্ডো ছাড়াই ব্যাকগ্রাউন্ড প্লেব্যাক
- সম্পূর্ণ ফ্রি এবং অফলাইন ফলব্যাক সুবিধাসহ
=============================================================================
"""

import os
import sys
import time
import re
import queue
import threading
import asyncio
import ctypes
import edge_tts
import pyttsx3

class SpeechFeedback:
    def __init__(self, speech_rate=175):
        self.tts_queue = queue.Queue()
        self.speech_rate = speech_rate
        self.temp_audio_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "temp_tts_voice.mp3"))

        # ব্যাকগ্রাউন্ড ওয়ার্কার থ্রেড চালু
        self.worker_thread = threading.Thread(target=self._run_tts, daemon=True)
        self.worker_thread.start()

    def speak(self, text):
        """যেকোনো টেক্সট কিউতে পাঠায়"""
        if text and text.strip():
            self.tts_queue.put(text.strip())

    def _speak_bengali_edge(self, text):
        """খাঁটি বাংলা কণ্ঠে উচ্চারণ করা"""
        async def _generate():
            comm = edge_tts.Communicate(text, "bn-BD-PradeepNeural")
            await comm.save(self.temp_audio_path)

        asyncio.run(_generate())

        # উইন্ডোজের বিল্ট-ইন winmm MCI ড্রাইভার দিয়ে সরাসরি ব্যাকগ্রাউন্ডে প্লে করা
        ctypes.windll.winmm.mciSendStringW(f'open "{self.temp_audio_path}" type mpegvideo alias jubayer_tts', None, 0, None)
        ctypes.windll.winmm.mciSendStringW('play jubayer_tts wait', None, 0, None)
        ctypes.windll.winmm.mciSendStringW('close jubayer_tts', None, 0, None)

    def _speak_english_sapi(self, text, engine):
        """ইংরেজি কণ্ঠ উচ্চারণ"""
        if engine:
            engine.say(text)
            engine.runAndWait()

    def _run_tts(self):
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', self.speech_rate)
            engine.setProperty('volume', 1.0)
            voices = engine.getProperty('voices')
            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id)
        except Exception:
            engine = None

        while True:
            text = self.tts_queue.get()
            if text:
                try:
                    has_bangla = bool(re.search(r'[\u0980-\u09FF]', text))
                    if has_bangla:
                        try:
                            self._speak_bengali_edge(text)
                        except Exception as e_bn:
                            print(f"[বাংলা TTS ফলব্যাক]: {e_bn}")
                            # ফলব্যাক: ইংরেজি ইঞ্জিন
                            if engine:
                                engine.say("Sir, I am executing your command.")
                                engine.runAndWait()
                    else:
                        # ইংরেজি বা রোমান টেক্সট
                        self._speak_english_sapi(text, engine)
                except Exception as e:
                    print(f"[TTS প্লেব্যাক ত্রুটি]: {e}")

            self.tts_queue.task_done()

if __name__ == "__main__":
    sf = SpeechFeedback()
    print("Testing SpeechFeedback...")
    sf.speak("আসসালামু আলাইকুম স্যার! আমি জুবায়ের, এখন থেকে আমি বাংলায় কথা বলছি।")
    time.sleep(5.0)
    print("Test complete.")
