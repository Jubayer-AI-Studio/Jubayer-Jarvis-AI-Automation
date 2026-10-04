"""
=============================================================================
STAGE 05: FILE MANAGER & WORKSPACE CONTROLLER
=============================================================================
কম্পিউটারের ফাইল, ফোল্ডার এবং ড্রাইভ সরাসরি মুখ দিয়ে পরিচালনা:
- ফাইল এক্সপ্লোরার ওপেন (Win + E)
- নির্দিষ্ট ফোল্ডার ওপেন (Downloads, Documents, Desktop, Pictures)
- নতুন ফোল্ডার তৈরি (Ctrl + Shift + N)
- ফাইল ও ফোল্ডারে সার্চ (Ctrl + F)
- রিনেম (F2) ও ডিলিট
- রিসাইকেল বিন খালি করা
=============================================================================
"""

import os
import subprocess
import pyautogui

pyautogui.PAUSE = 0.0
pyautogui.FAILSAFE = False

class FileManagerController:
    def __init__(self):
        self.user_home = os.path.expanduser("~")

    def open_explorer(self, folder_path=None):
        """ফাইল এক্সপ্লোরার বা নির্দিষ্ট ফোল্ডার ওপেন করা"""
        if folder_path and os.path.exists(folder_path):
            subprocess.Popen(f'explorer "{folder_path}"')
            print(f"[STAGE 5] Opened folder: {folder_path}")
        else:
            subprocess.Popen('explorer')
            print("[STAGE 5] Opened File Explorer (This PC)")

    def open_downloads(self):
        """ডাউনলোড ফোল্ডার ওপেন"""
        self.open_explorer(os.path.join(self.user_home, "Downloads"))

    def open_documents(self):
        """ডকুমেন্টস ফোল্ডার ওপেন"""
        self.open_explorer(os.path.join(self.user_home, "Documents"))

    def open_desktop_folder(self):
        """ডেস্কটপ ফোল্ডার ওপেন"""
        self.open_explorer(os.path.join(self.user_home, "Desktop"))

    def open_pictures(self):
        """পিকচার্স ফোল্ডার ওপেন"""
        self.open_explorer(os.path.join(self.user_home, "Pictures"))

    def create_new_folder(self):
        """নতুন ফোল্ডার তৈরি (Ctrl + Shift + N)"""
        pyautogui.hotkey('ctrl', 'shift', 'n')
        print("[STAGE 5] New Folder created")

    def search_files(self, keyword=None):
        """ফাইল এক্সপ্লোরারে সার্চ বক্স ফোকাস (Ctrl + F)"""
        pyautogui.hotkey('ctrl', 'f')
        if keyword:
            import pyperclip
            pyperclip.copy(keyword)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            print(f"[STAGE 5] Searched files for: {keyword}")

    def rename_selected(self):
        """সিলেক্ট করা ফাইল রিনেম (F2)"""
        pyautogui.press('f2')
        print("[STAGE 5] Rename mode activated (F2)")

    def delete_selected(self, permanent=False):
        """ফাইল ডিলিট করা"""
        if permanent:
            pyautogui.hotkey('shift', 'delete')
            print("[STAGE 5] Permanent delete triggered (Shift+Delete)")
        else:
            pyautogui.press('delete')
            print("[STAGE 5] File sent to Recycle Bin")

    def empty_recycle_bin(self):
        """রিসাইকেল বিন খালি করা"""
        try:
            import ctypes
            # SHERB_NOCONFIRMATION = 0x00000001, SHERB_NOPROGRESSUI = 0x00000002, SHERB_NOSOUND = 0x00000004
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 7)
            print("[STAGE 5] Recycle Bin emptied successfully")
            return True
        except Exception as e:
            print(f"[STAGE 5 WARNING] Empty recycle bin error: {e}")
            return False

if __name__ == "__main__":
    fm = FileManagerController()
    print("--- Testing Stage 05 File Manager Controller ---")
    fm.open_downloads()
    print("Test complete.")
