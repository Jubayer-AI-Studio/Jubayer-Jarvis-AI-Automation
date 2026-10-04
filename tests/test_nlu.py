"""
Verification test for NaturalBrain NLU
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

from actions.system_controls import SystemControls
from actions.app_launcher import AppLauncher
from voice.speech_feedback import SpeechFeedback
from core.wake_word import WakeWordDispatcher

sf = SpeechFeedback()
sc = SystemControls()
al = AppLauncher()
ww = WakeWordDispatcher(sf, sc, al)

test_sentences = [
    'আমার একটা গান শুনতে ইচ্ছে করতেছে, ইউটিউব থেকে হাফিজের একটা নাশিদ বাজাও তো',
    'একটু ইউটিউবে ঢুকে হাফিজের গজলটা ছাড়ো',
    'বোরিং লাগতেছে কিছু একটা চালিয়ে দাও',
    'পিসিটা এখন অফ করে দাও ঘুমাবো',
    'একটু শব্দটা বাড়িয়ে দাও তো শুনতে পাচ্ছি না',
    'আজকের আবহাওয়ার খবরটা একটু গুগল করো তো',
    'একটু নোটপ্যাডটা সামনে এনে দাও তো কিছু লিখব',
    'Hey can you play some relaxing rain sounds on YouTube',
    'Shut this thing down right now',
    'Turn the sound a bit higher',
    'First video open please',
    'What is the distance between earth and moon',
    'You are awesome thank you'
]

for s in test_sentences:
    print('---------------------------------------------')
    handled, intent = ww.process_speech(s)
    print(f'Sentence: "{s[:40]}..." -> Handled: {handled}, Intent: {intent}')
