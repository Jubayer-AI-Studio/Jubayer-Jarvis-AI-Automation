"""
=============================================================================
LIVE SLEEP & WAKE DEMO
=============================================================================
ব্যবহারকারীর চোখের সামনে লাইভ ডিসপ্লে সম্পূর্ণ অফ (Eco-Sleep) করে 
আবার অন করে দেখানো।
=============================================================================
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from stages.stage_01_core_system import CoreSystemController
from voice.speech_feedback import SpeechFeedback

def run_test():
    sf = SpeechFeedback()
    sc = CoreSystemController()

    print("\n" + "=" * 60)
    print("   🌙 ECO-SLEEP & VOICE-WAKE LIVE DEMONSTRATION ☀️")
    print("=" * 60 + "\n")

    print("[ধাপ ১] ভয়েস ঘোষণা...")
    sf.speak("Sir, please watch your monitor. I am turning off the screen in three seconds.")
    time.sleep(3.5)

    print("[ধাপ ২] স্ক্রিন সম্পূর্ণ অন্ধকার/অফ করা হচ্ছে...")
    sc.sleep_display()
    print("  --> স্ক্রিন এখন সম্পূর্ণ অফ (অন্ধকার)। সিস্টেম মাইক নিয়ে সজাগ আছে।")
    time.sleep(5.0)

    print("[ধাপ ৩] স্ক্রিন তাৎক্ষণিক অন করা হচ্ছে...")
    sc.wake_display()
    sf.speak("Welcome back, sir! The screen is back on and active.")
    print("  --> স্ক্রিন অন হয়েছে ও সিস্টেম সচল!")
    time.sleep(3.0)

    print("\n" + "=" * 60)
    print("   🎉 স্লিপ ও ওয়েক টেস্ট সফলভাবে সম্পন্ন হয়েছে! 🎉")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    run_test()
