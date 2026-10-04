"""
=============================================================================
JUBAYER AI: AUTONOMOUS OPERATOR (MAIN RUNTIME ORCHESTRATOR v2.1)
=============================================================================
UTF-8 Native Console (Zero '?' replacement characters).
Dual-Language Natural Voice Recognition (Bangla + English).
Floating Sci-Fi Arc Reactor Orb UI + Mobile WiFi Remote.
100% Hands-Free Control.
"""

import sys
import os
import time

# Enable native UTF-8 console output for Windows cmd
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from config import (
    AI_NAME,
    AI_NAME_ENGLISH,
    CAMERA_ENABLED,
    MOBILE_PORT
)

# Core subsystems
from security import VoiceLock
from voice import VoiceListener, SpeechFeedback
from actions import SystemControls, AppLauncher
from core.wake_word import WakeWordDispatcher
from mobile import MobileRemoteServer
from ui import ArcReactorOrb

class JubayerMasterApp:
    def __init__(self):
        print("\n" + "=" * 65)
        print(f"        {AI_NAME_ENGLISH.upper()} AI // AUTONOMOUS OPERATING ASSISTANT v2.1")
        print("=" * 65 + "\n")
        print(f"[{AI_NAME_ENGLISH}] Initializing core perception engines...")

        # Setup logs directory
        self.logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        os.makedirs(self.logs_dir, exist_ok=True)
        self.log_file = os.path.join(self.logs_dir, "heard_speech.log")

        # 1. Voice and Action Subsystems
        self.speech_feedback = SpeechFeedback()
        self.system_controls = SystemControls()
        self.app_launcher = AppLauncher()
        self.voice_lock = VoiceLock()

        # 2. Mobile WiFi Remote Server
        self.mobile_server = MobileRemoteServer(
            wake_engine=None,
            system_controls=self.system_controls,
            port=MOBILE_PORT
        )
        self.mobile_server.start()

        # 3. Floating Sci-Fi Arc Reactor Orb (UI)
        self.orb_ui = ArcReactorOrb(
            qr_path=self.mobile_server.qr_path,
            remote_url=self.mobile_server.remote_url
        )

        # 4. Wake-Word & Natural Intent Dispatcher
        self.wake_engine = WakeWordDispatcher(
            speech_feedback=self.speech_feedback,
            system_controls=self.system_controls,
            app_launcher=self.app_launcher,
            voice_lock=self.voice_lock,
            orb_ui=self.orb_ui
        )
        self.mobile_server.wake_engine = self.wake_engine

        # 5. Microphone Voice Listener
        self.voice_listener = VoiceListener()
        self.voice_listener.start()

        # Audible Welcome Acknowledgment
        self.speech_feedback.speak("আসসালামু আলাইকুম স্যার! আমি জুবায়ের, আপনার কথা শুনতে প্রস্তুত।")

        print("\n" + "-" * 65)
        print(f"  --> {AI_NAME_ENGLISH} is listening for your voice!")
        print(f"  --> Wake Word: '{AI_NAME_ENGLISH}' (Call in English or Bangla)")
        print(f"  --> Dual Mode: Understands both English and Bangla")
        print(f"  --> Mobile Remote URL: {self.mobile_server.remote_url}")
        print("  --> Click on the Arc Reactor Orb to show/hide Mobile QR Code")
        print("-" * 65 + "\n")

    def poll_events(self):
        """Polls microphone and background events every 30ms (<1% CPU)"""
        try:
            # Update visual audio reactor glow with live sound energy
            self.orb_ui.set_audio_level(self.voice_listener.audio_level)

            # Check for newly captured speech
            raw_data = self.voice_listener.get_raw_text()
            if raw_data:
                if isinstance(raw_data, tuple):
                    text_clean, audio_bytes = raw_data
                else:
                    text_clean, audio_bytes = raw_data, None

                # Clean display in console without replacing letters with '?'
                print(f"[MIC INPUT]: \"{text_clean}\"")

                # Log to file with timestamp
                try:
                    with open(self.log_file, "a", encoding="utf-8") as f:
                        f.write(f"[{time.strftime('%H:%M:%S')}] {text_clean}\n")
                except Exception:
                    pass

                self.wake_engine.process_speech(text_clean, audio_bytes)
        except Exception as e:
            print(f"[POLL ERROR]: {e}")
        finally:
            self.orb_ui.root.after(30, self.poll_events)

    def run(self):
        """Launches main event loop"""
        self.orb_ui.root.after(100, self.poll_events)
        try:
            self.orb_ui.run()
        except KeyboardInterrupt:
            pass
        finally:
            print(f"[{AI_NAME_ENGLISH}] Systems powering down cleanly...")
            self.voice_listener.stop()

if __name__ == "__main__":
    app = JubayerMasterApp()
    app.run()
