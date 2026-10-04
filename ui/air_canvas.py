"""
=============================================================================
ইউআই মডিউল: এয়ার ক্যানভাস (AIR CANVAS & LASER POINTER)
=============================================================================
বাতাসে আঙুল দিয়ে নিয়ন রঙে আঁকাআঁকি এবং স্লাইড দেখানোর জন্য লেজার পয়েন্টার।
"""

import numpy as np
import cv2
from config import CANVAS_COLORS

class AirCanvas:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)

        self.color_index = 0
        self.brush_thickness = 7
        self.eraser_thickness = 45
        self.prev_pt = None

        # লেজার পয়েন্টার ট্রেইল
        self.laser_trail = []
        self.laser_trail_max_len = 12

    def get_current_color(self):
        color_data = CANVAS_COLORS[self.color_index]
        return color_data["bgr"], color_data["name"]

    def cycle_color(self):
        self.color_index = (self.color_index + 1) % len(CANVAS_COLORS)
        return self.get_current_color()

    def draw_point(self, x, y):
        current_color, _ = self.get_current_color()
        if self.prev_pt is None:
            self.prev_pt = (x, y)
            return

        cv2.line(self.canvas, self.prev_pt, (x, y), current_color, self.brush_thickness, cv2.LINE_AA)
        cv2.circle(self.canvas, (x, y), self.brush_thickness // 2, current_color, -1, cv2.LINE_AA)
        self.prev_pt = (x, y)

    def stop_drawing(self):
        self.prev_pt = None

    def clear(self):
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.prev_pt = None
        self.laser_trail.clear()

    def update_laser_pointer(self, frame, x, y):
        self.laser_trail.append((x, y))
        if len(self.laser_trail) > self.laser_trail_max_len:
            self.laser_trail.pop(0)

        trail_len = len(self.laser_trail)
        for i, pt in enumerate(self.laser_trail):
            alpha = (i + 1) / trail_len
            radius = int(3 + alpha * 5)
            color = (int(50 * alpha), int(50 * alpha), int(255 * alpha))
            cv2.circle(frame, pt, radius, color, -1, cv2.LINE_AA)

        cv2.circle(frame, (x, y), 12, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.circle(frame, (x, y), 5, (255, 255, 255), -1, cv2.LINE_AA)

    def blend_onto_frame(self, frame):
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        inv_mask = cv2.bitwise_not(mask)

        bg = cv2.bitwise_and(frame, frame, mask=inv_mask)
        fg = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)
        return cv2.add(bg, fg)

    def render_palette_bar(self, frame):
        bar_w = 60
        bar_h = 35
        start_x = self.width // 2 - (len(CANVAS_COLORS) * (bar_w + 10)) // 2

        for i, c in enumerate(CANVAS_COLORS):
            x1 = start_x + i * (bar_w + 10)
            y1 = 15
            x2 = x1 + bar_w
            y2 = y1 + bar_h
            is_selected = (i == self.color_index)

            cv2.rectangle(frame, (x1, y1), (x2, y2), c["bgr"], -1)
            border_color = (255, 255, 255) if is_selected else (50, 50, 50)
            cv2.rectangle(frame, (x1, y1), (x2, y2), border_color, 3 if is_selected else 1)
            if is_selected:
                cv2.circle(frame, (x1 + bar_w // 2, y2 + 8), 4, (255, 255, 255), -1)
