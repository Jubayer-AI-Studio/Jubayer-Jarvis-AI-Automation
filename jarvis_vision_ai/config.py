"""
JARVIS-AETHER Configuration File
Stores all system constants, color palettes, sensitivity parameters, and multilingual command mappings.
100% Free & Open-Source (No Paid APIs).
"""

import pyautogui

# Screen & Camera Dimensions
CAMERA_INDEX = 0
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
FPS_TARGET = 30

# Retrieve native monitor resolution
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Cyberpunk Sci-Fi HUD Colors (OpenCV uses BGR format)
COLOR_CYAN = (255, 220, 0)         # Glowing Neon Cyan
COLOR_GREEN = (0, 255, 128)        # Neon Green
COLOR_PURPLE = (255, 0, 200)       # Electric Magenta / Purple
COLOR_RED = (50, 50, 255)          # Cyber Alert Red
COLOR_YELLOW = (0, 230, 255)       # High-contrast Alert Yellow
COLOR_WHITE = (245, 245, 245)
COLOR_DARK = (20, 20, 25)
COLOR_GRID = (60, 45, 30)

# Air Canvas Color Palette Options (BGR)
CANVAS_COLORS = [
    {"name": "CYAN", "bgr": (255, 220, 0), "rgb": (0, 220, 255)},
    {"name": "GREEN", "bgr": (0, 255, 100), "rgb": (100, 255, 0)},
    {"name": "RED", "bgr": (50, 60, 255), "rgb": (255, 60, 50)},
    {"name": "PURPLE", "bgr": (255, 50, 200), "rgb": (200, 50, 255)},
    {"name": "YELLOW", "bgr": (0, 240, 255), "rgb": (255, 240, 0)},
]

# Gesture Sensitivity & Thresholds
MOUSE_SMOOTHING = 0.65             # Exponential Moving Average factor (higher = smoother)
CLICK_PINCH_DISTANCE = 32          # Pixels between thumb tip & index tip for left click
RIGHT_CLICK_DISTANCE = 35          # Pixels between thumb tip & middle finger tip for right click
DRAG_HOLD_SECONDS = 0.5            # Hold pinch for 0.5s to start dragging
SWIPE_DISTANCE_THRESHOLD = 80      # Min horizontal pixel travel for slide swipe
VOLUME_MIN_DIST = 25               # Min thumb-index distance (0% volume)
VOLUME_MAX_DIST = 180              # Max thumb-index distance (100% volume)

# System Operational Modes
class SystemMode:
    MOUSE = "AIR_MOUSE"
    CANVAS = "AIR_CANVAS"
    PRESENTATION = "PRESENTATION"
    MEDIA = "MEDIA_CONTROL"
    HUD_ONLY = "STANDBY"

