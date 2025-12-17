import os
import pandas as pd
from scapy.all import sniff, IP, TCP, UDP, ICMP, get_if_list, conf
from datetime import datetime
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Define Log Directory and File Paths
# We go one level up (..) to reach the 'logs' folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'traffic_data.csv')

# Create logs directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def packet_handler(packet):
    """
    Parses the packet and saves features to the CSV file.
    """
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        protocol = "Other"
        src_port = 0
        dst_port = 0
        length = len(packet)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Determine Protocol
        if TCP in packet:
            protocol = "TCP"
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
        elif UDP in packet:
            protocol = "UDP"
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
        elif ICMP in packet:
            protocol = "ICMP"

        # Prepare Data Row
        new_data = pd.DataFrame([{
            'Timestamp': timestamp,
            'Src IP': src_ip,
            'Dst IP': dst_ip,
            'Protocol': protocol,
            'Src Port': src_port,
            'Dst Port': dst_port,
            'Length': length
        }])

        # Save to CSV
        try:
            if not os.path.isfile(LOG_FILE):
                # Write with header if file doesn't exist
                new_data.to_csv(LOG_FILE, index=False, mode='w')
            else:
                # Append without header if file exists
                new_data.to_csv(LOG_FILE, index=False, mode='a', header=False)
            
            # Optional: Minimal visual feedback
            # print(f"[+] {protocol} Packet: {src_ip} -> {dst_ip}")
            
        except PermissionError:
            print("[ERROR] Permission denied! Please close the CSV file if it's open.")

def packet_capture():
    print("\n--- Network Traffic Sniffer (Data Collector) ---")
    
    # List Network Interfaces
    ifaces = get_if_list()
    for i, iface in enumerate(ifaces):
        try: desc = conf.iface.description
        except: desc = ""
        print(f"{i}: {iface} {desc}")
    
    # Interface Selection
    choice = input("\nSelect Interface ID to Sniff: ")
    
    try:
        selected_iface = ifaces[int(choice)]
        print(f"\n[INFO] Sniffing started on: {selected_iface}")
        print(f"[INFO] Data is being saved to: {LOG_FILE}")
        print("[INFO] Press Ctrl+C to stop collection...\n")
        
        # Start Sniffing (store=0 to save memory)
        sniff(iface=selected_iface, prn=packet_handler, store=0)
        
    except ValueError:
        print("[ERROR] Invalid Input! Please enter a number.")
    except IndexError:
        print("[ERROR] Invalid Interface ID!")
    except KeyboardInterrupt:
        print("\n[STOP] Sniffer stopped by user.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    packet_capture()