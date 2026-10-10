"""
Air Canvas & Virtual Laser Engine for JARVIS-AETHER
Allows drawing glowing neon annotations directly in the air using finger gestures.
Includes Laser Pointer Mode with comet trails, multi-color palette, and instant eraser.
100% Free & Open-Source (OpenCV + NumPy).
"""

import numpy as np
import cv2
from config import CANVAS_COLORS

class AirCanvas:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height

        # Black canvas buffer for drawings
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)

        # Drawing attributes
        self.color_index = 0
        self.brush_thickness = 7
        self.eraser_thickness = 45

        # Previous point tracking for continuous smooth line drawing
        self.prev_pt = None

        # Laser pointer trail buffer
        self.laser_trail = []
        self.laser_trail_max_len = 12

    def get_current_color(self):
        """Returns active BGR color tuple and name"""
        color_data = CANVAS_COLORS[self.color_index]
        return color_data["bgr"], color_data["name"]

    def cycle_color(self):
        """Switches to the next color in the palette"""
        self.color_index = (self.color_index + 1) % len(CANVAS_COLORS)
        return self.get_current_color()

    def set_color_by_name(self, name):
        """Sets color by name string (e.g., 'RED', 'CYAN', 'GREEN')"""
        name_upper = name.upper()
        for idx, item in enumerate(CANVAS_COLORS):
            if item["name"] == name_upper:
                self.color_index = idx
                return True
        return False

    def draw_point(self, x, y):
        """Draws continuous line to current point from previous point"""
        current_color, _ = self.get_current_color()

        if self.prev_pt is None:
            self.prev_pt = (x, y)
            return

        # Draw anti-aliased thick glowing line on canvas
        cv2.line(self.canvas, self.prev_pt, (x, y), current_color, self.brush_thickness, cv2.LINE_AA)
        cv2.circle(self.canvas, (x, y), self.brush_thickness // 2, current_color, -1, cv2.LINE_AA)
        self.prev_pt = (x, y)

    def erase_at(self, x, y):
        """Erases drawings in proximity of (x, y)"""
        if self.prev_pt is None:
            self.prev_pt = (x, y)
        cv2.line(self.canvas, self.prev_pt, (x, y), (0, 0, 0), self.eraser_thickness, cv2.LINE_AA)
        cv2.circle(self.canvas, (x, y), self.eraser_thickness // 2, (0, 0, 0), -1)
        self.prev_pt = (x, y)

    def stop_drawing(self):
        """Breaks line continuity when finger is lifted or gesture stops"""
        self.prev_pt = None

    def clear(self):
        """Wipes entire drawing canvas"""
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.prev_pt = None
        self.laser_trail.clear()

    def update_laser_pointer(self, frame, x, y):
        """Renders glowing laser pointer dot with comet tail for presentations"""
        self.laser_trail.append((x, y))
        if len(self.laser_trail) > self.laser_trail_max_len:
            self.laser_trail.pop(0)

        # Draw fading comet trail
        trail_len = len(self.laser_trail)
        for i, pt in enumerate(self.laser_trail):
            alpha = (i + 1) / trail_len
            radius = int(3 + alpha * 5)
            color = (int(50 * alpha), int(50 * alpha), int(255 * alpha))
            cv2.circle(frame, pt, radius, color, -1, cv2.LINE_AA)

        # Glowing outer ring and core white point
        cv2.circle(frame, (x, y), 12, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.circle(frame, (x, y), 5, (255, 255, 255), -1, cv2.LINE_AA)

    def blend_onto_frame(self, frame):
        """
        Blends drawing canvas onto camera frame with vibrant neon transparency.
        Returns composite BGR image.
        """
        # Convert canvas to grayscale to create mask
        gray_canvas = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray_canvas, 10, 255, cv2.THRESH_BINARY)
        inv_mask = cv2.bitwise_not(mask)

        # Black-out area of drawings in original frame
        frame_bg = cv2.bitwise_and(frame, frame, mask=inv_mask)
        # Extract foreground drawings
        canvas_fg = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)

        # Add together
        combined = cv2.add(frame_bg, canvas_fg)
        return combined

    def render_palette_bar(self, frame):
        """Draws holographic color selector palette at the top of the screen"""
        bar_w = 60
        bar_h = 35
        start_x = self.width // 2 - (len(CANVAS_COLORS) * (bar_w + 10)) // 2

        for i, c in enumerate(CANVAS_COLORS):
            x1 = start_x + i * (bar_w + 10)
            y1 = 15
            x2 = x1 + bar_w
            y2 = y1 + bar_h

            is_selected = (i == self.color_index)
            # Draw color box
            cv2.rectangle(frame, (x1, y1), (x2, y2), c["bgr"], -1)

            # Border: highlighted if active
            border_color = (255, 255, 255) if is_selected else (50, 50, 50)
            border_thick = 3 if is_selected else 1
            cv2.rectangle(frame, (x1, y1), (x2, y2), border_color, border_thick)

            if is_selected:
                # Top pointer triangle
                cv2.circle(frame, (x1 + bar_w // 2, y2 + 8), 4, (255, 255, 255), -1)
