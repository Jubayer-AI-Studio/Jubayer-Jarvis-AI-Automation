"""
=============================================================================
ইউআই মডিউল: ফ্লোটিং সাই-ফাই 'আর্ক রিঅ্যাক্টর' অর্ব (ARC REACTOR ORB)
=============================================================================
স্ক্রিনে টনি স্টার্কের রিঅ্যাক্টরের মতো ভাসমান স্বচ্ছ নিয়ন সাই-ফাই অর্ব।
ক্যামেরা ছাড়াই এটি আপনার কণ্ঠের সাথে সাথে পালস করে, জুবায়েরের স্ট্যাটাস দেখায়
এবং ক্লিক করলে মোবাইল রিমোট কিউআর কোড প্রদর্শন করে।
১০০% ফ্রি - উইন্ডোজ বিল্ট-ইন Tkinter ক্যানভাস।
"""

import math
import time
import os
import tkinter as tk
from PIL import Image, ImageTk
from config import AI_NAME, AI_NAME_ENGLISH

class ArcReactorOrb:
    def __init__(self, qr_path=None, remote_url=""):
        self.root = tk.Tk()
        self.root.title("JUBAYER_ORB")
        
        # উইন্ডোর বর্ডার রিমুভ ও অলওয়েজ অন টপ
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # ট্রান্সপারেন্ট ব্যাকগ্রাউন্ড (#000001 রঙটি সম্পূর্ণ অদৃশ্য হয়ে যাবে)
        self.trans_color = "#000001"
        self.root.attributes("-transparentcolor", self.trans_color)
        self.root.config(bg=self.trans_color)

        self.size = 170
        self.width = self.size
        self.height = self.size + 40  # নিচে টেক্সটের জন্য জায়গা
        
        # স্ক্রিনের নিচের ডান কোণে প্রাথমিক অবস্থান
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.pos_x = screen_w - self.width - 40
        self.pos_y = screen_h - self.height - 80
        self.root.geometry(f"{self.width}x{self.height}+{self.pos_x}+{self.pos_y}")

        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg=self.trans_color,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        # State variables
        self.is_awake = False
        self.audio_level = 0.05
        self.tick = 0
        self.status_text = f"{AI_NAME_ENGLISH} // ONLINE"

        self.qr_path = qr_path
        self.remote_url = remote_url
        self.qr_window = None

        # Drag and Drop support
        self._drag_start_x = 0
        self._drag_start_y = 0
        self.canvas.bind("<ButtonPress-1>", self._start_drag)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<Double-Button-1>", lambda e: self.toggle_qr_popup())
        self.canvas.bind("<Button-3>", lambda e: self.toggle_qr_popup())

        # Start animation loop
        self.animate()

    def _start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def _on_drag(self, event):
        deltax = event.x - self._drag_start_x
        deltay = event.y - self._drag_start_y
        self.pos_x += deltax
        self.pos_y += deltay
        self.root.geometry(f"+{self.pos_x}+{self.pos_y}")

    def set_awake_state(self, awake=True):
        self.is_awake = awake
        self.status_text = f"{AI_NAME_ENGLISH} // LISTENING..." if awake else f"{AI_NAME_ENGLISH} // ONLINE"

    def set_audio_level(self, level):
        self.audio_level = max(0.05, min(1.0, level))

    def toggle_qr_popup(self):
        """Toggle Mobile QR Code Popup"""
        if self.qr_window and tk.Toplevel.winfo_exists(self.qr_window):
            self.qr_window.destroy()
            self.qr_window = None
            return

        self.qr_window = tk.Toplevel(self.root)
        self.qr_window.title("Mobile Remote Connection")
        self.qr_window.geometry("260x310")
        self.qr_window.configure(bg="#0d1117")
        self.qr_window.attributes("-topmost", True)

        lbl_title = tk.Label(
            self.qr_window,
            text="Scan with Phone Camera",
            fg="#38bdf8",
            bg="#0d1117",
            font=("Segoe UI", 11, "bold")
        )
        lbl_title.pack(pady=10)

        if self.qr_path and os.path.exists(self.qr_path):
            try:
                img = Image.open(self.qr_path).resize((180, 180))
                photo = ImageTk.PhotoImage(img)
                lbl_img = tk.Label(self.qr_window, image=photo, bg="#0d1117")
                lbl_img.image = photo
                lbl_img.pack()
            except Exception:
                pass

        lbl_url = tk.Label(
            self.qr_window,
            text=self.remote_url,
            fg="#22c55e",
            bg="#0d1117",
            font=("Consolas", 10)
        )
        lbl_url.pack(pady=8)

    def animate(self):
        """প্রতি ফ্রেমে সাই-ফাই রিঅ্যাক্টরের রোটেশন ও পালস আঁকা"""
        self.canvas.delete("all")
        cx, cy = self.size // 2, self.size // 2
        self.tick += 0.08

        # কালার স্কিম (সজাগ হলে গোল্ডেন/সবুজ, নয়তো নিয়ন সায়ান)
        core_color = "#22c55e" if self.is_awake else "#00e5ff"
        ring_color = "#eab308" if self.is_awake else "#0284c7"
        glow_color = "#15803d" if self.is_awake else "#0369a1"

        # ১. ব্যাকগ্রাউন্ড গ্লো অর্ব
        base_r = 45 + int(self.audio_level * 18)
        self.canvas.create_oval(
            cx - base_r, cy - base_r, cx + base_r, cy + base_r,
            fill=glow_color, outline="", stipple="gray50"
        )

        # ২. বাইরের রোটেটিং সাই-ফাই সেগমেন্টস
        num_spokes = 8
        spoke_r = 55
        for i in range(num_spokes):
            angle = self.tick + i * (2 * math.pi / num_spokes)
            x1 = cx + int(math.cos(angle) * (spoke_r - 6))
            y1 = cy + int(math.sin(angle) * (spoke_r - 6))
            x2 = cx + int(math.cos(angle) * spoke_r)
            y2 = cy + int(math.sin(angle) * spoke_r)
            self.canvas.create_line(x1, y1, x2, y2, fill=ring_color, width=3)

        # ৩. মাঝের কনসেন্ট্রিক রিংস
        self.canvas.create_oval(cx - 58, cy - 58, cx + 58, cy + 58, outline=ring_color, width=2)
        self.canvas.create_oval(cx - 48, cy - 48, cx + 48, cy + 48, outline="#38bdf8", width=1)

        # ৪. অভ্যন্তরীণ এনার্জি কোর (ভয়েসের সাথে পালস করে)
        core_r = 26 + int(self.audio_level * 12)
        self.canvas.create_oval(
            cx - core_r, cy - core_r, cx + core_r, cy + core_r,
            fill=core_color, outline="#ffffff", width=2
        )

        # সেন্ট্রাল ট্রায়াঙ্গেল রিঅ্যাক্টর মার্ক
        t_r = 10
        pts = [
            cx, cy - t_r,
            cx - int(t_r * 0.86), cy + int(t_r * 0.5),
            cx + int(t_r * 0.86), cy + int(t_r * 0.5)
        ]
        self.canvas.create_polygon(pts, fill="#ffffff", outline=ring_color, width=1)

        # ৫. নিচে স্ট্যাটাস টেক্সট
        self.canvas.create_text(
            cx, self.size + 16,
            text=self.status_text,
            fill="#ffffff",
            font=("Segoe UI", 9, "bold")
        )

        # পরবর্তী ফ্রেম সিডিউল (৩০ FPS)
        self.root.after(33, self.animate)

    def update_loop(self):
        """নন-ব্লকিং আপডেট"""
        try:
            self.root.update_idletasks()
            self.root.update()
        except Exception:
            pass

    def run(self):
        self.root.mainloop()
