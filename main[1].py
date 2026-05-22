"""
=============================================================
  CyberSec Monitor — Combined Tool
  Author : Mitesh Pravin Haldankar
  GitHub : github.com/miteshhaldankar   (add your profile)
  
  Modules:
    1. Ethical Keylogger
    2. Network Packet Sniffer
    3. Combined Session Report
=============================================================
  DISCLAIMER: For EDUCATIONAL & AUTHORIZED use ONLY.
  Use only on systems/networks you OWN or have written
  permission to test. Unauthorized use is ILLEGAL.
=============================================================
"""

import os
import sys
import time
import threading
from datetime import datetime

from keylogger import EthicalKeylogger
from packet_sniffer import PacketSniffer

BANNER = r"""
  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███████╗ ██████╗
 ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝
 ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗█████╗  ██║     
 ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║     
 ╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║███████╗╚██████╗
  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝
         MONITOR  —  Ethical Security Toolkit  —  v1.0
         Author: Mitesh Pravin Haldankar | Educational Use Only
"""

MENU = """
  ┌─────────────────────────────────────────────┐
  │  Select Mode                                │
  │  [1]  Ethical Keylogger only               │
  │  [2]  Network Packet Sniffer only          │
  │  [3]  Combined (both simultaneously)       │
  │  [4]  Generate Session Report              │
  │  [0]  Exit                                 │
  └─────────────────────────────────────────────┘
"""

def get_consent(tool_name: str) -> bool:
    print(f"\n  ⚠️  You are about to run: {tool_name}")
    print("  This tool must ONLY be used on systems/networks you OWN.")
    ans = input("  Type 'AGREE' to confirm: ").strip().upper()
    return ans == "AGREE"

def run_keylogger():
    if not get_consent("Ethical Keylogger"):
        print("[!] Consent not given."); return
    logger = EthicalKeylogger()
    logger.start()

def run_sniffer():
    if not get_consent("Network Packet Sniffer"):
        print("[!] Consent not given."); return
    try:
        n = int(input("  Max packets [default 50]: ").strip() or 50)
    except ValueError:
        n = 50
    sniffer = PacketSniffer(max_packets=n)
    sniffer.sniff()

def run_combined():
    if not get_consent("Combined Keylogger + Packet Sniffer"):
        print("[!] Consent not given."); return
    print("\n[*] Starting both tools in parallel threads...")
    print("[*] Press ESC in the keylogger window to stop both.\n")
    time.sleep(1)

    logger  = EthicalKeylogger()
    sniffer = PacketSniffer(max_packets=30)

    t1 = threading.Thread(target=logger.start,  daemon=True)
    t2 = threading.Thread(target=sniffer.sniff, daemon=True)

    t2.start()
    t1.start()  # blocking — ESC stops it
    t1.join()
    print("[*] Keylogger stopped. Waiting for sniffer to finish...")
    t2.join(timeout=5)
    print("[+] Combined session complete.")

def generate_report():
    """Merge keylog and packet log into one HTML report."""
    report_file = f"cybersec_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    def read_safe(fname):
        try:
            with open(fname) as f:
                return f.read()
        except FileNotFoundError:
            return "(No data captured yet — run the tool first)"

    keylog_data   = read_safe("keylog_output.txt")
    packet_data   = read_safe("packet_log.txt")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CyberSec Monitor — Session Report</title>
<style>
  body {{ font-family: 'Courier New', monospace; background: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; }}
  h1   {{ color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; }}
  h2   {{ color: #3fb950; margin-top: 30px; }}
  pre  {{ background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 6px;
          overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; font-size: 13px; }}
  .meta {{ color: #8b949e; font-size: 13px; margin-bottom: 20px; }}
  .badge {{ display:inline-block; background:#21262d; border:1px solid #30363d;
            padding: 2px 10px; border-radius: 12px; font-size: 12px; color: #f78166; }}
</style>
</head>
<body>
<h1>🛡️ CyberSec Monitor — Session Report</h1>
<p class="meta">
  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
  Author    : Mitesh Pravin Haldankar<br>
  <span class="badge">EDUCATIONAL USE ONLY</span>
</p>

<h2>📋 Keylogger Output</h2>
<pre>{keylog_data}</pre>

<h2>🌐 Packet Sniffer Output</h2>
<pre>{packet_data}</pre>

<h2>📊 Analysis Notes</h2>
<pre>
- Review keylog for any sensitive data patterns (passwords, personal info)
- Review packet capture for unusual ports, IPs, or protocols
- TCP SYN packets without ACK may indicate port scanning activity
- ICMP echo requests indicate ping activity on the network
- UDP traffic on port 53 = DNS queries
</pre>
</body>
</html>"""

    with open(report_file, "w") as f:
        f.write(html)
    print(f"\n[+] Report generated: {report_file}")
    print(f"[+] Open in your browser to view.")

def main():
    print(BANNER)
    while True:
        print(MENU)
        choice = input("  Enter choice: ").strip()
        if   choice == "1": run_keylogger()
        elif choice == "2": run_sniffer()
        elif choice == "3": run_combined()
        elif choice == "4": generate_report()
        elif choice == "0": print("\n  Goodbye.\n"); sys.exit(0)
        else: print("[!] Invalid choice.")

if __name__ == "__main__":
    main()
