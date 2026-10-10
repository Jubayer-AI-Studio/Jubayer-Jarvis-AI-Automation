"""
Action Controller for JARVIS-AETHER
Executes operating system level commands, mouse actions, multimedia controls,
presentation slide navigation, screenshot captures, and app launchers.
100% Free & Open-Source (PyAutoGUI + Windows APIs).
"""

import os
import time
import subprocess
import webbrowser
from datetime import datetime
import pyautogui

# Disable default PyAutoGUI artificial pause for ultra-smooth responsiveness
pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = True  # Move mouse to upper-left corner as hardware kill-switch

class ActionController:
    def __init__(self):
        self.is_dragging = False
        self.last_click_time = 0
        self.click_cooldown = 0.28  # Prevents accidental rapid-fire clicks
        self.last_volume_time = 0

        # Create screenshots folder
        self.screenshot_dir = os.path.join(os.path.expanduser("~"), "Pictures", "Jarvis_Captures")
        os.makedirs(self.screenshot_dir, exist_ok=True)

    # --- MOUSE & CURSOR AUTOMATION ---
    def move_mouse(self, screen_x, screen_y):
        """Moves cursor to screen coordinates"""
        pyautogui.moveTo(screen_x, screen_y)

    def left_click(self):
        """Triggers left click with debounce protection"""
        current_time = time.time()
        if current_time - self.last_click_time > self.click_cooldown:
            pyautogui.click()
            self.last_click_time = current_time
            return True
        return False

    def right_click(self):
        """Triggers right click with debounce protection"""
        current_time = time.time()
        if current_time - self.last_click_time > self.click_cooldown:
            pyautogui.rightClick()
            self.last_click_time = current_time
            return True
        return False

    def double_click(self):
        """Triggers double click"""
        pyautogui.doubleClick()

    def start_drag(self):
        """Presses and holds left mouse button for dragging"""
        if not self.is_dragging:
            pyautogui.mouseDown()
            self.is_dragging = True

    def stop_drag(self):
        """Releases mouse button after drag"""
        if self.is_dragging:
            pyautogui.mouseUp()
            self.is_dragging = False

    def scroll_page(self, direction="UP", amount=120):
        """Scrolls current window up or down"""
        if direction == "UP":
            pyautogui.scroll(amount)
        else:
            pyautogui.scroll(-amount)

    # --- PRESENTATION SLIDE AUTOMATION ---
    def next_slide(self):
        """Navigates to next slide (PowerPoint / PDF / Slides)"""
        pyautogui.press("right")

    def prev_slide(self):
        """Navigates to previous slide"""
        pyautogui.press("left")

    # --- SYSTEM & VOLUME AUTOMATION ---
    def volume_up(self, steps=2):
        """Increases system volume"""
        for _ in range(steps):
            pyautogui.press("volumeup")

    def volume_down(self, steps=2):
        """Decreases system volume"""
        for _ in range(steps):
            pyautogui.press("volumedown")

    def volume_mute_toggle(self):
        """Toggles mute on/off"""
        pyautogui.press("volumemute")

    def media_play_pause(self):
        """Toggles media play/pause"""
        pyautogui.press("playpause")

    def show_desktop(self):
        """Minimizes all windows to reveal desktop"""
        pyautogui.hotkey("win", "d")

    def lock_workstation(self):
        """Locks the Windows computer"""
        subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)

    def take_screenshot(self):
        """Captures full screen, saves with timestamp, and returns file path"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"JARVIS_SNAP_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)

        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        return filepath

    # --- APP LAUNCHERS ---
    def open_browser(self, url="https://www.google.com"):
        """Opens default browser or Google Chrome"""
        webbrowser.open(url)

    def open_youtube(self):
        """Opens YouTube in web browser"""
        webbrowser.open("https://www.youtube.com")

    def open_notepad(self):
        """Launches Windows Notepad"""
        subprocess.Popen("notepad.exe")

    def open_calculator(self):
        """Launches Windows Calculator"""
        subprocess.Popen("calc.exe")
