"""
=============================================================================
STAGE 06: CREATIVE & GRAPHICS AUTOMATION (ILLUSTRATOR / PHOTOSHOP)
=============================================================================
গ্রাফিক্স ডিজাইন ও ফটো এডিটিং সফটওয়্যার (Adobe Illustrator, Photoshop ইত্যাদি)
সম্পূর্ণ কণ্ঠস্বর দিয়ে পরিচালনা:
- ইলাস্ট্রেটর / ফটোশপ / পেইন্ট ওপেন করা
- নতুন ক্যানভাস / আর্টবোর্ড তৈরি (Ctrl + N, Enter)
- ইমেজ বা ফাইল ওপেন করা (Ctrl + O)
- আর্টবোর্ড জুম ইন (Ctrl++), জুম আউট (Ctrl+-), ফিট টু স্ক্রিন (Ctrl+0)
- সিলেকশন টুল (V), ডিরেক্ট সিলেকশন (A), পেন টুল (P), ব্রাশ (B), টেক্সট টুল (T)
- ডি-সিলেক্ট (Ctrl + Shift + A / Ctrl + D)
- গ্রুপ অবজেক্ট (Ctrl + G), আন-গ্রুপ (Ctrl + Shift + G)
- এক্সপোর্ট আর্টবোর্ড (Ctrl + Alt + Shift + S)
=============================================================================
"""

import os
import time
import subprocess
import pyautogui

pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = False

class CreativeGraphicsController:
    def __init__(self):
        # সাধারণ উইন্ডোজ ইন্সটল পাথ তালিকা
        self.illustrator_paths = [
            r"C:\Program Files\Adobe\Adobe Illustrator 2024\Support Files\Contents\Windows\Illustrator.exe",
            r"C:\Program Files\Adobe\Adobe Illustrator 2023\Support Files\Contents\Windows\Illustrator.exe",
            r"C:\Program Files\Adobe\Adobe Illustrator CC 2019\Support Files\Contents\Windows\Illustrator.exe",
        ]
        self.photoshop_paths = [
            r"C:\Program Files\Adobe\Adobe Photoshop 2024\Photoshop.exe",
            r"C:\Program Files\Adobe\Adobe Photoshop 2023\Photoshop.exe",
            r"C:\Program Files\Adobe\Adobe Photoshop CC 2019\Photoshop.exe",
        ]

    def open_illustrator(self):
        """অ্যাডোবি ইলাস্ট্রেটর চালু করা"""
        for path in self.illustrator_paths:
            if os.path.exists(path):
                subprocess.Popen(f'"{path}"')
                print(f"[STAGE 6] Launched Adobe Illustrator from {path}")
                return True

        # সিস্টেম কমান্ড ফলব্যাক
        try:
            subprocess.Popen("start illustrator", shell=True)
            print("[STAGE 6] Attempting to launch Illustrator via system path")
            return True
        except Exception:
            print("[STAGE 6] Illustrator executable not found; opening MS Paint as creative fallback")
            subprocess.Popen("mspaint.exe")
            return False

    def open_photoshop(self):
        """অ্যাডোবি ফটোশপ চালু করা"""
        for path in self.photoshop_paths:
            if os.path.exists(path):
                subprocess.Popen(f'"{path}"')
                print(f"[STAGE 6] Launched Adobe Photoshop from {path}")
                return True

        try:
            subprocess.Popen("start photoshop", shell=True)
            print("[STAGE 6] Attempting to launch Photoshop via system path")
            return True
        except Exception:
            print("[STAGE 6] Photoshop executable not found; opening MS Paint fallback")
            subprocess.Popen("mspaint.exe")
            return False

    def open_paint(self):
        """সহজ ড্রয়িং ও দ্রুত এডিটের জন্য MS Paint ওপেন"""
        subprocess.Popen("mspaint.exe")
        print("[STAGE 6] Opened Paint")

    def new_canvas(self):
        """নতুন ক্যানভাস তৈরি (Ctrl + N, তারপর এন্টার)"""
        pyautogui.hotkey('ctrl', 'n')
        time.sleep(0.5)
        pyautogui.press('enter')
        print("[STAGE 6] New Artboard / Canvas created")

    def open_file_dialog(self):
        """ফাইল বা ছবি ওপেন ডায়ালগ (Ctrl + O)"""
        pyautogui.hotkey('ctrl', 'o')
        print("[STAGE 6] Open File dialog triggered")

    def select_tool(self, tool_name):
        """
        টুলস শর্টকাট সক্রিয় করা (V, A, P, B, T, E, I)
        """
        tool_map = {
            "selection": "v",
            "select": "v",
            "direct": "a",
            "pen": "p",
            "brush": "b",
            "text": "t",
            "type": "t",
            "eraser": "e",
            "eyedropper": "i",
            "zoom": "z"
        }
        key = tool_map.get(tool_name.lower().strip(), "v")
        pyautogui.press(key)
        print(f"[STAGE 6] Selected tool: {tool_name} (Key: {key.upper()})")

    def deselect_all(self):
        """সিলেকশন বাতিল করা (Ctrl + Shift + A)"""
        pyautogui.hotkey('ctrl', 'shift', 'a')
        pyautogui.hotkey('ctrl', 'd')
        print("[STAGE 6] Deselected all items")

    def group_selection(self):
        """সিলেক্ট করা অবজেক্ট গ্রুপ করা (Ctrl + G)"""
        pyautogui.hotkey('ctrl', 'g')
        print("[STAGE 6] Objects grouped (Ctrl+G)")

    def ungroup_selection(self):
        """আনগ্রুপ করা (Ctrl + Shift + G)"""
        pyautogui.hotkey('ctrl', 'shift', 'g')
        print("[STAGE 6] Objects ungrouped")

    def fit_on_screen(self):
        """ক্যানভাস পুরো স্ক্রিনে ফিট করা (Ctrl + 0)"""
        pyautogui.hotkey('ctrl', '0')
        print("[STAGE 6] Canvas fit to screen (Ctrl+0)")

    def zoom_actual_size(self):
        """১০০% একচুয়াল সাইজ জুম (Ctrl + 1)"""
        pyautogui.hotkey('ctrl', '1')
        print("[STAGE 6] 100% Zoom activated")

    def export_for_web(self):
        """ওয়েবের জন্য সেভ ও এক্সপোর্ট ডায়ালগ (Ctrl + Alt + Shift + S)"""
        pyautogui.hotkey('ctrl', 'alt', 'shift', 's')
        print("[STAGE 6] Export for Web dialog triggered")

if __name__ == "__main__":
    creative = CreativeGraphicsController()
    print("--- Testing Stage 06 Creative & Graphics Automation ---")
    creative.open_paint()
    time.sleep(1.5)
    creative.select_tool("brush")
    print("Test complete.")
