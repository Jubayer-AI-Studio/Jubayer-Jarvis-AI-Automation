"""
=============================================================================
সিকিউরিটি মডিউল: অডিও ভয়েস লক (VOICE BIOMETRIC LOCK)
=============================================================================
মাইক্রোফোনের সাহায্যে মালিকের গলার ইউনিক কম্পাঙ্ক ও ফ্রিকোয়েন্সি (Acoustic Print)
শনাক্ত করে যাতে মালিক ছাড়া অন্য কারো গলার শব্দে পিসি কন্ট্রোল না হয়।
১০০% ফ্রি - কোনো ক্যামেরা বা পেইড API লাগে না। ব্যাকআপ পিন সমর্থন করে।
"""

import os
import json
import numpy as np
from config import BACKUP_PIN, VOICE_LOCK_ENABLED

class VoiceLock:
    def __init__(self, profile_path=None):
        if profile_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            profile_path = os.path.join(base_dir, "voice_profile.json")

        self.profile_path = profile_path
        self.owner_features = None
        self.similarity_threshold = 0.68  # ০.৬৮ এর বেশি মিললে মালিক হিসেবে গণ্য হবে
        self.enrollment_samples = []

        self.load_profile()

    def extract_features(self, audio_data_bytes):
        """
        অডিও বাইট ডাটা থেকে মানুষের কণ্ঠনালীর ১৬টি ফ্রিকোয়েন্সি ব্যান্ডের
        ইউনিক স্পেকট্রাম ফিচার এক্সট্র্যাক্ট করে।
        """
        try:
            samples = np.frombuffer(audio_data_bytes, dtype=np.int16).astype(np.float32)
            if len(samples) < 1024:
                return None

            # নর্মালাইজেশন
            samples = samples / (np.max(np.abs(samples)) + 1e-6)

            # ফাস্ট ফুরিয়ার ট্রান্সফর্ম (FFT) স্পেকট্রাম
            fft_data = np.abs(np.fft.rfft(samples))
            num_bins = len(fft_data)
            if num_bins < 16:
                return None

            # ১৬টি সাব-ব্যান্ডে ভাগ করে এনার্জি স্পেকট্রাম হিসাব করা
            band_size = num_bins // 16
            features = []
            for i in range(16):
                band_energy = np.mean(fft_data[i * band_size : (i + 1) * band_size])
                features.append(float(band_energy))

            features = np.array(features, dtype=np.float32)
            norm = np.linalg.norm(features)
            if norm > 0:
                features = features / norm
            return features.tolist()
        except Exception as e:
            print(f"[ভয়েস লক ফিচার ত্রুটি]: {e}")
            return None

    def enroll_sample(self, audio_data_bytes):
        """সেটআপের সময় মালিকের কণ্ঠের নমুনা সেভ করা"""
        feat = self.extract_features(audio_data_bytes)
        if feat:
            self.enrollment_samples.append(feat)
            if len(self.enrollment_samples) >= 3:
                # ৩টি নমুনার গড় নিয়ে চূড়ান্ত প্রোফাইল তৈরি
                avg_feat = np.mean(self.enrollment_samples, axis=0)
                norm = np.linalg.norm(avg_feat)
                if norm > 0:
                    avg_feat = avg_feat / norm
                self.owner_features = avg_feat.tolist()
                self.save_profile()
                self.enrollment_samples.clear()
                return True
        return False

    def is_owner(self, audio_data_bytes, spoken_text=""):
        """
        যাচাই করে যে কথা বলা ব্যক্তি আসল মালিক কিনা।
        যদি ভয়েস লক বন্ধ থাকে বা প্রোফাইল না থাকে তবে সত্য রিটার্ন করে।
        """
        if not VOICE_LOCK_ENABLED:
            return True

        # ব্যাকআপ পিন দিয়ে তাৎক্ষণিক আনলক যাচাই
        if BACKUP_PIN and BACKUP_PIN in spoken_text:
            print("[VOICE LOCK] Unlocked with emergency backup PIN.")
            return True

        # Pass by default if no profile is saved yet
        if not self.owner_features:
            return True

        current_feat = self.extract_features(audio_data_bytes)
        if current_feat is None:
            return True

        # Cosine similarity for speaker verification
        v1 = np.array(self.owner_features, dtype=np.float32)
        v2 = np.array(current_feat, dtype=np.float32)

        dot = np.dot(v1, v2)
        similarity = float(dot)
        print(f"[VOICE LOCK] Speaker similarity: {similarity:.2f} (Required: {self.similarity_threshold})")

        return similarity >= self.similarity_threshold

    def save_profile(self):
        try:
            with open(self.profile_path, "w", encoding="utf-8") as f:
                json.dump({"features": self.owner_features}, f, indent=2)
            print("[VOICE LOCK] Voice profile saved successfully.")
        except Exception as e:
            print(f"[VOICE LOCK SAVE ERROR]: {e}")

    def load_profile(self):
        if os.path.exists(self.profile_path):
            try:
                with open(self.profile_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.owner_features = data.get("features")
                print("[VOICE LOCK] Saved owner voice profile loaded.")
            except Exception:
                self.owner_features = None
