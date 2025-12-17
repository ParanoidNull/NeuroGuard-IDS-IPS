from scapy.all import IP, TCP, send, RandShort
import time

# TARGET CONFIGURATION
# We use Google DNS (8.8.8.8) to ensure traffic actually leaves the network interface
target_ip = "8.8.8.8" 
target_port = 666   # This port is defined as "Forbidden" in ids.py

print(f"Starting Attack Simulation... Target: {target_ip}:{target_port} (TCP)")

# Loop increased to 20 to ensure IDS captures the traffic
for i in range(20):
    try:
        # Construct a TCP SYN packet (Simulating a SYN Flood or Port Scan)
        pkt = IP(dst=target_ip) / TCP(dport=target_port, flags="S", sport=RandShort())
        
        # Send packet
        send(pkt, verbose=0)
        
        print(f"[{i+1}] Malicious packet sent! -> {target_ip}")
        
        # Short delay to prevent choking the terminal
        time.sleep(0.5)
        
    except Exception as e:
        print(f"Error: {e}")

print("Simulation finished.")
time.sleep(2)