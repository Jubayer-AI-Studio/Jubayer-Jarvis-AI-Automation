"""
Diagnostic test script for JUBAYER AI
Verifies audio recording, speaker, voice lock extraction, and Arc Reactor widget.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_microphone():
    print("[TEST 1/5] Testing Microphone (SoundDevice)...")
    try:
        import sounddevice as sd
        import numpy as np
        devs = sd.query_devices()
        print(f"  --> Found {len(devs)} audio devices.")
        rec = sd.rec(int(16000 * 0.5), samplerate=16000, channels=1, dtype='int16')
        sd.wait()
        rms = np.sqrt(np.mean(rec.astype(np.float64) ** 2))
        print(f"  --> Microphone test PASSED! (RMS: {rms:.1f})")
        return True
    except Exception as e:
        print(f"  [FAIL] Microphone error: {e}")
        return False

def test_tts():
    print("[TEST 2/5] Testing Voice Feedback (pyttsx3)...")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        engine.say("Jubayer diagnostics complete.")
        engine.runAndWait()
        print("  --> Text-to-Speech audio played successfully!")
        return True
    except Exception as e:
        print(f"  [FAIL] TTS error: {e}")
        return False

def test_voice_lock():
    print("[TEST 3/5] Testing Audio Voice Lock Feature Extraction...")
    try:
        from security.voice_lock import VoiceLock
        import numpy as np
        vl = VoiceLock()
        dummy_audio = np.random.randint(-1000, 1000, 16000, dtype=np.int16).tobytes()
        feat = vl.extract_features(dummy_audio)
        if feat and len(feat) == 16:
            print("  --> Voice Biometric 16-band feature extraction PASSED!")
            return True
        else:
            print("  [FAIL] Feature extraction returned invalid dimensions.")
            return False
    except Exception as e:
        print(f"  [FAIL] VoiceLock error: {e}")
        return False

def test_mobile_server():
    print("[TEST 4/5] Testing Mobile Remote Server & QR Generator...")
    try:
        import qrcode
        from mobile.server import MobileRemoteServer
        server = MobileRemoteServer(wake_engine=None, system_controls=None, port=5001)
        if os.path.exists(server.qr_path):
            print(f"  --> QR Code generated successfully at {server.qr_path}!")
            return True
        return False
    except Exception as e:
        print(f"  [FAIL] Mobile server error: {e}")
        return False

def test_arc_reactor():
    print("[TEST 5/5] Testing Arc Reactor Orb UI Initialization...")
    try:
        from ui.arc_reactor_orb import ArcReactorOrb
        orb = ArcReactorOrb()
        orb.set_audio_level(0.5)
        orb.set_awake_state(True)
        orb.root.update_idletasks()
        orb.root.destroy()
        print("  --> Arc Reactor Orb transparent canvas test PASSED!")
        return True
    except Exception as e:
        print(f"  [FAIL] Arc Reactor error: {e}")
        return False

def main():
    print("\n=======================================================")
    print("   JUBAYER AI SYSTEM READINESS DIAGNOSTIC")
    print("=======================================================\n")
    results = [
        test_microphone(),
        test_tts(),
        test_voice_lock(),
        test_mobile_server(),
        test_arc_reactor()
    ]
    print("\n-------------------------------------------------------")
    passed = sum(1 for r in results if r)
    print(f"RESULTS: {passed}/{len(results)} tests passed.")
    if passed == len(results):
        print("[SUCCESS] ALL SYSTEMS ARE 100% OPERATIONAL AND READY!")
    else:
        print("[NOTICE] Some components need check.")
    print("-------------------------------------------------------\n")

if __name__ == "__main__":
    main()
