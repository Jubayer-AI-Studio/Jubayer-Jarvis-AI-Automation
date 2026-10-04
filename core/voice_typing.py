"""
=============================================================================
কোর মডিউল: ভয়েস টাইপার (VOICE TYPING & DICTATION)
=============================================================================
মুখে যা বলবেন তা স্বয়ংক্রিয়ভাবে সক্রিয় যেকোনো সফটওয়্যার (Notepad, Word, Browser,
WhatsApp ইত্যাদি)-তে টাইপ করা।
বাংলা ও ইউনিকোড যেকোনো অক্ষর নির্ভুলভাবে টাইপ করার জন্য ক্লিপবোর্ড পেস্ট পদ্ধতি।
"""

import time
import pyautogui
import pyperclip

class VoiceTyper:
    def __init__(self):
        pass

    def type_text(self, text, add_space=True):
        """
        যেকোনো টেক্সট (বাংলা বা ইংরেজি) বর্তমান সক্রিয় উইন্ডোতে টাইপ/পেস্ট করে।
        """
        if not text:
            return

        to_type = text + (" " if add_space else "")
        # ইউনিকোড এবং বাংলা টেক্সট নিখুঁতভাবে ইনসার্ট করতে pyperclip ব্যবহার করা হয়েছে
        pyperclip.copy(to_type)
        time.sleep(0.05)
        pyautogui.hotkey('ctrl', 'v')

    def press_enter(self):
        """নতুন লাইন / এন্টার চাপুন"""
        pyautogui.press('enter')

    def backspace(self, times=1):
        """অক্ষর মুছুন"""
        for _ in range(times):
            pyautogui.press('backspace')

    def select_all(self):
        """সব সিলেক্ট করুন"""
        pyautogui.hotkey('ctrl', 'a')
