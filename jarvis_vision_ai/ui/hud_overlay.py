"""
Cyberpunk Sci-Fi HUD (Heads-Up Display) Overlay for JARVIS-AETHER
Renders Tony Stark / Iron Man laboratory aesthetic:
- Holographic corner brackets & targeting crosshairs
- Glowing hand skeleton & fingertip targeting reticles
- Face tracking cyber-box with status telemetry
- Dynamic real-time audio waveform visualizer
- Mode badge, FPS counter, and voice feed ticker
100% Free & Open-Source (OpenCV + NumPy).
"""

import math
import time
import numpy as np
import cv2
from config import (
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_PURPLE,
    COLOR_RED,
    COLOR_YELLOW,
    COLOR_WHITE,
    COLOR_DARK,
    SystemMode
)

class HudOverlay:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.anim_tick = 0

    def draw_corner_brackets(self, frame, x, y, w, h, color=COLOR_CYAN, line_len=20, thickness=2):
        """Draws sci-fi targeting corner brackets around any bounding box"""
        # Top-Left
        cv2.line(frame, (x, y), (x + line_len, y), color, thickness)
        cv2.line(frame, (x, y), (x, y + line_len), color, thickness)

        # Top-Right
        cv2.line(frame, (x + w, y), (x + w - line_len, y), color, thickness)
        cv2.line(frame, (x + w, y), (x + w, y + line_len), color, thickness)

        # Bottom-Left
        cv2.line(frame, (x, y + h), (x + line_len, y + h), color, thickness)
        cv2.line(frame, (x, y + h), (x, y + h - line_len), color, thickness)

        # Bottom-Right
        cv2.line(frame, (x + w, y + h), (x + w - line_len, y + h), color, thickness)
        cv2.line(frame, (x + w, y + h), (x + w, y + h - line_len), color, thickness)

    def draw_crosshair(self, frame, x, y, radius=16, color=COLOR_CYAN):
        """Draws glowing tactical crosshair around a point"""
        cv2.circle(frame, (x, y), radius, color, 1, cv2.LINE_AA)
        cv2.circle(frame, (x, y), 3, (255, 255, 255), -1, cv2.LINE_AA)
        # Crosshair lines
        gap = 5
        ext = 8
        cv2.line(frame, (x - radius - ext, y), (x - gap, y), color, 1)
        cv2.line(frame, (x + gap, y), (x + radius + ext, y), color, 1)
        cv2.line(frame, (x, y - radius - ext), (x, y - gap), color, 1)
        cv2.line(frame, (x, y + gap), (x, y + radius + ext), color, 1)

    def draw_cyber_hand(self, frame, lm_list, is_pinched=False):
        """Renders glowing cybernetic skeleton lines over detected hand"""
        if not lm_list or len(lm_list) < 21:
            return

        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),        # Index
            (5, 9), (9, 10), (10, 11), (11, 12),   # Middle
            (9, 13), (13, 14), (14, 15), (15, 16), # Ring
            (13, 17), (17, 18), (18, 19), (19, 20),# Pinky
            (0, 17)                                # Palm base
        ]

        # Draw glowing connection lines
        line_color = COLOR_PURPLE if is_pinched else COLOR_CYAN
        for p1, p2 in connections:
            cv2.line(frame, lm_list[p1], lm_list[p2], line_color, 2, cv2.LINE_AA)

        # Draw nodes on joints
        for i, pt in enumerate(lm_list):
            if i in [4, 8, 12, 16, 20]:
                # Fingertips have larger glowing dots
                cv2.circle(frame, pt, 5, COLOR_GREEN, -1, cv2.LINE_AA)
                cv2.circle(frame, pt, 8, line_color, 1, cv2.LINE_AA)
            else:
                cv2.circle(frame, pt, 3, (255, 255, 255), -1, cv2.LINE_AA)

        # Crosshair on index fingertip
        idx_pt = lm_list[8]
        self.draw_crosshair(frame, idx_pt[0], idx_pt[1], radius=14, color=COLOR_YELLOW if is_pinched else COLOR_CYAN)

    def draw_face_reticle(self, frame, face_telemetry):
        """Renders holographic target box around user's face"""
        face_box = face_telemetry.get("face_box")
        if face_box:
            fx, fy, fw, fh = face_box
            # Slightly expand box for sci-fi look
            pad = 12
            bx = max(0, fx - pad)
            by = max(0, fy - pad)
            bw = min(self.width - bx, fw + pad * 2)
            bh = min(self.height - by, fh + pad * 2)

            self.draw_corner_brackets(frame, bx, by, bw, bh, color=COLOR_CYAN, line_len=25, thickness=2)

            # Target telemetry label
            blink_str = " [BLINK]" if face_telemetry.get("is_blinking") else ""
            label = f"OPERATOR: LOCKED{blink_str}"
            cv2.putText(frame, label, (bx, by - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_CYAN, 1, cv2.LINE_AA)

    def draw_waveform(self, frame, audio_level, x=50, y=675, width=240, height=25):
        """Renders animated futuristic audio spectrum visualizer reacting to mic input"""
        self.anim_tick += 0.15
        num_bars = 24
        bar_w = int(width / num_bars) - 2

        # Frame border
        cv2.rectangle(frame, (x - 6, y - height - 4), (x + width + 6, y + 4), (40, 40, 40), 1)

        for i in range(num_bars):
            # Dynamic wave calculation
            freq = math.sin(self.anim_tick + i * 0.4) * 0.5 + 0.5
            bar_h = int((height * 0.15) + (height * 0.85 * audio_level * freq))
            bx = x + i * (bar_w + 2)
            by = y - bar_h

            color = COLOR_GREEN if audio_level > 0.4 else COLOR_CYAN
            cv2.rectangle(frame, (bx, by), (bx + bar_w, y), color, -1)

    def draw_volume_meter(self, frame, volume_pct, x=1220, y=200, w=22, h=250):
        """Renders vertical futuristic volume bar when volume mode is active"""
        # Outer frame
        cv2.rectangle(frame, (x, y), (x + w, y + h), (40, 40, 40), 2)
        cv2.rectangle(frame, (x - 2, y - 2), (x + w + 2, y + h + 2), COLOR_CYAN, 1)

        # Filled volume
        fill_h = int((volume_pct / 100.0) * h)
        fy = y + h - fill_h

        bar_color = COLOR_GREEN if volume_pct < 75 else COLOR_RED
        cv2.rectangle(frame, (x + 2, fy), (x + w - 2, y + h - 2), bar_color, -1)

        # Volume % text
        cv2.putText(frame, f"{volume_pct}%", (x - 12, y + h + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_WHITE, 1)
        cv2.putText(frame, "VOL", (x - 4, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_CYAN, 1)

    def render_hud_telemetry(self, frame, mode, fps, voice_engine, face_telemetry):
        """
        Renders the complete Cyberpunk Iron Man UI layout:
        - System status header
        - Active mode badge
        - Voice feed console
        - Screen framing grid
        """
        h, w, _ = frame.shape

        # 1. Screen Outer Tactical Border
        cv2.rectangle(frame, (10, 10), (w - 10, h - 10), (50, 40, 30), 1)
        self.draw_corner_brackets(frame, 15, 15, w - 30, h - 30, color=COLOR_CYAN, line_len=30, thickness=2)

        # 2. Header Status Banner (Top-Left)
        # Translucent background pill
        overlay = frame.copy()
        cv2.rectangle(overlay, (25, 20), (380, 85), COLOR_DARK, -1)
        cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

        cv2.rectangle(frame, (25, 20), (380, 85), COLOR_CYAN, 1)
        cv2.putText(frame, "AETHER // JARVIS AI SYSTEM", (38, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.58, COLOR_CYAN, 2, cv2.LINE_AA)
        cv2.putText(frame, f"FPS: {int(fps)} | STATUS: ARMED | FREE EDITION", (38, 62), cv2.FONT_HERSHEY_SIMPLEX, 0.40, COLOR_GREEN, 1, cv2.LINE_AA)
        cv2.putText(frame, face_telemetry.get("status_text", ""), (38, 77), cv2.FONT_HERSHEY_SIMPLEX, 0.35, COLOR_WHITE, 1, cv2.LINE_AA)

        # 3. Active Mode Badge (Top-Right)
        mode_colors = {
            SystemMode.MOUSE: COLOR_CYAN,
            SystemMode.CANVAS: COLOR_PURPLE,
            SystemMode.PRESENTATION: COLOR_GREEN,
            SystemMode.MEDIA: COLOR_YELLOW,
            SystemMode.HUD_ONLY: COLOR_WHITE
        }
        badge_color = mode_colors.get(mode, COLOR_CYAN)

        mode_overlay = frame.copy()
        cv2.rectangle(mode_overlay, (w - 360, 20), (w - 25, 85), COLOR_DARK, -1)
        cv2.addWeighted(mode_overlay, 0.75, frame, 0.25, 0, frame)

        cv2.rectangle(frame, (w - 360, 20), (w - 25, 85), badge_color, 2)
        cv2.putText(frame, "ACTIVE PROTOCOL:", (w - 345, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.42, COLOR_WHITE, 1, cv2.LINE_AA)
        cv2.putText(frame, f">> {mode} <<", (w - 345, 68), cv2.FONT_HERSHEY_SIMPLEX, 0.62, badge_color, 2, cv2.LINE_AA)

        # 4. Voice Feed Console (Bottom-Left)
        v_overlay = frame.copy()
        cv2.rectangle(v_overlay, (25, h - 90), (450, h - 20), COLOR_DARK, -1)
        cv2.addWeighted(v_overlay, 0.75, frame, 0.25, 0, frame)

        cv2.rectangle(frame, (25, h - 90), (450, h - 20), (60, 60, 60), 1)
        lang_name = voice_engine.get_current_language()["name"]
        cv2.putText(frame, f"VOICE RECOGNIZER [LANG: {lang_name}]:", (36, h - 72), cv2.FONT_HERSHEY_SIMPLEX, 0.40, COLOR_CYAN, 1)

        speech_text = voice_engine.last_recognized_text
        cv2.putText(frame, speech_text[:40], (36, h - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.50, COLOR_WHITE, 1)

        # Render real-time audio waveform next to voice console
        self.draw_waveform(frame, voice_engine.audio_level, x=470, y=h - 35, width=180, height=28)

        # 5. Controls Cheat-Hint (Bottom-Right)
        hint_text = "M: Mode | C: Color | E: Clear | L: Lang | Esc: Exit"
        cv2.putText(frame, hint_text, (w - 390, h - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (180, 180, 180), 1)
