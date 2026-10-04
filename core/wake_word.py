"""
=============================================================================
CORE MODULE: ROBUST NATURAL LANGUAGE INTENT ENGINE (JUBAYER v3.2)
=============================================================================
- ক্রোম অটোমেটিক পপ-আপ সম্পূর্ণ বন্ধ।
- সরাসরি তাৎক্ষণিক পিসি শাটডাউন (ঝামেলামুক্ত)।
- ভয়েস স্লিপ ও মুখে ডাকলে সাথে সাথে পিসি ও স্ক্রিন অন।
"""

import time
import subprocess
import urllib.parse
import pyautogui

from config import AI_NAME, AI_NAME_ENGLISH
from core.voice_typing import VoiceTyper
from core.natural_brain import NaturalBrain, clean_and_normalize

class WakeWordDispatcher:
    def __init__(self, speech_feedback, system_controls, app_launcher, voice_lock=None, orb_ui=None):
        self.speech_feedback = speech_feedback
        self.system_controls = system_controls
        self.app_launcher = app_launcher
        self.voice_lock = voice_lock
        self.orb_ui = orb_ui
        self.voice_typer = VoiceTyper()
        self.brain = NaturalBrain()

        self.is_awake = False
        self.awake_timestamp = 0
        self.awake_timeout = 30.0

        self.status_message = f"{AI_NAME_ENGLISH} // READY"
        self._build_wake_words()

    def _build_wake_words(self):
        names = [
            "জুবায়ের", "জুবায়ের", "জোবায়ের", "জুবায়েদ", "জুবায়েদ",
            "jubayer", "jubayed", "jobayer", "zobayer",
            f"hey {AI_NAME_ENGLISH.lower()}", f"hi {AI_NAME_ENGLISH.lower()}",
            "hey jubayer", "hello jubayer", "hi jubayer",
            "হেই জুবায়ের", "হ্যালো জুবায়ের", "হাই জুবায়ের"
        ]
        self.normalized_wake_words = [clean_and_normalize(n) for n in names if n.strip()]

    def check_wake_word(self, norm_text):
        if not norm_text:
            return False
        for ww in self.normalized_wake_words:
            if ww in norm_text:
                return True
        return False

    def activate_wake(self):
        # যদি পিসি স্লিপে থাকে, ডাক শোনামাত্র অন করে দেওয়া
        if getattr(self.system_controls, 'is_display_sleeping', False):
            self.system_controls.wake_display()
            self.speech_feedback.speak("Welcome back, sir! System powered ON and ready.")
            return

        self.is_awake = True
        self.awake_timestamp = time.time()
        self.status_message = f"{AI_NAME_ENGLISH} // LISTENING..."
        if self.orb_ui:
            self.orb_ui.set_awake_state(True)
        self.speech_feedback.speak("Yes sir, I am listening! What should I do?")

    def process_speech(self, raw_text, audio_bytes=None):
        """Processes incoming voice with full semantic NLP understanding"""
        if not raw_text or len(raw_text.strip()) == 0:
            return False, None

        norm = clean_and_normalize(raw_text)
        print(f"[{AI_NAME_ENGLISH} Engine]: \"{raw_text}\"")

        # ১. ওয়েক ওয়ার্ড ডিটেকশন (স্লিপে থাকলে সাথে সাথে পিসি ও স্ক্রিন অন করবে)
        if self.check_wake_word(norm):
            self.activate_wake()

            # ওয়েক ওয়ার্ড বাদ দিয়ে বাকি কথা
            cleaned = norm
            for ww in self.normalized_wake_words:
                cleaned = cleaned.replace(ww, '').strip()

            greetings = ["hey", "hello", "hi", "হেই", "হ্যালো", "হাই", "শোনো", "listen"]
            for g in greetings:
                cleaned = cleaned.replace(g, '').strip()

            if len(cleaned) > 2:
                return self.execute_natural_intent(cleaned)
            return True, "WAKE_WORD"

        # ২. সরাসরি যেকোনো স্বাভাবিক কথা বা আদেশ কার্যকর করা
        return self.execute_natural_intent(raw_text)

    def execute_natural_intent(self, text):
        """Runs the NaturalBrain semantic parser and executes the intent"""
        intent, payload = self.brain.parse_intent(text)
        print(f"[{AI_NAME_ENGLISH} NLU]: Intent={intent} | Payload={payload}")

        # =====================================================================
        # ১. পিসি অন করা (WAKE UP SCREEN & PC)
        # =====================================================================
        if intent == "POWER_WAKE":
            self.system_controls.wake_display()
            self.speech_feedback.speak("Yes sir! System is ON and ready for your command.")
            return True, "POWER_WAKE"

        # =====================================================================
        # ২. পিসি শাটডাউন / অফ করা (সরাসরি কার্যকর)
        # =====================================================================
        elif intent == "POWER_SHUTDOWN":
            self.status_message = f"{AI_NAME_ENGLISH} // SHUTTING DOWN"
            self.speech_feedback.speak("Shutting down the computer, sir. Good night!")
            self.system_controls.execute_shutdown()
            return True, "POWER_SHUTDOWN"

        # পিসি স্লিপ / স্ক্রিন অফ (যাতে মুখে ডাকলে আবার অন হয়)
        elif intent == "POWER_SLEEP":
            self.status_message = f"{AI_NAME_ENGLISH} // SLEEPING"
            self.speech_feedback.speak("Entering sleep mode, sir. Call my name to turn back ON.")
            time.sleep(1.0)
            self.system_controls.sleep_display()
            return True, "POWER_SLEEP"

        elif intent == "POWER_RESTART":
            self.status_message = f"{AI_NAME_ENGLISH} // RESTARTING"
            self.speech_feedback.speak("Restarting the computer, sir.")
            self.system_controls.execute_restart()
            return True, "POWER_RESTART"

        elif intent == "POWER_LOCK":
            self.status_message = f"{AI_NAME_ENGLISH} // PC LOCKED"
            self.speech_feedback.speak("Locking workstation, sir.")
            self.system_controls.lock_pc()
            return True, "POWER_LOCK"

        # =====================================================================
        # ৩. ভলিউম ও সাউন্ড
        # =====================================================================
        elif intent == "VOLUME_UP":
            self.system_controls.volume_up(steps=5)
            self.speech_feedback.speak("Volume increased.")
            return True, "VOLUME_UP"

        elif intent == "VOLUME_DOWN":
            self.system_controls.volume_down(steps=5)
            self.speech_feedback.speak("Volume decreased.")
            return True, "VOLUME_DOWN"

        elif intent == "VOLUME_MUTE":
            self.system_controls.media_play_pause()
            self.speech_feedback.speak("Audio muted.")
            return True, "VOLUME_MUTE"

        # =====================================================================
        # ৪. উইন্ডোজ স্ক্রিন ও উইন্ডো কন্ট্রোল
        # =====================================================================
        elif intent == "WINDOW_DESKTOP":
            self.system_controls.show_desktop()
            self.speech_feedback.speak("Showing desktop, sir.")
            return True, "WINDOW_DESKTOP"

        elif intent == "WINDOW_CLOSE":
            self.system_controls.close_active_window()
            self.speech_feedback.speak("Window closed, sir.")
            return True, "WINDOW_CLOSE"

        elif intent == "SCREENSHOT":
            path = self.system_controls.take_screenshot()
            self.speech_feedback.speak("Screenshot captured and saved to your pictures, sir.")
            return True, "SCREENSHOT"

        # =====================================================================
        # ৫. মিডিয়া ও ইউটিউব
        # =====================================================================
        elif intent == "YOUTUBE_PLAY":
            self.speech_feedback.speak(f"Playing {payload} on YouTube, sir.")
            self.app_launcher.open_youtube(payload, auto_play=True)
            return True, "YOUTUBE_PLAY"

        elif intent == "YOUTUBE_HOME":
            self.speech_feedback.speak("Opening YouTube now, sir.")
            self.app_launcher.open_youtube()
            return True, "YOUTUBE_HOME"

        elif intent == "FIRST_VIDEO":
            self.app_launcher.play_first_video_now()
            self.speech_feedback.speak("Playing the first video now, sir.")
            return True, "FIRST_VIDEO"

        elif intent == "MEDIA_PAUSE":
            self.app_launcher.toggle_youtube_play_pause()
            self.speech_feedback.speak("Playback toggled, sir.")
            return True, "MEDIA_PAUSE"

        elif intent == "MEDIA_FULLSCREEN":
            self.app_launcher.toggle_fullscreen()
            self.speech_feedback.speak("Toggling full screen.")
            return True, "MEDIA_FULLSCREEN"

        elif intent == "MEDIA_NEXT":
            self.app_launcher.next_video()
            self.speech_feedback.speak("Skipping to next video, sir.")
            return True, "MEDIA_NEXT"

        # =====================================================================
        # ৬. ক্রোম ব্রাউজার (শুধুমাত্র ক্রোম চাইলে)
        # =====================================================================
        elif intent == "BROWSER_OPEN":
            self.speech_feedback.speak("Opening Google Chrome, sir.")
            self.app_launcher.open_browser()
            return True, "BROWSER_OPEN"

        # =====================================================================
        # ৭. নোটপ্যাড ও টাইপিং
        # =====================================================================
        elif intent == "NOTEPAD_OPEN":
            self.app_launcher.open_notepad()
            self.speech_feedback.speak("Opening Notepad. Speak what you want to write, sir.")
            return True, "NOTEPAD_OPEN"

        elif intent == "VOICE_TYPING":
            self.voice_typer.type_text(payload)
            return True, "VOICE_TYPING"

        # =====================================================================
        # ৮. ফ্রেন্ডলি কথাবার্তা ও সাধারণ আড্ডা (ALWAYS RESPONDS WITH VOICE)
        # =====================================================================
        elif intent == "CHAT_HOW_ARE_YOU":
            self.speech_feedback.speak("আলহামদুলিল্লাহ স্যার, আমি খুব ভালো আছি! আপনি কেমন আছেন?")
            return True, "CHAT_HOW_ARE_YOU"

        elif intent == "CHAT_HEAR_ME":
            self.speech_feedback.speak("জি স্যার, আমি আপনাকে পরিষ্কার শুনতে পাচ্ছি! বলুন আমি কী করতে পারি?")
            return True, "CHAT_HEAR_ME"

        elif intent == "CHAT_WHO_ARE_YOU":
            self.speech_feedback.speak("আমি আপনার ব্যক্তিগত এআই সহকারী জুবায়ের। আমি আপনার পুরো কম্পিউটার ভয়েস দিয়ে পরিচালনা করি।")
            return True, "CHAT_WHO_ARE_YOU"

        elif intent == "CHAT_GREETING":
            self.speech_feedback.speak("হ্যালো স্যার! আমি শুনছি, বলুন কী সাহায্য করতে পারি?")
            return True, "CHAT_GREETING"

        elif intent == "CHAT_PROBLEM":
            self.speech_feedback.speak("কোনো সমস্যা নেই স্যার! আমি পুরোপুরি সজাগ ও প্রস্তুত। আমাকে আদেশ দিন।")
            return True, "CHAT_PROBLEM"

        elif intent == "CHAT_BHAI":
            self.speech_feedback.speak("জি ভাই, বলুন! আমি শুনতে পাচ্ছি।")
            return True, "CHAT_BHAI"

        elif intent == "CHAT_THANKS":
            self.speech_feedback.speak("আপনাকে অনেক ধন্যবাদ স্যার! আপনার কাজ করতে পেরে আমি আনন্দিত।")
            return True, "CHAT_THANKS"

        elif intent == "CHAT_FALLBACK":
            self.speech_feedback.speak("জি স্যার, আমি শুনতে পেয়েছি। আমাকে বলুন আপনি কী করতে চান, আমি করে দিচ্ছি।")
            return True, "CHAT_FALLBACK"

        # =====================================================================
        # ৯. গুগল সার্চ (শুধুমাত্র স্পষ্টভাবে সার্চ চাইলে)
        # =====================================================================
        elif intent == "WEB_SEARCH":
            encoded = urllib.parse.quote_plus(payload)
            self.speech_feedback.speak(f"গুগলে {payload} সার্চ করছি, স্যার।")
            self.app_launcher.open_browser(f"https://www.google.com/search?q={encoded}")
            return True, "WEB_SEARCH"

        self.speech_feedback.speak("জি স্যার, আমি শুনছি। আমাকে আদেশ দিন।")
        return True, "PROMPT"
