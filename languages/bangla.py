"""
=============================================================================
ভাষার মডিউল: বাংলা (BANGLA LANGUAGE PACK)
=============================================================================
এখানে আপনি যেকোনো নতুন বাংলা ভয়েস কমান্ড যোগ করতে বা পরিবর্তন করতে পারেন।
"""

# স্পিচ রিকগনিশনের ভাষা কোড
LANG_CODE = "bn-BD"
LANG_NAME = "বাংলা"

# ব্যবহারকারীর মুখের বাংলা কমান্ডের তালিকা
# প্রতিটি কাজের জন্য আপনি একাধিক সমার্থক শব্দ যোগ করতে পারেন
COMMANDS = {
    "open_browser": [
        "ব্রাউজার খোলো", "ক্রোম খোলো", "গুগল খোলো", "নেট খোলো", "ক্রোম"
    ],
    "open_youtube": [
        "ইউটিউব খোলো", "ইউটিউব চালাও", "ইউটিউব প্লে করো", "গান চালাও"
    ],
    "open_notes": [
        "নোটপ্যাড খোলো", "নোট খোলো", "খাতা খোলো", "লেখা শুরু করো"
    ],
    "take_screenshot": [
        "স্ক্রিনশট নাও", "ছবি তোলো", "স্ক্রিন ক্যাপচার", "ছবি নাও"
    ],
    "mode_mouse": [
        "মাউস মোড", "মাউস চালাও", "মাউস চালু করো", "কার্সর মোড"
    ],
    "mode_canvas": [
        "ড্রয়িং মোড", "ক্যানভাস মোড", "আঁকাআঁকি", "আঁকার মোড"
    ],
    "mode_presentation": [
        "প্রেজেন্টেশন মোড", "স্লাইড মোড", "স্লাইড চালু করো"
    ],
    "mode_media": [
        "মিডিয়া মোড", "গান মোড", "ভলিউম মোড"
    ],
    "clear_canvas": [
        "মুছে ফেলো", "ক্যানভাস পরিষ্কার করো", "সব মোছো", "ক্লিন করো"
    ],
    "next_slide": [
        "পরের স্লাইড", "পরবর্তী স্লাইড", "নেক্সট স্লাইড", "সামনে যাও"
    ],
    "prev_slide": [
        "আগের স্লাইড", "পেছনের স্লাইড", "প্রিভিয়াস স্লাইড", "পেছনে যাও"
    ],
    "volume_up": [
        "ভলিউম বাড়াও", "আওয়াজ বাড়াও", "সাউন্ড বাড়াও"
    ],
    "volume_down": [
        "ভলিউম কমাও", "আওয়াজ কমাও", "সাউন্ড কমাও"
    ],
    "show_desktop": [
        "ডেস্কটপ দেখাও", "সব মিনিমাইজ করো", "সব বন্ধ করো"
    ],
    "lock_pc": [
        "পিসি লক করো", "লক করো", "কম্পিউটার লক করো"
    ],
    "exit_system": [
        "সিস্টেম বন্ধ করো", "বিদায় জার্ভিস", "বন্ধ হও", "বিদায়"
    ]
}

# জার্ভিস মুখে যে উত্তরগুলো দেবে (Text-to-Speech Responses)
RESPONSES = {
    "welcome_boss": "Welcome back, Boss! All automation protocols armed, sir.",
    "mouse_mode": "Switched to Air Mouse mode.",
    "canvas_mode": "Air Canvas activated. Ready for drawing.",
    "present_mode": "Presentation copilot engaged.",
    "media_mode": "Media control active.",
    "screenshot": "Screenshot captured and saved to your pictures folder, sir.",
    "clear": "Canvas cleared.",
    "browser": "Opening browser immediately.",
    "youtube": "Launching YouTube, sir.",
    "notes": "Opening Notepad for you.",
    "next": "Advancing to next slide.",
    "prev": "Returning to previous slide.",
    "volume_up": "Increasing volume.",
    "volume_down": "Decreasing volume.",
    "desktop": "Minimizing all windows to desktop.",
    "locked": "Locking workstation now.",
    "shutdown": "Shutting down Jarvis systems. Goodbye, sir."
}
