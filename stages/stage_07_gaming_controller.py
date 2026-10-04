"""
=============================================================================
STAGE 07: GAMING & FAST INPUT CONTROLLER
=============================================================================
কীবোর্ড বা মাউস স্পর্শ না করে ভয়েস কমান্ড দিয়ে গেম খেলা ও ফাস্ট অ্যাকশন পরিচালনা:
- ডিরেকশনাল মুভমেন্ট: সামনে (W), পেছনে (S), বামে (A), ডানে (D)
- অ্যাকশন: লাফানো/জাম্প (Space), দৌড়ানো/স্প্রিন্ট (Shift), রিলোড (R), ইন্টার‍্যাক্ট (E), ক্রাউচ (Ctrl)
- মাউস শুটিং ও এইম: ফায়ার/অ্যাটাক (Left Click), স্কোপ/এইম (Right Click)
- প্রেস অ্যান্ড হোল্ড অ্যাকশন (যেমন: ৩ সেকেন্ড সামনে হাঁটা)
- গেম পজ / মেনু (Esc)
- স্টিম বা নির্দিষ্ট গেম লঞ্চ করা
=============================================================================
"""

import time
import subprocess
import threading
import pyautogui

pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = False

class GamingController:
    def __init__(self):
        pass

    def move_forward(self, seconds=1.0):
        """সামনে হাঁটা (W কি চেপে রাখা)"""
        threading.Thread(target=self._hold_key, args=('w', seconds), daemon=True).start()
        print(f"[STAGE 7] Moving forward for {seconds}s")

    def move_backward(self, seconds=1.0):
        """পেছনে হাঁটা (S কি চেপে রাখা)"""
        threading.Thread(target=self._hold_key, args=('s', seconds), daemon=True).start()
        print(f"[STAGE 7] Moving backward for {seconds}s")

    def move_left(self, seconds=0.5):
        """বামে যাওয়া (A কি)"""
        threading.Thread(target=self._hold_key, args=('a', seconds), daemon=True).start()
        print(f"[STAGE 7] Moving left for {seconds}s")

    def move_right(self, seconds=0.5):
        """ডানে যাওয়া (D কি)"""
        threading.Thread(target=self._hold_key, args=('d', seconds), daemon=True).start()
        print(f"[STAGE 7] Moving right for {seconds}s")

    def _hold_key(self, key, duration):
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)

    def jump(self):
        """লাফানো (Space)"""
        pyautogui.press('space')
        print("[STAGE 7] Jump executed")

    def crouch(self):
        """বসে পড়া / ক্রাউচ (Ctrl / C)"""
        pyautogui.press('c')
        print("[STAGE 7] Crouch toggled")

    def sprint(self, seconds=2.0):
        """দৌড়ানো (Shift + W)"""
        def _run():
            pyautogui.keyDown('shift')
            pyautogui.keyDown('w')
            time.sleep(seconds)
            pyautogui.keyUp('w')
            pyautogui.keyUp('shift')
        threading.Thread(target=_run, daemon=True).start()
        print(f"[STAGE 7] Sprinting for {seconds}s")

    def attack_or_fire(self, times=1):
        """অ্যাটাক বা ফায়ার করা (Left Click)"""
        for _ in range(times):
            pyautogui.click()
        print(f"[STAGE 7] Attacked {times} times")

    def aim_down_sight(self, hold_seconds=2.0):
        """স্কোপ বা এইম করা (Right Click)"""
        def _scope():
            pyautogui.mouseDown(button='right')
            time.sleep(hold_seconds)
            pyautogui.mouseUp(button='right')
        threading.Thread(target=_scope, daemon=True).start()
        print(f"[STAGE 7] Aiming down sight for {hold_seconds}s")

    def reload_weapon(self):
        """অস্ত্র রিলোড (R)"""
        pyautogui.press('r')
        print("[STAGE 7] Reload weapon (R)")

    def interact(self):
        """দরজা খোলা বা বস্তু সংগ্রহ (E / F)"""
        pyautogui.press('e')
        pyautogui.press('f')
        print("[STAGE 7] Interact executed (E/F)")

    def pause_game(self):
        """গেম পজ / মেনু (Esc)"""
        pyautogui.press('esc')
        print("[STAGE 7] Game paused / Menu opened")

if __name__ == "__main__":
    game = GamingController()
    print("--- Testing Stage 07 Gaming & Fast Input Controller ---")
    game.jump()
    time.sleep(0.5)
    game.reload_weapon()
    print("Test complete.")
