"""
=============================================================================
জেসচার মডিউল: প্রেজেন্টেশন সোয়াইপ (PRESENTATION SWIPE)
=============================================================================
হাতের দ্রুত ডানে-বামে সোয়াইপ শনাক্ত করে প্রেজেন্টেশন স্লাইড পরিবর্তন।
"""

import time
from config import SWIPE_DISTANCE_THRESHOLD

class PresentationSwipe:
    def __init__(self):
        self.prev_wrist_x = None
        self.last_swipe_time = 0
        self.swipe_cooldown = 0.65

    def detect_swipe(self, lm_list):
        """
        সোয়াইপের দিক নির্ণয় করে:
        - 'NEXT': হাত বামে সোয়াইপ করলে (মিরর ভিউতে পরের স্লাইড)
        - 'PREV': হাত ডানে সোয়াইপ করলে (আগের স্লাইড)
        """
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
