import os
import sys
import time
import threading

# Ensure local modules are discoverable
sys.path.append(os.path.join(os.path.dirname(__file__), 'agent'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))

try:
    from agent import sniffer, ids
    from server import train_model
except ImportError as e:
    # Graceful exit if dependencies are missing
    print(f"\033[91m[FATAL] Dependency error: {e}\033[0m")
    print("Ensure the virtual environment is active and requirements are installed.")
    sys.exit(1)

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    clear_terminal()
    # Cyan color for branding
    print("\033[96m")
    print(r"""
    _   __                     ______                     __
   / | / /__  __  ___________ / ____/__  ______ _________/ /
  /  |/ / _ \/ / / / ___/ __ \/ / __/ / / / __ `/ ___/ __  / 
 / /|  /  __/ /_/ / /  / /_/ / /_/ / /_/ / /_/ / /  / /_/ /  
/_/ |_/\___/\__,_/_/   \____/\____/\__,_/\__,_/_/   \__,_/   
                                                
            >> AI POWERED IDS / IPS SYSTEM <<
    """)
    print("\033[0m")
    
    # Menu Options
    print("\033[92m")
    print("="*56)
    print("    [1] Start Sniffer (Data Collection)")
    print("    [2] Train Model (Isolation Forest)")
    print("    [3] Enable IDS/IPS (Active Protection)")
    print("    [4] Launch Web Dashboard")
    print("    [5] Run Attack Simulation")
    print("    [Q] Quit")
    print("="*56 + "\033[0m")

def main():
    while True:
        display_banner()
        choice = input("\n\033[93mroot@neuroguard:~# \033[0m").upper()

        if choice == '1':
            print("\n\033[94m[*] Initializing Packet Sniffer...\033[0m")
            print("Logs path: logs/traffic_data.csv")
            time.sleep(1)
            try:
                sniffer.packet_capture()
            except KeyboardInterrupt:
                pass # Return to menu cleanly

        elif choice == '2':
            print("\n\033[94m[*] Starting Model Training...\033[0m")
            train_model.train()
            input("\n[PRESS ENTER]")

        elif choice == '3':
            print("\n\033[94m[*] Active Protection System (IPS) Enabled...\033[0m")
            try:
                ids.start_ids()
            except KeyboardInterrupt:
                print("\n[!] IPS Stopped.")
            input("\n[PRESS ENTER]")

        elif choice == '4':
            print("\n\033[94m[*] Deploying Streamlit Dashboard...\033[0m")
            time.sleep(1)
            os.system("streamlit run server/dashboard.py")

        elif choice == '5':
            print("\n\033[91m[!] Executing Attack Simulation...\033[0m")
            os.system("python attack.py")
            input("\n[simulation complete]")

        elif choice == 'Q':
            print("\nShutting down...")
            sys.exit(0)

        else:
            pass # Ignore invalid input and refresh

if __name__ == "__main__":
    main()