"""
=============================================================================
অ্যাকশন মডিউল: অ্যাপ ও মিডিয়া লঞ্চার (APPLICATION & MEDIA LAUNCHER)
=============================================================================
গুগল ক্রোম, ইউটিউব ভিডিও সরাসরি প্লে করা, এবং উইন্ডোজ অ্যাপ্লিকেশন পরিচালনা।
"""

import subprocess
import webbrowser
import urllib.parse
import threading
import time
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.0

class AppLauncher:
    def open_browser(self, url="https://www.google.com"):
        """সরাসরি গুগল ক্রোম সামনে চালু করে"""
        try:
            subprocess.Popen(f'start chrome "{url}"', shell=True)
            print(f"[LAUNCHER] Launched Chrome: {url}")
        except Exception as e:
            print(f"[LAUNCHER FALLBACK]: {e}")
            webbrowser.open(url)

    def open_youtube(self, query=None, auto_play=True):
        """ইউটিউব ওপেন করে এবং নির্দিষ্ট গান/ভিডিও থাকলে অটোমেটিক প্রথম ভিডিওটি চালু করে"""
        if query:
            encoded = urllib.parse.quote_plus(query)
            url = f"https://www.youtube.com/results?search_query={encoded}"
            try:
                subprocess.Popen(f'start chrome "{url}"', shell=True)
                print(f"[LAUNCHER] Searching YouTube for: {query}")
                if auto_play:
                    threading.Thread(target=self._auto_click_first_video, daemon=True).start()
            except Exception:
                webbrowser.open(url)
        else:
            url = "https://www.youtube.com"
            try:
                subprocess.Popen(f'start chrome "{url}"', shell=True)
                print(f"[LAUNCHER] Opened YouTube Home")
            except Exception:
                webbrowser.open(url)

    def _auto_click_first_video(self):
        """সার্চ রেজাল্ট লোড হওয়ার পর স্বয়ংক্রিয়ভাবে প্রথম ভিডিওতে ক্লিক করে চালানো"""
        time.sleep(3.0)
        try:
            screen_w, screen_h = pyautogui.size()
            # সাধারণ রেজোলিউশনে ইউটিউব সার্চ রেজাল্টের প্রথম ভিডিওর পজিশন
            target_x = int(screen_w * 0.38)
            target_y = int(screen_h * 0.35)
            pyautogui.click(target_x, target_y)
            print(f"[YOUTUBE AUTO-PLAY] Clicked first video at ({target_x}, {target_y})")
        except Exception as e:
            print(f"[YOUTUBE AUTO-PLAY ERROR]: {e}")

    def play_first_video_now(self):
        """স্ক্রিনে থাকা প্রথম ভিডিও তাৎক্ষণিক ক্লিক করে চালু করা"""
        try:
            screen_w, screen_h = pyautogui.size()
            target_x = int(screen_w * 0.38)
            target_y = int(screen_h * 0.35)
            pyautogui.click(target_x, target_y)
            print(f"[YOUTUBE] Clicked first video at ({target_x}, {target_y})")
            return True
        except Exception:
            return False

    def toggle_youtube_play_pause(self):
        """ভিডিও চলাকালীন পজ বা প্লে করা (Space বা K কি)"""
        pyautogui.press('k')

    def toggle_fullscreen(self):
        """ইউটিউব ফুলস্ক্রিন করা (F কি)"""
        pyautogui.press('f')

    def toggle_mute(self):
        """ইউটিউব সাউন্ড মিউট বা আনমিউট (M কি)"""
        pyautogui.press('m')

    def next_video(self):
        """পরের ভিডিও প্লে করা (Shift + N)"""
        pyautogui.hotkey('shift', 'n')

    def open_notepad(self):
        subprocess.Popen("notepad.exe")
        print("[LAUNCHER] Launched Notepad")

    def open_calculator(self):
        subprocess.Popen("calc.exe")
        print("[LAUNCHER] Launched Calculator")
