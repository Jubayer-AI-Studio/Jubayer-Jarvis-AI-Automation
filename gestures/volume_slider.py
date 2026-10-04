"""
=============================================================================
জেসচার মডিউল: ভলিউম স্লাইডার (VOLUME SLIDER)
=============================================================================
বুড়ো আঙুল ও তর্জনীর মধ্যকার ফাঁক মেপে সিস্টেমের সাউন্ড ০% থেকে ১০০% নিয়ন্ত্রণ।
"""

import math
import numpy as np
from config import VOLUME_MIN_DIST, VOLUME_MAX_DIST

class VolumeSlider:
    def calculate_distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def get_volume_percentage(self, lm_list):
        """আঙুলের দূরত্ব অনুযায়ী ভলিউমের শতকরা হার (০-১০০%) নির্ণয় করে"""
        if not lm_list or len(lm_list) < 21:
            return None
        dist = self.calculate_distance(lm_list[4], lm_list[8])
        vol_pct = np.interp(dist, [VOLUME_MIN_DIST, VOLUME_MAX_DIST], [0, 100])
        return int(np.clip(vol_pct, 0, 100))
