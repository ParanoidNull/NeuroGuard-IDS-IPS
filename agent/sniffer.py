import sys
import csv
import os
from scapy.all import sniff, IP, TCP, UDP, ICMP, get_if_list, conf
from datetime import datetime

# Log dosyasının konumu
LOG_FILE = "logs/traffic_data.csv"

class Renkler:
    YESIL = '\033[92m'
    MAVI = '\033[94m'
    KIRMIZI = '\033[91m'
    RESET = '\033[0m'

def csv_baslat():
    """CSV dosyasını ve başlıkları oluşturur (Eğer yoksa)"""
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    if not os.path.isfile(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Yapay zeka için gerekli öznitelikler (Features)
            writer.writerow(["Timestamp", "Src IP", "Dst IP", "Src Port", "Dst Port", "Protocol", "Flags", "Length"])
            print(f"{Renkler.MAVI}Log dosyası oluşturuldu: {LOG_FILE}{Renkler.RESET}")

def paket_isleyici(paket):
    """Paketi analiz eder ve CSV'ye yazar"""
    if IP in paket:
        # Temel Bilgiler
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        src_ip = paket[IP].src
        dst_ip = paket[IP].dst
        length = len(paket)
        
        # Detaylar (Varsayılan)
        protocol = "OTHER"
        src_port = 0
        dst_port = 0
        flags = "None"

        if TCP in paket:
            protocol = "TCP"
            src_port = paket[TCP].sport
            dst_port = paket[TCP].dport
            flags = str(paket[TCP].flags) # Flags string'e çevrildi
        elif UDP in paket:
            protocol = "UDP"
            src_port = paket[UDP].sport
            dst_port = paket[UDP].dport
        elif ICMP in paket:
            protocol = "ICMP"
        
        # Ekrana Özet Bas (Gözle takip için)
        print(f"{Renkler.YESIL}[LOG]{Renkler.RESET} {protocol} | {src_ip}:{src_port} -> {dst_ip}:{dst_port} | Flags: {flags}")

        # Dosyaya Kaydet
        try:
            with open(LOG_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, src_ip, dst_ip, src_port, dst_port, protocol, flags, length])
        except Exception as e:
            print(f"Dosya yazma hatası: {e}")

def dinlemeyi_baslat():
    csv_baslat()
    print(f"{Renkler.MAVI}--- NeuroGuard Veri Toplayıcı ---{Renkler.RESET}")
    
    # Windows'ta arayüz seçimi
    ifaces = get_if_list()
    for i, iface in enumerate(ifaces):
        try:
            # Bazen description alanı olmayabilir, hata vermesin
            desc = conf.iface.description if hasattr(conf.iface, 'description') else "Bilinmiyor"
        except:
            desc = "Bilinmiyor"
        print(f"{i}: {iface}")

    print("-" * 30)
    secim = input("Arayüz Numarası: ")
    
    try:
        secilen_iface = ifaces[int(secim)]
        print(f"Dinleniyor ve Kaydediliyor: {secilen_iface}")
        sniff(iface=secilen_iface, prn=paket_isleyici, store=0)
    except Exception as e:
        print(f"{Renkler.KIRMIZI}Hata: {e}{Renkler.RESET}")

if __name__ == "__main__":
    try:
        dinlemeyi_baslat()
    except KeyboardInterrupt:
        print(f"\n{Renkler.KIRMIZI}Kayıt durduruldu.{Renkler.RESET}")