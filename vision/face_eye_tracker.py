"""
=============================================================================
ভিশন মডিউল: ফেস ও আই ট্র্যাকার (FACE & EYE TRACKER)
=============================================================================
ইউজার সামনে আসলে স্বয়ংক্রিয় সম্ভাষণ জানানো এবং চোখের পলক গণনা করা।
"""

import os
import time
import math
import urllib.request
import mediapipe as mp
from mediapipe.tasks.python import vision

FACE_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"

class FaceEyeTracker:
    def __init__(self, model_path=None):
        if model_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, "models", "face_landmarker.task")

        if not os.path.exists(model_path):
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            print("[ফেস ট্র্যাকার] মডেল ডাউনলোড হচ্ছে...")
            urllib.request.urlretrieve(FACE_MODEL_URL, model_path)

        self.landmarker = vision.FaceLandmarker.create_from_model_path(model_path)

        # স্ট্যাটাস ভেরিয়েবল
        self.user_present = False
        self.last_seen_time = time.time()
        self.presence_just_detected = False

        # চোখের পলক
        self.blink_counter = 0
        self.total_blinks = 0
        self.last_blink_time = 0
        self.blink_cooldown = 0.25

        self.LEFT_EYE_PTS = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE_PTS = [362, 385, 387, 263, 373, 380]

    def _calc_ear(self, landmarks, eye_pts, w, h):
        """চোখের পলকের অনুপাত (EAR) নির্ণয়"""
        p = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye_pts]
        v1 = math.hypot(p[1][0] - p[5][0], p[1][1] - p[5][1])
        v2 = math.hypot(p[2][0] - p[4][0], p[2][1] - p[4][1])
        h_dist = math.hypot(p[0][0] - p[3][0], p[0][1] - p[3][1])
        if h_dist == 0:
            return 0.3
        return (v1 + v2) / (2.0 * h_dist)

    def process_frame(self, frame_rgb, frame_shape):
        """ফ্রেম প্রসেস করে ফেস ও আই টেলিমেট্রি প্রদান করে"""
        h, w, _ = frame_shape
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        results = self.landmarker.detect(mp_image)

        face_box = None
        is_blinking = False
        current_time = time.time()

        if results and results.face_landmarks and len(results.face_landmarks) > 0:
            landmarks = results.face_landmarks[0]
            xs = [int(lm.x * w) for lm in landmarks]
            ys = [int(lm.y * h) for lm in landmarks]
            min_x, max_x = max(0, min(xs)), min(w, max(xs))
            min_y, max_y = max(0, min(ys)), min(h, max(ys))
            face_box = (min_x, min_y, max_x - min_x, max_y - min_y)

            if not self.user_present:
                self.user_present = True
                self.presence_just_detected = True
            else:
                self.presence_just_detected = False

            self.last_seen_time = current_time

            left_ear = self._calc_ear(landmarks, self.LEFT_EYE_PTS, w, h)
            right_ear = self._calc_ear(landmarks, self.RIGHT_EYE_PTS, w, h)
            avg_ear = (left_ear + right_ear) / 2.0

            if avg_ear < 0.20:
                self.blink_counter += 1
            else:
                if self.blink_counter >= 1 and (current_time - self.last_blink_time > self.blink_cooldown):
                    self.total_blinks += 1
                    self.last_blink_time = current_time
                    is_blinking = True
                self.blink_counter = 0

            status_text = f"ইউজার উপস্থিত | পলক: {self.total_blinks}"
        else:
            if self.user_present and (current_time - self.last_seen_time > 3.0):
                self.user_present = False
                status_text = "ইউজার অনুপস্থিত (STANDBY)"
            else:
                status_text = "ইউজার খোঁজা হচ্ছে..."
            self.presence_just_detected = False

        return {
            "face_box": face_box,
            "is_blinking": is_blinking,
            "user_present": self.user_present,
            "just_arrived": self.presence_just_detected,
            "status_text": status_text
        }
