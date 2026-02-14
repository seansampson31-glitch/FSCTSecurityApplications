from scapy.all import sniff, IP, TCP, UDP, Raw, PcapReader
from collections import defaultdict, deque

THRESHOLD = 20
WINDOW_SIZE = 5  
PCAP_PATH = r"botnet-capture-20110812-rbot.pcap"

tcp_count = 0
udp_count = 0
ip_windows = defaultdict(deque)
suspicious_ips = set()

print(f"Opening PCAP file: {PCAP_PATH}...")

try:
    with PcapReader(PCAP_PATH) as pcap:
        print("Processing packets\n")

        for packet in pcap:
            if packet.haslayer(IP):
                src_ip = packet[IP].src
                timestamp = packet.time

                if packet.haslayer(TCP):
                    tcp_count += 1
                elif packet.haslayer(UDP):
                    udp_count += 1

                # 5 second window
                ip_windows[src_ip].append(timestamp)
                while ip_windows[src_ip] and timestamp - ip_windows[src_ip][0] > WINDOW_SIZE:
                    ip_windows[src_ip].popleft()

                # 20 packets max
                if len(ip_windows[src_ip]) > THRESHOLD:
                    if src_ip not in suspicious_ips: # Makes sure not to get duplicates
                        print(f"ALERT: Possible flooding detected from {src_ip}")
                        suspicious_ips.add(src_ip)

    print("\nAnalysis Complete")
    print(f"Total TCP Packets: {tcp_count}")
    print(f"Total UDP Packets: {udp_count}")
    print(f"Suspicious IPs Detected: {len(suspicious_ips)}")

except FileNotFoundError:
    print(f"Error: PCAP file not found at {PCAP_PATH}")
