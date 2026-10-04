"""
=============================================================================
JUBAYER AI: TRILINGUAL CONVERSATIONAL & PERMISSION AGENT
=============================================================================
তিনটি ভাষায় (বাংলা, English, এবং বাংলিশ) সার্বক্ষণিক কথা বলা ও অনুমতির প্রোটোকল:
১. ভাষা স্বয়ংক্রিয়ভাবে শনাক্তকরণ (Auto-Detect: Bangla / English / Banglish)
২. ব্যবহারকারী যে ভাষায় কথা বলবেন, ঠিক সেই ভাষায় সুন্দর ও বিনম্র উত্তর দেওয়া
৩. যে কোনো কাজের আগে স্বয়ংক্রিয়ভাবে সেই ভাষায় অনুমতি চাওয়া (Permission Protocol)
৪. অনুমতি দিলে কাজ করা, না দিলে বাতিল করা
=============================================================================
"""

import os
import sys
import time
import re

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from voice.speech_feedback import SpeechFeedback
from stages.stage_01_core_system import CoreSystemController
from stages.stage_02_voice_typing_doc import VoiceTypingDocController
from stages.stage_03_media_youtube import MediaYouTubeController

class TrilingualConversationalAgent:
    def __init__(self, speech_feedback=None):
        self.sf = speech_feedback if speech_feedback else SpeechFeedback()
        self.stage1_sys = CoreSystemController()
        self.stage2_doc = VoiceTypingDocController()
        self.stage3_media = MediaYouTubeController()

        self.pending_action = None
        self.waiting_for_permission = False
        self.current_lang = "BANGLA"

        # বহুভাষিক উত্তর ডিকশনারি
        self.dialogues = {
            "BANGLA": {
                "greetings": "হ্যালো স্যার! আমি জুবায়ের এআই। আমি আপনার কম্পিউটার পরিচালনা করতে প্রস্তুত।",
                "how_are_you": "আলহামদুলিল্লাহ স্যার, আমি খুব ভালো আছি! আপনার আজকের দিনটি কেমন কাটছে?",
                "who_are_you": "আমি আপনার ব্যক্তিগত হ্যান্ডস-ফ্রি এআই সহকারী 'জুবায়ের'। আমি আপনার কথা শুনে কম্পিউটার চালাই।",
                "thanks": "আপনাকে অনেক ধন্যবাদ স্যার! আপনার সেবা করতে পেরে আমি আনন্দিত।",
                "permission_ask": "স্যার, আপনি {desc} বলেছেন। আমি কি এটি করব? দয়া করে হ্যাঁ অথবা না বলুন।",
                "permission_granted": "অনুমতি দেওয়ার জন্য ধন্যবাদ স্যার। আমি এখনই কাজটি করে দিচ্ছি।",
                "permission_denied": "ঠিক আছে স্যার। আপনার নির্দেশ অনুযায়ী কাজটি বাতিল করা হলো। আমি এটি করব না।",
                "clarify_permission": "স্যার, আপনি কি কাজটি করতে অনুমতি দিচ্ছেন? অনুগ্রহ করে শুধু 'হ্যাঁ' অথবা 'না' বলুন।"
            },
            "ENGLISH": {
                "greetings": "Hello Sir! I am Jubayer AI. I am fully ready to operate your computer.",
                "how_are_you": "I am doing great, Sir! How is your day going?",
                "who_are_you": "I am your personal hands-free AI assistant Jubayer. I operate your PC by voice.",
                "thanks": "You are most welcome, Sir! It is my pleasure to assist you.",
                "permission_ask": "Sir, you requested to {desc}. Should I proceed? Please say yes or no.",
                "permission_granted": "Thank you for the permission, Sir. Executing the task right away.",
                "permission_denied": "Understood, Sir. The requested action has been cancelled.",
                "clarify_permission": "Sir, do you grant permission to proceed? Please simply say 'yes' or 'no'."
            },
            "BANGLISH": {
                "greetings": "Hello Sir! Ami Jubayer AI. Apnar computer chalate ami ready.",
                "how_are_you": "Alhamdulillah Sir, ami khub bhalo achi! Apnar ajker din kemon katche?",
                "who_are_you": "Ami apnar personal hands-free AI assistant Jubayer. Ami apnar kotha sune PC chalai.",
                "thanks": "Apnake onek dhonnobad Sir! Apnar sahajjo korte pere ami khushi.",
                "permission_ask": "Sir, apni {desc} bolechen. Ami ki eta korbo? Please ha ba na bolun.",
                "permission_granted": "Anumoti dewar jonno dhonnobad Sir. Ami ekhoni kajti kore dicchi.",
                "permission_denied": "Thik ache Sir, apnar nirdesh moto kajti batil kora holo.",
                "clarify_permission": "Sir, apni ki permission dicchen? Doya kore shudhu 'ha' ba 'na' bolun."
            }
        }

    def detect_language(self, text):
        """ইউজারের ভাষা স্বয়ংক্রিয়ভাবে শনাক্তকরণ (Bangla, Banglish, English)"""
        if not text:
            return "BANGLA"

        # ১. বাংলা স্ক্রিপ্ট আছে কি না (\u0980 - \u09FF)
        if re.search(r'[\u0980-\u09FF]', text):
            return "BANGLA"

        # ২. রোমান হরফে বাংলিশ কি-ওয়ার্ড
        banglish_indicators = [
            "kemon", "acho", "achen", "valo", "bhalo", "achi", "koro", "korbe", "kete",
            "dao", "bondho", "chalu", "barao", "komao", "chithi", "likhbo", "tumi",
            "amar", "apnar", "shuncho", "suncho", "thik", "ache", "hum", "ha", "na"
        ]
        words = text.lower().split()
        if any(w in banglish_indicators for w in words):
            return "BANGLISH"

        # ৩. ডিফল্ট ইংরেজি
        return "ENGLISH"

    def speak(self, text):
        """কথা বলা ও প্রদর্শন"""
        print(f"\n[জুবায়ের এআই] 🗣️ {text}")
        self.sf.speak(text)

    def process_user_input(self, text):
        if not text or not text.strip():
            return

        cleaned = text.strip().lower()
        print(f"\n[ব্যবহারকারী] 🎤 \"{text}\"")

        # ভাষা শনাক্তকরণ
        detected_lang = self.detect_language(text)
        self.current_lang = detected_lang
        print(f"  [ভাষা শনাক্ত]: {detected_lang}")

        # ধাপ ১: অনুমতির উত্তরের অপেক্ষায় আছি কি না?
        if self.waiting_for_permission and self.pending_action:
            self._handle_permission_response(cleaned, detected_lang)
            return

        # ধাপ ২: সাধারণ আড্ডা কি না?
        if self._handle_casual_conversation(cleaned, detected_lang):
            return

        # ধাপ ৩: কাজের অনুরোধ হলে আগে অনুমতি চাওয়া
        self._analyze_and_request_permission(cleaned, raw_text=text, lang=detected_lang)

    def _handle_casual_conversation(self, text, lang):
        """আড্ডা ও কুশল বিনিময়"""
        # কুশল বিনিময়
        if any(w in text for w in ["কেমন আছো", "কেমন আছেন", "how are you", "kemon acho", "kemon achen", "how are u"]):
            self.speak(self.dialogues[lang]["how_are_you"])
            return True

        # সম্ভাষণ
        if any(w in text for w in ["হাই", "হ্যালো", "hello", "hey", "hi", "জুবায়ের", "jubayer"]):
            if len(text.split()) <= 2:
                self.speak(self.dialogues[lang]["greetings"])
                return True

        # পরিচয়
        if any(w in text for w in ["কে তুমি", "তুমি কে", "তোমার নাম কি", "তোমার পরিচয়", "কে আপনি", "পরিচয় দাও", "who are you", "what is your name", "tumi k", "tumi ke"]):
            self.speak(self.dialogues[lang]["who_are_you"])
            return True

        # শুনতে পাচ্ছ / Hear me
        if any(w in text for w in ["শুনতে পাচ্ছ", "can you hear me", "shunte pao", "shuncho", "suncho", "are you there", "hear me"]):
            if lang == "BANGLA":
                self.speak("জি স্যার, আমি আপনাকে পরিষ্কার শুনতে পাচ্ছি! বলুন আমি কী কাজ করব?")
            elif lang == "BANGLISH":
                self.speak("Ji Sir, ami apnake porishkar shunte pacchi! Bolun ami ki kaj korbo?")
            else:
                self.speak("Yes Sir, I can hear you loud and clear! Tell me what you need.")
            return True

        # সমস্যা / কি অবস্থা
        if any(w in text for w in ["ki samasya", "কি সমস্যা", "problem", "ki problem", "ki obostha"]):
            if lang == "BANGLA":
                self.speak("কোনো সমস্যা নেই স্যার! আমি পুরোপুরি প্রস্তুত। আপনি কী কাজ করতে চান বলুন।")
            elif lang == "BANGLISH":
                self.speak("Kono problem nei Sir! Ami ready achi. Apni ki kaj korte chan bolun.")
            else:
                self.speak("No problem at all, Sir! I am fully ready for your command.")
            return True

        # ভাই
        if any(w in text.split() for w in ["bhai", "ভাই", "bro"]):
            if lang == "BANGLA":
                self.speak("জি ভাই, বলুন! আমি শুনতে পাচ্ছি।")
            else:
                self.speak("Ji bhai, I am listening! Tell me what you need.")
            return True

        # ধন্যবাদ
        if any(w in text for w in ["ধন্যবাদ", "থ্যাংক", "thank you", "thanks", "dhonnobad", "good boy", "valoi", "shabash"]):
            self.speak(self.dialogues[lang]["thanks"])
            return True

        return False

    def _analyze_and_request_permission(self, text, raw_text, lang):
        """কাজের ইনটেন্ট ধরে সংশ্লিষ্ট ভাষায় অনুমতি চাওয়া"""
        action = None

        # ১. পিসি শাটডাউন
        if any(w in text for w in ["shutdown", "shut down", "শাটডাউন"]) or (("pc" in text or "computer" in text or "পিসি" in text) and any(w in text for w in ["off", "বন্ধ", "bondho"])):
            action = {
                "name": "SHUTDOWN",
                "desc_bn": "কম্পিউটার সম্পূর্ণ বন্ধ করতে",
                "desc_en": "shut down the computer",
                "desc_bl": "computer bondho korte",
                "func": lambda: self.stage1_sys.execute_shutdown()
            }

        # ২. উইন্ডো / ইউটিউব / ক্রোম ক্লোজ
        elif (any(w in text for w in ["close", "বন্ধ", "band", "kete", "কাটো", "stop", "exit", "ber"]) and any(app in text for app in ["window", "উইন্ডো", "youtube", "ইউটিউব", "chrome", "ক্রোম", "this", "it", "video", "app", "music"])) or any(p in text for p in ["close window", "close youtube", "close chrome", "stop chrome", "band karo", "kete dao", "ber hou", "উইন্ডো বন্ধ", "ইউটিউব বন্ধ", "কেটে দাও"]) or (len(text.split()) <= 2 and any(w in text.split() for w in ["close", "কাটো", "বন্ধ", "exit"])):
            action = {
                "name": "CLOSE_WINDOW",
                "desc_bn": "বর্তমান উইন্ডো বা ইউটিউব কেটে বন্ধ করে দিতে",
                "desc_en": "close the active window or YouTube",
                "desc_bl": "current window ba YouTube kete bondho korte",
                "func": lambda: self.stage1_sys.close_active_window()
            }

        # ৩. ভলিউম বাড়ানো
        elif ("volume" in text or "sound" in text or "আওয়াজ" in text or "ভলিউম" in text) and any(w in text for w in ["increase", "up", "raise", "higher", "more", "বাড়াও", "barao", "bariye"]):
            action = {
                "name": "VOLUME_UP",
                "desc_bn": "ভলিউম ১০ শতাংশ বাড়িয়ে দিতে",
                "desc_en": "increase the system volume",
                "desc_bl": "sound 10 percent bariye dite",
                "func": lambda: self.stage1_sys.volume_up(5)
            }

        # ৪. স্ক্রিনশট নেওয়া
        elif any(w in text for w in ["screenshot", "স্ক্রিনশট", "screen capture", "snapshot", "chobi tolo"]):
            action = {
                "name": "SCREENSHOT",
                "desc_bn": "আপনার স্ক্রিনের একটি ছবি তুলে সেভ করতে",
                "desc_en": "capture and save a screenshot",
                "desc_bl": "screen er snapshot tule save korte",
                "func": lambda: self.stage1_sys.take_screenshot()
            }

        # ৫. ইউটিউব প্লে (যদি ক্লোজ না বলা হয়)
        elif any(w in text for w in ["youtube", "ইউটিউব", "গান", "song", "video", "play", "গজল", "tilawat"]) and not any(cw in text for cw in ["close", "বন্ধ", "band", "kete", "stop", "exit"]):
            query = raw_text
            for prefix in ["ইউটিউবে", "ইউটিউব", "প্লে করো", "গান ছাড়ো", "বাজাও", "play", "on youtube", "youtube e", "can you"]:
                query = query.replace(prefix, "")
            query = query.strip() or "Quran Tilawat"
            action = {
                "name": "YOUTUBE",
                "desc_bn": f"ইউটিউবে '{query}' সার্চ করে ভিডিও চালাতে",
                "desc_en": f"play '{query}' on YouTube",
                "desc_bl": f"YouTube e '{query}' search kore chalu korte",
                "func": lambda q=query: self.stage3_media.open_youtube(q, auto_play=True)
            }

        # ৬. নোটপ্যাড ওপেন ও টাইপিং
        elif any(w in text for w in ["notepad", "নোটপ্যাড", "চিঠি", "chithi", "likhbo", "write a letter", "document"]):
            action = {
                "name": "NOTEPAD",
                "desc_bn": "নোটপ্যাড ওপেন করে চিঠি টাইপ করার জন্য প্রস্তুত করতে",
                "desc_en": "open Notepad for letter typing",
                "desc_bl": "Notepad open kore chithi type korar jonno ready korte",
                "func": lambda: self.stage2_doc.open_notepad()
            }

        if action:
            self.pending_action = action
            self.waiting_for_permission = True

            desc_key = "desc_bn" if lang == "BANGLA" else ("desc_bl" if lang == "BANGLISH" else "desc_en")
            desc = action[desc_key]
            prompt = self.dialogues[lang]["permission_ask"].format(desc=desc)
            self.speak(prompt)
        else:
            if lang == "BANGLA":
                self.speak("স্যার, আমি আপনার কথা বুঝতে পেরেছি। আপনি কি আমাকে দিয়ে কোনো কাজ করাতে চান?")
            elif lang == "BANGLISH":
                self.speak("Sir, ami apnar kotha bujhte perechi. Apni ki amake kono kaj dite chan?")
            else:
                self.speak("Sir, I understood your words. Would you like me to perform a task for you?")

    def _handle_permission_response(self, text, lang):
        """অনুমতি হ্যাঁ বা না যাচাই করা"""
        positive_words = [
            "হ্যাঁ", "হ্যা", "করো", "কর", "yes", "yeah", "yep", "do it", "proceed", 
            "sure", "ok", "okay", "ঠিক আছে", "হুম", "hum", "ha", "haa", "thik ache"
        ]
        negative_words = [
            "না", "নাা", "করো না", "করিস না", "no", "nope", "cancel", "stop", "bad", 
            "বাদ দাও", "দরকার নাই", "থাক", "na", "naa", "koro na", "bad dao", "lagbe na"
        ]

        # সম্মতি দিলে
        if any(w in text for w in positive_words):
            self.speak(self.dialogues[lang]["permission_granted"])
            action_func = self.pending_action["func"]
            self.pending_action = None
            self.waiting_for_permission = False
            time.sleep(0.5)
            action_func()

        # বাতিল করলে
        elif any(w in text for w in negative_words):
            self.speak(self.dialogues[lang]["permission_denied"])
            self.pending_action = None
            self.waiting_for_permission = False

        else:
            self.speak(self.dialogues[lang]["clarify_permission"])

