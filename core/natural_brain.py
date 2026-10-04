"""
=============================================================================
কোর মডিউল: ন্যাচারাল ব্রেইন (NATURAL BRAIN NLU v4.0)
=============================================================================
বাংলা, ইংরেজি এবং রোমান বাংলিশের কথ্য ভাষা বিশ্লেষণ:
- সাধারণ আড্ডা ও যেকোনো কথার উত্তর দেওয়া
- ইউটিউব ও ক্রোম নিশ্চিতভাবে বন্ধ করা (close, band karo, kete dao)
- ফ্যান্টম ক্রোম পুরোপুরি নির্মূল
=============================================================================
"""

import re

def clean_and_normalize(text):
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s\u0980-\u09FF]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

class NaturalBrain:
    def __init__(self):
        pass

    def parse_intent(self, raw_text):
        norm = clean_and_normalize(raw_text)
        words = norm.split()

        if len(norm) == 0:
            return "UNKNOWN", None

        # =====================================================================
        # ১. ক্লোজ / উইন্ডো বা অ্যাপ বন্ধ করা (সর্বোচ্চ অগ্রাধিকার)
        # =====================================================================
        # "close youtube", "close chrome", "close", "band karo", "kete dao", "ber hou"
        close_patterns = [
            "close", "ক্লোজ", "বন্ধ", "band", "bandh", "bondho", "kete", "কাটো",
            "কেটে", "stop", "exit", "ber", "বের"
        ]
        has_close_keyword = any(w in norm for w in close_patterns)
        is_closing_app = has_close_keyword and any(app in norm for app in ["youtube", "chrome", "ইউটিউব", "ক্রোম", "window", "উইন্ডো", "this", "it", "music", "ভিডিও", "video", "app"])

        # সরাসরি "close", "close close", "kete dao", "band karo", "close this", "বন্ধ করো"
        if is_closing_app or any(p in norm for p in [
            "close window", "close this", "close youtube", "close chrome", "stop chrome",
            "stop music", "band karo", "bandhu karo", "bondho koro", "kete dao", "kete de",
            "ber hou", "ber ho", "theke ber", "উইন্ডো বন্ধ", "ইউটিউব বন্ধ", "ক্রোম বন্ধ",
            "কেটে দাও", "কেটে দে", "কাটো", "বের হও"
        ]) or (len(words) <= 2 and any(w in words for w in ["close", "কাটো", "বন্ধ", "exit"])):
            return "WINDOW_CLOSE", None

        # =====================================================================
        # ২. মিনিমাইজ / ডেস্কটপ
        # =====================================================================
        if any(w in norm for w in ["ডেস্কটপ", "মিনিমাইজ", "desktop", "minimize", "sorao", "chale jao", "disturb mein"]):
            return "WINDOW_DESKTOP", None

        # =====================================================================
        # ৩. পিসি অন / ওয়েক (POWER WAKE)
        # =====================================================================
        if any(t in norm for t in ["পিসি অন", "কম্পিউটার অন", "turn on", "wake up", "জাগো", "উঠো"]):
            return "POWER_WAKE", None

        # =====================================================================
        # ৪. পিসি বন্ধ / শাটডাউন (POWER SHUTDOWN)
        # =====================================================================
        shutdown_triggers = [
            "শাটডাউন", "shutdown", "shut down", "shut this", "shut the pc",
            "পিসি বন্ধ", "কম্পিউটার বন্ধ", "পিসি অফ", "কম্পিউটার অফ",
            "অফ করে দাও", "off kar do", "turn off the pc", "turn off pc"
        ]
        if any(t in norm for t in shutdown_triggers):
            return "POWER_SHUTDOWN", None

        # স্লিপ মোড / স্ক্রিন অফ
        sleep_triggers = [
            "পিসি স্লিপ", "স্লিপ মোড", "স্ক্রিন অফ", "ঘুমাবো",
            "sleep pc", "sleep mode", "sleep", "screen off"
        ]
        if any(t in norm for t in sleep_triggers):
            return "POWER_SLEEP", None

        if any(w in norm for w in ["রিস্টার্ট", "restart", "reboot"]):
            return "POWER_RESTART", None

        if any(w in norm for w in ["পিসি লক", "কম্পিউটার লক", "lock pc", "lock"]):
            return "POWER_LOCK", None

        # =====================================================================
        # ৫. ভলিউম ও সাউন্ড
        # =====================================================================
        sound_words = ["আওয়াজ", "সাউন্ড", "ভলিউম", "শব্দ", "sound", "volume"]
        down_words = ["কমা", "কমি", "কমিয়ে", "কমাও", "down", "decrease", "lower", "kamao", "komao"]
        up_words = ["বাড়া", "বাড়ি", "up", "increase", "higher", "louder", "barao", "bariye"]

        has_sound = any(sw in norm for sw in sound_words)
        has_down = any(dw in norm for dw in down_words)
        has_up = any(uw in norm for uw in up_words)

        if (has_sound and has_down) or any(w in norm for w in ["volume down", "sound down", "volume kamao", "volume komao"]):
            return "VOLUME_DOWN", None

        if (has_sound and has_up) or any(w in norm for w in ["volume up", "sound up", "volume barao"]):
            return "VOLUME_UP", None

        if any(w in words for w in ["মিউট", "mute", "unmute"]):
            return "VOLUME_MUTE", None

        # =====================================================================
        # ৬. স্ক্রিনশট
        # =====================================================================
        if any(w in norm for w in ["স্ক্রিনশট", "ছবি তোলো", "screenshot"]):
            return "SCREENSHOT", None

        # =====================================================================
        # ৭. ভিডিও প্লেয়ার কন্ট্রোল
        # =====================================================================
        if any(w in norm for w in ["থামাও", "পজ", "pause", "resume", "stop music"]):
            return "MEDIA_PAUSE", None
        if any(w in norm for w in ["ফুল স্ক্রিন", "fullscreen"]):
            return "MEDIA_FULLSCREEN", None
        if any(w in norm for w in ["পরের গান", "next video", "next song"]):
            return "MEDIA_NEXT", None
        if any(w in norm for w in ["প্রথম ভিডিও", "first video"]):
            return "FIRST_VIDEO", None

        # =====================================================================
        # ৮. ইউটিউব ও গান (শুধুমাত্র প্লে করতে বললে)
        # =====================================================================
        media_keywords = [
            "গান", "song", "music", "গজল", "নাশিদ", "nasheed", "তেলাওয়াত", "তেলাওয়াত", "quran", "কোরআন",
            "কুরআন", "সূরা", "surah"
        ]
        has_explicit_play = any(w in words for w in media_keywords) or any(k in norm for k in ["youtube e", "play ", "চালাও", "বাজাও"])

        if ("youtube" in norm or "ইউটিউব" in norm or has_explicit_play) and not has_close_keyword:
            filter_tokens = [
                "hey", "can", "you", "could", "please", "some", "play", "open",
                "stream", "listen", "to", "watch", "on", "from", "in", "youtube",
                "ইউটিউব", "ইউটিউবে", "থেকে", "ঢুকে", "গিয়ে", "একটা", "একটু",
                "গান", "song", "music", "ভিডিও", "video", "গজল", "নাশিদ",
                "শুনতে", "চালাও", "চালিয়ে দাও", "ছাড়ো", "ছাড়ো", "বাজাও",
                "প্লে করো", "প্লে", "দাও", "করো", "কর", "দে"
            ]
            query_tokens = [w for w in words if w not in filter_tokens]
            target_query = " ".join(query_tokens).strip()

            if len(target_query) > 0:
                return "YOUTUBE_PLAY", target_query
            else:
                return "YOUTUBE_HOME", None

        # =====================================================================
        # ৯. নোটপ্যাড ও টাইপিং
        # =====================================================================
        if any(w in norm for w in ["নোটপ্যাড", "open notepad", "notepad"]):
            return "NOTEPAD_OPEN", None

        # =====================================================================
        # ১০. সাধারণ আড্ডা ও ব্যবহারকারীর সাথে কথা বলা (CONVERSATIONAL DIALOGUE)
        # =====================================================================
        # কুশল বিনিময়
        if any(w in norm for w in ["কেমন আছ", "how are you", "kemon acho", "ki khobor", "ki obostha", "kemon"]):
            return "CHAT_HOW_ARE_YOU", None

        # শুনতে পাচ্ছ / আছো কি
        if any(w in norm for w in ["শুনতে পাচ্ছ", "can you hear me", "shunte pao", "shuncho", "suncho", "are you there", "shunte", "hear me"]):
            return "CHAT_HEAR_ME", None

        # পরিচয়
        if any(w in norm for w in ["তুমি কে", "কে তুমি", "who are you", "tumi ke", "tumi k", "তোমার নাম কি"]):
            return "CHAT_WHO_ARE_YOU", None

        # কুশল / সম্ভাষণ
        if any(w in norm for w in ["hello", "hi", "hey", "হ্যালো", "হাই", "হেই", "জুবায়ের", "zubair", "jubayer"]):
            return "CHAT_GREETING", None

        # সমস্যা কি / কি করছ
        if any(w in norm for w in ["ki samasya", "কি সমস্যা", "problem", "ki problem"]):
            return "CHAT_PROBLEM", None

        # ভাই
        if any(w in norm for w in ["bhai", "ভাই", "bro"]):
            return "CHAT_BHAI", None

        # ধন্যবাদ / প্রশংসা
        if any(w in norm for w in ["ধন্যবাদ", "thank you", "thanks", "good boy", "valoi", "shabash", "অসাধারণ"]):
            return "CHAT_THANKS", None

        # যেকোনো অনির্ধারিত কথা -> চুপ থাকবে না! ব্যবহারকারীর কথার উত্তর দেবে!
        return "CHAT_FALLBACK", raw_text
