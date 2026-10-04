"""
=============================================================================
JUBAYER AI: CINEMATIC JARVIS ARC REACTOR & EMOTION CORE (v4.0)
=============================================================================
টনি স্টার্কের আয়রন ম্যান জার্ভিস ফিল:
- বড়, প্রফেশনাল, স্বচ্ছ সাই-ফাই হলোফ্রেম
- ব্যবহারকারীর কণ্ঠ শুনলেই রিয়েল-টাইমে রঙ ও ইমোশনাল এক্সপ্রেশন পরিবর্তন:
    * IDLE (শান্ত/অনলাইন): ইলেকট্রিক সায়ান ও সাইবার ব্লু (#00f0ff, #0088ff)
    * LISTENING (মনোযোগ দিয়ে শুনছে): ভাইব্রেন্ট গোল্ডেন সান ও অ্যাম্বার (#ffaa00, #ff6600)
    * THINKING (চিন্তা করছে): সাইবার পার্পল ও ম্যাগনেটা (#c026d3, #8b5cf6)
    * PERMISSION (অনুমতি চাইছে): ইলেকট্রিক এমারেল্ড গ্রিন ও নিয়ন লাইম (#10b981, #22c55e)
    * ALERT / DENIED (বাতিল বা অ্যালার্ট): নিওন ক্রিমসন রুবি (#f43f5e, #ef4444)
- ডুয়েল কাউন্টার-রোটেটিং টেক রিংস ও অডিও সাউন্ড ওয়েভ ভিজ্যুয়ালাইজার
- ড্র্যাগ-অ্যান্ড-ড্রপ সুবিধা: স্ক্রিনের যেকোনো জায়গায় মাউস দিয়ে সরানো যাবে।
=============================================================================
"""

import math
import time
import os
import ctypes
import tkinter as tk

