"""
=============================================================================
STAGE 01: CORE OS & POWER CONTROLLER
=============================================================================
কম্পিউটার সিস্টেমের মূল নিয়ন্ত্রণ:
- ভলিউম নিয়ন্ত্রণ (+১০%, -১০%, মিউট/আনমিউট)
- ডিসপ্লে ইকো-স্লিপ (মনিটর অফ কিন্তু মাইক চালু) এবং ইনস্ট্যান্ট ওয়েক
- উইন্ডো ক্লোজ (Alt+F4)
- শো ডেস্কটপ / মিনিমাইজ অল (Win+D)
- পিসি লক (LockWorkStation)
- নির্ভরযোগ্য স্ক্রিনশট গ্রহণ (Pictures/Jubayer_Captures এ সংরক্ষণ)
- সরাসরি সিস্টেম শাটডাউন ও রিস্টার্ট
=============================================================================
"""

import os
import time
import subprocess
import ctypes
import shutil
from datetime import datetime
import pyautogui

pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = False

class CoreSystemController:
    def __init__(self):
        self.screenshot_dir = os.path.join(os.path.expanduser("~"), "Pictures", "Jubayer_Captures")
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.is_display_sleeping = False

    def volume_up(self, steps=5):
        """ভলিউম বাড়ানো (+১০%)"""
        for _ in range(steps):
            pyautogui.press("volumeup")
        print(f"[STAGE 1] Volume Increased (+{steps * 2}%)")
        return True

    def volume_down(self, steps=5):
        """ভলিউম কমানো (-১০%)"""
        for _ in range(steps):
            pyautogui.press("volumedown")
        print(f"[STAGE 1] Volume Decreased (-{steps * 2}%)")
        return True

    def toggle_mute(self):
        """সাউন্ড মিউট বা আনমিউট"""
        pyautogui.press("volumemute")
        print("[STAGE 1] Sound Mute/Unmute Toggled")
        return True

    def close_active_window(self):
        """বর্তমান উইন্ডো বন্ধ (Alt + F4)"""
        pyautogui.hotkey("alt", "f4")
        print("[STAGE 1] Active Window Closed")
        return True

    def show_desktop(self):
        """ডেস্কটপ টগল / সব উইন্ডো মিনিমাইজ (Win + D)"""
        pyautogui.hotkey("win", "d")
        print("[STAGE 1] Desktop Toggled")
        return True

    def lock_pc(self):
        """পিসি লক করা"""
        subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
        print("[STAGE 1] Workstation Locked")
        return True

    def sleep_display(self):
        """মনিটর অফ করে ইকো-স্লিপে পাঠানো (মাইক্রোফোন ও সিস্টেম সজাগ থাকে)"""
        try:
            self.is_display_sleeping = True
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, 2)
            print("[STAGE 1] Display sleeping (Voice-wake ready)")
            return True
        except Exception as e:
            print(f"[STAGE 1 ERROR] Sleep display failed: {e}")
            return False

    def wake_display(self):
        """স্লিপ থাকা ডিসপ্লে মুখে ডাকার সাথে সাথে তাৎক্ষণিক অন করা"""
        try:
            self.is_display_sleeping = False
            ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, -1)
            pyautogui.press("shift")
            print("[STAGE 1] Display awakened successfully")
            return True
        except Exception as e:
            print(f"[STAGE 1 ERROR] Wake display failed: {e}")
            return False

    def take_screenshot(self):
        """ফুল স্ক্রিনশট নিয়ে Pictures/Jubayer_Captures ফোল্ডারে সেভ করা"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"JUBAYER_STAGE1_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)

        try:
            pyautogui.screenshot().save(filepath)
            print(f"[STAGE 1] Screenshot saved: {filepath}")
            return filepath
        except Exception:
            try:
                pyautogui.hotkey("win", "prtsc")
                time.sleep(0.8)
                win_shots = os.path.join(os.path.expanduser("~"), "Pictures", "Screenshots")
                if os.path.exists(win_shots):
                    files = [os.path.join(win_shots, f) for f in os.listdir(win_shots) if f.lower().endswith(".png")]
                    if files:
                        latest = max(files, key=os.path.getmtime)
                        shutil.copy2(latest, filepath)
                        print(f"[STAGE 1] Screenshot saved (via Win+PrtSc): {filepath}")
                        return filepath
            except Exception as inner_e:
                print(f"[STAGE 1 WARNING] Screenshot copy failed: {inner_e}")
            return filepath

    def execute_shutdown(self):
        """কম্পিউটার সরাসরি শাটডাউন"""
        print("[STAGE 1] Initiating Immediate PC Shutdown...")
        subprocess.run("shutdown /s /t 2", shell=True)
        return True

    def execute_restart(self):
        """কম্পিউটার রিস্টার্ট"""
        print("[STAGE 1] Initiating PC Restart...")
        subprocess.run("shutdown /r /t 2", shell=True)
        return True

if __name__ == "__main__":
    controller = CoreSystemController()
    print("--- Testing Stage 01 Core System Controls ---")
    controller.volume_up()
    time.sleep(0.5)
    controller.volume_down()
    time.sleep(0.5)
    shot = controller.take_screenshot()
    print(f"Test complete. Screenshot: {shot}")