# Multilingual Voice Command Dictionaries
# Maps spoken phrases across English, Bengali, Urdu, and Arabic to internal actions
VOICE_COMMANDS = {
    # Open Browser
    "open_browser": [
        "open chrome", "open browser", "start browser", "chrome",
        "ক্রোম খোলো", "ব্রাউজার খোলো", "গুগল খোলো",
        "کروم کھولو", "براؤزر کھولو",
        "افتح المتصفح", "افتح كروم"
    ],
    # Open YouTube
    "open_youtube": [
        "open youtube", "start youtube", "play youtube", "youtube",
        "ইউটিউব খোলো", "ইউটিউব চালাও",
        "یوٹیوب کھولو", "یوٹیوب چلاؤ",
        "افتح يوتيوب", "شغل يوتيوب"
    ],
    # Take Screenshot
    "take_screenshot": [
        "take screenshot", "capture screen", "screenshot", "snap screen",
        "স্ক্রিনশট নাও", "ছবি তোলো", "স্ক্রিন ক্যাপচার",
        "اسکرین شاٹ لو", "تصویر لو",
        "التقط الشاشة", "صور الشاشة", "لقطة شاشة"
    ],
    # Switch to Mouse Mode
    "mode_mouse": [
        "mouse mode", "air mouse", "control mouse",
        "মাউস মোড", "মাউস চালাও",
        "ماؤس موڈ",
        "وضع الفأرة", "تحكم بالفأرة"
    ],
    # Switch to Canvas / Draw Mode
    "mode_canvas": [
        "draw mode", "canvas mode", "start drawing", "drawing mode",
        "ড্রয়িং মোড", "ক্যানভাস মোড", "আঁকাআঁকি",
        "ڈرائنگ موڈ", "کینوس موڈ",
        "وضع الرسم", "لوحة الرسم"
    ],
    # Switch to Presentation Mode
    "mode_presentation": [
        "presentation mode", "slide mode", "slides",
        "প্রেজেন্টেশন মোড", "স্লাইড মোড",
        "پریزنٹیشن موڈ",
        "وضع العرض", "عرض الشرائح"
    ],
    # Clear Canvas
    "clear_canvas": [
        "clear canvas", "clear screen", "erase all", "clean screen",
        "ক্যানভাস পরিষ্কার করো", "মুছে ফেলো", "সব মোছো",
        "کینوس صاف کرو", "مٹا دو",
        "امسح الشاشة", "نظف اللوحة"
    ],
    # Next Slide
    "next_slide": [
        "next slide", "next", "forward slide",
        "পরের স্লাইড", "পরবর্তী স্লাইড", "নেক্সট স্লাইড",
        "اگلی سلائیڈ", "آگے بڑھو",
        "الشريحة التالية", "التالي"
    ],
    # Previous Slide
    "prev_slide": [
        "previous slide", "back slide", "prev slide",
        "আগের স্লাইড", "পেছনের স্লাইড", "প্রিভিয়াস স্লাইড",
        "پچھلی سلائیڈ", "پیچھے جاؤ",
        "الشريحة السابقة", "السابق"
    ],
    # Volume Up
    "volume_up": [
        "volume up", "sound up", "increase volume",
        "ভলিউম বাড়াও", "আওয়াজ বাড়াও",
        "آواز بڑھاؤ",
        "ارفع الصوت", "زيادة الصوت"
    ],
    # Volume Down
    "volume_down": [
        "volume down", "sound down", "decrease volume",
        "ভলিউম কমাও", "আওয়াজ কমাও",
        "آواز کم کرو",
        "اخفض الصوت", "تقليل الصوت"
    ],
    # Show Desktop / Minimize all
    "show_desktop": [
        "show desktop", "minimize all", "clear windows",
        "ডেস্কটপ দেখাও", "সব মিনিমাইজ করো",
        "ڈیسک ٹاپ دکھاؤ",
        "أظهر سطح المكتب", "تصغير الكل"
    ],
    # Open Notepad / Notes
    "open_notes": [
        "open notepad", "open notes", "write note",
        "নোটপ্যাড খোলো", "নোট খোলো",
        "نوٹ پیڈ کھولو",
        "افتح المفكرة", "اكتب ملاحظة"
    ],
    # Lock Windows
    "lock_pc": [
        "lock system", "lock computer", "lock pc",
        "লক করো", "পিসি লক করো",
        "کمپیوٹر لاک کرو",
        "قفل الجهاز", "اقفل الكمبيوتر"
    ],
    # Exit / Stop
    "exit_system": [
        "exit system", "shutdown jarvis", "close jarvis", "quit",
        "সিস্টেম বন্ধ করো", "বিদায় জার্ভিস", "বন্ধ হও",
        "سسٹم بند کرو", "الوداع",
        "أغلق النظام", "إيقاف التشغيل"
    ]
}

# Jarvis Voice Response Audio Strings (Multilingual)
VOICE_RESPONSES = {
    "greeting": "AETHER Jarvis online. All automation protocols armed, sir.",
    "mouse_mode": "Switched to Air Mouse mode.",
    "canvas_mode": "Air Canvas activated. Ready for drawing.",
    "present_mode": "Presentation copilot engaged.",
    "screenshot": "Screenshot captured and saved to your pictures folder, sir.",
    "clear": "Canvas cleared.",
    "browser": "Opening browser immediately.",
    "youtube": "Launching YouTube, sir.",
    "notes": "Opening Notepad for you.",
    "next": "Advancing to next slide.",
    "prev": "Returning to previous slide.",
    "volume_up": "Increasing volume.",
    "volume_down": "Decreasing volume.",
    "desktop": "Minimizing all windows.",
    "locked": "Locking workstation now.",
    "unknown": "Command recognized. Executing action.",
    "welcome_boss": "Welcome back, Boss. System monitoring is active."
}