class CinematicJarvisReactor:
    def __init__(self, title="JUBAYER_JARVIS_CORE"):
        self.root = tk.Tk()
        self.root.title(title)

        # উইন্ডো বর্ডার রিমুভ ও অলওয়েজ অন টপ
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        # ট্রান্সপারেন্ট ব্যাকগ্রাউন্ড (#000001 রঙটি সম্পূর্ণ গায়েব হয়ে যাবে)
        self.trans_color = "#000001"
        self.root.attributes("-transparentcolor", self.trans_color)
        self.root.config(bg=self.trans_color)

        # বড় এবং গর্জিয়াস সাইজ (৩০০ x ৩৬০ পিক্সেল)
        self.size = 280
        self.width = self.size
        self.height = self.size + 70

        # স্ক্রিনের নিচের ডান পাশে সুন্দরভাবে স্থাপন
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.pos_x = screen_w - self.width - 50
        self.pos_y = screen_h - self.height - 70
        self.root.geometry(f"{self.width}x{self.height}+{self.pos_x}+{self.pos_y}")

        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg=self.trans_color,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # অ্যানিমেশন ও স্ট্যাটাস স্টেট
        self.tick = 0.0
        self.audio_level = 0.05
        self.emotion_state = "IDLE"  # IDLE, LISTENING, THINKING, PERMISSION, SUCCESS, ALERT
        self.status_title = "JARVIS // JUBAYER AI"
        self.status_subtitle = "SYSTEM ONLINE // STANDBY"

        # মাউস দিয়ে টেনে সরানোর সুবিধা (Drag & Drop)
        self._drag_x = 0
        self._drag_y = 0
        self.canvas.bind("<ButtonPress-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._on_drag)

        # প্যালেট কনফিগারেশন (ইমোশন অনুযায়ী রঙ পরিবর্তন)
        self.palettes = {
            "IDLE": {
                "core": "#00f0ff",
                "ring1": "#0284c7",
                "ring2": "#38bdf8",
                "glow": "#0369a1",
                "accent": "#e0f2fe",
                "subtitle": "SYSTEM ONLINE // STANDBY"
            },
            "LISTENING": {
                "core": "#fbbf24",
                "ring1": "#d97706",
                "ring2": "#f59e0b",
                "glow": "#b45309",
                "accent": "#fef3c7",
                "subtitle": "VOICE DETECTED // LISTENING..."
            },
            "THINKING": {
                "core": "#d946ef",
                "ring1": "#9333ea",
                "ring2": "#c084fc",
                "glow": "#7e22ce",
                "accent": "#fae8ff",
                "subtitle": "PROCESSING INTENT // ANALYZING"
            },
            "PERMISSION": {
                "core": "#10b981",
                "ring1": "#059669",
                "ring2": "#34d399",
                "glow": "#047857",
                "accent": "#d1fae5",
                "subtitle": "AWAITING USER AUTHORIZATION"
            },
            "ALERT": {
                "core": "#f43f5e",
                "ring1": "#be123c",
                "ring2": "#fb7185",
                "glow": "#9f1239",
                "accent": "#ffe4e6",
                "subtitle": "COMMAND CANCELLED // SECURE"
            }
        }

        # অ্যানিমেশন শুরু
        self.animate()

    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _on_drag(self, event):
        dx = event.x - self._drag_x
        dy = event.y - self._drag_y
        self.pos_x += dx
        self.pos_y += dy
        self.root.geometry(f"+{self.pos_x}+{self.pos_y}")

    def set_emotion(self, state, custom_subtitle=None):
        """ইমোশন ও রঙ পরিবর্তন: IDLE, LISTENING, THINKING, PERMISSION, ALERT"""
        if state in self.palettes:
            self.emotion_state = state
            if custom_subtitle:
                self.status_subtitle = custom_subtitle
            else:
                self.status_subtitle = self.palettes[state]["subtitle"]

    def set_audio_level(self, level):
        """ভয়েসের শব্দের তীব্রতা অনুযায়ী পালস ঘটানো"""
        self.audio_level = max(0.05, min(1.0, level))

    def animate(self):
        """প্রতি ফ্রেমে সিনেমাটিক সাই-ফাই আর্করিয়্যাক্টর রেন্ডার করা"""
        self.canvas.delete("all")
        cx = self.size // 2
        cy = self.size // 2
        self.tick += 0.05

        palette = self.palettes.get(self.emotion_state, self.palettes["IDLE"])

        # ১. ব্যাকগ্রাউন্ড সফট গ্লো পালস
        pulse = math.sin(self.tick * 2.5) * 6
        glow_r = int(90 + pulse + (self.audio_level * 25))
        self.canvas.create_oval(
            cx - glow_r, cy - glow_r, cx + glow_r, cy + glow_r,
            fill=palette["glow"], outline="", stipple="gray50"
        )

        # ২. বাইরের রোটেটিং সাইবার আর্মার রিংস (বাইরের রিং ক্লকওয়াইজ)
        num_outer_spokes = 12
        outer_r = 105
        for i in range(num_outer_spokes):
            angle = self.tick + (i * (2 * math.pi / num_outer_spokes))
            x1 = cx + int(math.cos(angle) * (outer_r - 10))
            y1 = cy + int(math.sin(angle) * (outer_r - 10))
            x2 = cx + int(math.cos(angle) * outer_r)
            y2 = cy + int(math.sin(angle) * outer_r)
            self.canvas.create_line(x1, y1, x2, y2, fill=palette["ring1"], width=3)

        self.canvas.create_oval(cx - 108, cy - 108, cx + 108, cy + 108, outline=palette["ring1"], width=1)
        self.canvas.create_oval(cx - 92, cy - 92, cx + 92, cy + 92, outline=palette["ring2"], width=2)

        # ৩. ভেতরের কাউন্টার-রোটেটিং টেক সেগমেন্টস (অ্যান্টিক্লকওয়াইজ)
        num_inner_spokes = 8
        inner_r = 75
        for j in range(num_inner_spokes):
            angle = -self.tick * 1.5 + (j * (2 * math.pi / num_inner_spokes))
            x1 = cx + int(math.cos(angle) * (inner_r - 8))
            y1 = cy + int(math.sin(angle) * (inner_r - 8))
            x2 = cx + int(math.cos(angle) * inner_r)
            y2 = cy + int(math.sin(angle) * inner_r)
            self.canvas.create_line(x1, y1, x2, y2, fill=palette["core"], width=2)

        self.canvas.create_oval(cx - 78, cy - 78, cx + 78, cy + 78, outline=palette["accent"], width=1)

        # ৪. সেন্ট্রাল ভাইব্রেন্ট এনার্জি আইরিস (ভয়েসে প্রসারিত ও সংকুচিত হয়)
        iris_r = int(38 + (self.audio_level * 18) + (math.sin(self.tick * 4) * 3))
        self.canvas.create_oval(
            cx - iris_r, cy - iris_r, cx + iris_r, cy + iris_r,
            fill=palette["core"], outline="#ffffff", width=2
        )

        # সেন্ট্রাল ট্রায়াঙ্গেল রিঅ্যাক্টর আইকন
        tr_size = 14 + int(self.audio_level * 6)
        pts = [
            cx, cy - tr_size,
            cx - int(tr_size * 0.86), cy + int(tr_size * 0.5),
            cx + int(tr_size * 0.86), cy + int(tr_size * 0.5)
        ]
        self.canvas.create_polygon(pts, fill="#ffffff", outline=palette["ring2"], width=2)

        # ৫. রিয়েলটাইম অডিও সাউন্ড ওয়েভ স্পেকট্রাম (নিচে ছোট বার)
        bar_count = 14
        bar_spacing = 8
        start_bx = cx - ((bar_count * bar_spacing) // 2)
        by = self.size - 10

        for b in range(bar_count):
            bh = int(3 + (self.audio_level * 22 * abs(math.sin(self.tick * 3 + b * 0.5))))
            bx = start_bx + (b * bar_spacing)
            self.canvas.create_line(bx, by - bh, bx, by + bh, fill=palette["core"], width=2)

        # ৬. সিনেমাটিক টেক্সট ও ইমোশন ডিসপ্লে
        self.canvas.create_text(
            cx, self.size + 20,
            text=self.status_title,
            fill="#ffffff",
            font=("Segoe UI", 10, "bold")
        )
        self.canvas.create_text(
            cx, self.size + 42,
            text=f"● {self.status_subtitle}",
            fill=palette["core"],
            font=("Consolas", 8, "bold")
        )

        # ৩০ FPS এ স্মুথ ফ্রেম আপডেট
        self.root.after(33, self.animate)

    def update_loop(self):
        try:
            self.root.update_idletasks()
            self.root.update()
        except Exception:
            pass

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    hud = CinematicJarvisReactor()

    # ডেমো ইমোশন পরিবর্তন সাইকেল
    def demo_cycle():
        emotions = [
            ("IDLE", "SYSTEM ONLINE // STANDBY", 0.05),
            ("LISTENING", "VOICE HEARD: 'কেমন আছো জুবায়ের'", 0.55),
            ("THINKING", "ANALYZING INTENT...", 0.20),
            ("PERMISSION", "AWAITING AUTHORIZATION: 'হ্যাঁ বলুন'", 0.40),
            ("IDLE", "SYSTEM ONLINE // STANDBY", 0.05),
        ]
        
        def run_step(index=0):
            if index < len(emotions):
                em, sub, aud = emotions[index]
                hud.set_emotion(em, sub)
                hud.set_audio_level(aud)
                hud.root.after(2500, lambda: run_step(index + 1))
            else:
                run_step(0)

        run_step(0)

    demo_cycle()
    hud.run()
