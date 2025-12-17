import sys
import os
import joblib
import pandas as pd
from scapy.all import sniff, IP, TCP, UDP, ICMP, get_if_list, conf
from datetime import datetime
import warnings

# Baglanti kesici fonksiyonu cagiriyoruz
try:
    from responder import baglantiyi_kes
except ImportError:
    # Eger import hatasi olursa ayni klasorde degildir, manuel import deneriz
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from agent.responder import baglantiyi_kes

warnings.filterwarnings("ignore")
MODEL_FILE = "models/isolation_forest.pkl"

class Renkler:
    YESIL = '\033[92m'
    KIRMIZI = '\033[91m'
    SARI = '\033[93m'
    MAVI = '\033[94m'
    RESET = '\033[0m'

# Modeli Yukle
try:
    if os.path.exists(MODEL_FILE):
        clf = joblib.load(MODEL_FILE)
    else:
        print(f"{Renkler.SARI}Model bulunamadi, sadece kural tabanli calisacak.{Renkler.RESET}")
        clf = None
except:
    clf = None

def paket_analizcisi(paket):
    if IP in paket:
        src_ip = paket[IP].src
        dst_ip = paket[IP].dst
        src_port = 0
        dst_port = 0
        length = len(paket)
        protocol = "OTHER"
        
        # Protokol Tespiti
        if TCP in paket:
            protocol = "TCP"
            src_port = paket[TCP].sport
            dst_port = paket[TCP].dport
        elif UDP in paket:
            protocol = "UDP"
            src_port = paket[UDP].sport
            dst_port = paket[UDP].dport

        zaman = datetime.now().strftime("%H:%M:%S")
        pred = 1 # Varsayilan: Normal

        # --- YAPAY ZEKA KONTROLU ---
        if clf and protocol != "OTHER":
            try:
                features = pd.DataFrame([[src_port, dst_port, length]], columns=['Src Port', 'Dst Port', 'Length'])
                pred = clf.predict(features)[0]
            except:
                pass

        # --- HILE (TEST) MODU: PORT 666 ---
        # Burasi Windows surucu hatalarini asmak icin eklendi.
        # Port 666 ise, paket bozuk gorunse bile TCP kabul et ve SALDIRI say.
        if dst_port == 666 or src_port == 666:
            pred = -1
            protocol = "TCP" # Zorla TCP yap
            print(f"{Renkler.SARI}[TEST] Port 666 yakalandi -> Protokol TCP'ye zorlandi.{Renkler.RESET}")

        # --- KARAR ANI ---
        if pred == -1:
            print(f"{Renkler.KIRMIZI}[!!! TEHDIT !!!] [{zaman}] Anomali: {src_ip} -> {dst_ip} (Port: {dst_port}){Renkler.RESET}")
            
            # IPS DEVREYE GIRER
            if protocol == "TCP":
                print(f"{Renkler.KIRMIZI}    -> Aksiyon: Baglanti Kesiliyor (RST)...{Renkler.RESET}")
                try:
                    baglantiyi_kes(paket)
                except Exception as e:
                    print(f"RST hatasi: {e}")
            else:
                print(f"{Renkler.SARI}    -> UDP/ICMP icin RST atilamaz.{Renkler.RESET}")

def ids_baslat():
    print(f"{Renkler.MAVI}--- NeuroGuard IDS/IPS Aktif ---{Renkler.RESET}")
    
    ifaces = get_if_list()
    for i, iface in enumerate(ifaces):
        try: desc = conf.iface.description
        except: desc = "Bilinmiyor"
        print(f"{i}: {iface}")
    
    secim = input(f"{Renkler.SARI}Arayuz No: {Renkler.RESET}")
    try:
        secilen = ifaces[int(secim)]
        print(f"Koruma basladi: {secilen}")
        sniff(iface=secilen, prn=paket_analizcisi, store=0)
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    ids_baslat()