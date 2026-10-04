"""
=============================================================================
ভিশন মডিউল: হ্যান্ড ট্র্যাকার (HAND TRACKER)
=============================================================================
হাতের ২১টি ল্যান্ডমার্ক পয়েন্ট শনাক্ত করা এবং আঙুল গণনার মূল কাজ এখানে হয়।
গুগল মিডিয়াপাইপ (MediaPipe) লোকাল মডেল ব্যবহার করে।
"""

import os
import urllib.request
import mediapipe as mp
from mediapipe.tasks.python import vision

HAND_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

class HandTracker:
    def __init__(self, model_path=None):
        if model_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, "models", "hand_landmarker.task")

        # মডেল না থাকলে স্বয়ংক্রিয়ভাবে ডাউনলোড হবে
        if not os.path.exists(model_path):
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            print("[হ্যান্ড ট্র্যাকার] মডেল ডাউনলোড হচ্ছে...")
            urllib.request.urlretrieve(HAND_MODEL_URL, model_path)

        self.landmarker = vision.HandLandmarker.create_from_model_path(model_path)

    def process_frame(self, frame_rgb):
        """ফ্রেম প্রসেস করে ল্যান্ডমার্কের রেজাল্ট রিটার্ন করে"""
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        return self.landmarker.detect(mp_image)

    def extract_landmarks(self, results, frame_shape):
        """২১টি পয়েন্টের পিক্সেল কোঅর্ডিনেট (x, y) বের করে"""
        h, w, _ = frame_shape
        if not results or not results.hand_landmarks or len(results.hand_landmarks) == 0:
            return None, None

        hand_landmarks = results.hand_landmarks[0]
        handedness = "Right"
        if results.handedness and len(results.handedness) > 0 and len(results.handedness[0]) > 0:
            handedness = results.handedness[0][0].category_name

        lm_list = []
        for lm in hand_landmarks:
            cx = int(lm.x * w)
            cy = int(lm.y * h)
            lm_list.append((cx, cy))

        return lm_list, handedness

    def get_fingers_up(self, lm_list, handedness="Right"):
        """কোন কোন আঙুল খাড়া আছে তা নির্ণয় করে [বুড়ো, তর্জনী, মধ্যমা, অনামিকা, কনিষ্ঠা]"""
        if not lm_list or len(lm_list) < 21:
            return [False] * 5

        fingers = []
        # বুড়ো আঙুল
        if handedness == "Right":
            fingers.append(lm_list[4][0] < lm_list[3][0])
        else:
            fingers.append(lm_list[4][0] > lm_list[3][0])

        # বাকি ৪ আঙুল
        tip_ids = [8, 12, 16, 20]
        pip_ids = [6, 10, 14, 18]
        for tip, pip in zip(tip_ids, pip_ids):
            fingers.append(lm_list[tip][1] < lm_list[pip][1])

        return fingers
