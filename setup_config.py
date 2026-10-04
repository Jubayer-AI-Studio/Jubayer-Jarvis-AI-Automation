"""
Helper script used by INSTALL.bat to write user-selected AI name and PIN into config.py cleanly.
"""

import sys
import re
import os

def update_config(ai_name, ai_pin):
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")
    if not os.path.exists(config_path):
        print(f"[ERROR] config.py not found at {config_path}")
        return

    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()

    # AI_NAME আপডেট
    content = re.sub(r'AI_NAME\s*=\s*["\'].*?["\']', f'AI_NAME = "{ai_name}"', content)
    content = re.sub(r'AI_NAME_ENGLISH\s*=\s*["\'].*?["\']', f'AI_NAME_ENGLISH = "{ai_name}"', content)
    
    # BACKUP_PIN আপডেট
    content = re.sub(r'BACKUP_PIN\s*=\s*["\'].*?["\']', f'BACKUP_PIN = "{ai_pin}"', content)

    with open(config_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] কনফিগারেশন আপডেট হয়েছে: AI নাম = '{ai_name}', ব্যাকআপ পিন = '{ai_pin}'")

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else "জুবায়ের"
    pin = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].strip() else "1234"
    update_config(name, pin)
