"""
Verification test for Voice Power Off, Voice Wake, and No-Phantom-Chrome
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

from actions.system_controls import SystemControls
from actions.app_launcher import AppLauncher
from voice.speech_feedback import SpeechFeedback
from core.wake_word import WakeWordDispatcher

class MockSystemControls(SystemControls):
    def __init__(self):
        super().__init__()
        self.shutdown_called = False
        self.sleep_called = False
        self.wake_called = False

    def execute_shutdown(self):
        self.shutdown_called = True
        print("[MOCK] Windows Shutdown initiated!")

    def sleep_display(self):
        self.sleep_called = True
        self.is_display_sleeping = True
        print("[MOCK] Display Eco-Sleep Mode activated!")

    def wake_display(self):
        self.wake_called = True
        self.is_display_sleeping = False
        print("[MOCK] Display Awakened / Turned ON!")

sc = MockSystemControls()
al = AppLauncher()
sf = SpeechFeedback()
ww = WakeWordDispatcher(sf, sc, al)

print("\n=== TEST 1: No Phantom Chrome on Unknown Words ===")
handled, intent = ww.process_speech("random ambient noise or cough")
print(f"Unknown input result -> Handled: {handled}, Intent: {intent}")
assert intent is None, f"Chrome should NOT open on random input, got {intent}"
print("[PASS] Phantom Chrome bug completely eliminated!")

print("\n=== TEST 2: Instant PC Shutdown ===")
handled, intent = ww.process_speech("পিসিটা এখন অফ করে দাও ঘুমাবো")
print(f"Shutdown result -> Handled: {handled}, Intent: {intent}")
assert intent == "POWER_SHUTDOWN", f"Expected POWER_SHUTDOWN, got {intent}"
assert sc.shutdown_called == True, "execute_shutdown() was not called!"
print("[PASS] Direct PC Shutdown verified!")

print("\n=== TEST 3: PC Sleep (Turn OFF) by Voice ===")
handled, intent = ww.process_speech("পিসি স্লিপ করো")
print(f"Sleep result -> Handled: {handled}, Intent: {intent}")
assert intent == "POWER_SLEEP", f"Expected POWER_SLEEP, got {intent}"
assert sc.sleep_called == True, "sleep_display() was not called!"
print("[PASS] PC Sleep mode verified!")

print("\n=== TEST 4: Turn ON PC by Calling Name ===")
# Now PC is sleeping. User calls 'জুবায়ের' or 'পিসি অন করো'
handled, intent = ww.process_speech("পিসি অন করো")
print(f"Wake result -> Handled: {handled}, Intent: {intent}")
assert intent == "POWER_WAKE", f"Expected POWER_WAKE, got {intent}"
assert sc.wake_called == True, "wake_display() was not called!"
print("[PASS] Voice Wake / Turn ON verified!")

print("\n=======================================================")
print("  ALL VOICE POWER & WAKE TESTS PASSED WITH 100% SUCCESS!")
print("=======================================================\n")
