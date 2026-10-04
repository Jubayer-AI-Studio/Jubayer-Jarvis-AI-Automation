"""
=============================================================================
STAGE 03: MEDIA & YOUTUBE AUTOMATION
=============================================================================
গান, ভিডিও ও মাল্টিমিডিয়া সরাসরি কণ্ঠ দিয়ে পরিচালনা:
- ইউটিউবে গান/ভিডিও সার্চ এবং স্বয়ংক্রিয়ভাবে ১ম ভিডিও প্লে
- ফুলস্ক্রিন টগল (F)
- ভিডিও পজ / প্লে (K / Space)
- সাউন্ড মিউট / আনমিউট (M)
- পরবর্তী ভিডিও (Shift + N) ও আগের ভিডিও (Shift + P)
- মিডিয়া প্লেয়ার হটকিজ
=============================================================================
"""

import time
import subprocess
import webbrowser
import urllib.parse
import threading
import pyautogui

pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = False

class MediaYouTubeController:
    def __init__(self):
        pass

    def open_youtube(self, query=None, auto_play=True):
        """
        ইউটিউবে গান/ভিডিও সার্চ করা এবং স্বয়ংক্রিয়ভাবে ভিডিও চালানো
        """
        if query:
            encoded = urllib.parse.quote_plus(query)
            url = f"https://www.youtube.com/results?search_query={encoded}"
            try:
                subprocess.Popen(f'start chrome "{url}"', shell=True)
                print(f"[STAGE 3] Searching YouTube for: {query}")
                if auto_play:
                    threading.Thread(target=self._auto_click_first_video, daemon=True).start()
            except Exception:
                webbrowser.open(url)
        else:
            url = "https://www.youtube.com"
            try:
                subprocess.Popen(f'start chrome "{url}"', shell=True)
                print("[STAGE 3] Opened YouTube Home")
            except Exception:
                webbrowser.open(url)

    def _auto_click_first_video(self):
        """রেজাল্ট লোড হওয়া মাত্র ১ম ভিডিওতে ক্লিক"""
        time.sleep(3.0)
        try:
            screen_w, screen_h = pyautogui.size()
            target_x = int(screen_w * 0.38)
            target_y = int(screen_h * 0.35)
            pyautogui.click(target_x, target_y)
            print(f"[STAGE 3] Autoplay clicked first video at ({target_x}, {target_y})")
        except Exception as e:
            print(f"[STAGE 3 AUTOPLAY WARNING]: {e}")

    def play_first_video_now(self):
        """বর্তমানে স্ক্রিনে থাকা রেজাল্টের ১ম ভিডিও ক্লিক করা"""
        try:
            screen_w, screen_h = pyautogui.size()
            target_x = int(screen_w * 0.38)
            target_y = int(screen_h * 0.35)
            pyautogui.click(target_x, target_y)
            print("[STAGE 3] Clicked first video")
            return True
        except Exception:
            return False

    def toggle_play_pause(self):
        """ভিডিও পজ বা প্লে"""
        pyautogui.press('k')
        print("[STAGE 3] Video Play/Pause toggled")

    def toggle_fullscreen(self):
        """ইউটিউব ফুলস্ক্রিন টগল (F)"""
        pyautogui.press('f')
        print("[STAGE 3] Fullscreen toggled")

    def toggle_mute(self):
        """মিউট বা আনমিউট (M)"""
        pyautogui.press('m')
        print("[STAGE 3] Mute toggled")

    def next_video(self):
        """পরবর্তী ভিডিও চালানো (Shift + N)"""
        pyautogui.hotkey('shift', 'n')
        print("[STAGE 3] Switched to next video")

    def prev_video(self):
        """পূর্ববর্তী ভিডিও চালানো (Shift + P)"""
        pyautogui.hotkey('shift', 'p')
        print("[STAGE 3] Switched to previous video")

if __name__ == "__main__":
    media = MediaYouTubeController()
    print("--- Testing Stage 03 Media & YouTube Controller ---")
    media.open_youtube("Relaxing Nature 4K", auto_play=True)
    print("Test complete.")
