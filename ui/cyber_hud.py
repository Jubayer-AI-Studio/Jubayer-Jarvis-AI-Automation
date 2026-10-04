"""
=============================================================================
ইউআই মডিউল: সাইবারপাঙ্ক HUD (JUBAYER CYBER HUD)
=============================================================================
টনি স্টার্কের ল্যাবের মতো সাই-ফাই গ্রাফিক্স, নিয়ন স্কেলিটন, ওয়েভফর্ম,
'জুবায়েদ' ওয়েক-ওয়ার্ড স্ট্যাটাস এবং মোবাইল রিমোট কানেকশন ইনফো।
"""

import math
import os
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

class CyberHud:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.anim_tick = 0
        self.show_mobile_qr = True
        self.qr_img = None

        # কিউআর কোড থাম্বনেইল লোড করা
        qr_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mobile", "qr_code.png")
        if os.path.exists(qr_path):
            try:
                img = cv2.imread(qr_path)
                if img is not None:
                    self.qr_img = cv2.resize(img, (95, 95))
            except Exception:
                self.qr_img = None

    def draw_corner_brackets(self, frame, x, y, w, h, color=COLOR_CYAN, line_len=20, thickness=2):
        cv2.line(frame, (x, y), (x + line_len, y), color, thickness)
        cv2.line(frame, (x, y), (x, y + line_len), color, thickness)
        cv2.line(frame, (x + w, y), (x + w - line_len, y), color, thickness)
        cv2.line(frame, (x + w, y), (x + w, y + line_len), color, thickness)
        cv2.line(frame, (x, y + h), (x + line_len, y + h), color, thickness)
        cv2.line(frame, (x, y + h), (x, y + h - line_len), color, thickness)
        cv2.line(frame, (x + w, y + h), (x + w - line_len, y + h), color, thickness)
        cv2.line(frame, (x + w, y + h), (x + w, y + line_len), color, thickness)

    def draw_crosshair(self, frame, x, y, radius=15, color=COLOR_CYAN):
        cv2.circle(frame, (x, y), radius, color, 1, cv2.LINE_AA)
        cv2.circle(frame, (x, y), 3, (255, 255, 255), -1, cv2.LINE_AA)
        gap, ext = 4, 8
        cv2.line(frame, (x - radius - ext, y), (x - gap, y), color, 1)
        cv2.line(frame, (x + gap, y), (x + radius + ext, y), color, 1)
        cv2.line(frame, (x, y - radius - ext), (x, y - gap), color, 1)
        cv2.line(frame, (x, y + gap), (x, y + radius + ext), color, 1)

    def draw_cyber_hand(self, frame, lm_list, is_pinched=False):
        if not lm_list or len(lm_list) < 21:
            return

        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (5, 6), (6, 7), (7, 8),
            (5, 9), (9, 10), (10, 11), (11, 12),
            (9, 13), (13, 14), (14, 15), (15, 16),
            (13, 17), (17, 18), (18, 19), (19, 20),
            (0, 17)
        ]

        line_color = COLOR_PURPLE if is_pinched else COLOR_CYAN
        for p1, p2 in connections:
            cv2.line(frame, lm_list[p1], lm_list[p2], line_color, 2, cv2.LINE_AA)

        for i, pt in enumerate(lm_list):
            if i in [4, 8, 12, 16, 20]:
                cv2.circle(frame, pt, 5, COLOR_GREEN, -1, cv2.LINE_AA)
                cv2.circle(frame, pt, 8, line_color, 1, cv2.LINE_AA)
            else:
                cv2.circle(frame, pt, 3, (255, 255, 255), -1, cv2.LINE_AA)

        idx_pt = lm_list[8]
        self.draw_crosshair(frame, idx_pt[0], idx_pt[1], radius=14, color=COLOR_YELLOW if is_pinched else COLOR_CYAN)

    def draw_face_reticle(self, frame, face_telemetry):
        face_box = face_telemetry.get("face_box")
        if face_box:
            fx, fy, fw, fh = face_box
            pad = 12
            bx = max(0, fx - pad)
            by = max(0, fy - pad)
            bw = min(self.width - bx, fw + pad * 2)
            bh = min(self.height - by, fh + pad * 2)

            self.draw_corner_brackets(frame, bx, by, bw, bh, color=COLOR_CYAN, line_len=25, thickness=2)
            blink_str = " [চোখের পলক]" if face_telemetry.get("is_blinking") else ""
            label = f"OPERATOR: LOCKED{blink_str}"
            cv2.putText(frame, label, (bx, by - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_CYAN, 1, cv2.LINE_AA)

    def draw_waveform(self, frame, audio_level, x=50, y=675, width=240, height=25):
        self.anim_tick += 0.15
        num_bars = 24
        bar_w = int(width / num_bars) - 2

        cv2.rectangle(frame, (x - 6, y - height - 4), (x + width + 6, y + 4), (40, 40, 40), 1)
        for i in range(num_bars):
            freq = math.sin(self.anim_tick + i * 0.4) * 0.5 + 0.5
            bar_h = int((height * 0.15) + (height * 0.85 * audio_level * freq))
            bx = x + i * (bar_w + 2)
            by = y - bar_h
            color = COLOR_GREEN if audio_level > 0.4 else COLOR_CYAN
            cv2.rectangle(frame, (bx, by), (bx + bar_w, y), color, -1)

    def draw_volume_meter(self, frame, volume_pct, x=1220, y=200, w=22, h=250):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (40, 40, 40), 2)
        cv2.rectangle(frame, (x - 2, y - 2), (x + w + 2, y + h + 2), COLOR_CYAN, 1)

        fill_h = int((volume_pct / 100.0) * h)
        fy = y + h - fill_h
        bar_color = COLOR_GREEN if volume_pct < 75 else COLOR_RED
        cv2.rectangle(frame, (x + 2, fy), (x + w - 2, y + h - 2), bar_color, -1)
        cv2.putText(frame, f"{volume_pct}%", (x - 12, y + h + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_WHITE, 1)
        cv2.putText(frame, "VOL", (x - 4, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLOR_CYAN, 1)

    def render_hud(self, frame, mode, fps, wake_engine, voice_listener, face_telemetry, mobile_url=""):
        h, w, _ = frame.shape

        # ১. আউটার সাই-ফাই বর্ডার
        cv2.rectangle(frame, (10, 10), (w - 10, h - 10), (50, 40, 30), 1)
        self.draw_corner_brackets(frame, 15, 15, w - 30, h - 30, color=COLOR_CYAN, line_len=30, thickness=2)

        # ২. টপ-লেফট স্ট্যাটাস ব্যানার (জুবায়েদ এআই ব্র্যান্ডিং)
        overlay = frame.copy()
        cv2.rectangle(overlay, (25, 20), (420, 90), COLOR_DARK, -1)
        cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

        is_awake = wake_engine.is_awake
        status_box_color = COLOR_GREEN if is_awake else COLOR_CYAN
        cv2.rectangle(frame, (25, 20), (420, 90), status_box_color, 2 if is_awake else 1)
        
        cv2.putText(frame, "JUBAYER AI // AUTONOMOUS OPERATOR", (38, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.54, COLOR_CYAN, 2, cv2.LINE_AA)
        
        wake_label = ">> জুবায়েদ সজাগ: আপনার কথা শুনছি... <<" if is_awake else "ডাকুন: 'জুবায়েদ' বা 'Hey Jubayer'"
        wake_color = COLOR_GREEN if is_awake else COLOR_YELLOW
        cv2.putText(frame, wake_label, (38, 64), cv2.FONT_HERSHEY_SIMPLEX, 0.45, wake_color, 1, cv2.LINE_AA)
        cv2.putText(frame, f"FPS: {int(fps)} | {face_telemetry.get('status_text', '')}", (38, 82), cv2.FONT_HERSHEY_SIMPLEX, 0.35, COLOR_WHITE, 1, cv2.LINE_AA)

        # ৩. মোড ব্যাজ (টপ-রাইট)
        mode_colors = {
            SystemMode.MOUSE: COLOR_CYAN,
            SystemMode.CANVAS: COLOR_PURPLE,
            SystemMode.PRESENTATION: COLOR_GREEN,
            SystemMode.MEDIA: COLOR_YELLOW
        }
        badge_color = mode_colors.get(mode, COLOR_CYAN)

        mode_overlay = frame.copy()
        cv2.rectangle(mode_overlay, (w - 360, 20), (w - 25, 85), COLOR_DARK, -1)
        cv2.addWeighted(mode_overlay, 0.75, frame, 0.25, 0, frame)

        cv2.rectangle(frame, (w - 360, 20), (w - 25, 85), badge_color, 2)
        cv2.putText(frame, "ACTIVE PROTOCOL:", (w - 345, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.42, COLOR_WHITE, 1, cv2.LINE_AA)
        cv2.putText(frame, f">> {mode} <<", (w - 345, 68), cv2.FONT_HERSHEY_SIMPLEX, 0.62, badge_color, 2, cv2.LINE_AA)

        # ৪. বটম-লেফট ভয়েস ও জুবায়েদ লাইভ অ্যাকশন কনসোল
        v_overlay = frame.copy()
        cv2.rectangle(v_overlay, (25, h - 90), (480, h - 20), COLOR_DARK, -1)
        cv2.addWeighted(v_overlay, 0.75, frame, 0.25, 0, frame)

        cv2.rectangle(frame, (25, h - 90), (480, h - 20), (60, 60, 60), 1)
        cv2.putText(frame, "JUBAYER LIVE INTENT MONITOR:", (36, h - 72), cv2.FONT_HERSHEY_SIMPLEX, 0.40, COLOR_CYAN, 1)
        cv2.putText(frame, wake_engine.status_message[:42], (36, h - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.48, COLOR_WHITE, 1)

        # অডিও ওয়েভফর্ম
        self.draw_waveform(frame, voice_listener.audio_level, x=500, y=h - 35, width=170, height=28)

        # ৫. মোবাইল রিমোট কিউআর কোড উইজেট (বটম-রাইট)
        if self.qr_img is not None and self.show_mobile_qr:
            qr_x = w - 120
            qr_y = h - 130
            # কিউআর ব্যাকগ্রাউন্ড
            cv2.rectangle(frame, (qr_x - 5, qr_y - 22), (qr_x + 100, qr_y + 100), COLOR_DARK, -1)
            cv2.rectangle(frame, (qr_x - 5, qr_y - 22), (qr_x + 100, qr_y + 100), COLOR_CYAN, 1)
            cv2.putText(frame, "MOBILE REMOTE", (qr_x - 2, qr_y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.35, COLOR_CYAN, 1)
            # ওভারলে কিউআর থাম্বনেইল
            frame[qr_y:qr_y+95, qr_x:qr_x+95] = self.qr_img
            cv2.putText(frame, mobile_url[-14:], (qr_x - 4, qr_y + 112), cv2.FONT_HERSHEY_SIMPLEX, 0.35, COLOR_GREEN, 1)
