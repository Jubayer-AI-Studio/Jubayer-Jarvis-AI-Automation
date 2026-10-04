"""
=============================================================================
অ্যাকশন মডিউল: সিস্টেম কন্ট্রোল (SYSTEM CONTROLS v3.0)
=============================================================================
উইন্ডোজ ভলিউম, স্ক্রিনশট, উইন্ডো ক্লোজ, এবং ভয়েস দিয়ে পিসি অফ ও অন (স্লিপ/ওয়েক)।
"""

import os
import time
import subprocess
import ctypes
from datetime import datetime
import pyautogui

pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = False

class SystemControls:
    def __init__(self):
        self.last_click_time = 0
        self.click_cooldown = 0.25

        # স্ক্রিনশট ফোল্ডার
        self.screenshot_dir = os.path.join(os.path.expanduser("~"), "Pictures", "Jubayer_Captures")
        os.makedirs(self.screenshot_dir, exist_ok=True)

        self.is_display_sleeping = False

    def volume_up(self, steps=5):
        """ভলিউম বাড়ানো (+১০%)"""
        for _ in range(steps):
            pyautogui.press("volumeup")
        print(f"[SYSTEM] Volume increased (+{steps * 2}%)")

    def volume_down(self, steps=5):
        """ভলিউম কমানো (-১০%)"""
        for _ in range(steps):
            pyautogui.press("volumedown")
        print(f"[SYSTEM] Volume decreased (-{steps * 2}%)")

    def media_play_pause(self):
        """প্লে/পজ বা মিউট"""
        pyautogui.press("playpause")
        print("[SYSTEM] Play/Pause toggled")

    def close_active_window(self):
        """বর্তমান উইন্ডো বন্ধ করা (Alt+F4)"""
        pyautogui.hotkey("alt", "f4")
        print("[SYSTEM] Window closed")

    def show_desktop(self):
        """ডেস্কটপ দেখানো (Win+D)"""
        pyautogui.hotkey("win", "d")
        print("[SYSTEM] Desktop shown")

    def lock_pc(self):
        """পিসি লক করা"""
        subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
        print("[SYSTEM] PC locked")

    def sleep_display(self):
        """
        পিসির ডিসপ্লে সম্পূর্ণ অফ করে স্লিপ মোডে পাঠানো (পিসি দেখতে বন্ধ মনে হবে)।
        মাইক্রোফোন চালু থাকবে যাতে মুখে ডাকলে আবার অন হয়।
        """
        try:
            self.is_display_sleeping = True
            # Windows API to turn off monitor (2 = off)
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
            print("[SYSTEM] Display turned OFF (Eco-Sleep mode active)")
            return True
        except Exception as e:
            print(f"[SYSTEM SLEEP ERROR]: {e}")
            return False

    def wake_display(self):
        """
        মুখে ডাকার সাথে সাথে বন্ধ থাকা স্ক্রিন ও পিসি অন করা।
        """
        try:
            self.is_display_sleeping = False
            # Windows API to turn on monitor (-1 = on)
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, -1)
            pyautogui.press("shift")
            print("[SYSTEM] Display turned ON (System Awakened!)")
            return True
        except Exception as e:
            print(f"[SYSTEM WAKE ERROR]: {e}")
            return False

    def take_screenshot(self):
        """স্ক্রিনশট নেওয়া"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"JUBAYER_SNAP_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)
        try:
            pyautogui.screenshot().save(filepath)
            print(f"[SYSTEM] Screenshot saved to: {filepath}")
            return filepath
        except Exception:
            try:
                import shutil
                pyautogui.hotkey("win", "prtsc")
                time.sleep(0.8)
                win_screenshots = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
                if os.path.exists(win_screenshots):
                    files = [os.path.join(win_screenshots, f) for f in os.listdir(win_screenshots) if f.lower().endswith(".png")]
                    if files:
                        latest_file = max(files, key=os.path.getmtime)
                        shutil.copy2(latest_file, filepath)
                        print(f"[SYSTEM] Screenshot saved to: {filepath}")
                        return filepath
            except Exception as inner_e:
                print(f"[SYSTEM SCREENSHOT WARNING]: {inner_e}")
            return filepath

    def execute_shutdown(self):
        """কম্পিউটার সরাসরি সম্পূর্ণ শাটডাউন করা"""
        print("[SYSTEM] Shutting down PC now...")
        subprocess.run("shutdown /s /t 2", shell=True)

    def execute_restart(self):
        """কম্পিউটার রিস্টার্ট করা"""
        print("[SYSTEM] Restarting PC now...")
        subprocess.run("shutdown /r /t 2", shell=True)
