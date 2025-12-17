#!/bin/bash

# --- COLORS (For terminal aesthetics) ---
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# --- DIRECTORY SETUP ---
# Ensure script runs from the project directory wherever it is called from
cd "$(dirname "$0")"

echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}  NeuroGuard - Linux/macOS Auto Launcher${NC}"
echo -e "${GREEN}==================================================${NC}"

# --- 1. ROOT PRIVILEGE CHECK ---
# 'sudo' is required for network sniffing.
if [ "$EUID" -ne 0 ]; then
  echo -e "${YELLOW}[WARNING] This script requires root privileges to sniff network traffic.${NC}"
  echo -e "Please enter your password..."
  # Restart script with sudo
  sudo "$0" "$@"
  exit
fi

# --- 2. PYTHON CHECK ---
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python3 not found!${NC}"
    echo "Please install it (Linux: sudo apt install python3 | Mac: brew install python)"
    exit 1
fi

# --- 3. VIRTUAL ENVIRONMENT (VENV) CHECK ---
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}[INFO] Creating virtual environment (venv) for the first time...${NC}"
    python3 -m venv venv
    
    # Activate environment
    source venv/bin/activate
    
    echo -e "${YELLOW}[INFO] Installing required libraries...${NC}"
    pip install --upgrade pip
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo -e "${RED}[ERROR] requirements.txt file is missing!${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}[OK] Setup complete!${NC}"
else
    echo -e "${GREEN}[OK] Virtual environment found. Activating...${NC}"
    source venv/bin/activate
fi

# --- 4. LAUNCH ---
echo -e "\n${GREEN}[INFO] Launching NeuroGuard Menu...${NC}"
python3 main.py