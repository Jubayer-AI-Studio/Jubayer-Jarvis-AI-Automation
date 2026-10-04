"""
=============================================================================
Language Module: Banglish (BANGLISH LANGUAGE PACK - ROMAN BENGALI)
=============================================================================
ক্যাজুয়াল রোমান অক্ষরে লেখা বা বলা বাংলা (বাংলিশ) ভাষা প্যাক।
যেমন: "kemon acho", "ami valo achi", "pc bondho koro", "sound barao"
=============================================================================
"""

LANG_CODE = "bn-Latn"
LANG_NAME = "বাংলিশ (Banglish)"

COMMANDS = {
    "greetings": [
        "kemon acho", "kemon achen", "ki khobor", "ki obostha", "hi jubayer", "hello jubayer", "jubayer suncho"
    ],
    "who_are_you": [
        "tumi k", "tumi ke", "parichoy dao", "tomar nam ki", "tumi ki korte paro"
    ],
    "shutdown_pc": [
        "pc bondho koro", "pc off koro", "computer bondho koro", "pc shutdown koro", "off kore dao"
    ],
    "close_window": [
        "window kete dao", "window bondho koro", "kete dao", "eta bondho koro", "close koro"
    ],
    "volume_up": [
        "sound barao", "awaj barao", "volume barao", "sound ektu barao"
    ],
    "volume_down": [
        "sound komao", "awaj komao", "volume komao", "sound ektu komao"
    ],
    "screenshot": [
        "screenshot nao", "chobi tolo", "screen snapshot nao"
    ],
    "open_youtube": [
        "youtube e gan bajao", "youtube chalu koro", "gan play koro", "gojol chalo", "quran tilawat chalao"
    ],
    "open_notepad": [
        "notepad kholo", "chithi likhbo", "kichu likhbo", "document kholo"
    ],
    "permission_yes": [
        "ha", "haa", "koro", "kor", "thik ache", "hou", "proceed", "chalao"
    ],
    "permission_no": [
        "na", "naa", "koro na", "koris na", "bad dao", "thak", "cancel", "lagbe na"
    ]
}

RESPONSES = {
    "greetings": "Alhamdulillah Sir, ami khub bhalo achi! Apnar ajker din kemon katche?",
    "who_are_you": "Ami apnar personal hands-free AI assistant 'Jubayer'. Ami apnar kotha sune PC chalai.",
    "permission_ask": "Sir, apni ki chan ami {action_desc}? Doya kore ha ba na bolun.",
    "permission_granted": "Anumoti dewar jonno dhonnobad Sir. Ami ekhoni kajti kore dicchi.",
    "permission_denied": "Thik ache Sir, apnar nirdesh moto kajti batil kora holo.",
    "thanks": "Apnake onek dhonnobad Sir! Apnar kaje sahajjo korte pere ami khushi."
}
