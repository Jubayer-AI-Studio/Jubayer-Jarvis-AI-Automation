"""
=============================================================================
STAGE 04: WEB BROWSER & INTERNET RESEARCH
=============================================================================
ইন্টারনেট ব্রাউজিং ও রিসার্চ স্বয়ংক্রিয়ভাবে নিয়ন্ত্রণ:
- গুগল ক্রোম বা ডিফল্ট ব্রাউজার ওপেন
- নতুন ট্যাব (Ctrl+T) ও ট্যাব বন্ধ (Ctrl+W)
- ট্যাব সুইচিং (পরের ট্যাব Ctrl+Tab, আগের ট্যাব Ctrl+Shift+Tab)
- গুগল সার্চ সরাসরি সম্পন্ন করা
- পেজ স্ক্রোল ডাউন (PageDown / Down), পেজ স্ক্রোল আপ (PageUp / Up)
- জুম ইন (Ctrl++), জুম আউট (Ctrl+-), রিসেট জুম (Ctrl+0)
- পেজ রিলোড (F5)
- ফেসবুক, জিমেইল, লিঙ্কডইন ইত্যাদি দ্রুত ওপেন
=============================================================================
"""

import time
import subprocess
import webbrowser
import urllib.parse
import pyautogui

pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = False

class WebBrowserController:
    def __init__(self):
        pass

    def open_browser(self, url="https://www.google.com"):
        """ব্রাউজার ওপেন করা"""
        try:
            subprocess.Popen(f'start chrome "{url}"', shell=True)
            print(f"[STAGE 4] Opened Chrome: {url}")
        except Exception:
            webbrowser.open(url)

    def search_google(self, query):
        """গুগলে কোনো কিছু সার্চ করা"""
        encoded = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}"
        self.open_browser(url)
        print(f"[STAGE 4] Searched Google for: {query}")

    def new_tab(self):
        """নতুন ট্যাব খোলা (Ctrl + T)"""
        pyautogui.hotkey('ctrl', 't')
        print("[STAGE 4] New tab opened")

    def close_tab(self):
        """বর্তমান ট্যাব বন্ধ (Ctrl + W)"""
        pyautogui.hotkey('ctrl', 'w')
        print("[STAGE 4] Tab closed")

    def reopen_tab(self):
        """বন্ধ করা ট্যাব পুনরায় খোলা (Ctrl + Shift + T)"""
        pyautogui.hotkey('ctrl', 'shift', 't')
        print("[STAGE 4] Reopened closed tab")

    def next_tab(self):
        """পরের ট্যাবে যাওয়া (Ctrl + Tab)"""
        pyautogui.hotkey('ctrl', 'tab')
        print("[STAGE 4] Switched to next tab")

    def prev_tab(self):
        """পূর্বের ট্যাবে যাওয়া (Ctrl + Shift + Tab)"""
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        print("[STAGE 4] Switched to previous tab")

    def scroll_down(self, clicks=3):
        """পেজ নিচে নামানো"""
        for _ in range(clicks):
            pyautogui.press('pagedown')
        print("[STAGE 4] Scrolled down")

    def scroll_up(self, clicks=3):
        """পেজ ওপরে উঠানো"""
        for _ in range(clicks):
            pyautogui.press('pageup')
        print("[STAGE 4] Scrolled up")

    def reload_page(self):
        """পেজ রিফ্রেশ (F5)"""
        pyautogui.press('f5')
        print("[STAGE 4] Page reloaded")

    def zoom_in(self):
        """জুম ইন করা"""
        pyautogui.hotkey('ctrl', '+')
        print("[STAGE 4] Zoomed in")

    def zoom_out(self):
        """জুম আউট করা"""
        pyautogui.hotkey('ctrl', '-')
        print("[STAGE 4] Zoomed out")

    def zoom_reset(self):
        """স্বাভাবিক জুমে ফেরা (Ctrl + 0)"""
        pyautogui.hotkey('ctrl', '0')
        print("[STAGE 4] Zoom reset")

if __name__ == "__main__":
    wb = WebBrowserController()
    print("--- Testing Stage 04 Web Browser Controller ---")
    wb.search_google("Bangladesh latest tech news")
    time.sleep(2.0)
    wb.scroll_down()
    print("Test complete.")
