from scapy.all import sniff, IP, TCP, UDP, Raw
from collections import defaultdict
import time 

# Part 4
protocol_count = defaultdict(int)

def packet_callback(packet):
    if packet.haslayer(IP):
        # Part 2
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = "Other"
        src_port = "-"
        dst_port = "-"
        
        # Part 2
        p_time = time.strftime('%H:%M:%S', time.localtime(packet.time))
        p_len = len(packet)
        tcp_flags = ""

        # Part 2
        if packet.haslayer(TCP):
            protocol = "TCP"
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            tcp_flags = f" | Flags: {packet[TCP].flags}" 
        elif packet.haslayer(UDP):
            protocol = "UDP"
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport

        protocol_count[protocol] += 1
        
        # Part 4
        print(f"[{p_time}] [{protocol}] {src_ip}:{src_port} --> {dst_ip}:{dst_port} | Len: {p_len}{tcp_flags}")

        # Part 3
        if packet.haslayer(Raw):
            try:
                payload = packet[Raw].load.decode(errors="ignore")
                sensitive_keys = ["user", "pass", "login", "set-cookie", "pwd"]
                if any(word in payload.lower() for word in sensitive_keys):
                    print("ALERT: Sensitive Data Detected")
                    print(f"Payload Snippet: {payload[:50]}")
            except:
                pass

print("Starting Live Packet Capture")

# Part 1
sniff(filter="ip and (tcp or udp)", count=50, prn=packet_callback)

print("\nSniffing Complete")
for proto, count in protocol_count.items():
    print(f"Total {proto} packets: {count}")
