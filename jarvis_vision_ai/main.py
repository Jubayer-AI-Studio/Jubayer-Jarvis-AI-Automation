"""
JARVIS-AETHER: Sci-Fi Multimodal AI Desktop Automation System
Main Runtime Orchestrator
Pairs Computer Vision (Hand & Eye Tracking), Multilingual Voice Recognition,
Air Canvas, and an Iron Man Cyberpunk HUD into an ultra-responsive automation suite.
100% Free & Open-Source.
"""

import sys
import time
import cv2
import numpy as np

from config import (
    CAMERA_INDEX,
    CAMERA_WIDTH,
    CAMERA_HEIGHT,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_YELLOW,
    COLOR_WHITE,
    SystemMode,
    VOICE_RESPONSES
)
from core.gesture_engine import GestureEngine
from core.face_eye_engine import FaceEyeEngine
from core.voice_engine import VoiceEngine
from core.action_controller import ActionController
from ui.air_canvas import AirCanvas
from ui.hud_overlay import HudOverlay

class JarvisOrchestrator:
    def __init__(self):
        print("[JARVIS] Initializing core perception subsystems...")

        # Core Engines
        self.gesture_engine = GestureEngine()
        self.face_engine = FaceEyeEngine()
        self.voice_engine = VoiceEngine()
        self.action_controller = ActionController()
        self.air_canvas = AirCanvas(width=CAMERA_WIDTH, height=CAMERA_HEIGHT)
        self.hud = HudOverlay(width=CAMERA_WIDTH, height=CAMERA_HEIGHT)

        # Operational State
        self.current_mode = SystemMode.MOUSE
        self.is_running = True

        # FPS calculation states
        self.prev_frame_time = 0
        self.current_fps = 30.0

        # Mode gesture cycling debounce
        self.last_mode_gesture_time = 0
        self.mode_cycle_cooldown = 1.2

        # Start Voice Engine
        self.voice_engine.start()
        self.voice_engine.speak("Jarvis initialized and operational, sir.")

    def cycle_mode(self):
        """Cycles through operational modes"""
        modes = [
            SystemMode.MOUSE,
            SystemMode.CANVAS,
            SystemMode.PRESENTATION,
            SystemMode.MEDIA
        ]
        curr_idx = modes.index(self.current_mode) if self.current_mode in modes else 0
        self.current_mode = modes[(curr_idx + 1) % len(modes)]
        self.air_canvas.stop_drawing()

        response_map = {
            SystemMode.MOUSE: VOICE_RESPONSES["mouse_mode"],
            SystemMode.CANVAS: VOICE_RESPONSES["canvas_mode"],
            SystemMode.PRESENTATION: VOICE_RESPONSES["present_mode"],
            SystemMode.MEDIA: "Switched to Media and Volume control mode."
        }
        self.voice_engine.speak(response_map.get(self.current_mode, "Mode updated."))
        print(f"[JARVIS] Mode changed to: {self.current_mode}")

    def handle_voice_commands(self):
        """Processes queued multilingual voice commands"""
        cmd = self.voice_engine.get_latest_command()
        if not cmd:
            return

        print(f"[JARVIS] Executing Voice Command: {cmd}")

        if cmd == "open_browser":
            self.action_controller.open_browser()
            self.voice_engine.speak(VOICE_RESPONSES["browser"])

        elif cmd == "open_youtube":
            self.action_controller.open_youtube()
            self.voice_engine.speak(VOICE_RESPONSES["youtube"])

        elif cmd == "open_notes":
            self.action_controller.open_notepad()
            self.voice_engine.speak(VOICE_RESPONSES["notes"])

        elif cmd == "take_screenshot":
            path = self.action_controller.take_screenshot()
            self.voice_engine.speak(VOICE_RESPONSES["screenshot"])
            print(f"[JARVIS] Screenshot saved to: {path}")

        elif cmd == "mode_mouse":
            self.current_mode = SystemMode.MOUSE
            self.air_canvas.stop_drawing()
            self.voice_engine.speak(VOICE_RESPONSES["mouse_mode"])

        elif cmd == "mode_canvas":
            self.current_mode = SystemMode.CANVAS
            self.voice_engine.speak(VOICE_RESPONSES["canvas_mode"])

        elif cmd == "mode_presentation":
            self.current_mode = SystemMode.PRESENTATION
            self.air_canvas.stop_drawing()
            self.voice_engine.speak(VOICE_RESPONSES["present_mode"])

        elif cmd == "clear_canvas":
            self.air_canvas.clear()
            self.voice_engine.speak(VOICE_RESPONSES["clear"])

        elif cmd == "next_slide":
            self.action_controller.next_slide()
            self.voice_engine.speak(VOICE_RESPONSES["next"])

        elif cmd == "prev_slide":
            self.action_controller.prev_slide()
            self.voice_engine.speak(VOICE_RESPONSES["prev"])

        elif cmd == "volume_up":
            self.action_controller.volume_up(steps=4)
            self.voice_engine.speak(VOICE_RESPONSES["volume_up"])

        elif cmd == "volume_down":
            self.action_controller.volume_down(steps=4)
            self.voice_engine.speak(VOICE_RESPONSES["volume_down"])

        elif cmd == "show_desktop":
            self.action_controller.show_desktop()
            self.voice_engine.speak(VOICE_RESPONSES["desktop"])

        elif cmd == "lock_pc":
            self.voice_engine.speak(VOICE_RESPONSES["locked"])
            time.sleep(0.5)
            self.action_controller.lock_workstation()

        elif cmd == "exit_system":
            self.voice_engine.speak("Shutting down Jarvis systems. Goodbye, sir.")
            time.sleep(1.0)
            self.is_running = False

    def run(self):
        """Primary real-time execution loop"""
        cap = cv2.VideoCapture(CAMERA_INDEX)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

        camera_opened = cap.isOpened()
        if not camera_opened:
            print(f"[JARVIS WARNING] Camera index {CAMERA_INDEX} not accessible.")
            print("[JARVIS] Entering simulation / standby mode.")

        cv2.namedWindow("JARVIS-AETHER // MULTIMODAL AUTOMATION", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("JARVIS-AETHER // MULTIMODAL AUTOMATION", CAMERA_WIDTH, CAMERA_HEIGHT)

        print("\n=======================================================")
        print("   JARVIS-AETHER SYSTEM ONLINE (100% FREE)")
        print("   Keybindings:")
        print("     [M]   Cycle Active Mode (Mouse, Canvas, Slides, Media)")
        print("     [C]   Cycle Drawing Colors in Canvas Mode")
        print("     [E]   Erase / Clear Canvas")
        print("     [L]   Cycle Voice Language (English, বাংলা, اردو, العربية)")
        print("     [S]   Take Timestamped Screenshot")
        print("     [Esc] or [Q] Quit Application")
        print("=======================================================\n")

        volume_display_pct = None

        while self.is_running:
            start_time = time.time()

            if camera_opened:
                ret, frame = cap.read()
                if not ret:
                    time.sleep(0.03)
                    continue
            else:
                # Standby synthetic frame if physical camera is offline
                frame = np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH, 3), dtype=np.uint8)
                cv2.putText(frame, "STANDBY MODE: CAMERA OFFLINE", (CAMERA_WIDTH // 2 - 250, CAMERA_HEIGHT // 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, COLOR_CYAN, 2)

            # Mirror webcam feed horizontally for natural interaction
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 1. Process Face & Eye Telemetry
            face_telemetry = self.face_engine.process_frame(frame_rgb, frame.shape)
            if face_telemetry.get("just_arrived"):
                self.voice_engine.speak(VOICE_RESPONSES["welcome_boss"])

            # 2. Process Voice Commands
            self.handle_voice_commands()

            # 3. Process Hand Gestures
            hand_results = self.gesture_engine.process_frame(frame_rgb)
            lm_list, handedness = self.gesture_engine.extract_landmarks(hand_results, frame.shape)

            is_pinched = False
            volume_display_pct = None

            if lm_list:
                fingers = self.gesture_engine.get_fingers_up(lm_list, handedness)
                num_fingers = sum(fingers)
                is_pinched, pinch_dist = self.gesture_engine.detect_pinch(lm_list)
                is_right_pinch, _ = self.gesture_engine.detect_right_pinch(lm_list)

                # Index fingertip coordinates
                idx_x, idx_y = lm_list[8][0], lm_list[8][1]

                # Check 3-finger gesture for Mode Cycling
                if fingers[1] and fingers[2] and fingers[3] and not fingers[0] and not fingers[4]:
                    if time.time() - self.last_mode_gesture_time > self.mode_cycle_cooldown:
                        self.cycle_mode()
                        self.last_mode_gesture_time = time.time()

                # --- MODE 1: AIR MOUSE ---
                if self.current_mode == SystemMode.MOUSE:
                    self.air_canvas.stop_drawing()

                    # Cursor Movement: Index finger is raised
                    if fingers[1]:
                        sx, sy = self.gesture_engine.get_smoothed_cursor(idx_x, idx_y, w, h)
                        self.action_controller.move_mouse(sx, sy)

                    # Left Click & Drag: Pinch thumb + index
                    if is_pinched:
                        self.action_controller.left_click()

                    # Right Click: Pinch thumb + middle
                    elif is_right_pinch:
                        self.action_controller.right_click()

                    # Page Scroll: Both Index and Middle fingers up
                    if fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
                        # Scroll based on vertical position
                        if idx_y < h * 0.35:
                            self.action_controller.scroll_page("UP", amount=70)
                        elif idx_y > h * 0.65:
                            self.action_controller.scroll_page("DOWN", amount=70)

                # --- MODE 2: AIR CANVAS ---
                elif self.current_mode == SystemMode.CANVAS:
                    # Drawing mode: Only Index finger up (Middle finger folded)
                    if fingers[1] and not fingers[2] and not fingers[3] and not fingers[4]:
                        # Check if finger is hovering over top color palette bar
                        if idx_y < 65:
                            self.air_canvas.stop_drawing()
                            bar_w = 60
                            start_x = w // 2 - (len(self.air_canvas.CANVAS_COLORS if hasattr(self.air_canvas, 'CANVAS_COLORS') else [0]*5) * (bar_w + 10)) // 2
                            # Check touch on palette
                            idx_color = (idx_x - (w // 2 - 175)) // 70
                            if 0 <= idx_color < 5:
                                self.air_canvas.color_index = idx_color
                        else:
                            self.air_canvas.draw_point(idx_x, idx_y)

                    # Laser Pointer / Hover: Both Index & Middle fingers up
                    elif fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
                        self.air_canvas.stop_drawing()
                        self.air_canvas.update_laser_pointer(frame, idx_x, idx_y)

                    # Eraser: Closed fist or open palm
                    elif num_fingers == 0:
                        self.air_canvas.clear()
                    else:
                        self.air_canvas.stop_drawing()

                # --- MODE 3: PRESENTATION COPILOT ---
                elif self.current_mode == SystemMode.PRESENTATION:
                    self.air_canvas.stop_drawing()

                    # Laser pointer overlay on presentation
                    if fingers[1]:
                        self.air_canvas.update_laser_pointer(frame, idx_x, idx_y)

                    # Slide navigation via hand swipe
                    swipe_dir = self.gesture_engine.detect_swipe(lm_list)
                    if swipe_dir == "NEXT":
                        self.action_controller.next_slide()
                        cv2.putText(frame, ">> NEXT SLIDE >>", (w // 2 - 120, h // 2),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, COLOR_GREEN, 3)
                    elif swipe_dir == "PREV":
                        self.action_controller.prev_slide()
                        cv2.putText(frame, "<< PREV SLIDE <<", (w // 2 - 120, h // 2),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, COLOR_YELLOW, 3)

                # --- MODE 4: MEDIA & VOLUME CONTROL ---
                elif self.current_mode == SystemMode.MEDIA:
                    self.air_canvas.stop_drawing()

                    # Continuous volume slider via thumb-index distance
                    vol_pct = self.gesture_engine.get_volume_percentage(lm_list)
                    if vol_pct is not None:
                        volume_display_pct = vol_pct
                        # Relative volume steps
                        if vol_pct > 65:
                            self.action_controller.volume_up(steps=1)
                        elif vol_pct < 35:
                            self.action_controller.volume_down(steps=1)

                    # Media Play/Pause toggle on Open Palm
                    if num_fingers == 5:
                        if time.time() - self.action_controller.last_click_time > 1.0:
                            self.action_controller.media_play_pause()
                            self.action_controller.last_click_time = time.time()

                # Draw glowing cybernetic hand skeleton
                self.hud.draw_cyber_hand(frame, lm_list, is_pinched=is_pinched)

            else:
                self.air_canvas.stop_drawing()

            # 4. Blend Air Canvas Drawings onto Frame
            frame = self.air_canvas.blend_onto_frame(frame)

            # 5. Render HUD Elements & Visualizers
            self.hud.draw_face_reticle(frame, face_telemetry)

            if volume_display_pct is not None:
                self.hud.draw_volume_meter(frame, volume_display_pct)

            if self.current_mode == SystemMode.CANVAS:
                self.air_canvas.render_palette_bar(frame)

            self.hud.render_hud_telemetry(frame, self.current_mode, self.current_fps, self.voice_engine, face_telemetry)

            # Calculate actual FPS
            frame_duration = time.time() - start_time
            if frame_duration > 0:
                self.current_fps = 0.9 * self.current_fps + 0.1 * (1.0 / frame_duration)

            # Display composite visual output
            cv2.imshow("JARVIS-AETHER // MULTIMODAL AUTOMATION", frame)

            # Handle Keyboard Hotkeys
            key = cv2.waitKey(1) & 0xFF
            if key in [27, ord('q'), ord('Q')]:  # Esc or Q
                print("[JARVIS] Exit signal received.")
                break
            elif key in [ord('m'), ord('M')]:
                self.cycle_mode()
            elif key in [ord('c'), ord('C')]:
                color_bgr, color_name = self.air_canvas.cycle_color()
                self.voice_engine.speak(f"{color_name} brush selected.")
            elif key in [ord('e'), ord('E')]:
                self.air_canvas.clear()
                self.voice_engine.speak("Canvas cleared.")
            elif key in [ord('l'), ord('L')]:
                self.voice_engine.cycle_language()
            elif key in [ord('s'), ord('S')]:
                path = self.action_controller.take_screenshot()
                self.voice_engine.speak(VOICE_RESPONSES["screenshot"])
                print(f"[JARVIS] Screenshot captured: {path}")

        # Cleanup
        print("[JARVIS] Releasing resources...")
        self.voice_engine.stop()
        if camera_opened:
            cap.release()
        cv2.destroyAllWindows()
        print("[JARVIS] Shutdown complete.")

if __name__ == "__main__":
    app = JarvisOrchestrator()
    app.run()
