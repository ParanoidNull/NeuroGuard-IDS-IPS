#!/bin/bash

# --- RENKLER (Terminalde guzel gorunsun) ---
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# --- DIZIN AYARI ---
# Script nerede olursa olsun, calisma dizinini proje klasoru yap
cd "$(dirname "$0")"

echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}  NeuroGuard - Linux/macOS Otomatik Baslatici${NC}"
echo -e "${GREEN}==================================================${NC}"

# --- 1. ROOT (YONETICI) KONTROLU ---
# Ag dinlemek icin 'sudo' sarttir.
if [ "$EUID" -ne 0 ]; then
  echo -e "${YELLOW}[UYARI] Bu script ag kartini dinlemek icin yetki ister.${NC}"
  echo -e "Lutfen yonetici sifrenizi girin..."
  # Kendini sudo ile tekrar baslatir
  sudo "$0" "$@"
  exit
fi

# --- 2. PYTHON KONTROLU ---
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[HATA] Python3 bulunamadi!${NC}"
    echo "Lutfen yukleyin (Linux: sudo apt install python3 | Mac: brew install python)"
    exit 1
fi

# --- 3. SANAL ORTAM (VENV) KONTROLU ---
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}[BILGI] Sanal ortam (venv) ilk kez olusturuluyor...${NC}"
    python3 -m venv venv
    
    # Ortami aktif et
    source venv/bin/activate
    
    echo -e "${YELLOW}[BILGI] Gerekli kutuphaneler yukleniyor...${NC}"
    pip install --upgrade pip
    
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    else
        echo -e "${RED}[HATA] requirements.txt dosyasi eksik!${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}[OK] Kurulum tamamlandi!${NC}"
else
    echo -e "${GREEN}[OK] Sanal ortam mevcut. Aktif ediliyor...${NC}"
    source venv/bin/activate
fi

# --- 4. BASLATMA ---
echo -e "\n${GREEN}[BILGI] NeuroGuard Menusu Aciliyor...${NC}"
python3 main.py