#!/bin/bash

# Ensure the script runs from its directory
cd "$(dirname "$0")"

# Colors for terminal output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}[*] NeuroGuard System Launcher${NC}"

# --- 1. ROOT CHECK ---
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}[!] Root privileges required for packet sniffing.${NC}"
  echo "Requesting sudo access..."
  sudo "$0" "$@"
  exit
fi

# --- 2. ENVIRONMENT SETUP ---
if [ ! -d "venv" ]; then
    echo -e "${GREEN}[+] First time setup detected.${NC}"
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    source venv/bin/activate
    
    echo "Installing dependencies..."
    pip install --upgrade pip > /dev/null
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# --- 3. LAUNCH ---
echo -e "${GREEN}[+] Starting Main Module...${NC}"
python3 main.py