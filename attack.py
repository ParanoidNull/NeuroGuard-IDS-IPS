from scapy.all import IP, TCP, send, RandShort
import time
import sys

# Configuration
TARGET_IP = "8.8.8.8" # External IP to force routing through the interface
TARGET_PORT = 666     # Flagged port for IDS detection
PACKET_COUNT = 20

print(f"\n[+] Starting TCP SYN Flood Simulation")
print(f"[+] Target: {TARGET_IP}:{TARGET_PORT}")
print("-" * 40)

try:
    for i in range(PACKET_COUNT):
        # Crafting a malicious packet (SYN Flag set)
        pkt = IP(dst=TARGET_IP) / TCP(dport=TARGET_PORT, flags="S", sport=RandShort())
        
        # Sending without verbose output for speed
        send(pkt, verbose=0)
        
        sys.stdout.write(f"\r[->] Packet sent: {i+1}/{PACKET_COUNT} to {TARGET_IP}")
        sys.stdout.flush()
        
        time.sleep(0.2) # Slight delay to prevent local congestion

except Exception as e:
    print(f"\n[ERROR] Simulation failed: {e}")

print(f"\n\n[+] Simulation finished. Check IDS logs.")
time.sleep(2)