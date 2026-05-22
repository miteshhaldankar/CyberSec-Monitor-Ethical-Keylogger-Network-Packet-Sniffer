# 🛡️ CyberSec Monitor — Ethical Keylogger + Network Packet Sniffer

**Author:** Mitesh Pravin Haldankar  
**Type:** Cybersecurity Portfolio Project  
**Stack:** Python 3, pynput, socket, struct  

> ⚠️ **DISCLAIMER:** This tool is for **educational and authorized use ONLY.**  
> Use exclusively on systems and networks **you own** or have **written permission** to test.  
> Unauthorized use is illegal under the IT Act 2000 (India) and international law.

---

## 📌 Project Overview

A combined security monitoring toolkit demonstrating:
- **Keystroke capture** — how keyloggers work and why they're a threat vector
- **Packet sniffing** — how network traffic is captured and analyzed at the protocol level
- **Multi-threaded execution** — running both tools simultaneously
- **Session reporting** — auto-generated HTML reports for analysis

---

## 🔧 Modules

| Module | Description |
|---|---|
| `keylogger.py` | Captures keystrokes, classifies special keys, buffers & logs |
| `packet_sniffer.py` | Raw socket capture, parses Ethernet/IP/TCP/UDP/ICMP layers |
| `main.py` | Interactive menu launcher with consent gate |

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install pynput
```

### 2. Run the main tool
```bash
# Keylogger only
python3 main.py

# Packet sniffer (requires root on Linux)
sudo python3 main.py
```

### 3. View report
Select option `[4]` from the menu to generate an HTML report.

---

## 🧠 What I Learned / Skills Demonstrated

- TCP/IP stack — parsing raw Ethernet, IP, TCP, UDP, ICMP headers manually using `struct`
- Socket programming — `AF_PACKET` raw sockets for low-level network access
- Multi-threading — concurrent keylogger + sniffer using `threading.Thread`
- Input handling — keyboard event listeners using `pynput`
- Security mindset — understanding attacker techniques to build better defenses
- Ethical hacking — consent-first design, disclaimer enforcement
- Report generation — automated HTML output for documentation

---

## 🔒 Security Concepts Covered

- **Defense use case:** Detect unauthorized keyloggers on endpoints
- **Network monitoring:** Baseline normal traffic; spot anomalies (port scans, ICMP floods)
- **Attack awareness:** Understanding how data exfiltration via keyloggers works
- **Protocol analysis:** Deep packet inspection concepts (Wireshark does this at scale)

---

## 📁 Output Files

| File | Contents |
|---|---|
| `keylog_output.txt` | Captured keystrokes with timestamps |
| `packet_log.txt` | Captured packets with protocol breakdown |
| `cybersec_report_*.html` | Combined HTML session report |

---

## 🎯 Resume Keywords This Project Covers

`Penetration Testing` · `Network Security` · `Packet Analysis` · `TCP/IP` · `Python Scripting`  
`Socket Programming` · `Ethical Hacking` · `IDS/IPS Concepts` · `Wireshark` · `Cybersecurity`  
`OWASP` · `Threat Analysis` · `Security Monitoring` · `Linux` · `Multi-threading`
