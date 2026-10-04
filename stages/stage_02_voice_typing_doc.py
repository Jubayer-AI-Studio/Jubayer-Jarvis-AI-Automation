"""
=============================================================================
STAGE 02: VOICE TYPING & OFFICE DOCUMENTATION
=============================================================================
হাত ছাড়া মুখে বলে চিঠিপত্র, ডকুমেন্ট ও টেক্সট টাইপ এবং এডিটিং:
- ইউনিকোড বাংলা ও ইংরেজি নিখুঁত ক্লিপবোর্ড ইনজেকশন
- নতুন লাইন / প্যারাগ্রাফ তৈরি
- টেক্সট সিলেক্ট, কপি, কাট, পেস্ট, ডিলিট / ব্যাকস্পেস
- আনডু (Ctrl+Z) ও রিডু (Ctrl+Y)
- ডকুমেন্ট সেভ (Ctrl+S) ও সেভ অ্যাজ (F12)
- সরাসরি নোটপ্যাড / ওয়ার্ডপ্যাড ওপেন ও অটোমেশন
=============================================================================
"""

import time
import subprocess
import pyautogui
import pyperclip

pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = False

class VoiceTypingDocController:
    def __init__(self):
        pass

    def open_notepad(self):
        """নোটপ্যাড চালু করা"""
        subprocess.Popen("notepad.exe")
        print("[STAGE 2] Notepad opened")
        time.sleep(1.0)
        return True

    def open_wordpad(self):
        """ওয়ার্ডপ্যাড চালু করা"""
        subprocess.Popen("write.exe")
        print("[STAGE 2] Wordpad opened")
        time.sleep(1.0)
        return True

    def type_text(self, text, add_space=True):
        """
        যেকোনো বাংলা বা ইংরেজি বাক্য সরাসরি বর্তমান সক্রিয় উইন্ডোতে টাইপ/পেস্ট করে।
        """
        if not text:
            return False

        to_type = text + (" " if add_space else "")
        pyperclip.copy(to_type)
        time.sleep(0.05)
        pyautogui.hotkey("ctrl", "v")
        print(f"[STAGE 2] Typed: {text[:30]}...")
        return True

    def new_line(self, times=1):
        """নতুন লাইন তৈরি (Enter)"""
        for _ in range(times):
            pyautogui.press("enter")
        print("[STAGE 2] New line inserted")

    def backspace(self, times=1):
        """অক্ষর বা শব্দ মোছা"""
        for _ in range(times):
            pyautogui.press("backspace")
        print(f"[STAGE 2] Backspaced {times} times")

    def select_all(self):
        """সম্পূর্ণ লেখা সিলেক্ট (Ctrl + A)"""
        pyautogui.hotkey("ctrl", "a")
        print("[STAGE 2] All text selected")

    def copy_text(self):
        """সিলেক্ট করা অংশ কপি (Ctrl + C)"""
        pyautogui.hotkey("ctrl", "c")
        print("[STAGE 2] Text copied to clipboard")

    def cut_text(self):
        """সিলেক্ট করা অংশ কাট (Ctrl + X)"""
        pyautogui.hotkey("ctrl", "x")
        print("[STAGE 2] Text cut")

    def paste_text(self):
        """পেস্ট করা (Ctrl + V)"""
        pyautogui.hotkey("ctrl", "v")
        print("[STAGE 2] Text pasted")

    def undo(self):
        """পূর্বাবস্থায় ফেরা (Ctrl + Z)"""
        pyautogui.hotkey("ctrl", "z")
        print("[STAGE 2] Undo action")

    def redo(self):
        """পুনরাবৃত্তি (Ctrl + Y)"""
        pyautogui.hotkey("ctrl", "y")
        print("[STAGE 2] Redo action")

    def save_file(self):
        """ফাইল সেভ করা (Ctrl + S)"""
        pyautogui.hotkey("ctrl", "s")
        print("[STAGE 2] Save command sent (Ctrl+S)")

if __name__ == "__main__":
    doc = VoiceTypingDocController()
    print("--- Testing Stage 02 Voice Typing & Documentation ---")
    doc.open_notepad()
    time.sleep(1.0)
    doc.type_text("Hello Sir! Stage 2 Voice Typing Module is working seamlessly.")
    doc.new_line()
    doc.type_text("হাত ছাড়া স্বয়ংক্রিয় বাংলা ও ইংরেজি টাইপিং সক্ষম।")
    print("Test complete.")
