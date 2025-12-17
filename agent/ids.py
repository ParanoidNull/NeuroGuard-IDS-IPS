import sys
import os
import joblib
import pandas as pd
from scapy.all import sniff, IP, TCP, UDP, get_if_list, conf
from datetime import datetime
import warnings

try:
    from responder import kill_connection
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from agent.responder import kill_connection

warnings.filterwarnings("ignore")
MODEL_FILE = "models/isolation_forest.pkl"

class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

# Load Model
try:
    if os.path.exists(MODEL_FILE):
        clf = joblib.load(MODEL_FILE)
    else:
        clf = None
except:
    clf = None

def packet_analyzer(packet):
    if IP in packet:
        # Ignore UDP for noise reduction in demo
        if UDP in packet or not TCP in packet:
            return

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        length = len(packet)
        
        pred = 1 

        # AI Prediction
        if clf:
            try:
                features = pd.DataFrame([[src_port, dst_port, length]], columns=['Src Port', 'Dst Port', 'Length'])
                pred = clf.predict(features)[0]
            except:
                pass

        # HARDCODED RULE: Port 666 is always an attack
        if dst_port == 666 or src_port == 666:
            pred = -1
            print(f"\n{Colors.YELLOW}[TEST] Target Detected (Port 666)!{Colors.RESET}")

        # THREAT DETECTED
        if pred == -1:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"{Colors.RED}[!!! THREAT !!!] [{timestamp}] Anomaly: {src_ip} -> {dst_ip}:{dst_port}{Colors.RESET}")
            
            print(f"{Colors.RED}    -> Action: Terminating Connection (RST Injection)...{Colors.RESET}")
            try:
                kill_connection(packet)
            except Exception as e:
                print(f"RST Error: {e}")

def start_ids():
    print(f"{Colors.BLUE}--- NeuroGuard IDS/IPS (Active Defense) ---{Colors.RESET}")
    print("Monitoring TCP traffic for anomalies...\n")
    
    ifaces = get_if_list()
    for i, iface in enumerate(ifaces):
        try: desc = conf.iface.description
        except: desc = ""
        print(f"{i}: {iface} {desc}")
    
    choice = input(f"{Colors.YELLOW}Select Interface ID: {Colors.RESET}")
    try:
        selected_iface = ifaces[int(choice)]
        print(f"Protection Started on: {selected_iface}")
        sniff(iface=selected_iface, prn=packet_analyzer, store=0)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    start_ids()