def test_trilingual_scenarios():
    print("\n" + "=" * 75)
    print(" 🌍 JUBAYER AI: TRILINGUAL CONVERSATIONAL & PERMISSION TEST 🌍")
    print("=" * 75)
    print("টেস্ট ১: খাঁটি বাংলা কথপোকথন ও অনুমতি")
    print("টেস্ট ২: English Conversation & Permission")
    print("টেস্ট ৩: বাংলিশ (Roman Bengali) Conversation & Permission")
    print("=" * 75 + "\n")

    agent = TrilingualConversationalAgent()

    # ১. বাংলা টেস্ট
    print("\n--- [১. বাংলা টেস্ট] ---")
    agent.process_user_input("হ্যালো জুবায়ের, কেমন আছো?")
    time.sleep(2.5)
    agent.process_user_input("উইন্ডো কেটে দাও তো")
    time.sleep(2.5)
    agent.process_user_input("হ্যাঁ করো")
    time.sleep(2.5)

    # ২. ইংরেজি টেস্ট
    print("\n--- [২. English Test] ---")
    agent.process_user_input("Hey Jubayer, how are you?")
    time.sleep(2.5)
    agent.process_user_input("Can you increase the volume")
    time.sleep(2.5)
    agent.process_user_input("Yes do it")
    time.sleep(2.5)

    # ৩. বাংলিশ টেস্ট
    print("\n--- [৩. বাংলিশ (Banglish) Test] ---")
    agent.process_user_input("kemon acho jubayer")
    time.sleep(2.5)
    agent.process_user_input("chithi likhbo notepad kholo")
    time.sleep(2.5)
    agent.process_user_input("ha koro")
    time.sleep(2.5)

if __name__ == "__main__":
    test_trilingual_scenarios()
