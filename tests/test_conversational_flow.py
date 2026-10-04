"""
Test conversational dialogue and window closing
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

from core.natural_brain import NaturalBrain

nb = NaturalBrain()

test_cases = [
    ("hello hello", "CHAT_GREETING"),
    ("can you hear me", "CHAT_HEAR_ME"),
    ("close YouTube", "WINDOW_CLOSE"),
    ("YouTube band karo", "WINDOW_CLOSE"),
    ("stop the Chrome", "WINDOW_CLOSE"),
    ("theke ber hou", "WINDOW_CLOSE"),
    ("ki samasya", "CHAT_PROBLEM"),
    ("bhai", "CHAT_BHAI"),
    ("kemon acho", "CHAT_HOW_ARE_YOU"),
    ("tumi ke", "CHAT_WHO_ARE_YOU"),
    ("play Quran Tilawat", "YOUTUBE_PLAY"),
    ("kichu ekta bolo", "CHAT_FALLBACK")
]

all_passed = True
print("\n=== RUNNING CONVERSATIONAL & CLOSE TESTS ===")
for text, expected_intent in test_cases:
    intent, payload = nb.parse_intent(text)
    status = "PASS" if intent == expected_intent else "FAIL"
    if status == "FAIL":
        all_passed = False
    print(f"[{status}] '{text}' -> Intent: {intent} (Expected: {expected_intent})")

assert all_passed, "Some conversational test cases failed!"
print("\n🎉 ALL CONVERSATIONAL AND WINDOW CLOSE TESTS PASSED 100%! 🎉\n")
