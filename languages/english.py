"""
=============================================================================
Language Module: English (ENGLISH LANGUAGE PACK)
=============================================================================
Modify or extend English voice commands and responses here.
"""

LANG_CODE = "en-US"
LANG_NAME = "English"

COMMANDS = {
    "open_browser": [
        "open chrome", "open browser", "start browser", "chrome", "open google"
    ],
    "open_youtube": [
        "open youtube", "start youtube", "play youtube", "youtube"
    ],
    "open_notes": [
        "open notepad", "open notes", "write note", "notepad"
    ],
    "take_screenshot": [
        "take screenshot", "capture screen", "screenshot", "snap screen"
    ],
    "mode_mouse": [
        "mouse mode", "air mouse", "control mouse", "cursor mode"
    ],
    "mode_canvas": [
        "draw mode", "canvas mode", "start drawing", "drawing mode"
    ],
    "mode_presentation": [
        "presentation mode", "slide mode", "slides"
    ],
    "mode_media": [
        "media mode", "volume mode", "music mode"
    ],
    "clear_canvas": [
        "clear canvas", "clear screen", "erase all", "clean screen"
    ],
    "next_slide": [
        "next slide", "next", "forward slide"
    ],
    "prev_slide": [
        "previous slide", "back slide", "prev slide"
    ],
    "volume_up": [
        "volume up", "sound up", "increase volume"
    ],
    "volume_down": [
        "volume down", "sound down", "decrease volume"
    ],
    "show_desktop": [
        "show desktop", "minimize all", "clear windows"
    ],
    "lock_pc": [
        "lock system", "lock computer", "lock pc"
    ],
    "exit_system": [
        "exit system", "shutdown jarvis", "close jarvis", "quit"
    ]
}

RESPONSES = {
    "welcome_boss": "Welcome back, Boss! All automation protocols armed, sir.",
    "mouse_mode": "Switched to Air Mouse mode.",
    "canvas_mode": "Air Canvas activated. Ready for drawing.",
    "present_mode": "Presentation copilot engaged.",
    "media_mode": "Media and volume control active.",
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
    "shutdown": "Shutting down Jarvis systems. Goodbye, sir."
}
