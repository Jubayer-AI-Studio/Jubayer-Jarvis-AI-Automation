"""
=============================================================================
মোবাইল মডিউল: লোকাল ওয়াইফাই রিমোট সার্ভার (MOBILE WIFI REMOTE SERVER)
=============================================================================
আপনার ল্যাপটপ/পিসিতে একটি লোকাল ফ্ল্যাঙ্ক (Flask) ওয়েব সার্ভার চালায়।
মোবাইলের ক্যামেরা দিয়ে পিসির কিউআর কোড স্ক্যান করলেই মোবাইলটি মাউস টাচপ্যাড,
রিমোট মাইক্রোফোন ও কন্ট্রোলারে পরিণত হয়। ১০০% ফ্রি ও লোকাল।
"""

import os
import socket
import threading
import logging
import pyautogui
import qrcode
from flask import Flask, render_template, request, jsonify, send_file

# Flask এর ডিফল্ট টার্মিনাল লগিং শান্ত রাখা
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class MobileRemoteServer:
    def __init__(self, wake_engine, system_controls, port=5000):
        self.wake_engine = wake_engine
        self.system_controls = system_controls
        self.port = port

        # প্রজেক্ট ও টেমপ্লেট ডিরেক্টরি
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.app = Flask(
            __name__,
            template_folder=os.path.join(base_dir, "templates"),
            static_folder=os.path.join(base_dir, "static")
        )

        self.local_ip = self._get_local_ip()
        self.remote_url = f"http://{self.local_ip}:{self.port}"
        self.qr_path = os.path.join(base_dir, "qr_code.png")

        # কিউআর কোড তৈরি
        self._generate_qr()

        # রুটগুলো সেটআপ
        self._setup_routes()

        # সার্ভার থ্রেড
        self.server_thread = None

    def _get_local_ip(self):
        """পিসির লোকাল ওয়াইফাই আইপি বের করা"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

    def _generate_qr(self):
        """মোবাইলে ওপেন করার জন্য কিউআর কোড ইমেজ তৈরি"""
        qr = qrcode.QRCode(box_size=8, border=2)
        qr.add_data(self.remote_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(self.qr_path)

    def _setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('remote.html')

        @self.app.route('/qr')
        def get_qr():
            return send_file(self.qr_path, mimetype='image/png')

        @self.app.route('/api/mouse/move', methods=['POST'])
        def mouse_move():
            data = request.json or {}
            dx = float(data.get('dx', 0))
            dy = float(data.get('dy', 0))
            pyautogui.moveRel(dx, dy)
            return jsonify({'status': 'ok'})

        @self.app.route('/api/mouse/click', methods=['POST'])
        def mouse_click():
            data = request.json or {}
            btn = data.get('button', 'left')
            if btn == 'left':
                self.system_controls.left_click()
            elif btn == 'right':
                self.system_controls.right_click()
            return jsonify({'status': 'ok'})

        @self.app.route('/api/action', methods=['POST'])
        def action_trigger():
            data = request.json or {}
            act = data.get('action', '')
            if act == 'vol_up':
                self.system_controls.volume_up(steps=3)
            elif act == 'vol_down':
                self.system_controls.volume_down(steps=3)
            elif act == 'mute':
                self.system_controls.media_play_pause()
            elif act == 'screenshot':
                self.system_controls.take_screenshot()
            elif act == 'desktop':
                self.system_controls.show_desktop()
            elif act == 'lock':
                self.system_controls.lock_pc()
            elif act == 'shutdown':
                os.system("shutdown /s /t 2")
            elif act == 'browser':
                self.wake_engine.app_launcher.open_browser()
            elif act == 'youtube':
                self.wake_engine.app_launcher.open_youtube()
            return jsonify({'status': 'ok'})

        @self.app.route('/api/command', methods=['POST'])
        def voice_command():
            data = request.json or {}
            cmd = data.get('command', '')
            if cmd:
                self.wake_engine.process_speech(cmd)
            return jsonify({'status': 'ok'})

        @self.app.route('/api/type', methods=['POST'])
        def type_text():
            data = request.json or {}
            txt = data.get('text', '')
            if txt:
                self.wake_engine.voice_typer.type_text(txt)
            return jsonify({'status': 'ok'})

    def start(self):
        """ব্যাকগ্রাউন্ড থ্রেডে সার্ভার চালানো"""
        self.server_thread = threading.Thread(
            target=lambda: self.app.run(host='0.0.0.0', port=self.port, debug=False, use_reloader=False),
            daemon=True
        )
        self.server_thread.start()
        print(f"[MOBILE REMOTE] Server active at: {self.remote_url}")
