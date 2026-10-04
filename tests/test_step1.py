"""
Step 1 Verification Test: Windows System & Power Controls
Tests Volume (10%), Window Close, Desktop, Screenshot, and Shutdown confirmation safety.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

from actions.system_controls import SystemControls
from actions.app_launcher import AppLauncher
from voice.speech_feedback import SpeechFeedback
from core.wake_word import WakeWordDispatcher

# Mock system_controls execute_shutdown to avoid actually shutting down during test!
class MockSystemControls(SystemControls):
    def execute_shutdown(self):
        print("[MOCK SUCCESS] execute_shutdown() called safely in test!")

    def execute_restart(self):
        print("[MOCK SUCCESS] execute_restart() called safely in test!")

sc = MockSystemControls()
al = AppLauncher()
sf = SpeechFeedback()
ww = WakeWordDispatcher(sf, sc, al)

print("\n=== TEST 1: Volume Up (10%) ===")
handled, intent = ww.process_speech("আওয়াজ একটু বাড়িয়ে দে তো")
print(f"Result -> Handled: {handled}, Intent: {intent}")
assert intent == "VOLUME_UP", f"Expected VOLUME_UP, got {intent}"

print("\n=== TEST 2: Volume Down (10%) ===")
handled, intent = ww.process_speech("শব্দটা একটু কমাও অনেক বেশি জোরে")
print(f"Result -> Handled: {handled}, Intent: {intent}")
assert intent == "VOLUME_DOWN", f"Expected VOLUME_DOWN, got {intent}"

print("\n=== TEST 3: Show Desktop ===")
handled, intent = ww.process_speech("সব সরাও ডেস্কটপ দেখাও")
print(f"Result -> Handled: {handled}, Intent: {intent}")
assert intent == "WINDOW_DESKTOP", f"Expected WINDOW_DESKTOP, got {intent}"

print("\n=== TEST 4: Close Active Window ===")
handled, intent = ww.process_speech("উইন্ডোটা কেটে দে")
print(f"Result -> Handled: {handled}, Intent: {intent}")
assert intent == "WINDOW_CLOSE", f"Expected WINDOW_CLOSE, got {intent}"

print("\n=== TEST 5: Capture Screenshot ===")
handled, intent = ww.process_speech("স্ক্রিনের একটা ছবি তুলে রাখ")
print(f"Result -> Handled: {handled}, Intent: {intent}")
assert intent == "SCREENSHOT", f"Expected SCREENSHOT, got {intent}"

print("\n=== TEST 6: Workstation Lock ===")
handled, intent = ww.process_speech("এখন বাইরে যাব পিসি লক করো")
print(f"Result -> Handled: {handled}, Intent: {intent}")
assert intent == "POWER_LOCK", f"Expected POWER_LOCK, got {intent}"

print("\n=== TEST 7: Shutdown with Cancel (Safety Confirmation) ===")
handled, intent1 = ww.process_speech("পিসিটা এখন অফ করে দাও ঘুমাবো")
print(f"Step 7a -> Intent: {intent1} (Awaiting user confirmation)")
assert intent1 == "AWAITING_SHUTDOWN_CONFIRM"

handled, intent2 = ww.process_speech("না থাক")
print(f"Step 7b -> User said 'না থাক' -> Intent: {intent2}")
assert intent2 == "CONFIRMATION_CANCELLED"

print("\n=== TEST 8: Shutdown with Approval (Safety Confirmation) ===")
handled, intent3 = ww.process_speech("shut down the computer")
print(f"Step 8a -> Intent: {intent3} (Awaiting user confirmation)")
assert intent3 == "AWAITING_SHUTDOWN_CONFIRM"

handled, intent4 = ww.process_speech("yes")
print(f"Step 8b -> User said 'yes' -> Intent: {intent4}")
assert intent4 == "SHUTDOWN_CONFIRMED"

print("\n=======================================================")
print("  ALL STEP 1 TESTS PASSED WITH 100% SUCCESS!")
print("=======================================================\n")
