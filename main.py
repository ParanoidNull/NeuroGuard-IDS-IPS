import os
import sys
import time
import threading

# Add module paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))

try:
    from agent import sniffer, ids
    from server import train_model
except ImportError as e:
    print(f"[ERROR] Module missing: {e}")
    print("Please run 'baslat.bat' or 'pip install -r requirements.txt'")
    sys.exit()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print("\033[94m")
    print("========================================================")
    print("    N E U R O G U A R D  -  AI IDS/IPS SYSTEM")
    print("========================================================")
    print("    [1] Start Data Collection (Sniffer)")
    print("    [2] Train AI Model")
    print("    [3] Start AI Protection (IDS/IPS Mode)")
    print("    [4] Launch Dashboard (Web UI)")
    print("    [5] Attack Simulation (Test)")
    print("    [Q] Exit")
    print("========================================================\033[0m")

def main():
    while True:
        print_banner()
        choice = input("\nSelect Option: ").upper()

        if choice == '1':
            print("\n[INFO] Starting Sniffer Module...")
            print("Data will be saved to 'logs/traffic_data.csv'")
            time.sleep(2)
            try:
                sniffer.packet_capture()
            except KeyboardInterrupt:
                print("\n[STOP] Sniffer stopped.")

        elif choice == '2':
            print("\n[INFO] Starting AI Training...")
            train_model.train()
            input("\nPress Enter to return to menu...")

        elif choice == '3':
            print("\n[INFO] Initializing Active Protection System...")
            ids.start_ids()
            input("\nPress Enter to return to menu...")

        elif choice == '4':
            print("\n[INFO] Launching Web Dashboard...")
            os.system("streamlit run server/dashboard.py")

        elif choice == '5':
            print("\n[TEST] Starting Attack Simulation...")
            os.system("python saldirgan.py")
            input("\nSimulation finished. Press Enter...")

        elif choice == 'Q':
            print("Exiting... Stay safe!")
            sys.exit()
        else:
            print("[!] Invalid Selection!")
            time.sleep(1)

if __name__ == "__main__":
    main()