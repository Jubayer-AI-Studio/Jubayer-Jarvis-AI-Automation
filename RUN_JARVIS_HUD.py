"""
=============================================================================
JUBAYER AI: CINEMATIC JARVIS INTERACTIVE LAUNCHER (v4.5)
=============================================================================
- ওপেন করলেই অপ্রয়োজনীয় উইন্ডো ক্লিন করে সিনেমাটিক সাই-ফাই ভাইব
- বড় ভাসমান স্বচ্ছ আয়রন ম্যান জার্ভিস আর্করিয়্যাক্টর
- লাইভ মাইক্রোফোন ডিটেকশন (raw_text_queue থেকে তাৎক্ষণিক প্রতিটি কথা পড়া)
- মুখের আওয়াজের সাথে সাথে আর্করিয়্যাক্টরের পালস ও রঙের রূপান্তর (Emotion Engine)
- ৩ ভাষায় (বাংলা, English, বাংলিশ) অবিরাম কথা বলা ও অনুমতি গ্রহণ
=============================================================================
"""

import sys
import os
import time
import threading
import ctypes
import pyautogui

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from ui.cinematic_jarvis_reactor import CinematicJarvisReactor
from voice.speech_feedback import SpeechFeedback
from voice.voice_listener import VoiceListener
from CONVERSATIONAL_PERMISSION_AGENT import TrilingualConversationalAgent

class CinematicJarvisLauncher:
    def __init__(self):
        print("\n" + "=" * 65)
        print("      🚀 INITIALIZING CINEMATIC JARVIS HUD & EMOTION CORE 🚀")
        print("=" * 65 + "\n")

        # ১. ডেস্কটপ ক্লিন করা (সিনেমাটিক সাই-ফাই লুকের জন্য)
        try:
            pyautogui.hotkey('win', 'd')
            time.sleep(0.3)
        except Exception:
            pass

        # ২. কনসোল উইন্ডো ব্যাকগ্রাউন্ডে মিনিমাইজ করা
        try:
            console_hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if console_hwnd:
                ctypes.windll.user32.ShowWindow(console_hwnd, 6) # SW_MINIMIZE
        except Exception:
            pass

        # ৩. ইঞ্জিনসমূহ লোড
        self.hud = CinematicJarvisReactor()
        self.sf = SpeechFeedback()
        self.agent = TrilingualConversationalAgent(speech_feedback=self.sf)
        self.listener = VoiceListener()

        # স্বাগতম বার্তা
        self.hud.set_emotion("LISTENING", "INITIALIZING SYSTEMS...")
        self.sf.speak("আসসালামু আলাইকুম স্যার! জুবায়ের সিস্টেম সক্রিয় হয়েছে। আমি আপনার কথা শুনতে প্রস্তুত।")
        self.hud.set_emotion("IDLE", "SYSTEM ONLINE // LISTENING FOR VOICE")

        # ৪. ভয়েস লিসেনার সক্রিয়
        self.listener.start()
        print("[JARVIS] Microphone listener started. Speak in Bangla, English, or Banglish!")

        # ৫. রিয়েল-টাইম ইভেন্ট লুপ সিডিউল
        self.hud.root.after(30, self._poll_voice_and_audio)

    def _poll_voice_and_audio(self):
        """প্রতি ৩০ মিলিসেকেন্ডে মাইকের সাউন্ড ও রিকগনাইজড কথা চেক করা"""
        try:
            # মাইকের শব্দের তীব্রতা অনুযায়ী অর্বের গ্লো পালস আপডেট
            live_level = getattr(self.listener, 'audio_level', 0.05)
            self.hud.set_audio_level(live_level)

            # মাইকে ব্যবহারকারীর কোনো নতুন কথা ধরা পড়েছে কি না?
            raw_item = self.listener.get_raw_text()
            if raw_item:
                if isinstance(raw_item, tuple):
                    user_speech, _ = raw_item
                else:
                    user_speech = raw_item

                if user_speech and user_speech.strip():
                    print(f"\n[MIC HEARD]: \"{user_speech}\"")

                    # ১. তাৎক্ষণিক সোনালী আলোতে রূপান্তর (LISTENING)
                    self.hud.set_emotion("LISTENING", f"HEARD: '{user_speech[:20]}...'")
                    self.hud.set_audio_level(0.9)

                    # ২. প্রসেসিং ও উত্তর দেওয়ার জন্য থ্রেডে পাঠানো যাতে UI আটকে না যায়
                    threading.Thread(target=self._process_speech_thread, args=(user_speech,), daemon=True).start()

        except Exception as e:
            print(f"[POLL ERROR]: {e}")
        finally:
            self.hud.root.after(30, self._poll_voice_and_audio)

    def _process_speech_thread(self, speech_text):
        """কথা বিশ্লেষণ করে উত্তর দেওয়া ও ইমোশন স্টেট আপডেট করা"""
        try:
            time.sleep(0.3)
            # প্রসেসিং (পার্পল রঙ)
            self.hud.set_emotion("THINKING", "ANALYZING YOUR INTENT...")

            # কথোপকথন এজেন্ট দিয়ে প্রসেসিং
            self.agent.process_user_input(speech_text)

            if self.agent.waiting_for_permission:
                # অনুমতি চাইছে (সবুজ এমারেল্ড রঙ)
                self.hud.set_emotion("PERMISSION", "AWAITING YOUR PERMISSION ('হ্যাঁ' বলুন)")
            else:
                # কাজ সম্পন্ন বা সাধারণ কথা শেষ (কুল সায়ান রঙ)
                time.sleep(1.5)
                self.hud.set_emotion("IDLE", "SYSTEM ONLINE // LISTENING FOR VOICE")

        except Exception as err:
            print(f"[PROCESS ERROR]: {err}")
            self.hud.set_emotion("IDLE", "SYSTEM ONLINE // STANDBY")

    def run(self):
        self.hud.run()

if __name__ == "__main__":
    app = CinematicJarvisLauncher()
    app.run()
