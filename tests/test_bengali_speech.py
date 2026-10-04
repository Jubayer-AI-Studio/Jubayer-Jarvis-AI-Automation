"""
Test native Bengali TTS using edge-tts (bn-BD-PradeepNeural) and native Windows MCI playback.
"""
import os
import sys
import asyncio
import ctypes
import edge_tts

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

async def speak_bangla(text):
    temp_mp3 = os.path.abspath("temp_speech.mp3")
    comm = edge_tts.Communicate(text, "bn-BD-PradeepNeural")
    await comm.save(temp_mp3)

    # Play natively via Windows winmm (built-in Windows multimedia API)
    ctypes.windll.winmm.mciSendStringW(f'open "{temp_mp3}" type mpegvideo alias bn_voice', None, 0, None)
    ctypes.windll.winmm.mciSendStringW('play bn_voice wait', None, 0, None)
    ctypes.windll.winmm.mciSendStringW('close bn_voice', None, 0, None)
    print(f"[BENGALI TTS PLAYED]: {text}")

if __name__ == "__main__":
    asyncio.run(speak_bangla("আসসালামু আলাইকুম স্যার! আমি জুবায়ের, আমি এখন থেকে সরাসরি বাংলায় আপনার সাথে কথা বলব।"))
