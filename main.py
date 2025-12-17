import os
import sys
import time

# Renk Kodlari (Terminalde havali durmasi icin)
class Renkler:
    YESIL = '\033[92m'
    KIRMIZI = '\033[91m'
    MAVI = '\033[94m'
    SARI = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def ekran_temizle():
    # Windows icin 'cls', Linux/Mac icin 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print(f"{Renkler.MAVI}{Renkler.BOLD}")
    print("""
    _   _                      ____uard
   | \ | | ___ _   _ _ __ ___ / ___|
   |  \| |/ _ \ | | | '__/ _ \ |  _ 
   | |\  |  __/ |_| | | | (_) | |_| |
   |_| \_|\___|\__,_|_|  \___/ \____|
                                      
    AI Powered IDS / IPS System v1.0
    --------------------------------
    """)
    print(f"{Renkler.RESET}")

def menu():
    while True:
        ekran_temizle()
        banner()
        print(f"{Renkler.SARI}Lutfen bir modul secin:{Renkler.RESET}\n")
        print(f"[{Renkler.YESIL}1{Renkler.RESET}] Veri Toplama Modulu (Sniffer)")
        print(f"[{Renkler.YESIL}2{Renkler.RESET}] Yapay Zeka Egitimi (Model Training)")
        print(f"[{Renkler.YESIL}3{Renkler.RESET}] IDS/IPS Koruma Kalkanini Baslat")
        print(f"[{Renkler.YESIL}4{Renkler.RESET}] Dashboard (Web Arayuzu)")
        print(f"[{Renkler.YESIL}5{Renkler.RESET}] Saldiri Simulasyonu (Test)")
        print(f"[{Renkler.KIRMIZI}0{Renkler.RESET}] Cikis")
        
        print("\n" + "-"*30)
        secim = input(f"{Renkler.MAVI}NeuroGuard > {Renkler.RESET}")

        if secim == '1':
            print(f"\n{Renkler.SARI}>> Sniffer baslatiliyor... (Cikmak icin Ctrl+C){Renkler.RESET}")
            time.sleep(1)
            # Python dosyasini sanki terminale yazmis gibi calistirir
            os.system(f"{sys.executable} agent/sniffer.py")
            input(f"\n{Renkler.MAVI}Ana menuye donmek icin Enter'a basin...{Renkler.RESET}")

        elif secim == '2':
            print(f"\n{Renkler.SARI}>> Model egitimi basliyor...{Renkler.RESET}")
            os.system(f"{sys.executable} server/train_model.py")
            input(f"\n{Renkler.MAVI}Ana menuye donmek icin Enter'a basin...{Renkler.RESET}")

        elif secim == '3':
            print(f"\n{Renkler.KIRMIZI}>> KORUMA MODU AKTIF! (Durdurmak icin Ctrl+C){Renkler.RESET}")
            time.sleep(1)
            os.system(f"{sys.executable} agent/ids.py")
            input(f"\n{Renkler.MAVI}Ana menuye donmek icin Enter'a basin...{Renkler.RESET}")

        elif secim == '4':
            print(f"\n{Renkler.MAVI}>> Dashboard aciliyor... Tarayicinizi kontrol edin.{Renkler.RESET}")
            # Streamlit ozel bir komutla calisir
            os.system("streamlit run server/dashboard.py")
        
        elif secim == '5':
             print(f"\n{Renkler.KIRMIZI}>> Saldiri Simulasyonu Baslatiliyor...{Renkler.RESET}")
             os.system(f"{sys.executable} saldirgan.py")
             input(f"\n{Renkler.MAVI}Simulasyon bitti. Donmek icin Enter...{Renkler.RESET}")

        elif secim == '0':
            print(f"\n{Renkler.KIRMIZI}Sistem kapatiliyor. Guvenli gunler!{Renkler.RESET}")
            sys.exit()
        
        else:
            print(f"\n{Renkler.KIRMIZI}Hatali secim!{Renkler.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nCikis yapildi.")