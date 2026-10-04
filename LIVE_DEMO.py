"""
=============================================================================
JUBAYER AI: লাইভ ডেমোস্ট্রেশন (LIVE DEMO FOR USER)
=============================================================================
ব্যবহারকারীর চোখের সামনে উইন্ডোজের সমস্ত ফিচার একে একে লাইভ রান করে দেখানো।
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from actions.system_controls import SystemControls
from actions.app_launcher import AppLauncher
from core.voice_typing import VoiceTyper
from voice.speech_feedback import SpeechFeedback

def run_live_demo():
    print("\n" + "=" * 65)
    print("      🚀 JUBAYER AI // লাইভ ডেমোস্ট্রেশন শুরু হচ্ছে... 🚀")
    print("=" * 65 + "\n")

    sf = SpeechFeedback()
    sc = SystemControls()
    al = AppLauncher()
    vt = VoiceTyper()

    # সূচনা
    print("[ডেমো ১/৬] সিস্টেম সূচনা ও ভয়েস সম্ভাষণ...")
    sf.speak("Welcome, sir! I am Jubayer AI. Initiating live demonstration on your screen now.")
    time.sleep(4.0)

    # ১. ভলিউম কন্ট্রোল লাইভ
    print("[ডেমো ২/৬] ভলিউম নিয়ন্ত্রণ লাইভ টেস্ট...")
    sf.speak("Step 1: Testing system volume controls.")
    time.sleep(2.0)
    print("  --> ভলিউম বাড়ানো হচ্ছে (+১০%)...")
    sc.volume_up(steps=5)
    time.sleep(1.5)
    print("  --> ভলিউম কমানো হচ্ছে (-১০%)...")
    sc.volume_down(steps=5)
    time.sleep(1.5)

    # ২. নোটপ্যাড ওপেন ও অটোমেটিক টাইপিং লাইভ
    print("[ডেমো ৩/৬] নোটপ্যাড ওপেন ও হাত ছাড়া স্বয়ংক্রিয় টাইপিং...")
    sf.speak("Step 2: Opening Notepad and typing text live without hands.")
    time.sleep(2.0)
    al.open_notepad()
    time.sleep(1.5)
    demo_text = "Hello Sir! This is Jubayer AI operating your PC live without touching keyboard or mouse!"
    vt.type_text(demo_text)
    time.sleep(2.5)

    # ৩. স্ক্রিনশট লাইভ টেস্ট
    print("[ডেমো ৪/৬] লাইভ স্ক্রিনশট টেস্ট...")
    sf.speak("Step 3: Taking a live screenshot of your desktop.")
    time.sleep(1.5)
    shot_path = sc.take_screenshot()
    print(f"  --> স্ক্রিনশট সেভ হয়েছে: {shot_path}")
    time.sleep(2.0)

    # ৪. ডেস্কটপ মিনিমাইজ লাইভ
    print("[ডেমো ৫/৬] ডেস্কটপ শো ও উইন্ডো মিনিমাইজ টেস্ট...")
    sf.speak("Step 4: Minimizing windows to show your desktop.")
    time.sleep(1.5)
    sc.show_desktop()
    time.sleep(2.0)

    # ৫. ইউটিউব অটোমেশন লাইভ
    print("[ডেমো ৬/৬] ইউটিউব ওপেন ও ভিডিও সার্চ লাইভ টেস্ট...")
    sf.speak("Step 5: Opening YouTube and launching video.")
    time.sleep(1.5)
    al.open_youtube("Quran Tilawat", auto_play=True)
    time.sleep(4.0)

    # সমাপ্তি
    print("\n" + "=" * 65)
    print("  🎉 লাইভ ডেমো সফলভাবে সম্পন্ন হয়েছে! সমস্ত ফিচার সক্রিয়! 🎉")
    print("=" * 65 + "\n")
    sf.speak("Live demonstration complete, sir! All systems are one hundred percent operational and ready for you.")
    time.sleep(4.0)

if __name__ == "__main__":
    run_live_demo()
