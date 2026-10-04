"""
=============================================================================
কোর মডিউল: ওয়েক-ওয়ার্ড ও ইন্টেন্ট ইঞ্জিন (JUBAYER WAKE-WORD & INTENT ENGINE)
=============================================================================
'জুবায়েদ' নাম শুনলেই সজাগ হয়ে উত্তর দেয়: 'জি স্যার, বলুন!'
এবং আপনার হুকুম অনুযায়ী পুরো পিসি নিয়ন্ত্রণ করে।
"""

import time
import re
import urllib.parse
import webbrowser
import subprocess
import pyautogui

from core.voice_typing import VoiceTyper

WAKE_WORDS = [
    "জুবায়েদ", "জুবায়ের", "জুবায়ের", "জুবায়েত", "জোবায়ের",
    "jubayer", "jubayed", "jobayer", "hey jubayer"
]

class WakeWordEngine:
    def __init__(self, speech_feedback, system_controls, app_launcher):
        self.speech_feedback = speech_feedback
        self.system_controls = system_controls
        self.app_launcher = app_launcher
        self.voice_typer = VoiceTyper()

        self.is_awake = False
        self.awake_timestamp = 0
        self.awake_timeout = 8.0  # জেগে থাকার সময়সীমা (সেকেন্ড)

        self.status_message = "জুবায়েদ প্রস্তুত (নাম ধরে ডাকুন)..."

    def check_wake_word(self, text):
        """টেক্সটে 'জুবায়েদ' বা কোনো ওয়েক-ওয়ার্ড আছে কিনা যাচাই করে"""
        if not text:
            return False
        text_lower = text.lower()
        for ww in WAKE_WORDS:
            if ww in text_lower:
                return True
        return False

    def activate_wake(self):
        """জুবায়েদকে সক্রিয় করা"""
        self.is_awake = True
        self.awake_timestamp = time.time()
        self.status_message = "জুবায়েদ: জি স্যার, বলুন!"
        self.speech_feedback.speak("জি স্যার, বলুন! কী করতে হবে?")

    def process_speech(self, text):
        """
        স্পিচ রিকগনিশন থেকে আসা প্রতিটি বাক্য প্রসেস করে।
        রিটার্ন করে (was_handled: bool, action_name: str)
        """
        if not text:
            return False, None

        now = time.time()

        # ১. ওয়েক-ওয়ার্ড চেক
        if self.check_wake_word(text):
            self.activate_wake()
            # যদি একই বাক্যে কমান্ডও থাকে (যেমন: 'জুবায়েদ ক্রোম খোলো')
            cleaned = text
            for ww in WAKE_WORDS:
                cleaned = re.sub(re.escape(ww), '', cleaned, flags=re.IGNORECASE)
            cleaned = cleaned.strip()
            if len(cleaned) > 2:
                return self.execute_intent(cleaned)
            return True, "WAKE_WORD"

        # ২. যদি জুবায়েদ ইতিমধ্যে জেগে থাকে
        if self.is_awake:
            if now - self.awake_timestamp > self.awake_timeout:
                self.is_awake = False
                self.status_message = "জুবায়েদ প্রস্তুত (নাম ধরে ডাকুন)..."
                return False, None

            # নির্দেশ পালন করা
            self.awake_timestamp = now  # সময় বাড়িয়ে নেওয়া
            return self.execute_intent(text)

        return False, None

    def execute_intent(self, cmd_text):
        """কমান্ডের উদ্দেশ্য বুঝে কাজ সম্পন্ন করা"""
        cmd = cmd_text.lower().strip()
        print(f"[জুবায়েদ প্রসেসিং]: {cmd}")

        # --- ১. সিস্টেম পাওয়ার ও উইন্ডোজ অপারেশন ---
        if any(w in cmd for w in ["শাটডাউন", "পিসি বন্ধ", "কম্পিউটার বন্ধ"]):
            self.status_message = "জুবায়েদ: পিসি শাটডাউন করা হচ্ছে..."
            self.speech_feedback.speak("পিসি শাটডাউন করা হচ্ছে, স্যার। বিদায়!")
            time.sleep(1.5)
            subprocess.run("shutdown /s /t 2", shell=True)
            return True, "SHUTDOWN"

        elif any(w in cmd for w in ["রিস্টার্ট", "রিবুট"]):
            self.status_message = "জুবায়েদ: পিসি রিস্টার্ট করা হচ্ছে..."
            self.speech_feedback.speak("পিসি রিস্টার্ট করা হচ্ছে, স্যার।")
            time.sleep(1.5)
            subprocess.run("shutdown /r /t 2", shell=True)
            return True, "RESTART"

        elif any(w in cmd for w in ["লক করো", "পিসি লক"]):
            self.status_message = "জুবায়েদ: পিসি লক করা হচ্ছে..."
            self.speech_feedback.speak("পিসি লক করা হয়েছে, স্যার।")
            self.system_controls.lock_pc()
            self.is_awake = False
            return True, "LOCK"

        elif any(w in cmd for w in ["উইন্ডো কাটো", "ক্লোজ করো", "বন্ধ করো", "কেটে দাও"]):
            self.status_message = "জুবায়েদ: উইন্ডো বন্ধ করা হলো।"
            self.speech_feedback.speak("উইন্ডো বন্ধ করে দিয়েছি।")
            pyautogui.hotkey('alt', 'f4')
            return True, "CLOSE_WINDOW"

        elif any(w in cmd for w in ["ডেস্কটপ", "মিনিমাইজ", "সব বন্ধ"]):
            self.status_message = "জুবায়েদ: ডেস্কটপ দেখানো হচ্ছে।"
            self.speech_feedback.speak("সব মিনিমাইজ করে ডেস্কটপ দেখাচ্ছি।")
            self.system_controls.show_desktop()
            return True, "DESKTOP"

        elif any(w in cmd for w in ["পরের উইন্ডো", "উইন্ডো বদলাও", "অ্যাপ বদলাও"]):
            pyautogui.hotkey('alt', 'tab')
            self.speech_feedback.speak("উইন্ডো পরিবর্তন করেছি।")
            return True, "ALT_TAB"

        elif any(w in cmd for w in ["স্ক্রিনশট", "ছবি তোলো"]):
            path = self.system_controls.take_screenshot()
            self.status_message = "জুবায়েদ: স্ক্রিনশট সেভ হয়েছে!"
            self.speech_feedback.speak("স্ক্রিনশট নিয়ে আপনার পিকচার্স ফোল্ডারে সেভ করেছি, স্যার।")
            return True, "SCREENSHOT"

        # --- ২. সাউন্ড ও ভলিউম ---
        elif any(w in cmd for w in ["ভলিউম বাড়াও", "আওয়াজ বাড়াও", "সাউন্ড বাড়াও"]):
            self.system_controls.volume_up(steps=4)
            self.speech_feedback.speak("ভলিউম বাড়িয়েছি।")
            return True, "VOL_UP"

        elif any(w in cmd for w in ["ভলিউম কমাও", "আওয়াজ কমাও", "সাউন্ড কমাও"]):
            self.system_controls.volume_down(steps=4)
            self.speech_feedback.speak("ভলিউম কমিয়েছি।")
            return True, "VOL_DOWN"

        elif any(w in cmd for w in ["মিউট", "চুপ"]):
            self.system_controls.media_play_pause()
            self.speech_feedback.speak("মিডিয়া পজ করা হয়েছে।")
            return True, "MUTE"

        # --- ৩. ইউটিউবে গান বা ভিডিও প্লে ---
        elif "ইউটিউব" in cmd or "গান" in cmd or "প্লে" in cmd or "চালাও" in cmd:
            query = cmd
            for remove_word in ["ইউটিউবে", "ইউটিউব", "চালাও", "প্লে করো", "গান", "ভিডিও", "শুনবো", "দেখাও"]:
                query = query.replace(remove_word, "")
            query = query.strip()

            if len(query) > 0:
                encoded = urllib.parse.quote_plus(query)
                url = f"https://www.youtube.com/results?search_query={encoded}"
                webbrowser.open(url)
                self.status_message = f"জুবায়েদ: ইউটিউবে '{query}' চলছে..."
                self.speech_feedback.speak(f"ইউটিউবে {query} চালিয়ে দিচ্ছি, স্যার।")
            else:
                self.app_launcher.open_youtube()
                self.speech_feedback.speak("ইউটিউব ওপেন করেছি, স্যার।")
            self.is_awake = False
            return True, "YOUTUBE"

        # --- ৪. গুগলে সার্চ করা ---
        elif "গুগল" in cmd or "সার্চ" in cmd or "খুঁজে বের করো" in cmd:
            query = cmd
            for remove_word in ["গুগলে", "গুগল", "সার্চ করো", "সার্চ", "খুঁজে বের করো", "কী", "কেমন"]:
                query = query.replace(remove_word, "")
            query = query.strip()

            if len(query) > 0:
                encoded = urllib.parse.quote_plus(query)
                url = f"https://www.google.com/search?q={encoded}"
                webbrowser.open(url)
                self.status_message = f"জুবায়েদ: গুগলে '{query}' খোঁজা হচ্ছে..."
                self.speech_feedback.speak(f"গুগলে {query} সার্চ করে ফলাফল দেখাচ্ছি।")
            else:
                self.app_launcher.open_browser()
                self.speech_feedback.speak("গুগল ওপেন করেছি।")
            self.is_awake = False
            return True, "GOOGLE_SEARCH"

        # --- ৫. ভয়েস টাইপিং ও নোটপ্যাড ---
        elif "নোটপ্যাড" in cmd or "খাতা" in cmd:
            self.app_launcher.open_notepad()
            self.speech_feedback.speak("নোটপ্যাড ওপেন করেছি। আপনি এখন যা বলবেন তা টাইপ করতে প্রস্তুত।")
            return True, "NOTEPAD"

        elif cmd.startswith("লেখো") or cmd.startswith("টাইপ করো"):
            text_to_type = cmd.replace("লেখো", "").replace("টাইপ করো", "").strip()
            if text_to_type:
                self.voice_typer.type_text(text_to_type)
                self.status_message = f"জুবায়েদ টাইপ করেছে: {text_to_type}"
                return True, "TYPED"

        # --- ৬. মোবাইল কানেক্ট কিউআর কোড ---
        elif "মোবাইল" in cmd or "রিমোট" in cmd or "ফোন" in cmd:
            self.status_message = "জুবায়েদ: মোবাইল রিমোট কিউআর কোড সক্রিয়।"
            self.speech_feedback.speak("মোবাইল রিমোট সক্রিয় হয়েছে। স্ক্রিনের কিউআর কোডটি আপনার ফোনের ক্যামেরা দিয়ে স্ক্যান করুন।")
            return True, "SHOW_MOBILE_REMOTE"

        # অজানা কোনো বাক্য হলে
        self.status_message = f"জুবায়েদ শুনেছে: '{cmd}'"
        return False, None
