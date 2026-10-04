"""
=============================================================================
জেসচার মডিউল: এয়ার মাউস (AIR MOUSE)
=============================================================================
আঙুলের নড়াচড়া দিয়ে মাউস কার্সর পরিচালনা, চিমটি দিয়ে ক্লিক এবং পেজ স্ক্রল।
"""

import math
import numpy as np
import pyautogui
from config import (
    MOUSE_SMOOTHING,
    CLICK_PINCH_DISTANCE,
    RIGHT_CLICK_DISTANCE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

class AirMouse:
    def __init__(self):
        self.prev_x = SCREEN_WIDTH // 2
        self.prev_y = SCREEN_HEIGHT // 2
        self.margin_x = 110
        self.margin_y = 80

    def calculate_distance(self, p1, p2):
        """দুই পয়েন্টের মধ্যে ইউক্লিডিয়ান দূরত্ব"""
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def get_smooth_cursor(self, index_x, index_y, cam_w, cam_h):
        """ক্যামেরার কোঅর্ডিনেটকে স্ক্রিনের কোঅর্ডিনেটে স্মুথভাবে কনভার্ট করে"""
        x = np.interp(index_x, [self.margin_x, cam_w - self.margin_x], [0, SCREEN_WIDTH])
        y = np.interp(index_y, [self.margin_y, cam_h - self.margin_y], [0, SCREEN_HEIGHT])

        x = max(0, min(SCREEN_WIDTH - 1, x))
        y = max(0, min(SCREEN_HEIGHT - 1, y))

        smooth_x = int(self.prev_x * MOUSE_SMOOTHING + x * (1 - MOUSE_SMOOTHING))
        smooth_y = int(self.prev_y * MOUSE_SMOOTHING + y * (1 - MOUSE_SMOOTHING))

        self.prev_x = smooth_x
        self.prev_y = smooth_y
        return smooth_x, smooth_y

    def is_left_click(self, lm_list):
        """বুড়ো আঙুল ও তর্জনীর চিমটি দিয়ে লেফট ক্লিক ডিটেকশন"""
        if not lm_list or len(lm_list) < 21:
            return False, 999
        dist = self.calculate_distance(lm_list[4], lm_list[8])
        return (dist < CLICK_PINCH_DISTANCE), dist

    def is_right_click(self, lm_list):
        """বুড়ো আঙুল ও মধ্যমার চিমটি দিয়ে রাইট ক্লিক ডিটেকশন"""
        if not lm_list or len(lm_list) < 21:
            return False, 999
        dist = self.calculate_distance(lm_list[4], lm_list[12])
        return (dist < RIGHT_CLICK_DISTANCE), dist
