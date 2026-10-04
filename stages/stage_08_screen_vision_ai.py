"""
=============================================================================
STAGE 08: SCREEN VISION & AI INSPECTOR
=============================================================================
স্ক্রিনে কী চলছে তা পর্যবেক্ষণ ও স্বয়ংক্রিয় এআই বিশ্লেষণ:
- স্ক্রিন রেজোলিউশন ও অ্যাক্টিভ বাউন্ডস নির্ধারণ
- স্ক্রিনশট এনালিসিস ও এরর সনাক্তকরণ
- মাউস কার্সারের বর্তমান অবস্থান নির্ধারণ
- নির্দিষ্ট কোঅর্ডিনেটে স্মুথ ক্লিক ও ড্র্যাগ
- স্ক্রিনে নির্দিষ্ট টেক্সট বা বোতাম খোঁজার ভিত্তি
=============================================================================
"""

import os
import time
import pyautogui

pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = False

class ScreenVisionInspector:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

    def get_screen_resolution(self):
        """স্ক্রিনের আকার জানা"""
        return {"width": self.screen_width, "height": self.screen_height}

    def get_mouse_position(self):
        """মাউস কার্সার বর্তমানে কোথায় আছে তা জানা"""
        x, y = pyautogui.position()
        print(f"[STAGE 8] Mouse is at ({x}, {y})")
        return x, y

    def move_mouse_to_center(self):
        """মাউস ঠিক স্ক্রিনের মাঝখানে নেওয়া"""
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        pyautogui.moveTo(center_x, center_y, duration=0.3)
        print(f"[STAGE 8] Mouse centered at ({center_x}, {center_y})")

    def click_at_percent(self, x_pct, y_pct):
        """
        স্ক্রিনের শতকরা অনুপাত অনুযায়ী ক্লিক (যেমন: মাঝখানে ৫০%, ৫০%)
        """
        target_x = int(self.screen_width * (x_pct / 100.0))
        target_y = int(self.screen_height * (y_pct / 100.0))
        pyautogui.click(target_x, target_y)
        print(f"[STAGE 8] Clicked at {x_pct}%, {y_pct}% -> ({target_x}, {target_y})")

    def inspect_active_screen(self):
        """স্ক্রিনের সারসংক্ষেপ প্রদান"""
        res = self.get_screen_resolution()
        mx, my = self.get_mouse_position()
        summary = (
            f"Screen Resolution: {res['width']}x{res['height']}. "
            f"Cursor Position: ({mx}, {my}). Ready to inspect UI elements."
        )
        print(f"[STAGE 8] {summary}")
        return summary

if __name__ == "__main__":
    inspector = ScreenVisionInspector()
    print("--- Testing Stage 08 Screen Vision & AI Inspector ---")
    summary = inspector.inspect_active_screen()
    inspector.move_mouse_to_center()
    print("Test complete.")
