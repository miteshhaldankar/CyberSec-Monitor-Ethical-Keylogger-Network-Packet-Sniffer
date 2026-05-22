"""
=============================================================
  Network Packet Sniffer Module
  Author : Mitesh Pravin Haldankar
  Purpose: Educational / Portfolio Demonstration ONLY
           Run with sudo on your OWN network interface.
=============================================================
"""

import sys
import time
import socket
import struct
import textwrap
import threading
from datetime import datetime
from collections import defaultdict

# ── ANSI colour codes ─────────────────────────────────────
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

LOG_FILE = "packet_log.txt"

PROTOCOL_MAP = {1: "ICMP", 6: "TCP", 17: "UDP"}

class PacketSniffer:
    """
    Captures raw network packets on the local interface.
    Parses Ethernet → IP → TCP/UDP/ICMP layers.
    Logs summary and raw data to file.
    """

    def __init__(self, log_file: str = LOG_FILE, max_packets: int = 100):
        self.log_file = log_file
        self.max_packets = max_packets
        self.packet_count = 0
        self.stats = defaultdict(int)
        self.running = False
        self.lock = threading.Lock()
        self.start_time = datetime.now()

    # ── Parsers ───────────────────────────────────────────

    def parse_ethernet(self, raw):
        """Parse Ethernet II frame header (14 bytes)."""
        dest_mac, src_mac, proto = struct.unpack("! 6s 6s H", raw[:14])
        return self._format_mac(dest_mac), self._format_mac(src_mac), socket.htons(proto), raw[14:]

    def parse_ipv4(self, data):
        """Parse IPv4 header."""
        version_ihl = data[0]
        ihl = (version_ihl & 0xF) * 4  # header length in bytes
        ttl, proto, src, target = struct.unpack("! 8x B B 2x 4s 4s", data[:20])
        src_ip = socket.inet_ntoa(src)
        dst_ip = socket.inet_ntoa(target)
        return proto, ttl, src_ip, dst_ip, data[ihl:]

    def parse_tcp(self, data):
        """Parse TCP segment."""
        src_port, dst_port, seq, ack, offset_flags = struct.unpack("! H H L L H", data[:14])
        offset = (offset_flags >> 12) * 4
        flags = {
            "URG": bool(offset_flags & 0x20),
            "ACK": bool(offset_flags & 0x10),
            "PSH": bool(offset_flags & 0x08),
            "RST": bool(offset_flags & 0x04),
            "SYN": bool(offset_flags & 0x02),
            "FIN": bool(offset_flags & 0x01),
        }
        active_flags = [f for f, v in flags.items() if v]
        return src_port, dst_port, seq, ack, active_flags, data[offset:]

    def parse_udp(self, data):
        """Parse UDP datagram."""
        src_port, dst_port, length = struct.unpack("! H H 2x H", data[:8])
        return src_port, dst_port, length, data[8:]

    def parse_icmp(self, data):
        """Parse ICMP message."""
        icmp_type, code, checksum = struct.unpack("! B B H", data[:4])
        return icmp_type, code, checksum, data[4:]

    def _format_mac(self, raw_mac) -> str:
        return ":".join(f"{b:02x}" for b in raw_mac)

    def _format_payload(self, data, indent=2) -> str:
        if not data:
            return ""
        try:
            decoded = data.decode("utf-8", errors="replace")
            printable = "".join(c if c.isprintable() else "." for c in decoded)
            lines = textwrap.wrap(printable, 60)
            pad = " " * indent
            return "\n".join(f"{pad}{l}" for l in lines[:5])  # max 5 lines
        except Exception:
            return " " * indent + repr(data[:60])

    # ── Logging ───────────────────────────────────────────

    def _log(self, message: str):
        """Print to console AND write to log file."""
        print(message)
        with self.lock:
            with open(self.log_file, "a") as f:
                f.write(message.replace(RED,"").replace(GREEN,"")
                        .replace(YELLOW,"").replace(CYAN,"")
                        .replace(BOLD,"").replace(RESET,"") + "\n")

    def _print_header(self):
        header = (
            f"\n{'='*65}\n"
            f"  {BOLD}NETWORK PACKET SNIFFER{RESET} — Educational Use Only\n"
            f"  Started : {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"  Max     : {self.max_packets} packets\n"
            f"  Log     : {self.log_file}\n"
            f"{'='*65}\n"
        )
        self._log(header)

    def _print_summary(self):
        duration = datetime.now() - self.start_time
        summary = (
            f"\n{'='*65}\n"
            f"  CAPTURE SUMMARY\n"
            f"  Duration : {str(duration).split('.')[0]}\n"
            f"  Total    : {self.packet_count} packets\n"
            f"  TCP      : {self.stats['TCP']}\n"
            f"  UDP      : {self.stats['UDP']}\n"
            f"  ICMP     : {self.stats['ICMP']}\n"
            f"  Other    : {self.stats['OTHER']}\n"
            f"{'='*65}\n"
        )
        self._log(summary)

    # ── Core sniff loop ───────────────────────────────────

    def sniff(self):
        """Main packet capture loop using raw socket."""
        try:
            # AF_PACKET works on Linux; use SOCK_RAW
            conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        except PermissionError:
            print(f"{RED}[!] Permission denied. Run with: sudo python3 packet_sniffer.py{RESET}")
            sys.exit(1)
        except AttributeError:
            print(f"{RED}[!] AF_PACKET not supported on this OS (Linux required for raw sockets).{RESET}")
            print(f"[*] On Windows use Scapy: scapy.sniff(prn=...) instead.")
            sys.exit(1)

        self.running = True
        self._print_header()
        print(f"{GREEN}[*] Sniffing started. Ctrl+C to stop early.{RESET}\n")

        try:
            while self.running and self.packet_count < self.max_packets:
                raw_data, addr = conn.recvfrom(65535)
                self._process_packet(raw_data)
        except KeyboardInterrupt:
            print(f"\n{YELLOW}[!] Interrupted by user.{RESET}")
        finally:
            conn.close()
            self._print_summary()

    def _process_packet(self, raw_data):
        self.packet_count += 1
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]

        try:
            dest_mac, src_mac, eth_proto, data = self.parse_ethernet(raw_data)
        except Exception:
            return

        # Only process IPv4 (proto 8)
        if eth_proto != 8:
            self.stats["OTHER"] += 1
            return

        try:
            proto_num, ttl, src_ip, dst_ip, payload = self.parse_ipv4(data)
        except Exception:
            return

        proto_name = PROTOCOL_MAP.get(proto_num, "OTHER")
        self.stats[proto_name] += 1

        # ── TCP ──
        if proto_num == 6:
            try:
                s_port, d_port, seq, ack, flags, tcp_payload = self.parse_tcp(payload)
                flags_str = ",".join(flags) if flags else "—"
                msg = (
                    f"{CYAN}[#{self.packet_count:04d}]{RESET} {ts} | "
                    f"{BOLD}TCP{RESET} | "
                    f"{GREEN}{src_ip}:{s_port}{RESET} → {RED}{dst_ip}:{d_port}{RESET} | "
                    f"Flags:[{YELLOW}{flags_str}{RESET}] TTL:{ttl}"
                )
                self._log(msg)
                if tcp_payload:
                    payload_str = self._format_payload(tcp_payload)
                    if payload_str.strip():
                        self._log(f"  Payload:\n{payload_str}")
            except Exception:
                pass

        # ── UDP ──
        elif proto_num == 17:
            try:
                s_port, d_port, length, udp_payload = self.parse_udp(payload)
                msg = (
                    f"{CYAN}[#{self.packet_count:04d}]{RESET} {ts} | "
                    f"{BOLD}UDP{RESET} | "
                    f"{GREEN}{src_ip}:{s_port}{RESET} → {RED}{dst_ip}:{d_port}{RESET} | "
                    f"Len:{length} TTL:{ttl}"
                )
                self._log(msg)
            except Exception:
                pass

        # ── ICMP ──
        elif proto_num == 1:
            try:
                icmp_type, code, checksum, _ = self.parse_icmp(payload)
                type_map = {0: "Echo Reply", 8: "Echo Request", 3: "Dest Unreachable",
                            11: "Time Exceeded", 5: "Redirect"}
                type_str = type_map.get(icmp_type, f"Type-{icmp_type}")
                msg = (
                    f"{CYAN}[#{self.packet_count:04d}]{RESET} {ts} | "
                    f"{BOLD}ICMP{RESET} | "
                    f"{GREEN}{src_ip}{RESET} → {RED}{dst_ip}{RESET} | "
                    f"{YELLOW}{type_str}{RESET} (Code:{code}) TTL:{ttl}"
                )
                self._log(msg)
            except Exception:
                pass


if __name__ == "__main__":
    print("=" * 65)
    print("  NETWORK PACKET SNIFFER — EDUCATIONAL USE ONLY")
    print("  Capture packets on YOUR OWN network ONLY.")
    print("=" * 65)
    confirm = input("\n  Type 'AGREE' to confirm you own/authorise this network: ")
    if confirm.strip().upper() != "AGREE":
        print("[!] Consent not given. Exiting.")
        sys.exit(0)

    try:
        max_p = int(input("  Max packets to capture [default 50]: ").strip() or 50)
    except ValueError:
        max_p = 50

    sniffer = PacketSniffer(max_packets=max_p)
    sniffer.sniff()
