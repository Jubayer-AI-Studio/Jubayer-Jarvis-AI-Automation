"""
Gesture Engine for JARVIS-AETHER
Uses official Google MediaPipe HandLandmarker Tasks API (Python 3.14 Compatible).
Provides real-time hand landmark tracking, jitter-free cursor smoothing,
finger counting, pinch measurement, swipe detection, and gesture classification.
100% Free & Open-Source.
"""

import os
import math
import time
import urllib.request
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision
from config import (
    MOUSE_SMOOTHING,
    CLICK_PINCH_DISTANCE,
    RIGHT_CLICK_DISTANCE,
    SWIPE_DISTANCE_THRESHOLD,
    VOLUME_MIN_DIST,
    VOLUME_MAX_DIST,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

HAND_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

class GestureEngine:
    def __init__(self, model_path=None):
        if model_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, "models", "hand_landmarker.task")

        # Auto-download model if missing
        if not os.path.exists(model_path):
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            print("[GestureEngine] Downloading official hand_landmarker model...")
            urllib.request.urlretrieve(HAND_MODEL_URL, model_path)

        self.landmarker = vision.HandLandmarker.create_from_model_path(model_path)

        # Smoothing states
        self.prev_screen_x = SCREEN_WIDTH // 2
        self.prev_screen_y = SCREEN_HEIGHT // 2

        # Swipe tracking states
        self.prev_wrist_x = None
        self.last_swipe_time = 0
        self.swipe_cooldown = 0.6

        # Active margins for mapping camera to screen
        self.frame_margin_x = 110
        self.frame_margin_y = 80

    def process_frame(self, frame_rgb):
        """Processes RGB numpy frame and returns task result"""
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        return self.landmarker.detect(mp_image)

    def extract_landmarks(self, results, frame_shape):
        """
        Extracts pixel coordinates of hand landmarks.
        Returns list of (x, y) tuples for 21 landmarks if hand detected, else None.
        """
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
        """
        Returns list of 5 booleans [thumb, index, middle, ring, pinky]
        True if finger is extended, False otherwise.
        """
        if not lm_list or len(lm_list) < 21:
            return [False] * 5

        fingers = []

        # Thumb: compare tip (4) with IP joint (3)
        if handedness == "Right":
            fingers.append(lm_list[4][0] < lm_list[3][0])
        else:
            fingers.append(lm_list[4][0] > lm_list[3][0])

        # 4 Fingers: Tip.y < PIP.y
        tip_ids = [8, 12, 16, 20]
        pip_ids = [6, 10, 14, 18]

        for tip, pip in zip(tip_ids, pip_ids):
            fingers.append(lm_list[tip][1] < lm_list[pip][1])

        return fingers

    def get_smoothed_cursor(self, index_x, index_y, frame_w, frame_h):
        """
        Maps camera coordinates to screen coordinates with exponential smoothing.
        Returns (screen_x, screen_y)
        """
        x = np.interp(index_x, [self.frame_margin_x, frame_w - self.frame_margin_x], [0, SCREEN_WIDTH])
        y = np.interp(index_y, [self.frame_margin_y, frame_h - self.frame_margin_y], [0, SCREEN_HEIGHT])

        x = max(0, min(SCREEN_WIDTH - 1, x))
        y = max(0, min(SCREEN_HEIGHT - 1, y))

        smooth_x = int(self.prev_screen_x * MOUSE_SMOOTHING + x * (1 - MOUSE_SMOOTHING))
        smooth_y = int(self.prev_screen_y * MOUSE_SMOOTHING + y * (1 - MOUSE_SMOOTHING))

        self.prev_screen_x = smooth_x
        self.prev_screen_y = smooth_y

        return smooth_x, smooth_y

    def calculate_distance(self, p1, p2):
        """Euclidean distance between two pixel coordinates"""
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def detect_pinch(self, lm_list):
        """Detects pinch between thumb tip (4) and index tip (8)"""
        if not lm_list or len(lm_list) < 21:
            return False, 999
        dist = self.calculate_distance(lm_list[4], lm_list[8])
        return (dist < CLICK_PINCH_DISTANCE), dist

    def detect_right_pinch(self, lm_list):
        """Detects pinch between thumb tip (4) and middle finger tip (12)"""
        if not lm_list or len(lm_list) < 21:
            return False, 999
        dist = self.calculate_distance(lm_list[4], lm_list[12])
        return (dist < RIGHT_CLICK_DISTANCE), dist

    def detect_swipe(self, lm_list):
        """Detects fast horizontal hand swipe across frames"""
        if not lm_list or len(lm_list) < 21:
            self.prev_wrist_x = None
            return None

        current_time = time.time()
        wrist_x = lm_list[0][0]

        if self.prev_wrist_x is None:
            self.prev_wrist_x = wrist_x
            return None

        dx = wrist_x - self.prev_wrist_x
        self.prev_wrist_x = wrist_x

        if current_time - self.last_swipe_time > self.swipe_cooldown:
            if dx > SWIPE_DISTANCE_THRESHOLD:
                self.last_swipe_time = current_time
                return "PREV"
            elif dx < -SWIPE_DISTANCE_THRESHOLD:
                self.last_swipe_time = current_time
                return "NEXT"

        return None

    def get_volume_percentage(self, lm_list):
        """Calculates volume % (0 to 100) based on thumb and index distance"""
        if not lm_list or len(lm_list) < 21:
            return None
        dist = self.calculate_distance(lm_list[4], lm_list[8])
        vol_pct = np.interp(dist, [VOLUME_MIN_DIST, VOLUME_MAX_DIST], [0, 100])
        return int(np.clip(vol_pct, 0, 100))
